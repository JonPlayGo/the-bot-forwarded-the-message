import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types ,executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import random
import sqlite3
from validate_email import validate_email


def reg():
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls() 

    server.login('YOUR_OUTLOOK_EMAIL', 'EMAIL_PASSWORD')

    # Составляем сообщение
    message = MIMEMultipart()
    message['From'] = 'YOUR_EMAIL'
    message['To'] = email
    message['Subject'] = 'Регистрация'
    body = str(code)
    message.attach(MIMEText(body, 'plain'))

    # Отправляем сообщение
    text = message.as_string()
    server.sendmail('OUTLOOK_EMAIL', email, text)

    # Закрываем соединение с сервером
    server.quit()

def email_test():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    search_text = email

    cursor.execute("SELECT * FROM users WHERE email = ?", (search_text,))

    # Выводим найденные строки
    rows = cursor.fetchall()
    global email_test_result
    if rows:
        for row in rows:
            print(row[1])
        email_test_result = True 
    else:
        print("Совпадений не найдено")
        email_test_result = False

    # Закрываем соединение с базой данных
    cursor.close()
    conn.close()

def login_test():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    search_text = username

    cursor.execute("SELECT * FROM users WHERE login = ?", (search_text,))

    # Выводим найденные строки
    rows = cursor.fetchall()
    global login_test_result
    if rows:
        for row in rows:
            print(row[1])
        login_test_result = True 
    else:
        print("Совпадений не найдено")
        login_test_result = False

    # Закрываем соединение с базой данных
    cursor.close()
    conn.close()

def email_test():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    search_text = email

    cursor.execute("SELECT * FROM users WHERE email = ?", (search_text,))

    rows = cursor.fetchall()
    global email_test_result
    if rows:
        for row in rows:
            print(row[1])
        email_test_result = True 
    else:
        print("Совпадений не найдено")
        email_test_result = False

    # Закрываем соединение с базой данных
    cursor.close()
    conn.close()

def pasword_test():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    search_text = username

    cursor.execute("SELECT * FROM users WHERE login = ?", (search_text,))

    # Выводим найденные строки
    rows = cursor.fetchall()
    global password_test_result
    if rows:
        for row in rows:
            print(row[2])
        password_test_result = row[2]
    else:
        print("Совпадений не найдено")
        password_test_result = None

    # Закрываем соединение с базой данных
    cursor.close()
    conn.close()

bot_token = 'YOUR_BOT_TOKEN'
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())

class Registration(StatesGroup):
    email = State()
    code = State()
    username = State()
    password = State()
    confirm_password = State()

class Login(StatesGroup):
    email = State()
    code = State()
    username = State()
    password = State()
   

@dp.message_handler(commands=['start', 'reg'], state='*')
async def register_start(message: types.Message):
    await message.answer("Please enter your email address")
    await Registration.email.set()

@dp.message_handler(state=Registration.email)
async def enter_email(message: types.Message, state: FSMContext):
    global email
    email = message.text
    email_test()
    valid = validate_email(email, verify=True)
    if valid == False:
        await message.answer("Такого email не существует")
    elif email_test_result == False:
        global code
        code = random.randint(10000, 99999)
        await message.answer(f"Please enter the 5 digit code that was sent to {email}")
        print(code)
        reg()
        await state.update_data(email=email, code=code)
        await Registration.code.set()
    else:
        await message.answer("Такой email уже зарегестрирован попробуйте войти или изменить email")
    
@dp.message_handler(state=Registration.code)
async def confirm_code(message: types.Message, state: FSMContext):
    user_code = message.text
    data = await state.get_data()
    if int(user_code) == data['code']:
        await message.answer("Code confirmed. Please choose a username")
        await Registration.username.set()
    else:
        await message.answer("Code incorrect. Please enter the correct code")

@dp.message_handler(state=Registration.username)
async def enter_username(message: types.Message, state: FSMContext):
    global username
    username = message.text
    login_test()
    if login_test_result == False:
        await message.answer("Please enter a password")
        await state.update_data(username=username)
        await Registration.password.set()
    else:
        await message.answer("такой логин уже существует!")

@dp.message_handler(state=Registration.password)
async def enter_password(message: types.Message, state: FSMContext):
    password = message.text
    await message.answer("Please confirm your password")
    await state.update_data(password=password)
    await Registration.confirm_password.set()

@dp.message_handler(state=Registration.confirm_password)
async def confirm_password(message: types.Message, state: FSMContext):
    confirm_password = message.text
    data = await state.get_data()
    if confirm_password == data['password']:
        # save login, email, and password in SQLite database here
        conn = sqlite3.connect('user_database.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (login, email, password, money) VALUES (?, ?, ?, ?)", (data['username'], data['email'], data['password'], 0))
        conn.commit()
        conn.close()
        await message.answer("Registration successful")
        await state.finish()
    else:
        await message.answer("Passwords do not match. Please try again") 

@dp.message_handler(commands=['login'], state='*')
async def register_start(message: types.Message):
    await message.answer("Введите ваш email")
    await Login.email.set()

@dp.message_handler(state=Login.email)
async def enter_email(message: types.Message, state: FSMContext):
    global email
    email = message.text
    email_test()
    valid = validate_email(email, verify=True)
    if valid == False:
        await message.answer("Такого email не существует")
    elif email_test_result == True:
        global code
        code = random.randint(10000, 99999)
        await message.answer(f"Введите код отправленный в {email}")
        print(code)
        reg()
        await state.update_data(email=email, code=code)
        await Login.code.set()
    else:
        await message.answer("Такой email не зарегестрирован попробуйте войти или изменить email")

@dp.message_handler(state=Login.code)
async def confirm_code(message: types.Message, state: FSMContext):
    user_code = message.text
    data = await state.get_data()
    if int(user_code) == data['code']:
        await message.answer("Код совпадает. Введите логин")
        await Login.username.set()
    else:
        await message.answer("Код не совпадает. Пожалуйста введите правильный код")

@dp.message_handler(state=Login.username)
async def enter_username(message: types.Message, state: FSMContext):
    global username
    username = message.text
    login_test()
    if login_test_result == True:
        await message.answer("Введите пароль")
        await state.update_data(username=username)
        await Login.password.set()
    else:
        await message.answer("такой логин уже существует!")

@dp.message_handler(state=Login.password)
async def enter_password(message: types.Message, state: FSMContext):
    global password
    password = message.text
    await state.update_data(password=password)
    pasword_test()
    if password_test_result == password:
        # save login, email, and password in SQLite database here
        await message.answer("Вход выполнен успешно")
        await state.finish()
    else:
        await message.answer("Неправильный нароль") 

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
