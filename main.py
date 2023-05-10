from sqlite3 import OperationalError
import aiogram
from aiogram import executor, types, Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import ButtonDataInvalid
import requests
import aiosqlite
from config import token


bot = Bot(token)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


class Form(StatesGroup):
    city = State()
    category_name = State()
    add_category_to_database = State()
    product_name = State()
    product_price = State()
    communication_with_operator = State()
    answer_to_users_question = State()
    product_type = State()
    product_photo = State()
    promocode = State()
    promocode_price = State()
    promocode_total = State()
    promocode_check = State()
    delivery_by_taxi = State()
    delivery_pickup = State()
    mailing = State()
    mailing_final = State()
    greet = State()
    adress = State()


@dp.message_handler(commands=['start'])
async def start(message: Message):
    async with aiosqlite.connect('database.db') as conn:
        cur = await conn.cursor()
        await cur.execute(f'SELECT * FROM greetadress WHERE type = ?', ('greet',))
        rows = await cur.fetchall()
        rows = [list(i) for i in rows]
        print(rows)
        greet = rows[0][1]

    await bot.send_photo(chat_id=message.chat.id, photo=open('photos/2023-02-03 3.09.36 PM.jpg', 'rb'),
                         caption=f'{message.from_user.full_name}, '
                                 f'добро пожаловать в наш магазин Норвашская Форель.\n{greet}')

    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('Продолжить как физ лицо', callback_data='individual')
    button2 = InlineKeyboardButton('Продолжить как юр лицо', callback_data='legalentitymenu')
    markup.add(button1)
    markup.add(button2)
    await bot.send_message(chat_id=message.chat.id, text='Прежде чем начать,'
                                                         ' пожалуйста нажмите кнопку ниже, чтобы уточнить, кто вы',
                           reply_markup=markup)


@dp.message_handler(commands=['addcategory', 'addproduct', 'deletecategory', 'deleteproduct', 'addpromocode', 'restart', 'deletepromocode', 'mailing', 'changegreeting', 'changeadress'])
async def add_category(message: Message):

    markup = InlineKeyboardMarkup()

    if message.text == '/addcategory':
        button1 = InlineKeyboardButton('Для физ лиц', callback_data='addcategoryforindividual')
        button2 = InlineKeyboardButton('Для магазинов', callback_data='addcategoryforshop')
        button3 = InlineKeyboardButton('Для ресторанов', callback_data='addcategoryforrestaurant')
        button4 = InlineKeyboardButton('Для обработчиков', callback_data='addcategoryforhandler')
        markup.add(button1)
        markup.add(button2)
        markup.add(button3)
        markup.add(button4)
        await bot.send_message(chat_id=message.chat.id, text='Хорошо, для начала уточните,'
                                                         ' для какой категории пользователей'
                                                         ' вы собираетесь добавлять эту категорию', reply_markup=markup)
    elif message.text == '/addproduct':
        button1 = InlineKeyboardButton('Для физ лиц', callback_data='addproductforindividual')
        button2 = InlineKeyboardButton('Для магазинов', callback_data='addproductforshop')
        button3 = InlineKeyboardButton('Для ресторанов', callback_data='addproductforrestaurant')
        button4 = InlineKeyboardButton('Для обработчиков', callback_data='addproductforhandler')
        markup.add(button1)
        markup.add(button2)
        markup.add(button3)
        markup.add(button4)
        await bot.send_message(chat_id=message.chat.id, text='Хорошо, для начала уточните,'
                                                             ' для какой категории пользователей'
                                                             ' вы собираетесь добавлять этот товар',
                               reply_markup=markup)
    elif message.text == '/deletecategory':

        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton('Удалить категорию для физ лиц', callback_data='deleteindividualcategory')
        button2 = InlineKeyboardButton('Удалить категорию для магазинов', callback_data='deleteshopcategory')
        button3 = InlineKeyboardButton('Удалить категорию для ресторана', callback_data='deleterestaurantcategory')
        button4 = InlineKeyboardButton('Удалить категорию для обработчика', callback_data='deletehandlercategory')

        markup.add(button1)
        markup.add(button2)
        markup.add(button3)
        markup.add(button4)
        await bot.send_message(chat_id=message.chat.id,
                               text='Уточните, для какой категории пользователей вы собираетесь удалять категорию:',
                               reply_markup=markup)

    elif message.text == '/deleteproduct':

        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton('Удалить товар для физ лиц', callback_data='deleteindividualproduct')
        button2 = InlineKeyboardButton('Удалить товар для магазинов', callback_data='deleteshopproduct')
        button3 = InlineKeyboardButton('Удалить товар для ресторана', callback_data='deleterestaurantproduct')
        button4 = InlineKeyboardButton('Удалить товар для обработчика', callback_data='deletehandlerproduct')

        markup.add(button1)
        markup.add(button2)
        markup.add(button3)
        markup.add(button4)
        await bot.send_message(chat_id=message.chat.id,
                               text='Уточните, для какой категории пользователей вы собираетесь удалять товар:',
                               reply_markup=markup)

    elif message.text == '/addpromocode':
        await bot.send_message(chat_id=message.chat.id,
                               text='Хорошо, отправьте промокод:',
                               reply_markup=markup)

        await Form.promocode.set()
    elif message.text == '/deletepromocode':
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute('SELECT * FROM promocodes')
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            buttons = [InlineKeyboardButton(text=f'{i[0]}', callback_data=f'{i[0]}promocodetodelete') for i in rows]

        markup = InlineKeyboardMarkup()
        for i in buttons:
            markup.add(i)


        await bot.send_message(chat_id=message.chat.id,
                               text='Хорошо, выберите промокод, который вы собираетесь удалить:',
                               reply_markup=markup)

    elif message.text == '/restart':
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'SELECT * FROM greetadress WHERE type = ?', ('greet',))
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            print(rows)
            greet = rows[0][1]

        await bot.send_photo(chat_id=message.chat.id, photo=open('photos/2023-02-03 3.09.36 PM.jpg', 'rb'),
                             caption=f'{message.from_user.full_name}, '
                                     f'добро пожаловать в наш магазин Приладожье.\n\n{greet}')

        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'DELETE FROM users WHERE id = ?', (message.from_user.id,))
            await conn.commit()

        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton('Продолжить как физ лицо', callback_data='individual')
        button2 = InlineKeyboardButton('Продолжить как юр лицо', callback_data='legalentitymenu')
        # button3 = InlineKeyboardButton('Продолжить как ресторан', callback_data='restaurant')
        # button4 = InlineKeyboardButton('Продолжить как производитель', callback_data='handler')

        markup.add(button1)
        markup.add(button2)
        # markup.add(button3)
        # markup.add(button4)
        await bot.send_message(chat_id=message.chat.id, text='Прежде чем начать,'
                                                             ' пожалуйста нажмите кнопку ниже, чтобы уточнить, кто вы',
                               reply_markup=markup)
    elif message.text == '/mailing':
        await bot.send_message(chat_id=message.chat.id, text='Хорошо, пришлите сообщение, которое собираетесь разослать по пользователям:')
        await Form.mailing.set()

    elif message.text == '/changegreeting':
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(
                '''CREATE TABLE IF NOT EXISTS greetadress
                (type TEXT, message TEXT)''')
            await conn.commit()

        await bot.send_message(chat_id=message.chat.id, text='Хорошо, отправьте новое приветственное сообщение сюда одним сообщением:')
        await Form.greet.set()

    elif message.text == '/changeadress':
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(
                '''CREATE TABLE IF NOT EXISTS greetadress
                (type TEXT, message TEXT)''')
            await conn.commit()
        await bot.send_message(chat_id=message.chat.id, text='Хорошо, отправьте новый адрес сюда одним сообщением:')
        await Form.adress.set()



