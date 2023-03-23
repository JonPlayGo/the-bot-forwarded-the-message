import sqlite3
import logging
from aiogram import *

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS idname(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,gruip TEXT)''')

API_TOKEN = 'youapi'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['namegr'])
async def process_namegr_command(message: types.Message):
    # Save the group name in a variable
    namegroup = message.text.split(' ')[1]
    await message.reply(f'Group name is: {namegroup}')
    catid = message.chat.id
    c.execute("INSERT INTO idname (name, gruip) VALUES (?, ?)", (namegroup, catid))
    conn.commit()
    
@dp.message_handler(commands=['sendat'])
async def process_sendat_command(message: types.Message):
    
    @dp.message_handler(content_types=[ContentType.PHOTO])
    async def process_photo(message: types.Message):
        # Save the photo file_id in a variable
        global photo_id
        photo_id = message.photo[-1].file_id
        await message.reply('Got your photo!')
        
        @dp.message_handler()
        async def process_message(message: types.Message):
            # Save the message text in a variable
            global caption
            caption = message.text
            await message.reply('Got your message!')


@dp.message_handler(commands=['sendto'])
async def process_sendto_command(message: types.Message):
    # Get the group ID from the command argument
    group_id = message.text.split(' ')[1]
    search_term = group_id
    query = "SELECT gruip FROM idname WHERE name LIKE ?"
    for row in c.execute(query, ('%' + search_term + '%',)):
        print(row[0])
        chadid = row[0]
    await bot.send_photo(chat_id=chadid, photo=photo_id, caption=caption)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


