# SOLUTION DESIGN: Экосистема автоматической публикации YouTube (AI-Driven)

**Автор:** Gemini (AI Architect)  
**Назначение:** Полная автономная цепочка производства и дистрибуции видеоконтента.

---

## 1. Архитектурная концепция (The Workflow)

Система строится на базе трех независимых слоев:
1.  **Слой наблюдения (Watcher):** Мониторинг входящих файлов (локально или облако).
2.  **Слой интеллекта (Gemini 1.5 Pro):** Мультимодальный анализ видеоряда и генерация смысловой «упаковки».
3.  **Слой исполнения (Transport):** Загрузка на платформу через API или эмуляцию браузера.



---

## 2. Слой Интеллекта: Анализ и Смыслы
Самый важный этап. Мы не просто просим «описать видео», мы заставляем модель работать как SEO-специалист и маркетолог.

### Логика обработки (Python):
```python
import google.generativeai as genai
import json
import time

def get_video_intel(file_path):
    # Конфигурация модели
    genai.configure(api_key="YOUR_API_KEY")
    model = genai.GenerativeModel('gemini-1.5-pro')

    # Загрузка видео во временное хранилище Google
    print(f"[SYSTEM] Загрузка видео в облако для анализа: {file_path}")
    video_file = genai.upload_file(path=file_path)

    # Ожидание индексации (важно: модель не может анализировать, пока статус не ACTIVE)
    while video_file.state.name == "PROCESSING":
        time.sleep(2)
        video_file = genai.get_file(video_file.name)

    # Системный промпт (инструкция для агента)
    prompt = """
    Ты — экспертный контент-менеджер YouTube. Твоя задача:
    1. Проанализировать видео и понять его главную ценность.
    2. Создать заголовок (CTR > 10%) и описание с ключевыми словами.
    3. Выделить таймкоды для навигации.
    4. Предложить 3 варианта промпта для генерации обложки.

    ВЫДАЙ ОТВЕТ СТРОГО В JSON:
    {
      "title": "...",
      "description": "...",
      "tags": ["...", "..."],
      "chapters": "00:00 Введение\\n05:20 Настройка агента",
      "thumbnail_prompts": ["...", "..."]
    }
    """

    response = model.generate_content([video_file, prompt])
    return json.loads(response.text.strip('```json').strip('```'))
```

---

## 3. Слой Исполнения: Два пути загрузки

### Путь А: YouTube Data API (Стабильность)
Используется для регулярного постинга до 5-6 роликов в день.

```python
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

def upload_via_api(file_path, intel):
    # Авторизация (используем OAuth2)
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', 
        scopes=['https://www.googleapis.com/auth/youtube.upload'])
    credentials = flow.run_local_server(port=0)
    youtube = build('youtube', 'v3', credentials=credentials)

    request_body = {
        'snippet': {
            'title': intel['title'],
            'description': f"{intel['description']}\n\nТаймкоды:\n{intel['chapters']}",
            'tags': intel['tags'],
            'categoryId': '27' # Education
        },
        'status': {
            'privacyStatus': 'unlisted', # Загружаем как 'по ссылке' для проверки
            'selfDeclaredMadeForKids': False
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    response = youtube.videos().insert(part='snippet,status', body=request_body, media_body=media).execute()
    return response['id']
```

### Путь Б: Playwright (Масштабируемость и Обход лимитов)
Используется, если нужно имитировать действия человека или обходить квоты API.

```python
from playwright.sync_api import sync_playwright

def upload_via_playwright(file_path, intel):
    with sync_playwright() as p:
        # Важно: используем существующий профиль браузера, чтобы не вводить пароль и 2FA
        context = p.chromium.launch_persistent_context(
            user_data_dir="./youtube_session", 
            headless=False # Включаем видимость для отладки
        )
        page = context.new_page()
        page.goto("https://studio.youtube.com")

        # Навигация по интерфейсу YouTube Studio
        page.click("#create-icon")
        page.set_input_files("input[type='file']", file_path)

        # Заполнение данных из JSON (от Gemini)
        page.wait_for_selector("#title-textarea")
        page.fill("#title-textarea", intel['title'])
        page.fill("#description-textarea", f"{intel['description']}\n{intel['chapters']}")

        # Автоматическое прохождение шагов (Проверки, Дополнения, Доступ)
        for _ in range(3):
            page.click("#next-button")
            time.sleep(1)

        page.click("tp-yt-paper-radio-button[name='PUBLIC']") # Сразу в паблик
        page.click("#done-button")
        context.close()
```

---

## 4. Слой Оркестрации (Логика Агента)

Чтобы всё это работало как единая система (например, на сервере), нужен главный цикл:

