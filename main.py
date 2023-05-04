import telebot, wikipedia, re,logging, time, sqlite3
from telebot import types

#pip install pyTelegramBotAPI

bot = telebot.TeleBot('6077737981:AAEqwrGN5xk7sWt6jmTuy-5QxC4QPbK199o')

conn = sqlite3.connect('school.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_name TEXT, user_surname TEXT, username TEXT, datetime INTEGER)')

cursor.execute('CREATE TABLE IF NOT EXISTS Records (id INTEGER PRIMARY KEY, user_name TEXT, user_surname TEXT, username TEXT, Records TEXT, datetime INTEGER)')

cursor.execute('CREATE TABLE IF NOT EXISTS Photo (id INTEGER PRIMARY KEY, user_name TEXT, user_surname TEXT, username TEXT, Photo BLOB, datetime INTEGER)')

wikipedia.set_lang("ru")

@bot.message_handler(commands=['start'])
def menu1(message):
    #us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    logging.info(f'{time.asctime()}')
    Datetime = (f'{time.strftime("%d-%m-%y %H:%M:%S")}')
    cursor.execute("INSERT INTO users (user_name, user_surname, username, datetime) VALUES (?, ?, ?, ?)", ( us_name, us_sname, username, Datetime))
    conn.commit()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    menu = types.KeyboardButton('/menu')
    start = types.KeyboardButton('/interesting')
    markup.add(menu, start)
    bot.send_message(message.chat.id, "Добро пожаловать, выберите меню!", reply_markup=markup)


#Комманды Боту
@bot.message_handler(commands=["menu"])
def menu_glavnoe(message):
    start_markup = types.InlineKeyboardMarkup()

    btn1= types.InlineKeyboardButton('какой сейчас день недели?', callback_data = '2')
    btn3= types.InlineKeyboardButton('Сайт Лицея', url="https://rtlguboglo.edu-cl.net/")
    start_markup.row(btn1, btn3)

    btn4= types.InlineKeyboardButton('фото', callback_data = '3')
    btn6= types.InlineKeyboardButton('id', callback_data = '4')
    btn8= types.InlineKeyboardButton('about', callback_data = '5')
    start_markup.row(btn4, btn6, btn8)
    bot.send_message(message.chat.id, "Привет дорогой посетитель, Выбери что тебе нужно)", reply_markup=start_markup)