global messages_of_the_cart
global messages_of_the_menu
messages_of_the_cart = {}
messages_of_the_menu = {}


@dp.message_handler(content_types=['text'])
async def textbuttons(message: Message):

    global id_of_the_final_cart_message
    global total

    if message.text == 'Меню':
        try:
            global id_of_the_basic_photo

            user_id_message = message.from_user.id
            messages_of_the_menu[user_id_message] = {}
            message = await bot.send_photo(chat_id=message.chat.id, photo=open('photos/2023-02-03 3.09.36 PM.jpg', 'rb'))
            messages_of_the_menu[user_id_message]['basic'] = message.message_id
            async with aiosqlite.connect('database.db') as conn:
                cur = await conn.cursor()
                await cur.execute(f'SELECT * FROM users WHERE id = ?', (user_id_message,))
                rows = await cur.fetchall()
                rows = [list(i) for i in rows]
                table_name = rows[0][1]
                city = rows[0][2].strip("'")
                await cur.execute(f'SELECT * FROM {table_name} WHERE city = "{city}"')
                rows = await cur.fetchall()
                rows = [list(i) for i in rows]
                buttons = [InlineKeyboardButton(text=f'{i[0]}', callback_data=f'{i[0]}chosencategory') for i in rows]

            markup = InlineKeyboardMarkup()
            for i in buttons:
                markup.add(i)

            await bot.send_message(chat_id=message.chat.id, text='Выберите нужную категорию:', reply_markup=markup)
        except OperationalError as E:
            await bot.send_message(chat_id=message.chat.id, text='Кажется, категорий в меню еще нет')

    elif message.text == 'Связь с оператором':
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='Связаться с оператором через бота', callback_data='communication')
        markup.add(button1)
        await bot.send_message(chat_id=message.chat.id,
                               text='Вы можете позвонить нам по номеру телефона: '
                                    '+79.. или написать в Whatsapp по нему. \nТакже, '
                                    'у нас есть и контакт в самом телеграме: @username.'
                                    ' \n\nТакже, вы можете нажать на кнопку ниже чтобы'
                                    ' связаться с оператором прямо через бота',
                               reply_markup=markup)

    elif message.text == 'О нас':
        await bot.send_message(chat_id=message.chat.id,
                               text='''Мы - компания Приладожье. С 2005 года в живописном заливе Кирьявалахти на семейной ферме «Приладожье» с любовью и заботой мы выращиваем радужную форель, солим её, коптим и вялим.\n
Наша философия — экологичность, крафтовое производство и честные цены. Мы тщательно контролируем каждый этап роста рыбы, используем натуральные корма лучших производителей — без химии, ускорителей и стимуляторов, вкладываем сердце в каждый продукт и рецепт.\n
Свежий улов запекаем на углях, готовим из него сливочный лохикейто с красной икрой, румяные калитки, пельмени ручной лепки, сытные фишбургеры, начиняем нежным малосольным форелевым филе кружевные блинчики.\n
Каждую неделю отправляем продукцию и самые популярные блюда из меню кафе в Петрозаводск, Москву и Санкт-Петербург — с бережной адресной доставкой.\n
Маркером правильно выбранного пути для нас стала победа в национальном конкурсе «Вкусы России 2020» как гастрономического бренда с перспективами по развитию туристического потенциала.\n
Мы построили рыбоперерабатывающий завод нового поколения, а также современный комфортабельный кемпинг для автодомов и караванинга с зарядной станцией для электромобилей. Строим ресторан с видом на Ладогу и культурно-досуговый центр для детей. Разрабатываем масштабный проект по очистке Ладожского озера.\n
Всегда рады друзьям в нашем карельском Муми-доме цвета ясного июньского неба ♡''')

    elif message.text == 'Корзина':
        total = 0
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'SELECT * FROM cart WHERE id = ?', (message.from_user.id,))
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
        t = 1

        messages_of_the_cart[message.from_user.id] = {}
        userid = message.from_user.id

        if rows:
            for i in rows:
                markup = InlineKeyboardMarkup()
                button1 = InlineKeyboardButton(text='Увеличить', callback_data=f'{i[0]}➕')
                button2 = InlineKeyboardButton(text='Уменьшить', callback_data=f'{i[0]}➖')
                button3 = InlineKeyboardButton(text='❌ Удалить', callback_data=f'{i[0]}❌')
                markup.add(button1, button2)
                markup.add(button3)
                id = await bot.send_message(chat_id=message.chat.id,
                                            text=f'{t}. {i[0]} - {i[1]}руб./{i[2]}\n\nКоличество: {i[3]} \n\nИтог: {i[1] * i[3]}руб.', reply_markup=markup)
                messages_of_the_cart[message.from_user.id][i[0]] = id.message_id
                t += 1
                total += i[1] * i[3]

        else:
            await bot.send_message(chat_id=message.chat.id,
                                   text='Кажется, в корзине еще ничего нет. Зайдите в меню для добавления товаров.')

        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='У меня есть промокод!', callback_data='promocode')
        button2 = InlineKeyboardButton(text='Продолжить без промокода', callback_data='continuetodelivery')
        markup.add(button1)
        markup.add(button2)
        the_final_cart_message = await bot.send_message(chat_id=message.chat.id,
                               text=f'Итоговая стоимость: {total}руб.\n\n'
                                    f'Если у вас есть промокод, '
                                    f'вы можете нажать на кнопку ниже для его ввода:', reply_markup=markup)


        messages_of_the_cart[userid]['id_of_the_final_cart_message'] = the_final_cart_message.message_id
        print(messages_of_the_cart)
    elif message.text == 'Накопительная программа':
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'SELECT * FROM orders WHERE id = ?', (message.from_user.id,))
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            sum_of_orders = 0
            for i in rows:
                sum_of_orders += i[1]
        await bot.send_message(chat_id=message.chat.id,
                               text=f'У нас есть действующая накопительная программа! '
                                    f'Она позволяет получать скидку в зависимости от общей суммы ваших заказов!'
                                    f'\n\nВаша текущая сумма заказов: {sum_of_orders}руб.')


