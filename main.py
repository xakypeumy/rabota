import telebot
from telebot import types

# токен бота
bot = telebot.TeleBot('7483199961:AAEbY7Vutbov7ticRMKam3vdeUd53TsnaVE')

@bot.message_handler(commands=['start']) #декоратор комманды
def main(message):
    welcome_text = (
    f"Привет! {message.from_user.first_name}\n\n"
    "Я бот для обмена учебными материалами, который поможет тебе получить доступ к знаниям и делиться своими! 📚\n\n"
    "Вот мои возможности:\n"
    "- 🔍 <b>Искать учебные материалы</b> по ключевым словам, категориям и тегам.\n"
    "- 📤 <b>Загружать свои материалы</b>: конспекты, презентации, задачи, учебники и многое другое.\n"
    "- 💬 <b>Общаться в группах и каналах</b>: задавай вопросы, обсуждай темы и помогай другим.\n"
    "- 📂 <b>Сохранять порядок</b>: я организую материалы по категориям и тегам, чтобы их было легко найти.\n\n"
    "Как начать?\n"
    "- Чтобы загрузить материал, используй команду /upload_material.\n"
    "- Чтобы найти что-то, используй команду /search.\n"
    "- Для общения в канале используй команду /join_discussion.\n\n"
    "Если у Тебя есть вопросы, напиши /help, и я всё объясню. 😊\n\n"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='html')

@bot.message_handler(commands=['help'])
def main(message):
    help_text = (
    "💡 <b>Справка по командам бота:</b>\n\n"
    "📤 <b>Загрузка материалов:</b>\n"
    "Отправь файл (PDF, DOCX, PPT или изображение) в чат, и бот попросит добавить описание, категорию и теги.\n\n"
    "🔍 <b>Поиск материалов:</b>\n"
    "Используй команду /search, чтобы найти материалы по ключевым словам, категориям или тегам.\n"
    "Пример: `/search математика алгебра`\n\n"
    "💬 <b>Общение:</b>\n"
    "Для обсуждения материалов или вопросов присоединяйся к группе или каналу с помощью команды /join_discussion.\n\n"
    )
    bot.send_message(message.chat.id, help_text, parse_mode='html')











# для отладки
@bot.message_handler(commands=['message']) 
def main(message):
    bot.send_message(message.chat.id, message)




#программа работает бесконечно
bot.polling(none_stop=True)