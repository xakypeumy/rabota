from telebot import TeleBot, types
import os

# Папка для загрузки файлов от пользователя
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Файл для хранения тегов, выбранных пользователем при загрузке файла в бота
SETTINGS_FILE = os.path.join(UPLOAD_FOLDER, "search.txt")

# Словарь для хранения данных о загружаемом материале
upload_data = {}

# Временное хранилище данных поиска
search_data = {}

# Доступные дисциплины и типы файлов
DISCIPLINES = ["Математика", "История", "Осн. алг. и прог.", "МДК 02.02", "МДК 05.01", "Английский язык"]
DOC_TYPES = ["Конспект", "Презентация", "Скан", "Изображение"]

# Токен бота
bot = TeleBot('7483199961:AAEbY7Vutbov7ticRMKam3vdeUd53TsnaVE')


# /start
@bot.message_handler(commands=['start'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    # Первый ряд
    help = types.InlineKeyboardButton('Помощь', callback_data='help_btn')
    markup.row(help)
    # Второй ряд
    upload_button = types.InlineKeyboardButton("Загрузить материал", callback_data="upload_material")
    search_button = types.InlineKeyboardButton('Найти материал', callback_data='search_btn')
    markup.row(upload_button, search_button)
    # Третий ряд
    discussion = types.InlineKeyboardButton("Присоединиться к обсуждению", callback_data="join_discussion")
    markup.row(discussion)
    welcome_text = (
        f"Привет! {message.from_user.first_name}\n\n"
        "Я бот для обмена учебными материалами, который поможет тебе получить доступ к знаниям и делиться своими! 📚\n\n"
        "Вот мои возможности:\n"
        "- 🔍 <b>Искать учебные материалы</b> по ключевым словам, категориям и тегам.\n"
        "- 📤 <b>Загружать свои материалы</b>: конспекты, презентации, задачи, учебники и многое другое.\n"
        "- 💬 <b>Общаться в группах и каналах</b>: задавай вопросы, обсуждай темы и помогай другим.\n"
        "- 📂 <b>Сохранять порядок</b>: я организую материалы по категориям и тегам, чтобы их было легко найти.\n\n"
        "Если у Тебя есть вопросы, напиши /help, и я всё объясню.\n\n"
    )
    
    bot.send_message(message.chat.id, welcome_text, parse_mode='html', reply_markup=markup)


# /upload_material
@bot.message_handler(commands=['upload_material'])
def start_upload(message):
    initiate_upload(message.chat.id)

# Начало поиска: выбор дисциплины
def start_search(chat_id):
    search_data[chat_id] = {}  # Очищаем предыдущие данные

    markup = types.InlineKeyboardMarkup()
    for discipline in DISCIPLINES:
        markup.add(types.InlineKeyboardButton(text=discipline, callback_data=f"search_discipline_{discipline}"))
    
    bot.send_message(chat_id, "📚 Выберите дисциплину:", reply_markup=markup)


# Обработчик выбора дисциплины
@bot.callback_query_handler(func=lambda call: call.data.startswith("search_discipline_"))
def save_discipline(call):
    chat_id = call.message.chat.id
    discipline = call.data.split("_")[2]
    search_data[chat_id]["discipline"] = discipline

    markup = types.InlineKeyboardMarkup()
    for doc_type in DOC_TYPES:
        markup.add(types.InlineKeyboardButton(text=doc_type, callback_data=f"search_doc_type_{doc_type}"))
    
    markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_discipline"))
    
    bot.send_message(chat_id, f"📚 Дисциплина: {discipline}\n📄 Теперь выберите тип документа:", reply_markup=markup)


# Обработчик выбора типа документа
@bot.callback_query_handler(func=lambda call: call.data.startswith("search_doc_type_"))
def save_doc_type(call):
    chat_id = call.message.chat.id
    doc_type = call.data.split("_")[2]
    search_data[chat_id]["doc_type"] = doc_type

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_doc_type"))

    bot.send_message(chat_id, "🔍 Введите ключевые слова для поиска (например, 'алгебра уравнения').", reply_markup=markup)
    bot.register_next_step_handler(call.message, search_files)


# Обработчик кнопки "Назад" (к выбору дисциплины)
@bot.callback_query_handler(func=lambda call: call.data == "back_to_discipline")
def back_to_discipline(call):
    start_search(call.message.chat.id)


# Обработчик кнопки "Назад" (к выбору типа документа)
@bot.callback_query_handler(func=lambda call: call.data == "back_to_doc_type")
def back_to_doc_type(call):
    chat_id = call.message.chat.id
    discipline = search_data[chat_id].get("discipline", "Неизвестно")

    markup = types.InlineKeyboardMarkup()
    for doc_type in DOC_TYPES:
        markup.add(types.InlineKeyboardButton(text=doc_type, callback_data=f"search_doc_type_{doc_type}"))
    
    markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_discipline"))

    bot.send_message(chat_id, f"📚 Вы выбрали дисциплину: {discipline}\n📄 Теперь выберите тип документа:", reply_markup=markup)


# Функция поиска файлов
def search_files(message):
    chat_id = message.chat.id
    query = message.text.lower()
    discipline = search_data[chat_id]["discipline"]
    doc_type = search_data[chat_id]["doc_type"]

    results = []

    # Читаем файл с материалами и ищем совпадения
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                _, file_path, file_discipline, file_doc_type = line.strip().split(",")

                # Проверяем совпадения по дисциплине, типу документа и ключевым словам
                file_name = os.path.basename(file_path).lower()
                if (any(word in file_name for word in query.split()) or query in file_discipline.lower()) and \
                   file_discipline == discipline and file_doc_type == doc_type:
                    results.append(file_path)

    # Разметка с кнопками "Попробовать снова" и "Назад"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔄 Попробовать снова", callback_data="try_search_again"))
    markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_doc_type"))

    # Если есть результаты, отправляем файлы
    if results:
        bot.send_message(chat_id, f"📂 Найдено {len(results)} материалов. Отправляю файлы...")

        for file_path in results:
            with open(file_path, "rb") as file:
                bot.send_document(chat_id, file, caption=f"📄 {os.path.basename(file_path)}")
    else:
        bot.send_message(chat_id, "❌ Ничего не найдено. Попробуйте изменить параметры поиска.", reply_markup=markup)


# Обработчик команды /search
@bot.message_handler(commands=['search'])
def search_command(message):
    start_search(message.chat.id)


# Обработчик нажатия кнопки "Найти материал"
@bot.callback_query_handler(func=lambda call: call.data == "search_btn")
def handle_search_button(call):
    start_search(call.message.chat.id)


# Обработчик кнопки "🔄 Попробовать снова"
@bot.callback_query_handler(func=lambda call: call.data == "try_search_again")
def retry_search(call):
    start_search(call.message.chat.id)

# функция обсуждения
def join_discussion(chat_id):
    link = 'https://t.me/+0flZl9J57fs4MGMy'
    text =(
        'У нас есть свой собственный чат, где Вы можете обсудить нажный вам материал и запросить у знакомыйх новый.\n\n'
        'Для того чтобы присоединиться к обсуждению перейдите по ссылке ниже:\n'
        f'<a href="{link}"> Присоединиться к обсуждению</a>'
    )
    bot.send_message(chat_id, text, parse_mode='html')


# Обработчик нажатия кнопки "Присоединиться к обсуждению"
@bot.callback_query_handler(func=lambda call: call.data == "join_discussion")
def handle_upload_button(call):
    join_discussion(call.message.chat.id)


# /join_discussion
@bot.message_handler(commands=['join_discussion'])
def main(message):
    join_discussion(message.chat.id)




# функция помощи
def help_btn(chat_id):
    markup = types.InlineKeyboardMarkup()
    upload_button = types.InlineKeyboardButton("Загрузить материал", callback_data="upload_material")
    search_button = types.InlineKeyboardButton('Найти материал', callback_data='search_btn')
    markup.row(upload_button, search_button)
    discussion = types.InlineKeyboardButton("Присоединиться к обсуждению", callback_data="join_discussion")
    markup.row(discussion)
    help_text = (
    "💡 <b>Справка по командам бота:</b>\n\n"
    "📤 <b>Загрузка материалов:</b>\n"
    "Отправь файл (PDF, DOCX, PPT или изображение) в чат, и бот попросит добавить описание, категорию и теги.\n\n"
    "🔍 <b>Поиск материалов:</b>\n"
    "Используй команду /search, чтобы найти материалы по ключевым словам, категориям или тегам.\n"
    "Пример: '/search математика алгебра'\n\n"
    "💬 <b>Общение:</b>\n"
    "Для обсуждения материалов или вопросов присоединяйся к группе или каналу с помощью команды /join_discussion.\n\n"
    )
    bot.send_message(chat_id, help_text, parse_mode='html', reply_markup=markup)


# Обработчик нажатия кнопки "Помощь"
@bot.callback_query_handler(func=lambda call: call.data == "help_btn")
def handle_upload_button(call):
    help_btn(call.message.chat.id)

# /help
@bot.message_handler(commands=['help'])
def main(message):
    help_btn(message.chat.id)


# Функция, запускающая процесс загрузки
def initiate_upload(chat_id):
    bot.send_message(
        chat_id,
        "Отправьте файл, который хотите загрузить. Поддерживаемые форматы: PDF, DOCX, PPT, TXT, WORD, изображение."
    )
    upload_data[chat_id] = {}  # Инициализируем место для хранения данных


# Обработчик нажатия кнопки "Загрузить материал"
@bot.callback_query_handler(func=lambda call: call.data == "upload_material")
def handle_upload_button(call):
    initiate_upload(call.message.chat.id)


# Обработчик загрузки файла
@bot.message_handler(content_types=['document', 'photo'])
def handle_file_upload(message):
    if not message.document and not message.photo:
        bot.send_message(message.chat.id, "Это не файл. Пожалуйста, отправьте файл.")
        return initiate_upload(message.chat.id)  # Повторно вызываем функцию для нового ввода.

    # Определяем имя файла
    if message.document:
        file_info = bot.get_file(message.document.file_id)
        file_extension = os.path.splitext(message.document.file_name)[-1].lower()
    elif message.photo:
        file_info = bot.get_file(message.photo[-1].file_id)
        file_extension = ".jpg"

    # Проверяем формат файла
    allowed_extensions = ['.pdf', '.docx', '.pptx', '.txt', '.jpg', '.png']
    if file_extension not in allowed_extensions:
        bot.send_message(
            message.chat.id, 
            "Неподдерживаемый формат файла. Попробуйте снова."
        )
        return initiate_upload(message.chat.id)

    # Загружаем файл с сервера Telegram
    downloaded_file = bot.download_file(file_info.file_path)
    temp_file_path = os.path.join(UPLOAD_FOLDER, f"temp_{message.chat.id}{file_extension}")
    with open(temp_file_path, "wb") as file:
        file.write(downloaded_file)

    # Сохраняем временный путь и ожидаем дальнейших действий
    upload_data[message.chat.id] = {"file_path": temp_file_path}
    bot.send_message(message.chat.id, "Файл успешно загружен! Теперь выберите дисциплину.")
    ask_for_discipline(message)


# Выбор дисциплины
def ask_for_discipline(message):
    markup = types.InlineKeyboardMarkup()
    disciplines = ["Математика", "История", "Осн. алг. и прог.", "МДК 02.02", "МДК 05.01", "Английский язык"]
    for discipline in disciplines:
        markup.add(types.InlineKeyboardButton(text=discipline, callback_data=f"discipline_{discipline}"))
    
    bot.send_message(
        message.chat.id, 
        "Выберите дисциплину:", 
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("discipline_"))
def save_discipline(call):
    discipline = call.data.split("_")[1]
    upload_data[call.message.chat.id]["discipline"] = discipline
    bot.send_message(call.message.chat.id, f"Вы выбрали дисциплину: {discipline}. Теперь выберите тип документа.")
    ask_for_doc_type(call.message)


# Выбор типа документа
def ask_for_doc_type(message):
    markup = types.InlineKeyboardMarkup()
    doc_types = ["Конспект", "Презентация", "Скан", "Изображение"]
    for doc_type in doc_types:
        markup.add(types.InlineKeyboardButton(text=doc_type, callback_data=f"doc_type_{doc_type}"))
    
    bot.send_message(
        message.chat.id, 
        "Выберите тип документа:", 
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("doc_type_"))
def save_doc_type(call):
    doc_type = call.data.split("_")[1]
    upload_data[call.message.chat.id]["doc_type"] = doc_type
    bot.send_message(
        call.message.chat.id, 
        f"Вы выбрали тип документа: {doc_type}. Теперь введите название для файла."
    )
    bot.register_next_step_handler(call.message, save_file_with_name)


# Сохранение файла с заданным пользователем именем
def save_file_with_name(message):
    user_data = upload_data.get(message.chat.id, {})
    if not user_data:
        bot.send_message(message.chat.id, "Произошла ошибка. Начните заново командой /upload_material.")
        return

    file_path = user_data.get("file_path")
    discipline = user_data.get("discipline")
    doc_type = user_data.get("doc_type")
    file_extension = os.path.splitext(file_path)[-1]

    # Получаем название файла от пользователя
    file_name = f"{message.text}{file_extension}"
    final_path = os.path.join(UPLOAD_FOLDER, file_name)

    # Переименовываем и сохраняем файл
    os.rename(file_path, final_path)

    # Сохраняем информацию в текстовом файле
    with open(SETTINGS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{message.chat.id},{final_path},{discipline},{doc_type}\n")

    # Создаем разметку с кнопкой "Вернуться к выбору действия"
    markup = types.InlineKeyboardMarkup()
    return_to_menu_btn = types.InlineKeyboardButton(
        text="Вернуться к выбору действия", callback_data="return_to_menu"
    )
    markup.add(return_to_menu_btn)

    bot.send_message(
        message.chat.id,
        f"Файл успешно сохранён под названием: {file_name}. Вы можете найти его позже с помощью команды поиска.",
        reply_markup=markup
    )

    # Очищаем временные данные
    upload_data.pop(message.chat.id, None)



# Обработчик кнопки "Вернуться к выбору действия"
@bot.callback_query_handler(func=lambda call: call.data == "return_to_menu")
def return_to_menu(call):
    markup = types.InlineKeyboardMarkup()
    upload_button = types.InlineKeyboardButton("Загрузить файл", callback_data="upload_material")
    search_button = types.InlineKeyboardButton("Найти файл", callback_data="search_btn")
    markup.row(upload_button, search_button)
    discussion = types.InlineKeyboardButton("Присоединиться к обсуждению", callback_data="join_discussion")
    markup.row(discussion)
    

    bot.send_message(
        call.message.chat.id,
        "Что Вы хотите сделать?",
        reply_markup=markup
    )


# Программа работает бесконечно
bot.polling(none_stop=True)