1.  **Scan:** Проверить папку `upload_queue`.
2.  **Validate:** Проверить размер файла (если > 2 ГБ, запустить сжатие через `ffmpeg`).
3.  **Process:**
    * Отправить в Gemini -> Получить JSON.
    * Попробовать загрузить через API.
    * Если ошибка `Quota Exceeded` -> Переключиться на Playwright.
4.  **Notify:** Отправить отчет в Telegram со ссылкой на видео.
5.  **Clean:** Переместить обработанный файл в папку `Archive`.

---

## 5. Почему это решение подходит для Предпринимателя (Product Owner)

1.  **Мультимодальность:** Мы не используем сторонние сервисы транскрибации (типа Whisper). Gemini «видит» картинку и «слышит» звук одновременно, что дает более глубокое описание (например, он поймет, что вы показываете на графике).
2.  **Экономика:** Вы платите только за токены API (копейки за ролик) вместо дорогих подписок на сервисы автопостинга.
3.  **Гибкость:** Вы можете добавить в цепочку этап «Генерация обложки», где агент будет брать `thumbnail_prompts` и отправлять их в Midjourney или DALL-E 3.

---


Это отличный подход. Мы превратим этот код в **«живую документацию»**. Ниже представлен полный, готовый к работе Python-скрипт. Я снабдил его избыточными комментариями, чтобы даже новичок понял логику каждого шага: от импорта библиотек до нажатия кнопки «Опубликовать».

---

# 📄 Полное техническое руководство: Python-агент для YouTube

Этот документ объединяет архитектурную логику и исполняемый код. Вы можете скопировать его в файл `youtube_agent.py` и запустить после настройки ключей.

## 1. Подготовка окружения
Прежде чем запускать код, нужно установить «инструменты» (библиотеки). Откройте терминал и введите:
```bash
pip install google-generativeai google-auth-oauthlib google-api-python-client playwright
playwright install chromium
```

---

## 2. Полный код агента (с подробными комментариями)

```python
import os
import time
import json
import google.generativeai as genai
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

# ==========================================================
# БЛОК 1: НАСТРОЙКИ И ПЕРЕМЕННЫЕ
# Здесь мы храним "ключи от квартиры", где лежат данные
# ==========================================================

# Ваш ключ от Google AI Studio (для "мозгов" Gemini)
GEMINI_API_KEY = "ВАШ_КЛЮЧ_ЗДЕСЬ"

# Путь к файлу секретов от YouTube API (скачивается из Google Cloud Console)
CLIENT_SECRETS_FILE = "client_secret.json"

# Папка, в которой лежат видео для загрузки
SOURCE_FOLDER = "./videos_to_upload"

# Настройка Gemini
genai.configure(api_key=GEMINI_API_KEY)

# ==========================================================
# БЛОК 2: МОЗГОВОЙ ЦЕНТР (АНАЛИЗ ВИДЕО)
# Эта функция заменяет работу целого отдела маркетинга
# ==========================================================

def get_video_metadata(file_path):
    """
    Отправляет видео в Gemini, чтобы ИИ посмотрел его и 
    придумал название, описание и таймкоды.
    """
    print(f"--- Шаг 1: Анализ видео ИИ ({os.path.basename(file_path)}) ---")
    
    # Загружаем видео во временное хранилище Google (оно там лежит 48 часов)
    video_file = genai.upload_file(path=file_path)
    
    # Видео не анализируется мгновенно, нужно подождать, пока Google его "переварит"
    while video_file.state.name == "PROCESSING":
        print("ИИ смотрит видео, подождите...")
        time.sleep(10)
        video_file = genai.get_file(video_file.name)

    # Создаем модель (используем 1.5 Pro, так как она лучше всего понимает видео)
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    
    # Инструкция для ИИ (Промпт)
    prompt = """
    Ты профессиональный YouTube-продюсер. Проанализируй видео и верни JSON:
    {
      "title": "Заголовок с высоким CTR",
      "description": "SEO-описание с ключевыми словами",
      "tags": ["тег1", "тег2", "тег3"],
      "chapters": "00:00 - Вступление\\n01:30 - Основная часть"
    }
    Верни ТОЛЬКО чистый JSON, без лишних слов.
    """

    # Получаем ответ от ИИ
    response = model.generate_content([video_file, prompt])
    
    # Превращаем текстовый ответ ИИ в структуру данных Python (словарь)
    # Очищаем текст от возможных кавычек программного кода ```json
    clean_json = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(clean_json)

# ==========================================================
# БЛОК 3: ТРАНСПОРТ (ЗАГРУЗКА НА YOUTUBE)
# Эта функция берет готовый файл и текст и несет их на сервер
# ==========================================================