@dp.callback_query_handler(lambda c: True)
async def inline_buttons(call: types.CallbackQuery):
    req = call.data
    global type_of_users_while_adding_category
    global name_of_users_for_bot_admin
    global city_for_database_while_adding_category
    global city_for_database_while_adding_product
    global type_of_users_while_adding_product
    global category_while_adding_product
    global id_of_the_user_to_answer
    global id_of_the_message_to_delete_while_answering
    global deleting_category
    global deleting_category_for_bot
    global city_for_deleting_category
    global category_to_remove_from_database
    global promocode_to_delete
    global deleting_product
    global deleting_product_for_bot
    global product_to_remove_from_database
    global city_for_deleting_product
    global method_of_the_delivery
    global method_of_the_delivery_for_user
    global phone_number
    global is_promocode
    global total
    is_promocode = False

    # User Registration Part

    if req in ['individual', 'shop', 'restaurant', 'handler']:
        global status_of_the_user
        await bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton('Казань', callback_data='Kazan')
        button2 = InlineKeyboardButton('Чебоксары', callback_data='Cheboksary')
        markup.add(button1)
        markup.add(button2)
        if req == 'individual':
            status_of_the_user = 'individual'
            await bot.send_message(chat_id=call.message.chat.id,
                                   text='Хорошо! Вы продолжаете как физ лицо.'
                                        ' Еще, для начала также нужно выбрать город,'
                                        ' в котором вы находитесь:', reply_markup=markup)
        elif req == 'shop':
            status_of_the_user = 'shop'
            await bot.send_message(chat_id=call.message.chat.id,
                                   text='Хорошо! Вы продолжаете как магазин.'
                                        ' Еще, для начала также нужно выбрать город,'
                                        ' в котором вы находитесь:', reply_markup=markup)
        elif req == 'restaurant':
            status_of_the_user = 'restaurant'
            await bot.send_message(chat_id=call.message.chat.id,
                                   text='Хорошо! Вы продолжаете как ресторан.'
                                        ' Еще, для начала также нужно выбрать город,'
                                        ' в котором вы находитесь:', reply_markup=markup)
        elif req == 'handler':
            status_of_the_user = 'handler'
            await bot.send_message(chat_id=call.message.chat.id,
                                   text='Хорошо! Вы продолжаете как производитель.'
                                        ' Еще, для начала также нужно выбрать город,'
                                        ' в котором вы находитесь:', reply_markup=markup)

    elif req == 'legalentitymenu':
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='Магазин', callback_data='shop')
        button2 = InlineKeyboardButton(text='Ресторан', callback_data='restaurant')
        button3 = InlineKeyboardButton(text='Производитель', callback_data='handler')
        button4 = InlineKeyboardButton(text='Вернуться назад', callback_data='backtochoosinguserstatus')
        markup.add(button1)
        markup.add(button2)
        markup.add(button3)
        markup.add(button4)

        await bot.edit_message_text(message_id=call.message.message_id,
                                    chat_id=call.message.chat.id,
                                    text='Пожалуйста, уточните вашу категорию:',
                                    reply_markup=markup)
    elif req == 'backtochoosinguserstatus':
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton('Продолжить как физ лицо', callback_data='individual')
        button2 = InlineKeyboardButton('Продолжить как юр лицо', callback_data='legalentitymenu')
        markup.add(button1)
        markup.add(button2)
        await bot.edit_message_text(message_id=call.message.message_id,
                                    chat_id=call.message.chat.id,
                                    text='Прежде чем начать, пожалуйста нажмите кнопку ниже, чтобы уточнить, кто вы',
                                    reply_markup=markup)

    elif req in ['Kazan', 'Cheboksary']:
        await bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(
                '''CREATE TABLE IF NOT EXISTS users
                (username TEXT UNIQUE, status TEXT, city TEXT, id TEXT)''')
            await conn.commit()
            if req == 'Kazan':
                if call.from_user.username is not None:
                    await cur.execute("INSERT OR IGNORE INTO users (id, username, status, city) "
                                      "VALUES (?, ?, ?, ?)", (call.from_user.id, call.from_user.username, status_of_the_user, 'Kazan'))
                    await conn.commit()
                else:
                    await cur.execute("INSERT OR IGNORE INTO users (id, status, city) "
                                      "VALUES (?, ?, ?)",
                                      (call.from_user.id, status_of_the_user, 'Kazan'))
                    await conn.commit()

            else:
                if call.from_user.username is not None:
                    await cur.execute("INSERT OR IGNORE INTO users (username, status, city, id) "
                                      "VALUES (?, ?, ?, ?)",
                                      (call.from_user.username, status_of_the_user, 'Cheboksary', call.from_user.id))
                    await conn.commit()
                else:
                    await cur.execute("INSERT OR IGNORE INTO users (status, city, id) "
                                      "VALUES (?, ?, ?)",
                                      (status_of_the_user, 'Kazan', call.from_user.id))
                    await conn.commit()
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton('Меню')
        button2 = KeyboardButton('Связь с оператором')
        button3 = KeyboardButton('Корзина')
        button4 = KeyboardButton('О нас')
        button5 = KeyboardButton('Накопительная программа')
        markup.add(button1, button3)
        markup.add(button2, button4)
        markup.add(button5)
        await bot.send_message(chat_id=call.message.chat.id,
                               text='Добро пожаловать!', reply_markup=markup)

    # Adding a category

    elif req in ['addcategoryforindividual', 'addcategoryforshop',
                 'addcategoryforrestaurant', 'addcategoryforhandler']:
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        if req == 'addcategoryforindividual':
            type_of_users_while_adding_category = 'individual'
            name_of_users_for_bot_admin = 'Физ лица'
        elif req == 'addcategoryforshop':
            type_of_users_while_adding_category = 'shop'
            name_of_users_for_bot_admin = 'Магазины'
        elif req == 'addcategoryforrestaurant':
            type_of_users_while_adding_category = 'restaurant'
            name_of_users_for_bot_admin = 'Рестораны'
        elif req == 'addcategoryforhandler':
            type_of_users_while_adding_category = 'handler'
            name_of_users_for_bot_admin = 'Обработчики'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton('Казань', callback_data='Kazanfordatabase')
        button2 = InlineKeyboardButton('Чебоксары', callback_data='Cheboksaryfordatabase')
        markup.add(button1)
        markup.add(button2)

        await bot.send_message(chat_id=call.message.chat.id,
                               text='Хорошо, теперь выберите город, в котором эта категория будет отображаться:',
                               reply_markup=markup)
    elif req in ['Kazanfordatabase', 'Cheboksaryfordatabase']:
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        if req == 'Kazanfordatabase':
            city_for_database_while_adding_category = 'Kazan'
        elif req == 'Cheboksaryfordatabase':
            city_for_database_while_adding_category = 'Cheboksary'
        await bot.send_message(chat_id=call.message.chat.id, text='Хорошо, введите название новой '
                                                                  'категории (не более 35 символов)')
        await Form.category_name.set()

    elif req == 'addingcategorytodatabase':
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(
                f'''CREATE TABLE IF NOT EXISTS {type_of_users_while_adding_category}
                (name TEXT, type TEXT, city TEXT, category TEXT)''')
            await conn.commit()
            await cur.execute(f'''INSERT OR IGNORE INTO {type_of_users_while_adding_category} (name, type, city) 
                              VALUES (?, ?, ?)''', (name_of_category,
                                                    'category', city_for_database_while_adding_category,))
            await conn.commit()
        await bot.send_message(chat_id=call.message.chat.id, text='Успешно!')

    # Deleting a category

    elif req in ['deleteindividualcategory', 'deleteshopcategory', 'deleterestaurantcategory', 'deletehandlercategory']:
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        if req == 'deleteindividualcategory':
            deleting_category = 'individual'
            deleting_category_for_bot = 'Физ лица'
        elif req == 'deleteshopcategory':
            deleting_category = 'shop'
            deleting_category_for_bot = 'Магазины'
        elif req == 'deleterestaurantcategory':
            deleting_category = 'restaurant'
            deleting_category_for_bot = 'Рестораны'
        elif req == 'deletehandlercategory':
            deleting_category = 'handler'
            deleting_category_for_bot = 'Обработчики'

        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton('Казань', callback_data='Kazandeletecategory')
        button2 = InlineKeyboardButton('Чебоксары', callback_data='Cheboksarydeletecategory')
        markup.add(button1)
        markup.add(button2)

        await bot.send_message(chat_id=call.message.chat.id,
                               text='Хорошо, теперь выберите город, в котором вы хотите удалить категорию:',
                               reply_markup=markup)

    elif req in ['Kazandeletecategory', 'Cheboksarydeletecategory']:
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        city_for_deleting_category = 'Kazan' if req == 'Kazandeletecategory' else 'Cheboksarydeletecategory'


        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'SELECT * FROM {deleting_category} WHERE type = ? AND city = ?', ('category', city_for_deleting_category))
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            buttons = [InlineKeyboardButton(text=f'{i[0]}', callback_data=f'{i[0]}deletecategory') for i in rows]
        markup = InlineKeyboardMarkup()
        for i in buttons:
            markup.add(i)

        await bot.send_message(chat_id=call.message.chat.id,
                               text='Выберите, какую категорию вы собираетесь удалять:', reply_markup=markup)

    elif req[-14:] == 'deletecategory':
        category_to_remove_from_database = req[:-14]
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='Продолжить', callback_data='continuedeletingcategory')
        button2 = InlineKeyboardButton(text='Отмена', callback_data='Cancel')
        markup.add(button1)
        markup.add(button2)
        await bot.send_message(chat_id=call.message.chat.id,
                               text=f'Итак, вы удаляете категорию: {category_to_remove_from_database}, \n\n'
                                    f'Которая отображается у категории пользователей: {deleting_category_for_bot}, \n\n'
                                    f'Которая отображается в городе: {city_for_deleting_category}', reply_markup=markup)

    elif req == 'continuedeletingcategory':
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'DELETE FROM {deleting_category} WHERE name = ?', (category_to_remove_from_database,))
            await conn.commit()
        await bot.send_message(chat_id=call.message.chat.id, text=f'Успешно!')

    # Adding a product

    elif req in ['addproductforindividual', 'addproductforshop',
                 'addproductforrestaurant', 'addproductforhandler']:
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        if req == 'addproductforindividual':
            type_of_users_while_adding_product = 'individual'
            name_of_users_for_bot_admin = 'Физ лица'
        elif req == 'addproductforshop':
            type_of_users_while_adding_product = 'shop'
            name_of_users_for_bot_admin = 'Магазины'
        elif req == 'addproductforrestaurant':
            type_of_users_while_adding_product = 'restaurant'
            name_of_users_for_bot_admin = 'Рестораны'
        elif req == 'addproductforhandler':
            type_of_users_while_adding_product = 'handler'
            name_of_users_for_bot_admin = 'Обработчики'

        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton('Казань', callback_data='Kazanproductfordatabase')
        button2 = InlineKeyboardButton('Чебоксары', callback_data='Cheboksaryproductfordatabase')
        markup.add(button1)
        markup.add(button2)

        await bot.send_message(chat_id=call.message.chat.id,
                               text='Хорошо, теперь выберите город, в котором этот товар будет отображаться:',
                               reply_markup=markup)
    elif req in ['Kazanproductfordatabase', 'Cheboksaryproductfordatabase']:
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        city_for_database_while_adding_product = 'Kazan' if req == 'Kazanproductfordatabase' else 'Cheboksary'

        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'SELECT * FROM {type_of_users_while_adding_product} WHERE type = ? AND city = ?', ('category', city_for_database_while_adding_product))
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            buttons = [InlineKeyboardButton(text=f'{i[0]}', callback_data=f'{i[0]}addtothecategory') for i in rows]

        markup = InlineKeyboardMarkup()
        for i in buttons:
            markup.add(i)

        await bot.send_message(chat_id=call.message.chat.id, text='Выберите, к какой категории будет отнесен этот товар:', reply_markup=markup)

    elif req[-16:] == 'addtothecategory':

        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        category_while_adding_product = req[:-16]
        await bot.send_message(chat_id=call.message.chat.id, text='Хорошо, напишите название товара (не более 35 символов):')
        await Form.product_price.set()

    elif req == 'continueaddingproduct':
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(
                '''CREATE TABLE IF NOT EXISTS products
                (name TEXT, price INT, type TEXT, city TEXT, category TEXT, customer TEXT, photo TEXT)''')
            await conn.commit()
            await cur.execute("INSERT OR IGNORE INTO products (name, price, type, city, category, customer, photo) "
                              "VALUES (?, ?, ?, ?, ?, ?, ?)", (theproductname, theproductprice,
                                                         theproducttype, city_for_database_while_adding_product,
                                                         category_while_adding_product,
                                                         type_of_users_while_adding_product, photo_path))
            await conn.commit()
        await bot.send_message(chat_id=call.message.chat.id, text='Успешно добавлено!')

    # menu interaction

    elif req[-14:] == 'chosencategory':
        global chosencategory
        chosencategory = req[:-14]
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'SELECT * FROM users WHERE id = ?', (call.from_user.id,))
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            customer = rows[0][1]
            city = rows[0][2].strip("'")
            await cur.execute(f'SELECT * FROM products WHERE city = "{city}" '
                              f'AND customer = "{customer}" AND category = "{chosencategory}"')
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            buttons = [InlineKeyboardButton(text=f'{i[0]}', callback_data=f'{i[0]}prod') for i in rows]

        markup = InlineKeyboardMarkup()

        for i in buttons:
            markup.add(i)
        markup.add(InlineKeyboardButton(text=f'Вернуться назад', callback_data=f'Mainmenu'))

        await bot.edit_message_text(text=f'Категория {chosencategory}', reply_markup=markup,
                                    chat_id=call.message.chat.id,
                                    message_id=call.message.message_id)

    elif req[-4:] == 'prod':
        chosenproduct = req[:-4]
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()

            await cur.execute(f'SELECT * FROM users WHERE id = ?', (call.from_user.id,))
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            customer = rows[0][1]
            city = rows[0][2].strip("'")

            await cur.execute(f'SELECT * FROM products WHERE name = ? AND city = ? AND category = ? AND customer = ?', (chosenproduct, city, chosencategory, customer))
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            global product
            product = rows[0]
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='Добавить в корзину', callback_data='add')
        button2 = InlineKeyboardButton(text='Вернуться назад', callback_data='back')
        markup.add(button1)
        markup.add(button2)
        await bot.edit_message_media(media=types.InputMedia(media=open(f'{product[6]}', 'rb'), type="photo"),
                                     chat_id=call.message.chat.id, message_id=messages_of_the_menu[call.from_user.id]['basic'])

        await bot.edit_message_text(message_id=call.message.message_id,
                                    chat_id=call.message.chat.id,
                                    reply_markup=markup,
                                    text=f'Вы выбрали: {product[0]}, его цена: {product[1]}руб./{product[2]}')
    elif req == 'add':
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(
                '''CREATE TABLE IF NOT EXISTS cart
                (name TEXT, price INT, type TEXT, amount INT, id TEXT)''')
            await cur.execute(f'SELECT * FROM cart WHERE id = ?', (call.from_user.id,))
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            in_cart = False
            for i in rows:
                if i[0] == product[0]:
                    in_cart = True
            if in_cart:
                await bot.answer_callback_query(callback_query_id=call.id,
                                                text='Кажется, этот товар уже есть в корзине! \n \n Для изменения количества перейдите в корзину',
                                                show_alert=True)
            else:

                await cur.execute("INSERT OR IGNORE INTO cart (name, price, type, amount, id) "
                                  "VALUES (?, ?, ?, ?, ?)", (product[0], product[1], product[2], 1, call.from_user.id))
                await conn.commit()
                await bot.answer_callback_query(callback_query_id=call.id,
                                                text='Добавлено! \n \n Для изменения количества перейдите в корзину',
                                                show_alert=True)
    elif req == 'back':
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'SELECT * FROM users WHERE id = ?', (call.from_user.id,))
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            customer = rows[0][1]
            city = rows[0][2].strip("'")
            await cur.execute(f'SELECT * FROM products WHERE city = "{city}" '
                              f'AND customer = "{customer}" AND category = "{chosencategory}"')
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            buttons = [InlineKeyboardButton(text=f'{i[0]}', callback_data=f'{i[0]}prod') for i in rows]
        markup = InlineKeyboardMarkup()
        for i in buttons:
            markup.add(i)
        markup.add(InlineKeyboardButton(text=f'Вернуться назад', callback_data=f'Mainmenu'))
        await bot.edit_message_media(media=types.InputMedia(media=open(f'photos/2023-02-03 3.09.36 PM.jpg', 'rb'), type="photo"), chat_id=call.message.chat.id, message_id=messages_of_the_menu[call.from_user.id]['basic'])
        await bot.edit_message_text(text=f'Категория {chosencategory}', reply_markup=markup,
                                    chat_id=call.message.chat.id,
                                    message_id=call.message.message_id)

    elif req == 'promocode':
        await bot.send_message(chat_id=call.message.chat.id, text='Хорошо! Отправьте промокод сюда!')
        await Form.promocode_check.set()

    # Communication with operator

    elif req == 'communication':
        await bot.send_message(text='Хорошо, отправьте сообщение с вашим вопросом.'
                                    ' Мы постараемся ответить как можно скорее:', chat_id=call.message.chat.id)
        await Form.communication_with_operator.set()

    elif req[-20:] == 'answertousersqustion':
        id_of_the_user_to_answer = int(req[:-20])
        id_of_the_message_to_delete_while_answering = call.message.message_id
        await bot.send_message(text='Хорошо, отправьте сообщение с вашим ответом:', chat_id=call.message.chat.id)
        await Form.answer_to_users_question.set()

    # Main menu thing

    elif req == 'Mainmenu':
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'SELECT * FROM users WHERE id = ?', (call.from_user.id,))
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            table_name = rows[0][1]
            city = rows[0][2].strip("'")
            await cur.execute(f'SELECT * FROM {table_name} WHERE city = "{city}"')
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            buttons = [InlineKeyboardButton(text=f'{i[0]}', callback_data=f'{i[0]}chosencategory') for i in rows]

        markup = InlineKeyboardMarkup()
        for i in buttons:
            markup.add(i)

        await bot.edit_message_text(chat_id=call.from_user.id, text='Выберите нужную категорию:', reply_markup=markup, message_id=call.message.message_id)


    # Cart thing

    elif req[-1] in ['➖', '➕', '❌']:
        product_to_change = req[:-1]
        global messages_of_the_cart
        global id_of_the_final_cart_message

        if req[-1] == '➕':
            async with aiosqlite.connect('database.db') as conn:
                cur = await conn.cursor()
                await cur.execute("UPDATE cart SET amount = amount + 1 WHERE id = ? AND name = ?",
                                      (call.from_user.id, product_to_change))
                await conn.commit()
            for i in messages_of_the_cart[call.from_user.id].values():
                await bot.delete_message(chat_id=call.message.chat.id, message_id=i)
            await bot.answer_callback_query(callback_query_id=call.id,
                                            text='Количество увеличено на 1. \n\nНажмите на кнопку "Корзина", чтобы увидеть обновленную корзину',
                                            show_alert=True)
        elif req[-1] == '➖':
            async with aiosqlite.connect('database.db') as conn:
                cur = await conn.cursor()
                await cur.execute('SELECT * FROM cart where id = ? AND name = ?', (call.from_user.id, product_to_change))
                rows = await cur.fetchall()
                rows = [list(i) for i in rows]
                if rows[0][3] == 1:
                    await cur.execute('DELETE FROM cart where id = ? AND name = ?',
                                      (call.from_user.id, product_to_change))
                    await conn.commit()
                    for i in messages_of_the_cart[call.from_user.id].values():
                        await bot.delete_message(chat_id=call.message.chat.id, message_id=i)
                    await bot.delete_message(chat_id=call.message.chat.id, message_id=messages_of_the_cart[call.from_user.id]['id_of_the_final_cart_message'])
                    await bot.answer_callback_query(callback_query_id=call.id,
                                                    text='Успешно удалено! \n\nНажмите на кнопку "Корзина", чтобы увидеть обновленную корзину',
                                                    show_alert=True)
                else:
                    await cur.execute("UPDATE cart SET amount = amount - 1 WHERE id = ? AND name = ?",
                                      (call.from_user.id, product_to_change))
                    await conn.commit()
                    for i in messages_of_the_cart[call.from_user.id].values():
                        await bot.delete_message(chat_id=call.message.chat.id, message_id=i)
                    await bot.answer_callback_query(callback_query_id=call.id,
                                                    text='Количество уменьшено на 1! \n\nНажмите на кнопку "Корзина", чтобы увидеть обновленную корзину',
                                                    show_alert=True)

        elif req[-1] == '❌':
            async with aiosqlite.connect('database.db') as conn:
                cur = await conn.cursor()
                await cur.execute('DELETE FROM cart where id = ? AND name = ?',
                                  (call.from_user.id, product_to_change))
                await conn.commit()
                for i in messages_of_the_cart[call.from_user.id].values():
                    await bot.delete_message(chat_id=call.message.chat.id, message_id=i)

                await bot.answer_callback_query(callback_query_id=call.id,
                                                text='Успешно удалено! \n\nНажмите на кнопку "Корзина", чтобы увидеть обновленную корзину',
                                                show_alert=True)

    # The cancel button

    # The promocode adding

    elif req == 'continueaddingpromocode':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(
                '''CREATE TABLE IF NOT EXISTS promocodes
                (name TEXT, size INT)''')
            await conn.commit()
            await cur.execute("INSERT OR IGNORE INTO promocodes (name, size) "
                              "VALUES (?, ?)", (thepromocodename, thepromocodesize))
            await conn.commit()
        await bot.send_message(chat_id=call.message.chat.id, text='Успешно добавлено!')

    elif req[-17:] == 'promocodetodelete':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        promocode_to_delete = req[:-17]
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='Продолжить', callback_data='continuedeletingromocode')
        button2 = InlineKeyboardButton(text='Отмена', callback_data='Cancel')

        markup.add(button1)
        markup.add(button2)


        await bot.send_message(chat_id=call.message.chat.id,
                               text=f'Вы собираетесь удалить промокод {promocode_to_delete}, \n\nПродолжить?', reply_markup=markup)

    elif req == 'continuedeletingromocode':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'DELETE FROM promocodes WHERE name = ?', (promocode_to_delete,))
            await conn.commit()
        await bot.send_message(chat_id=call.message.chat.id, text=f'Успешно!')

    elif req in ['deleteindividualproduct', 'deleteshopproduct',
                 'deleterestaurantproduct', 'deletehandlerproduct']:

        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        if req == 'deleteindividualproduct':
            deleting_product = 'individual'
            deleting_product_for_bot = 'Физ лица'
        elif req == 'deleteshopproduct':
            deleting_product = 'shop'
            deleting_product_for_bot = 'Магазины'
        elif req == 'deleterestaurantproduct':
            deleting_product = 'restaurant'
            deleting_product_for_bot = 'Рестораны'
        elif req == 'deletehandlerproduct':
            deleting_product = 'handler'
            deleting_product_for_bot = 'Обработчики'

        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton('Казань', callback_data='Kazandeleteproduct')
        button2 = InlineKeyboardButton('Чебоксары', callback_data='Cheboksarydeleteproduct')
        markup.add(button1)
        markup.add(button2)

        await bot.send_message(chat_id=call.message.chat.id,
                               text='Хорошо, теперь выберите город, в котором вы хотите удалить товар:',
                               reply_markup=markup)

    elif req in ['Kazandeleteproduct', 'Cheboksarydeleteproduct']:
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        city_for_deleting_product = 'Kazan' if req == 'Kazandeleteproduct' else 'Cheboksarydeleteproduct'

        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'SELECT * FROM {deleting_product} WHERE type = ? AND city = ?',
                              ('category', city_for_deleting_product))
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            buttons = [InlineKeyboardButton(text=f'{i[0]}', callback_data=f'{i[0]}deleteproduct') for i in rows]
        markup = InlineKeyboardMarkup()
        for i in buttons:
            markup.add(i)

        await bot.send_message(chat_id=call.message.chat.id,
                               text='Выберите, в какой категории вы собираетесь удалять:', reply_markup=markup)

    elif req[-13:] == 'deleteproduct':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        product_to_remove_from_database = req[:-13]
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'SELECT * FROM products WHERE category = ? AND city = ?',
                              (product_to_remove_from_database, city_for_deleting_product))
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            buttons = [InlineKeyboardButton(text=f'{i[0]}', callback_data=f'{i[0]}todel') for i in rows]

        markup = InlineKeyboardMarkup()
        for i in buttons:
            markup.add(i)

        await bot.send_message(chat_id=call.message.chat.id,
                               text=f'Выберите товар, который вы собираетесь удалять:', reply_markup=markup)

    elif req[-5:] == 'todel':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        theproducttodelete = req[:-5]
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'DELETE FROM products WHERE name = ? AND city = ? AND category = ?',
                              (theproducttodelete, city_for_deleting_product, product_to_remove_from_database))
            await conn.commit()
        await bot.send_message(chat_id=call.message.chat.id, text=f'Успешно!')


    elif req == 'continuetodelivery':
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='Оформить доставку', callback_data='delivery')
        button2 = InlineKeyboardButton(text='Оформить самовывоз', callback_data='pickup')
        button3 = InlineKeyboardButton(text='Отмена', callback_data='Cancel')

        markup.add(button1)
        markup.add(button2)
        markup.add(button3)


        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text='Выберите способ доставки:',
                                    reply_markup=markup)
    elif req == 'delivery':
        method_of_the_delivery = 'delivery'
        method_of_the_delivery_for_user = 'Доставка'

        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text='Хорошо! Вы выбрали доставку! \n\nОбратите внимание, '
                                         'что доставка будет в дальнейшем включена в сумму заказа\n\n'
                                         'Напишите пожалуйста, адрес и время, '
                                         'в которое вам было бы удобно забрать товар, '
                                         'а также любые другие пожелания:')
        await Form.delivery_by_taxi.set()

    elif req == 'pickup':
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'SELECT * FROM greetadress WHERE type = ?', ('adress',))
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            print(rows)
            adress = rows[0][1]


        method_of_the_delivery = 'pickup'
        method_of_the_delivery_for_user = 'Самовывоз'
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=f'Хорошо! Вы выбрали самовывоз! \n\n Мы находимся по адресу:\n\n{adress}\n\n'
                                         'Напишите пожалуйста, время, '
                                         'в которое вам было бы удобно забрать товар, '
                                         'а также любые другие пожелания:')
        await Form.delivery_pickup.set()

    elif req == 'proceedtooperator':

        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'''SELECT * FROM cart WHERE id = ?''', (call.from_user.id,))
            await conn.commit()
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            final_order = f'Заказ от пользователя +{phone_number}:\n\n'
            final_order += f'Итоговая стоимость заказа: {total}руб.\n\nСостав заказа:\n\n'
            for i in rows:
                final_order += f'{i[0]} - {i[1]}руб. - {i[3]}{i[2]}\n'
            final_order += f'Его номер телефона: +{phone_number}\n'
            final_order += f'Способ доставки: {method_of_the_delivery_for_user}\n'
            final_order += f'Комментарий от пользователя: {commentary}\n'
            await bot.send_message(chat_id=2849128, text=final_order)
            await bot.send_message(chat_id=call.message.chat.id,
                                   text='Успешно! В ближайшее время с вами свяжется наш оператор для уточнения деталей')
            await cur.execute(
                f'''CREATE TABLE IF NOT EXISTS orders
                        (id TEXT, size INT)''')
            await conn.commit()

            await cur.execute("INSERT INTO orders (id, size) "
                              "VALUES (?, ?)", (call.from_user.id, total))
            await conn.commit()


            await cur.execute(f'DELETE FROM cart WHERE id = ?', (call.from_user.id,))
            await conn.commit()

    elif req[-22:] == 'finalthemessagingstage':

        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'''SELECT * FROM users''', )
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            users = [i[3] for i in rows]

            for i in users:
                await bot.send_message(text=message_to_send_as_mailing, chat_id=i)
        await bot.edit_message_text(chat_id=call.message.chat.id, text='Успешно!', message_id=call.message.message_id)

    elif req == 'continueaddingadress':
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'''SELECT * FROM greetadress WHERE type = ?''', ('adress',))
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            if rows:
                await cur.execute(f'DELETE FROM greetadress WHERE type = ?', ('adress',))
                await conn.commit()
                await cur.execute(f'''INSERT INTO greetadress (type, message) 
                                                          VALUES (?, ?)''', ('adress', new_adress,))
                await conn.commit()

            else:
                await cur.execute(f'''INSERT INTO greetadress (type, message) 
                                          VALUES (?, ?)''', ('adress', new_adress,))
                await conn.commit()
        await bot.send_message(chat_id=call.message.chat.id, text='Успешно!')

    elif req == 'continueaddinggreet':
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'''SELECT * FROM greetadress WHERE type = ?''', ('greet',))
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            if rows:
                await cur.execute(f'DELETE FROM greetadress WHERE type = ?', ('greet',))
                await conn.commit()
                await cur.execute(f'''INSERT INTO greetadress (type, message) 
                                                          VALUES (?, ?)''', ('greet', greet,))
                await conn.commit()

            else:
                await cur.execute(f'''INSERT INTO greetadress (type, message) 
                                          VALUES (?, ?)''', ('greet', greet,))
                await conn.commit()
        await bot.send_message(chat_id=call.message.chat.id, text='Успешно!')


    elif req == 'Cancel':
        await bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
        await bot.send_message(chat_id=call.message.chat.id,
                               text='Хорошо, вы можете попробовать снова, нажав на кнопку или введя команду')
    else:
        print(req)


