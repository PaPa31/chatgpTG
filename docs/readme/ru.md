- Бот: https://t.me/chismegptbpt

[![ru](https://img.shields.io/badge/Переменные-ru-blue)](https://gg.resisto.rodeo/yo/chatgpTG/src/branch/main/docs/variables/ru.md)

## Команды:
- /new - Начать новый диалог.
- /img - Создать изображения.
- /retry - Повторить последний ответ бота.
- /chat_mode - Выбрать режим разговора.
- /model - Показать модели ИИ.
- /api - Показать API.
- /lang - Показать доступные языки.
- /status - Показать текущую конфигурацию: Модель, Режим чата и API.
- /reset - Сбросить настройки на значения по умолчанию.
- /search - Поиск в интернете.
- /help - Показать это сообщение снова.

## Особенности:
- Вызов функций! (плагины, прямо подключенные к GPT, модели за июнь>).
- Локальная база данных JSON.
- Очень модульный и настраиваемый.
- Позволяет GPT получать доступ к Интернету с помощью /search!
- Отправляйте текстовые файлы, PDF или URL, и бот сможет их проанализировать!
- Добавляйте обратные прокси от OpenAI и соответствующие модели сколько угодно!
- Мультиязычность.
- Чтение текста с изображений.
- Транскрибация аудио.

# Важно:
- Пользовательские API должны иметь ту же структуру, что и OpenAI, то есть "https://domain.dom/v1/..."

## Установка
1. Получите свой ключ [OpenAI API](https://openai.com/api/)

2. Получите токен вашего бота в Telegram от [@BotFather](https://t.me/BotFather)

3. Отредактируйте `config/api.example.json`, чтобы настроить ваш API-KEY или добавить пользовательские API

4. Добавьте ваш токен Telegram, базу данных Mongo, измените другие переменные в 'docker-compose.example.yml' и переименуйте `docker-compose.example.yml` в `docker-compose.yml`

5. 🔥 Зайдите в каталог через терминал и **выполните**:
    ```bash
    docker-compose up --build
    ```
# История звезд

<a href="https://gg.resisto.rodeo/yo/chatgpTG"><img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=soyelmismo/chatgpTG&type=Date"></a> 

## Ссылки
1. Источник: <a href="https://github.com/karfly/chatgpt_telegram_bot" alt="Karfly">Karfly/chatgpt_telegram_bot</a>