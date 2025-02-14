# Бот для обмена учебными материалами @oaip22_bot
Описание:
Бот для обмена учебными материалами может стать отличным ресурсом для студентов, желающих делиться своими учебными материалами, такими как конспекты, презентации, задачи и учебники. Это позволит создать сообщество, где студенты могут легко находить и обмениваться знаниями.
## Функциональность

1. Загрузка материалов:
   - Пользователи могут загружать свои учебные материалы в бота.
   - Бот поддерживает разные форматы, такие как PDF, DOCX, PPT и изображения (например, сканы).
   - Файлы, загруженные в бота, сохраняются в папке на устройстве, на котором запущен бот.
2. Категоризация материалов:
   - Материалы будут организованы по категориям (дисциплины, типы документов).
   - Пользователи смогут добавлять теги к материалам для удобства поиска.
3. Поиск и фильтрация:
   - Бот предоставляет возможность искать материалы по ключевым словам, категориям и тегам.
   - Пользователи могут фильтровать результаты поиска по популярности или дате загрузки.
   - Поиск выполняется из файлов, находящихся в определённой папке
4. Чат для обсуждений:
   - Бот  создаёт каналы или группы для обсуждения материалов и вопросов по учебе.
   - Студенты могут задавать вопросы и получать помощь от других участников.
Преимущества:
- Удобный и быстрый доступ к учебным ресурсам.
- Создание сообщества, где студенты могут поддерживать друг друга.
- Обогащение учебного процесса благодаря обмену знаниями и опытом.
  
## Установка

1. Установка зависимостей:
   ```bash
   Для быстрой установки всех необходимых библиотек запустите файл setup.py
   ```
   Либо вручную через cmd или powershell:
   ```bash
   pip install pyTelegramBotAPI==4.26.0
   ```
2. Установка токена:
   ```bash 
   в файле main.py замените значение переменной в скобках `bot = TeleBot('')` на нужное Вам.
   ```
4. Запустите бота:
   ```bash
   python main.py
   ```
## ВАЖНО!!!

Бот автоматические создаёт нужные для корректной работы папки и файлы. Вручную создавать ничего не нужно!   
Создаваемые файлы и папки:

**\rabota-main\uploads** - папка для хранения выгружаемых в бота файлов   
**\rabota-main\uploads\search.txt** - файл для хранения данных для работы функции поиска

## 💡 Использование

### Основные команды:

- **/start** — Запуск бота и отображение главного меню.
- **/help** — Вызов окна помощи.
- **/join_discussion** — Присоединиться к обсуждению.
- **/upload** — Загрузить файл в бота.
- **/search** — Поиск ранее загруженных файлов.

<ins>К каждой команде привязана соответствующая кнопка</ins>
  
  

  
### Установить библиотеки вручную можно по спику ниже.  
  
Используемые библиотеки:  

[pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)  
  