# Also a category adding
@dp.message_handler(state=Form.category_name)
async def new_category(message: types.Message, state: FSMContext):
    global name_of_category
    name_of_category = message.text
    if len(name_of_category) < 35:
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton('Продолжить', callback_data='addingcategorytodatabase')
        button2 = InlineKeyboardButton('Отмена', callback_data='Cancel')

        markup.add(button1, button2)
        await bot.send_message(chat_id=message.chat.id,
                               text=f'Хорошо, вы добавляете категорию: {name_of_category}\n\n'
                                    f'Для пользователей: {name_of_users_for_bot_admin}. \n\n'
                                    f'Для города: {city_for_database_while_adding_category} \n\nПродолжить?',
                               reply_markup=markup)
        await state.finish()
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text='Ошибка! название категории слишком длинное! '
                                    'Постарайтесь сократить его до 35 символов,'
                                    ' чтобы кнопка корректно работала!\n\n'
                                    'Для этого начните добавление товара заново введя команду!')
        await state.finish()


# Adding product price
@dp.message_handler(state=Form.product_price)
async def productname(message: types.Message, state: FSMContext):
    global theproductname
    theproductname = message.text
    if len(theproductname) < 35:
        await bot.send_message(chat_id=message.chat.id, text='Хорошо, теперь пришлите стоимость цифрами, например: 1000')

        await Form.product_name.set()
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text='Ошибка! название товара слишком длинное! '
                                    'Постарайтесь сократить его до 35 символов,'
                                    ' чтобы кнопка корректно работала!\n\n'
                                    'Для этого начните добавление товара заново введя команду!')
        await state.finish()


