
#                           " Задача Регистрация покупателей"

from crud_function_14_5 import get_all_products, add_users, is_include

product = get_all_products()


from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = '7931532450:AAEjecHB-9N1rK8ov4523YrZCvXNDrWeLMc'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())



# Изменения в Telegram-бот:
# Кнопки главного меню дополните кнопкой "Регистрация".

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.row(KeyboardButton('Регистрация'))
kb.row(KeyboardButton('Купить'),KeyboardButton('Рассчитать'),KeyboardButton('Информация'))




ki = InlineKeyboardMarkup()
i_button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
i_button2 = InlineKeyboardButton(text='Формулы расчета', callback_data='formulas')
ki.add(i_button1,i_button2)




ki_buy = InlineKeyboardMarkup()
for i in range(1, 5):
    buy_button = InlineKeyboardButton(text=f'Product{i}', callback_data='product_buying')
    ki_buy.add(buy_button)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Напишите новый класс состояний RegistrationState с следующими объектами класса State:
# username, email, age, balance(по умолчанию 1000).
class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

# Создайте цепочку изменений состояний RegistrationState.
# Фукнции цепочки состояний RegistrationState:

# sing_up(message):
# Оберните её в message_handler, который реагирует на текстовое сообщение 'Регистрация'.
# Эта функция должна выводить в Telegram-бот сообщение "Введите имя пользователя (только латинский алфавит):".
# После ожидать ввода имени в атрибут RegistrationState.username при помощи метода set.

@dp.message_handler(text='Регистрация')
async def sing_up(message: types.Message):
    await message.answer('Введите имя пользователя (только латинский алфавит)')
    await RegistrationState.username.set()


# set_username(message, state):
# Оберните её в message_handler, который реагирует на состояние RegistrationState.username.
# Если пользователя message.text ещё нет в таблице, то должны обновляться данные в состоянии username на message.text.
# Далее выводится сообщение "Введите свой email:" и принимается новое состояние RegistrationState.email.
# Если пользователь с таким message.text есть в таблице, то выводить "Пользователь существует, введите другое имя"
# и запрашивать новое состояние для RegistrationState.username.
@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state):
    if not is_include(message.text):
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()

# set_email(message, state):
# Оберните её в message_handler, который реагирует на состояние RegistrationState.email.
# Эта функция должна обновляться данные в состоянии RegistrationState.email на message.text.
# Далее выводить сообщение "Введите свой возраст:":
# После ожидать ввода возраста в атрибут RegistrationState.age.

@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


# set_age(message, state):
# Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
# Эта функция должна обновляться данные в состоянии RegistrationState.age на message.text.
# Далее брать все данные (username, email и age) из состояния и записывать в таблицу Users при помощи ранее написанной crud-функции add_user.
# В конце завершать приём состояний при помощи метода finish().

@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_users(data['username'], data['email'], data['age'])
    await state.finish()
    await message.answer('Регистрация прошла успешно')

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет. Я бот, помогающий твоему здоровью', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def  main_menu(message: types.Message):
    await message.answer(text='Выберите опцию', reply_markup=ki)


@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')


# Измените функцию get_buying_list в модуле с Telegram-ботом, используя вместо обычной нумерации продуктов
# функцию get_all_products. Полученные записи используйте в выводимой надписи: \
# "Название: <title> | Описание: <description> | Цена: <price>"

@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    for i in range(4):
        with open(f'Pictures/{i}.jpg','rb') as img:
            await message.answer(f'*Название*:{product[i][0]} , *Описание*: {product[i][1]} , *Цена*: {product[i][2]} руб',
                                 parse_mode="Markdown")
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=ki_buy)


@dp.callback_query_handler(text='product_buying')
async def set_age(call):
    await call.message.answer('Вы успешно приобрели продукт')


@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growht(message: types.Message, state):
    await state.update_data(age=int(message.text))
    await message.answer(f"Введите свой рост")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state):
    await state.update_data(growth=int(message.text))
    await message.answer(f"Введите свой вес")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()

    calories = 10*(data['weight']) + 6*(data['growth']) - 5*(data['age']) + 5

    await message.answer(f"Ваша норма калорий = {calories}")
    await state.finish()


@dp.message_handler()
async def all_message(message: types.Message):
    await message.answer('Введите команду /start')


if __name__ == '__main__':
    executor. start_polling(dp, skip_updates=True)


















