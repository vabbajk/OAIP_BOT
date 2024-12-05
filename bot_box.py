from aiogram import Bot



token = open("token.txt")
API_TOKEN = token.read()
token.close()

pas = open("handlers/password.txt")
password = pas.read()
pas.close()

a = open("chat_id.txt")
archive_chat = a.read()
a.close()

async def get_arch_mes():

    b = open("message_id.txt")

    c = b.read()

    b.close()

    return int(c)

async def red_archive_message(a):

    b = open("message_id.txt", "w", encoding='utf-8')

    b.write(str(a))

    b.close()

    return

bot = Bot(token=API_TOKEN)