@dp.message_handler(state=Form.product_name)
async def productprice(message: types.Message):
    global theproductprice
    theproductprice = int(message.text)
    await bot.send_message(chat_id=message.chat.id, text='Хорошо, теперь пришлите тип товара, например: шт или кг')

    await Form.product_type.set()


@dp.message_handler(state=Form.product_type)
async def producttype(message: types.Message, state: FSMContext):

    global theproducttype
    theproducttype = message.text

    await bot.send_message(chat_id=message.chat.id, text='Хорошо, теперь пришлите фото товара:')
    await Form.product_photo.set()

@dp.message_handler(state=Form.product_photo, content_types=['photo'])
async def save_photo(message: Message, state: FSMContext):
    global photo_path

    photo = message.photo[-1].file_id
    file = await bot.get_file(photo)
    response = requests.get(f"https://api.telegram.org/file/bot{token}/{file.file_path}")
    with open(f"photos/{file.file_id}.jpg", "wb") as f:
        photo_path = f"photos/{file.file_id}.jpg"
        f.write(response.content)

    await Form.product_type.set()

    markup = InlineKeyboardMarkup()

    button1 = InlineKeyboardButton(text='Продолжить', callback_data='continueaddingproduct')
    button2 = InlineKeyboardButton(text='Отмена', callback_data='Cancel')

    markup.add(button1, button2)
    await bot.send_message(chat_id=message.chat.id, text=f'Всё готово! \n\nИтак, вы добавляете товар '
                                                         f'"{theproductname}", его цена: {theproductprice}р./'
                                                         f'{theproducttype}. \n\nОн будет отображаться в категории '
                                                         f'{category_while_adding_product} в городе '
                                                         f'{city_for_database_while_adding_product} для покупателей {name_of_users_for_bot_admin}',
                           reply_markup=markup)

    await state.finish()


