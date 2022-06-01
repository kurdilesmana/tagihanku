import logging
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette import status

# setup loggers
logging.config.fileConfig('app/logging.conf', disable_existing_loggers=False)

# logger file
# fileHandler = logging.FileHandler(f'app/logs/{datetime.strftime(datetime.now(), "%Y-%m-%d")}.log', 'a')
logFormatter = logging.Formatter('%(asctime)s loglevel=%(levelname)-6s logger=%(name)s %(funcName)s() L%(lineno)-4d %(message)s')
# fileHandler.setFormatter(logFormatter)
# fileHandler.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
# logger.addHandler(fileHandler)

RC_CODE = {
    "01": "Nasabah tidak ditemukan.",
    "04": "Data not found.",
    "90": "Rollback: Db transaction failed",
    "99": "Sistem Dalam Pemeliharaan. Silakan Coba Beberapa Saat Lagi."
}


def setErrMsg(resCode, resMsg="", customMsg=False):
    rcType = RC_CODE
    rcMsg = rcType.get(resCode, resMsg)
    if customMsg:
        rcMsg = resMsg
    # --

    rcMsg = '{0} ({1})'.format(rcMsg, resCode)

    return rcMsg
# --


def setExcMessage(e, txType="GEN", customMsg=False, addParams=None):
    resCode = "999"
    resMsg = str(e)

    excMsg = resMsg.split('::')
    if len(excMsg) > 1:
        resCode = excMsg[0]
        resMsg = excMsg[1]
    # --

    resMsg = setErrMsg(resCode, resMsg=resMsg, customMsg=customMsg)
    response = {
        "response_code": resCode,
        "response_msg": resMsg
    }

    if addParams not in [None, 0, '']:
        response['response_data'] = addParams
    # --

    logger.error('-------------------------------------------')
    logger.error('ExcMessage:')
    logger.error(str(e))
    logger.error('-------------------------------------------')

    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(response))
# --