@bot.message_handler(commands=["interesting"])
def write(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Привет', callback_data = 'Hello')
    button2 = types.InlineKeyboardButton('Как дела?', callback_data = 'dela')
    button3 = types.InlineKeyboardButton('Скинь расписание на сегодня', callback_data='raspisanie_segodnea')
    button4 = types.InlineKeyboardButton('Какое сегодня меню?', callback_data='menu_segodnea')
    markup.row(button1, button2)
    markup.row(button3, button4)
    bot.send_message(message.chat.id, "Привет дорогой посетитель, Выбери что тебе нужно)", reply_markup=markup)


@bot.callback_query_handler(func = lambda call: True)
def answer(call):
    if call.data == '1':
        bot.send_message(call.message.chat.id, 'Перейдите по ссылке на сайт Лицея: https://rtlguboglo.edu-cl.net/')
    elif call.data == '2':
        logging.info(f'{time.asctime()}')
        bot.send_message(call.message.chat.id, f'{time.strftime("Today is %A.")}')
    elif call.data == 'Hello':
        bot.send_message(call.message.chat.id, "И тебе привет😀")
    elif call.data == 'фото':
        bot.send_message(call.message.chat.id, "Для регистрации Напишите Имя, Фамилию и Клас")
    elif call.data == '3':
        photo = open('teacers.png', 'rb')
        bot.send_photo(call.message.chat.id, photo)
    elif call.data == 'dela':
        bot.send_message(call.message.chat.id, 'Дела отлично, думаю о развитии😎')
    elif call.data == 'raspisanie_segodnea':
        logging.info(f'{time.asctime()}')
        if (f'{time.strftime("%A")}') == "Monday":
            photo = open('Monday.png', 'rb')
            bot.send_message(call.message.chat.id, f'Вот расписание на понедельник:')
            bot.send_photo(call.message.chat.id, photo)
        elif (f'{time.strftime("%A")}') == "Tuesday":
            photo = open('Tuesday.png', 'rb')
            bot.send_message(call.message.chat.id, f'Вот расписание на вторник:')
            bot.send_photo(call.message.chat.id, photo)
        elif (f'{time.strftime("%A")}') == "Wednesday":
            photo = open('Wednesday.png', 'rb')
            bot.send_message(call.message.chat.id, f'Вот расписание на среду:')
            bot.send_photo(call.message.chat.id, photo)
        elif (f'{time.strftime("%A")}') == "Thursday":
            photo = open('Thursday.png', 'rb')
            bot.send_message(call.message.chat.id, f'Вот расписание на четверг:')
            bot.send_photo(call.message.chat.id, photo)
        elif (f'{time.strftime("%A")}') == "Friday":
            photo = open('Friday.png', 'rb')
            bot.send_message(call.message.chat.id, f'Вот расписание на пятницу:')
            bot.send_photo(call.message.chat.id, photo)
        else:
            bot.send_message(call.message.chat.id, "Сегодня выходной!")
    elif call.data == '4':
        bot.send_message(call.message.chat.id, f"Твой ID: {call.message.from_user.id}", parse_mode='html')
    elif call.data == 'menu_segodnea':
        if (f'{time.strftime("%A")}') == "Monday":
            bot.send_message(call.message.chat.id, f'Сегодня вас ожидаает молочная каша😜')
        elif (f'{time.strftime("%A")}') == "Tuesday":
            bot.send_message(call.message.chat.id, f'Сегодня вас ожидаает плов с мясом😜')
        elif (f'{time.strftime("%A")}') == "Wednesday":
            bot.send_message(call.message.chat.id, f'Сегодня вас ожидаает картошка пюре с салатом😜')
        elif (f'{time.strftime("%A")}') == "Thursday":
            bot.send_message(call.message.chat.id, f'Сегодня вас ожидают макароны с творогом😜')
        elif (f'{time.strftime("%A")}') == "Friday":
            bot.send_message(call.message.chat.id, f'Сегодня вас ожидаает гречка с катлеткой😜')
        else:
            bot.send_message(call.message.chat.id, "Сегодня выходной!")
    elif call.data == '5':
        bot.send_message(call.message.chat.id, 'Данного бота создал ученик 12А класса Кусурсуз Максим')
    else:
        bot.send_message(call.message.chat.id, 'Что-то пошло не так!')


@bot.message_handler(commands=['регистрация', 'register'])
def handle_comment(message):
    bot.send_message(message.chat.id, "Для регистрации на конкурс 'Мэрцишор' введите: Имя, Фамилию и класс")
    bot.register_next_step_handler(message, register)

def register(message):
    #us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    record = message.text
    logging.info(f'{time.asctime()}')
    Datetime = (f'{time.strftime("%d-%m-%y %H:%M:%S")}')
    cursor.execute("INSERT INTO Records (user_name, user_surname, username, Records, datetime) VALUES (?, ?, ?, ?, ?)", (us_name, us_sname, username, record, Datetime))
    bot.send_message(message.chat.id, "вы успешно зарегестрированы, можете скинуть фото! ")


#Википедия
def getwiki(s):
    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wikitext=ny.content[:1000]
        # Разделяем по точкам
        wikimas=wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not('==' in x):
                    # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'В энциклопедии нет информации об этом'

@bot.message_handler(commands=['комментарий', 'comment'])
def handle_comment(message):
    bot.send_message(message.chat.id, "Введите ваш комментарий:")
    bot.register_next_step_handler(message, handle_text)


def get_sentiment_score(sentence):
    # Define lists of positive and negative words
    positive_words = ['хорошо', 'отлично', 'красивый', 'прекрасно', 'лучший', 'хороший', 'отличный', 'красиво', 'прекрасно', 'не плохо', 'Спасибо', 'Красивый', 'Прекрасно', 'Лучший', 'хорошую', 'отличную', 'Красиво', 'прекрасную', 'Не плохо','не плохую']
    negative_words = ['плохой', 'плохо', 'ужасно', 'ужасный', 'не красиво', 'не работает', 'криво', 'не нравится', 'никогда', 'ужас']

    # Calculate the number of positive and negative words in the sentence
    num_positive = sum([1 for word in sentence.split() if word.lower() in positive_words])
    num_negative = sum([1 for word in sentence.split() if word.lower() in negative_words])

    # Calculate the sentiment score by subtracting the number of negative words from the number of positive words
    sentiment_score = num_positive - num_negative

    return sentiment_score


def handle_text(message):

    # us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    record = message.text
    logging.info(f'{time.asctime()}')
    Datetime = (f'{time.strftime("%d-%m-%y %H:%M:%S")}')
    cursor.execute("INSERT INTO Records (user_name, user_surname, username, Records, datetime) VALUES (?, ?, ?, ?, ?)", (us_name, us_sname, username, record, Datetime))
    sentiment_score = get_sentiment_score(message.text)
    if sentiment_score > 0:
        response = "Спасибо за позитивный комментарий!"
    elif sentiment_score < 0:
        response = "Это негативный комментарий."
    else:
        response = "Это неитральный комментарий."
    bot.send_message(message.chat.id, response)
  #  bot.send_message(message.chat.id, "Комментарий получен: " + message.text)

#Работа с сообщениями
@bot.message_handler(content_types=['text'])
def get_user_text(message):
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    record = message.text
    logging.info(f'{time.asctime()}')
    Datetime = (f'{time.strftime("%d-%m-%y %H:%M:%S")}')
    cursor.execute("INSERT INTO Records (user_name, user_surname, username, Records, datetime) VALUES (?, ?, ?, ?, ?)", (us_name, us_sname, username, record, Datetime))

    if message.text == "как дела?":
        bot.send_message(message.chat.id, message)
    elif message.text == "Расписание":
        bot.send_message(message.chat.id, "Перейдите по ссылке на сайт Лицея: https://rtlguboglo.edu-cl.net/", parse_mode='html')
    elif message.text == "фото":
        photo = open('teacers.png', 'rb')
        bot.send_photo(message.chat.id, photo)
    elif message.text == "id":
        bot.send_message(message.chat.id, f"Твой ID: {message.from_user.id}", parse_mode='html')
    else:
        bot.send_message(message.chat.id, "Ищу в Википедии: ")
        bot.send_message(message.chat.id, getwiki(message.text))


@bot.message_handler(content_types=['photo', 'file'])
def get_user_photo(message):
    if message.content_type == 'photo':
        us_name = message.from_user.first_name
        us_sname = message.from_user.last_name
        username = message.from_user.username
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        Photo = bot.download_file(file_path)
        logging.info(f'{time.asctime()}')
        Datetime = (f'{time.strftime("%d-%m-%y %H:%M:%S")}')
        cursor.execute("INSERT INTO Photo (user_name, user_surname, username, Photo, datetime) VALUES (?, ?, ?, ?, ?)", ( us_name, us_sname, username, Photo, Datetime))
        bot.send_message(message.chat.id, 'Вау, красивое фото!')
    else:
        bot.send_message(message.chat.id, 'скиньте фото без сжатия в пнг формате!')

#Запуск работы Бота
bot.polling(none_stop=True)