# Also communication with user
@dp.message_handler(state=Form.communication_with_operator)
async def communication(message: types.Message, state: FSMContext):
    message_to_operator = message.text
    async with aiosqlite.connect('database.db') as conn:
        cur = await conn.cursor()
        await cur.execute(
            f'''CREATE TABLE IF NOT EXISTS questions
            (id TEXT, message TEXT)''')
        await conn.commit()
        await cur.execute(f'''INSERT OR IGNORE INTO questions (id, message) 
                          VALUES (?, ?)''', (message.from_user.id, message_to_operator,))
        await conn.commit()

    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text='Ответить', callback_data=f'{message.from_user.id}answertousersqustion')
    markup.add(button1)
    await bot.send_message(chat_id=2849128, text=f'Сообщение от пользователя: @{message.from_user.username}\n\n{message_to_operator}', reply_markup=markup)
    await bot.send_message(chat_id=message.chat.id, text='Отправлено!')
    await state.finish()


@dp.message_handler(state=Form.answer_to_users_question)
async def answer_to_user(message: types.Message, state: FSMContext):
    await bot.delete_message(chat_id=2849128, message_id=id_of_the_message_to_delete_while_answering)
    message_from_operator = message.text
    await bot.send_message(chat_id=id_of_the_user_to_answer, text=f'Ответ от оператора:\n\n{message_from_operator}\n\nДля дальнейшей связи вы можете снова нажать на кнопку "Связь с оператором"')
    await bot.send_message(chat_id=2849128, text='Успешно!')
    await state.finish()


