tok = "5607174844:AAE8cKcxxQEtKU4O8--PpE6Uvi5Z50c3gRw"

import aiogram
from aiogram import Bot, Dispatcher ,types ,executor

bot = aiogram.Bot(token=tok)
dp = Dispatcher(bot)

@dp.message_handler(commands=['get_chatid'])
async def get_chat_id(message: aiogram.types.Message):
    global chat_ide
    chat_ide = message.chat.id
    await message.answer(f"Ваш ID чата: {chat_ide}")

@dp.message_handler(commands=['namegr'])
async def namegr(message: types.Message):
    text = message.text.split(' ')[1]
    global chat_ide
    chat_ide = message.chat.id
    await message.answer(f"Ваш ID чата: {chat_ide}")
    global gr_id
    gr_id = text
    await bot.send_message(message.chat.id, f'Ваш идентификатор группы был установлен как {text}')

@dp.message_handler(commands=['sel_gr'])
async def sel_gr(message: types.Message):
    ls_ide = message.chat.id
    await message.answer(f"Ваш ID чата: {ls_ide}")
    text = message.text.split(' ')[1]

    if text == gr_id:
        await bot.send_message(chat_ide, 'Группа выбрана! Все сообщения, которые вы отправляете после этой команды, будут перенаправлены в группу с соответствующим идентификатором.')

    @dp.message_handler()
    async def echo_message(msg: types.Message):
        print("l" ,msg.from_user ,"l")
        print("l" , ls_ide, "l")
        global text3
        text3 = msg.text
        useid = msg.from_user.id
        if str(useid) == str(ls_ide):
            await bot.send_message(chat_ide,text3)
            print(ls_ide)
        else:
            print("pizd")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)