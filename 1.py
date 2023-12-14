import telebot

bot = telebot.TeleBot('6034256644:AAE08XAUlHuS5RaqCLZCERCeitTWg03tjTU')

students = {}  # Словарь для хранения логинов и оценок студентов
teachers = {}  # Словарь для хранения кодов доступа преподавателей

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Добро пожаловать! Выберите опцию:")
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    register_button = telebot.types.KeyboardButton(text='Зарегистрироваться')
    login_button = telebot.types.KeyboardButton(text='Войти')
    keyboard.add(register_button, login_button)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if message.text == 'Студент':
        handle_student_login(message)
    elif message.text == 'Преподаватель':
        handle_teacher_login(message)
    else:
        bot.reply_to(message, "Пожалуйста, выберите 'Студент' или 'Преподаватель'.")




@bot.message_handler(func=lambda message: message.text == 'Студент')
def handle_student_login(message):
    bot.reply_to(message, "Пожалуйста, введите ваш логин:")
    bot.register_next_step_handler(message, process_student_login_step)



def process_student_login_step(message):
    login = message.text
    if login in students:
        bot.reply_to(message, f"Вход выполнен успешно, {login}!")
        student_panel(message)
    else:
        bot.reply_to(message, "Логин не найден. Попробуйте еще раз.")


@bot.message_handler(func=lambda message: message.text == 'Преподаватель')
def handle_teacher_login(message):
    bot.reply_to(message, "Введите код доступа для преподавателя:")
    bot.register_next_step_handler(message, process_teacher_login_step)


def process_teacher_login_step(message):
    access_code = message.text
    if access_code == 'universalkey':
        teachers[message.from_user.id] = access_code
        bot.reply_to(message, "Вы успешно вошли в систему как преподаватель!")
        teacher_panel(message)
    else:
        bot.reply_to(message, "Неверный код доступа. Попробуйте еще раз.")


def student_panel(message):
    pass
def teacher_panel(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = telebot.types.KeyboardButton(text="Выставить оценку")
    keyboard.add(button)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Выставить оценку')
def handle_grade_input(message):
    if message.from_user.id not in teachers:
        bot.reply_to(message,"Вы не авторизованы как преподаватель. Пожалуйста, выполните вход с использованием правильного кода доступа.")
        return

    bot.reply_to(message, "Введите логин студента:")
    bot.register_next_step_handler(message, process_grade_input_step)


def process_grade_input_step(message):
    student_login = message.text
    if student_login in students:
        bot.reply_to(message, f"Введите оценку для студента {student_login}:")
        bot.register_next_step_handler(message, process_grade_save_step)
    else:
        bot.reply_to(message, "Логин студента не найден. Попробуйте еще раз.")


def process_grade_save_step(message):
    try:
        grade = float(message.text)
        # добавление логики для сохранения оценки студента
        bot.reply_to(message, "Оценка сохранена успешно.")
    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите число в качестве оценки.")


bot.polling(none_stop=True)