@dp.message_handler(state=Form.promocode)
async def promocode(message: types.Message, state: FSMContext):
    global thepromocodename
    thepromocodename = message.text
    await bot.send_message(chat_id=message.chat.id, text='Хорошо, теперь пришлите размер скидки, который этот промокод предоставляет числом. Например: 5')
    await Form.promocode_price.set()


@dp.message_handler(state=Form.promocode_price)
async def promocode(message: types.Message, state: FSMContext):
    global thepromocodesize
    thepromocodesize = int(message.text)
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text='Продолжить', callback_data='continueaddingpromocode')
    button2 = InlineKeyboardButton(text='Отмена', callback_data='Cancel')
    markup.add(button1)
    markup.add(button2)
    await bot.send_message(chat_id=message.chat.id,
                           text=f'Хорошо, вы добавляете промокод: {thepromocodename}. \n\n'
                                f'Он предоставляет скидку: {thepromocodesize}%', reply_markup=markup)

    await state.finish()

@dp.message_handler(state=Form.promocode_check)
async def check_promocode(message: types.Message, state: FSMContext):
    promocode_to_check = message.text
    global is_promocode
    global total
    rows = False
    async with aiosqlite.connect('database.db') as conn:
        cur = await conn.cursor()
        await cur.execute(f'''SELECT * FROM promocodes WHERE name = ?''', (promocode_to_check,))
        await conn.commit()
        rows = await cur.fetchall()
        rows = [list(i) for i in rows]
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text='Продолжить оформление', callback_data='continuetodelivery')
    button2 = InlineKeyboardButton(text='Отмена', callback_data='Cancel')
    markup.add(button1)
    markup.add(button2)
    if rows:
        is_promocode = (100-rows[0][1]) / 100
        total *= (100-rows[0][1]) / 100
        await bot.send_message(chat_id=message.chat.id,
                               text=f'Этот промокод дает скидку в {rows[0][1]}%! \n\nИтоговая стоимость будет составлять {total}руб.', reply_markup=markup)
    else:
        await bot.send_message(chat_id=message.chat.id, text='Кажется, такого промокода нет! Пожалуйста, проверьте точность написания', reply_markup=markup)
    await state.finish()