def upload_video_to_youtube(file_path, metadata):
    """
    Использует официальный YouTube API для загрузки видео.
    """
    print(f"--- Шаг 2: Загрузка на YouTube ---")
    
    # 1. Авторизация. При первом запуске откроется браузер, где надо нажать "Разрешить"
    scopes = ["[https://www.googleapis.com/auth/youtube.upload](https://www.googleapis.com/auth/youtube.upload)"]
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes)
    credentials = flow.run_local_server(port=0)
    
    # 2. Строим "мост" к YouTube API
    youtube = build("youtube", "v3", credentials=credentials)

    # 3. Собираем "конверт" с данными видео
    body = {
        "snippet": {
            "title": metadata['title'],
            "description": f"{metadata['description']}\n\nТаймкоды:\n{metadata['chapters']}",
            "tags": metadata['tags'],
            "categoryId": "27" # Категория 27 - это "Образование"
        },
        "status": {
            "privacyStatus": "private", # Видео будет доступно только вам (для проверки)
            "selfDeclaredMadeForKids": False
        }
    }

    # 4. Настраиваем передачу самого тяжелого - видеофайла
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

    # 5. Запускаем процесс
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = request.execute()
    print(f"УРА! Видео загружено. ID видео: {response['id']}")
    return response['id']

# ==========================================================
# БЛОК 4: ГЛАВНЫЙ ОРКЕСТРАТОР
# Логика, которая запускает все процессы по очереди
# ==========================================================

if __name__ == "__main__":
    # Проверяем, есть ли папка с видео, если нет - создаем
    if not os.path.exists(SOURCE_FOLDER):
        os.makedirs(SOURCE_FOLDER)
        print(f"Положите видео в папку {SOURCE_FOLDER} и запустите снова.")
    else:
        # Проходим по всем файлам в папке
        for filename in os.listdir(SOURCE_FOLDER):
            if filename.endswith((".mp4", ".mov", ".mkv")):
                full_path = os.path.join(SOURCE_FOLDER, filename)
                
                try:
                    # 1. Сначала спрашиваем у ИИ, о чем видео
                    data = get_video_metadata(full_path)
                    
                    # 2. Потом загружаем с этими данными на YouTube
                    upload_video_to_youtube(full_path, data)
                    
                    # 3. После успеха можно переместить файл в папку "Готово"
                    print(f"Файл {filename} успешно обработан!")
                    
                except Exception as e:
                    print(f"Ошибка при обработке {filename}: {e}")
```

---

## 3. Описание структуры данных и переменных

| Переменная | Тип | Что это делает |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | Строка | Ваш пароль для доступа к интеллекту Google. |
| `video_file` | Объект Google | Ссылка на файл, который временно лежит в облаке для анализа. |
| `metadata` | Словарь (JSON) | Объект, содержащий `title`, `description`, `tags`. Это "паспорт" видео. |
| `scopes` | Список | Разрешения, которые вы просите у YouTube (в данном случае - право на загрузку). |
| `privacyStatus` | Строка | Режим видимости (`private` — никто не видит, `public` — видят все, `unlisted` — по ссылке). |

## 4. Как это работает (понятным языком)

1.  **Библиотека `google-generativeai`**: Это «телефон», по которому мы звоним Gemini и просим его посмотреть видео. Она умеет передавать огромные файлы частями.
2.  **Библиотека `googleapiclient`**: Это официальный курьер от YouTube. Он знает, в какую «дверь» на сервере постучать, чтобы оставить там файл и описание.
3.  **JSON**: Это универсальный язык общения. Gemini говорит на нем, чтобы наш скрипт мог легко вытащить заголовок отдельно от тегов.
4.  **`time.sleep(10)`**: ИИ нужно время, чтобы «отсмотреть» ролик. Мы просим программу подождать 10 секунд, прежде чем снова спрашивать «Ну что, готово?».

---

## 5. Что делать, если вы новичок (Инструкция)

1.  **Получите API Key:** Зайдите в [Google AI Studio](https://aistudio.google.com/) и создайте бесплатный ключ.
2.  **Настройте YouTube API:** * Создайте проект в [Google Cloud Console](https://console.cloud.google.com/).
    * Включите "YouTube Data API v3".
    * В разделе "Credentials" создайте "OAuth 2.0 Client ID" (тип Desktop App).
    * Скачайте JSON-файл и переименуйте его в `client_secret.json`. Положите его рядом со скриптом.
3.  **Запустите:** Вставьте свое видео в папку и запустите скрипт. В первый раз он попросит вас залогиниться в Google-аккаунт через браузер.

Этот документ теперь — ваш полноценный фундамент. Хотите, чтобы я добавил в этот скрипт блок автоматической генерации обложки через DALL-E, чтобы цикл стал совсем полным?
