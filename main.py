from telebot import TeleBot
from telebot import types
import openai
import telegram

# Импортируем токен бота
BOT_TOKEN = "6343679302:AAHE6yURaT3oVGuaOLeQXhIjMUxiSIk5Z6w"


# Создаём объект бота
bot = TeleBot(BOT_TOKEN)

size = ""
genre = ""
mainHeroName = ""

# Подключение и настройка искуственного интеллекта
openai.api_key = "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"
# responce = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {
#             "role": "system",
#             "content": f"Ты - программа, генерирующая сказки, у тебя есть 3 входных данных: Размер сказки: {size}, Жанр: {genre}, Имя главного героя: {mainHeroName}. Сгенерируй сказку по этому запросу",
#         }
#     ],
# )


def getNumberOfCompletions(size):
    if size == "Маленькая":
        return 10
    elif size == "Средняя":
        return 15
    elif size == "Большая":
        return 20


def changeSize(newSize, msg):
    global size
    size = newSize
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    fantasy = types.KeyboardButton("Фентези")
    comedy = types.KeyboardButton("Комедия")
    fantastic = types.KeyboardButton("Фантастика")
    markup.add(fantasy, comedy, fantastic)
    bot.send_message(
        msg.chat.id,
        'Отлично, с размером определились, теперь жанр.\nНа текущий момент имеются 3 жанра: "Фентези", "Комедия", "Фантастика"',
        reply_markup=markup,
    )


def changeGenre(newGenre, msg):
    global genre
    genre = newGenre
    remove = types.ReplyKeyboardRemove()
    bot.send_message(
        msg.chat.id,
        "Хорошо, а какое имя будет у главного героя? Пожалуйста, напиши сообщением",
        reply_markup=remove,
    )


def changeMainHeroName(msg):
    global mainHeroName
    mainHeroName = msg.text
    bot.send_chat_action(chat_id=msg.chat.id, action="Typing", timeout=10)
    responce = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Ты - генератор сказок. У тебя есть единственная задача - создать сказку по заданным параметрам: Размер, жанр, имя главного героя. Сгенерируй сказку по этим параметрам, если жанр - {genre}, а имя главного героя - {mainHeroName}",
        max_tokens=2048,
        n=getNumberOfCompletions(size),
        stop=None,
        temperature=0.5,
    )
    reply = responce.choices[0].text
    answer = f"{reply}\n\nЕсли ты хочешь создать ещё сказку, нажми на кнопку ниже или напиши /fairytail"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    createButton = types.KeyboardButton("Создать сказку")
    markup.add(createButton)
    bot.send_message(msg.chat.id, answer, reply_markup=markup)


def clearAllValues():
    global size
    global genre
    global mainHeroName
    size = ""
    genre = ""
    mainHeroName = ""


# Начало приложения и обработка нажатия кнопки "Создать сказку"
@bot.message_handler(commands=["fairytail"])
@bot.message_handler(regexp="Создать сказку")
def start(msg):
    clearAllValues()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    smallSize = types.KeyboardButton("Маленькая")
    middleSize = types.KeyboardButton("Средняя")
    largeSize = types.KeyboardButton("Большая")
    markup.add(smallSize, middleSize, largeSize)
    bot.send_message(
        msg.chat.id,
        'Отлично, вижу твой настрой.\nДавай теперь определимся с размером сказки.\nНажми на кнопку ниже или напиши "Маленькая", "Средняя" или "Большая"',
        reply_markup=markup,
    )


# Выбор размера сказки


@bot.message_handler(regexp="Маленькая")
def sizeChange(msg):
    changeSize("Маленькая", msg)


@bot.message_handler(regexp="Средняя")
def sizeChange(msg):
    changeSize("Средняя", msg)


@bot.message_handler(regexp="Большая")
def sizeChange(msg):
    changeSize("Большая", msg)


# Конец выбора размера сказки


# Выбор жанра сказки


@bot.message_handler(regexp="Фентези")
def sizeChange(msg):
    changeGenre("Фентези", msg)


@bot.message_handler(regexp="Комедия")
def sizeChange(msg):
    changeGenre("Комедия", msg)


@bot.message_handler(regexp="Фантастика")
def sizeChange(msg):
    changeGenre("Фантастика", msg)


# Конец выбора жанра сказки


# Обработка любого сообщения
@bot.message_handler(func=lambda msg: True)
def echo(msg):
    if genre and not (mainHeroName):
        changeMainHeroName(msg)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        createButton = types.KeyboardButton("Создать сказку")
        markup.add(createButton)
        bot.send_message(
            msg.chat.id,
            "Если ты готов создать сказку, пропиши /fairytail или нажми на кнопку ниже",
            reply_markup=markup,
        )


# Запуск сервера бота
bot.infinity_polling(restart_on_change=True)