@dp.message_handler(state=Form.delivery_by_taxi)
async def delivery_by_taxi(message: types.Message, state: FSMContext):
    global commentary
    commentary = message.text
    markup = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton(text='Отправить номер телефона', request_contact=True)
    markup.add(button1)
    await bot.send_message(chat_id=message.chat.id,
                           text=f'Хорошо! Ваш комментарий: {commentary}. \n\n'
                                f'Для продолжения заказа нам нужно узнать ваш номер телефона. '
                                f'Пожалуйста, нажмите кнопку ниже для его отправки', reply_markup=markup)
    await state.finish()


@dp.message_handler(state=Form.delivery_pickup)
async def delivery_by_taxi(message: types.Message, state: FSMContext):
    global commentary
    commentary = message.text
    markup = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton(text='Отправить номер телефона', request_contact=True)
    markup.add(button1)
    await bot.send_message(chat_id=message.chat.id,
                           text=f'Хорошо! Ваш комментарий: {commentary}. \n\n'
                                f'Для продолжения заказа нам нужно узнать ваш номер телефона. '
                                f'Пожалуйста, нажмите кнопку ниже для его отправки', reply_markup=markup)
    await state.finish()


@dp.message_handler(content_types=['contact'])
async def phone_number(message: types.Message, state: FSMContext):
    global phone_number
    global total
    phone_number = message.contact.phone_number
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('Меню')
    button2 = KeyboardButton('Связь с оператором')
    button3 = KeyboardButton('Корзина')
    button4 = KeyboardButton('О нас')
    button5 = KeyboardButton('Накопительная программа')
    markup.add(button1, button3)
    markup.add(button2, button4)
    markup.add(button5)
    await bot.send_message(chat_id=message.chat.id, text='Одну секунду...', reply_markup=markup)
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text='Оформить!', callback_data='proceedtooperator')
    button2 = InlineKeyboardButton(text='Отмена', callback_data='Cancel')
    markup.add(button1)
    markup.add(button2)
    if is_promocode:

        await bot.send_message(chat_id=message.chat.id,
                           text=f'Итак, ваш заказ на сумму {total}. \n\n'
                                f'Способ доставки: {method_of_the_delivery_for_user} \n\n'
                                f'Комментарий: {commentary} \n\nГотовы оформить?', reply_markup=markup)
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text=f'Итак, ваш заказ на сумму {total}. \n\n'
                                    f'Способ доставки: {method_of_the_delivery_for_user} \n\n'
                                    f'Комментарий: {commentary} \n\nГотовы оформить?', reply_markup=markup)
    await state.finish()


@dp.message_handler(state=Form.mailing)
async def phone_number(message: types.Message, state: FSMContext):
    global message_to_send_as_mailing
    message_to_send_as_mailing = message.text
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text='Продолжить', callback_data=f'finalthemessagingstage')
    button2 = InlineKeyboardButton(text='Отмена', callback_data='Cancel')
    markup.add(button1, button2)

    await bot.send_message(chat_id=message.chat.id,
                           text=f'Хорошо, вы собираетесь отправить следующее сообщение пользователям: \n\n{message_to_send_as_mailing}',
                           reply_markup=markup)

    await state.finish()


@dp.message_handler(state=Form.greet)
async def greet_and_adress(message: types.Message, state: FSMContext):
    global greet
    greet = message.text
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text='Продолжить', callback_data='continueaddinggreet')
    button2 = InlineKeyboardButton(text='Отмена', callback_data='Cancel')
    markup.add(button1)
    markup.add(button2)
    await bot.send_message(chat_id=message.chat.id,
                           text=f'Хорошо, вы добавляете приветственное сообщение: {greet}.', reply_markup=markup)

    await state.finish()


@dp.message_handler(state=Form.adress)
async def greet_and_adress(message: types.Message, state: FSMContext):
    global new_adress
    new_adress = message.text
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text='Продолжить', callback_data='continueaddingadress')
    button2 = InlineKeyboardButton(text='Отмена', callback_data='Cancel')
    markup.add(button1)
    markup.add(button2)
    await bot.send_message(chat_id=message.chat.id,
                           text=f'Хорошо, вы добавляете адрес: {new_adress}.', reply_markup=markup)

    await state.finish()


executor.start_polling(dp, skip_updates=True)
