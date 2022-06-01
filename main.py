import random
import string
import time

from starlette import status
from starlette.middleware.cors import CORSMiddleware

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.api.api_v1.api import api_router as api_v1_router
from app.db import engine, database, metadata
from app.models import models
from app.config import settings
from app.utils import logger


metadata.create_all(engine)

app = FastAPI(title=settings.app_name, openapi_url=settings.openapi_url)
app.include_router(api_v1_router, prefix=settings.prefix)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"ERROR: {exc}")
    err = exc.errors()
    err_info = [f"{(e['loc'][-1])}: {e['msg']}" for e in err]

    return JSONResponse(
        content=jsonable_encoder({
            "response_code": "99",
            "response_msg": "error",
            "response_data": err_info}),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
# --


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")

    start_time = time.time()
    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(
        f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}"
    )

    return response
# --


@app.on_event("startup")
async def startup():
    await database.connect()
# --


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
# --


# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
