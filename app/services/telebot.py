import asyncio
import psycopg2
from databases import Database

import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


TOKEN = "5458637763:AAGKDJTRPARSHqx1kJ0uSp3wUSbgzTDN3oM"
message_with_inline_keyboard = None
db: Database = None


def ini_db():
    host = "ec2-34-197-84-74.compute-1.amazonaws.com"
    port = "5432"
    database = "dc2r0mln1dkrmh"
    user = "ppybttvixunchd"
    password = "6dbc90ba9d51af753fc696df82f6b7fef61167531742e7d62cdba2ced4421fd2"
    db = Database(f"postgresql://{user}:{password}@{host}:{port}/{database}", min_size=3, max_size=5)

    return db
# --


async def connect():
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        await db.connect()
        print('Connected...')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    # --
# --


async def disconnect():
    try:
        # connect to the PostgreSQL server
        print('Disconnecting to the PostgreSQL database...')
        await db.disconnect()
        print('Dosonnected...')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    # --
# --


async def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    username = msg['from']['username']
    print('Chat:', content_type, chat_type, chat_id, username)

    if content_type != 'text':
        return

    if msg['text'].lower() == '/start':
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Aktifkan Notification', callback_data='notification_on')],
            [InlineKeyboardButton(text='Non Aktifkan Notification', callback_data='notification_off')]
        ])

        global message_with_inline_keyboard
        message_with_inline_keyboard = await bot.sendMessage(chat_id, 'Selamat Datang, Silahkan pilih :', reply_markup=markup)
    else:
        message = "Maaf, silahkan mulai dengan /start. Terimakasih"
        await bot.sendMessage(chat_id, message)
    # --
# --


async def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    username = msg['from']['username']
    print('Callback query:', query_id, from_id, data)
    print('Username: ', username)

    try:
        # check exist
        query = f"SELECT * FROM user_chat WHERE username = {username!r}"
        userExist = await db.fetch_one(query=query)
        if not userExist:
            return await bot.sendMessage(from_id, 'Username belum terdaftar, Silahkan Update Profile Anda!')
        # --

        is_active = 'T'
        message = 'Berhasil Aktif. Selesai!'
        notification = 'Notification Actived!'
        if data == 'notification_off':
            is_active = 'F'
            message = 'Berhasil Non-Aktif. Selesai!'
            notification = 'Notification Deactived!'
        # --

        # update data
        query = f"UPDATE user_chat SET is_active = {is_active!r}, chat_id = {from_id} WHERE username = {username!r}"
        await db.execute(query)

        await bot.sendMessage(from_id, message)
        await bot.answerCallbackQuery(query_id, text=notification)
    except Exception as e:
        raise Exception(e)
    # --
# --

try:
    db = ini_db()
    bot = telepot.aio.Bot(TOKEN)
    answerer = telepot.aio.helper.Answerer(bot)

    loop = asyncio.get_event_loop()
    loop.create_task(MessageLoop(bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_forever())
    loop.run_until_complete(connect())

    print('Running ...')
    loop.run_forever()
except Exception as e:
    raise Exception(str(e))
finally:
    loop.run_until_complete(disconnect())
# --
