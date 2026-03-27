Это классическая задача миграции данных («Data Migration»), и ваша интуиция вас не подводит: тянуть 4K-видео с Vimeo ради анализа текста — это пустая трата времени и денег. 

Для Vimeo существует отличный способ автоматизации через **Vimeo API** в связке с **yt-dlp**. Последняя утилита, несмотря на название, великолепно работает с Vimeo, позволяя выбирать конкретное качество (например, 360p или вообще только аудио).

Вот архитектурное решение для вашего «переезда» за неделю:

---

### 1. Подготовка: Получение списка ссылок
Vimeo API позволяет выгрузить список всех URL ваших видео.
* Вам нужно создать приложение в [Vimeo Developer Portal](https://developer.vimeo.com/).
* Получить **Access Token** с правами `public` и `private` (чтобы видеть свои скрытые видео).

### 2. Сценарий миграции (Python + yt-dlp)
Самый эффективный способ — не скачивать файл на диск, а сразу «переливать» его. Но так как YouTube API требует файл для загрузки, мы будем использовать промежуточный буфер.

**Логика скрипта:**
1. Скрипт запрашивает список видео через Vimeo API.
2. Для каждого видео запускается `yt-dlp` с параметром `-f "worst"` (худшее качество) или `-f "ba"` (best audio — только звук).
3. Скачанный легкий файл отправляется в YouTube API.

#### Пример кода для скачивания в низком качестве:

```python
import subprocess

def download_low_res_vimeo(vimeo_url, output_name):
    # Команда для yt-dlp: 
    # -f "worst" выбирает самое низкое разрешение (обычно 240p или 360p)
    # Это идеально для ваших целей: файл будет весить в 20-50 раз меньше оригинала
    command = [
        'yt-dlp',
        '-f', 'worst', 
        '--external-downloader', 'aria2c', # aria2c ускоряет загрузку в несколько потоков
        '-o', f'{output_name}.mp4',
        vimeo_url
    ]
    
    print(f"[PROCESS] Начало загрузки: {vimeo_url}")
    subprocess.run(command)

# Пример использования:
# download_low_res_vimeo('https://vimeo.com/123456789', 'historical_video_001')
```

---

### 3. Стратегия "За неделю" (Оптимизация)

Для 3000 длинных видео обычный последовательный запуск будет долгим. Чтобы уложиться в неделю, нужно использовать **параллелизм**:

1.  **Разделение на батчи:** Разбейте список из 3000 видео на 7 частей (по ~430 видео в день).
2.  **Параллельные потоки:** Запускайте скрипт в 3-5 потоков. Современный интернет в Калифорнии и мощность процессора легко справятся с одновременной загрузкой 5 видео в низком разрешении.
3.  **Исключительно Аудио:** Если видеоряд вам действительно не нужен, используйте формат `-f "bestaudio"`. YouTube примет аудиофайл (в контейнере m4a/mp3) и создаст из него видео со статической заставкой. Это **в 100 раз быстрее** и легче для анализа.



---

### 4. Почему низкое разрешение — это правильно?
1.  **Экономия места:** 3000 видео по 1 часу в 4K — это ~30-50 Терабайт. В 360p — это всего ~300-500 Гб.
2.  **Скорость обработки YouTube:** YouTube обработает («прожует») 360p-ролик и создаст транскрипт в 10 раз быстрее, чем тяжелый файл.
3.  **API Quotas:** Загрузка легких файлов через YouTube API реже вызывает ошибки тайм-аута.

### 5. Риски: Лимиты Vimeo
Vimeo может ограничить скорость скачивания, если увидит слишком много запросов с одного IP. 
* **Решение:** Добавьте небольшую паузу (`time.sleep(5)`) между видео или используйте прокси, если планируете агрессивную выкачку в 10+ потоков.

---

### Итоговый план действий:
1.  **Скрипт-собиратель:** Выгружает все ссылки из Vimeo в текстовый файл `links.txt`.
2.  **Скрипт-качалка:** Читает `links.txt`, скачивает через `yt-dlp -f worst` и складывает в локальную папку.
3.  **Скрипт-загрузчик:** Берет файлы из папки и заливает на YouTube (используя код, который мы обсуждали ранее).

**Хотите, я напишу для вас полный скрипт, который автоматически берет ссылку из Vimeo, скачивает только аудио (или мини-видео) и сразу готовит его к отправке?** Это будет самый быстрый «транспорт» для ваших исторических архивов.


Для реализации такого масштабного «переезда» (3000 видео) нам понадобится скрипт, который работает максимально бережно к ресурсам. Мы будем использовать **комбинированный подход**:
1. **Vimeo API** — чтобы быстро получить список всех ID и названий.
2. **yt-dlp** — чтобы выкачать только «скелет» видео (низкое разрешение) или только звук.

Вот полный код «Мигратора», разбитый на логические блоки.

---

### 1. Получение списка всех видео с Vimeo
Вам нужно будет создать [Personal Access Token](https://developer.vimeo.com/api/guides/start) в кабинете разработчика Vimeo.

```python
import requests
import csv

VIMEO_TOKEN = "ВАШ_VIMEO_ACCESS_TOKEN"

def get_all_vimeo_videos():
    url = "https://api.vimeo.com/me/videos"
    headers = {"Authorization": f"bearer {VIMEO_TOKEN}"}
    params = {"per_page": 100, "page": 1}
    
    all_videos = []
    
    while True:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        for video in data['data']:
            # Сохраняем только ссылку и название
            all_videos.append([video['name'], video['link']])
            
        print(f"[INFO] Собрано {len(all_videos)} ссылок...")
        
        # Проверка, есть ли следующая страница
        if 'next' in data['paging'] and data['paging']['next']:
            params['page'] += 1
        else:
            break
            
    # Сохраняем реестр в CSV
    with open('vimeo_migration_list.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'URL'])
        writer.writerows(all_videos)
    
    print("[SUCCESS] Реестр на 3000+ видео готов!")

if __name__ == "__main__":
    get_all_vimeo_videos()
```

---

### 2. Скрипт «Транспортировщик» (Download & Compress)
Этот скрипт берет список из CSV и начинает скачивать файлы. Мы используем формат `144p` или `240p`. Этого достаточно для распознавания речи, но файл будет весить копейки.

```python
import subprocess
import os
import pandas as pd

def migrate_batch(csv_file, start_index=0, batch_size=50):
    df = pd.read_csv(csv_file)
    
    # Создаем папку для временного хранения
    if not os.path.exists('vimeo_temp'):
        os.makedirs('vimeo_temp')

    # Берем только нужную порцию (чтобы не забить диск)
    batch = df.iloc[start_index : start_index + batch_size]

    for index, row in batch.iterrows():
        title = "".join([c for c in row['Title'] if c.isalnum() or c==' ']).rstrip()
        url = row['URL']
        output_file = f"vimeo_temp/video_{index}.mp4"

        print(f"[DOWNLOADING] {title} ({url})")
        
        # Команда yt-dlp:
        # -f "worst" — самое низкое разрешение
        # --extract-audio — если видео не нужно ВООБЩЕ (сэкономит еще больше места)
        command = [
            'yt-dlp',
            '-f', 'worst[ext=mp4]/worst', # Ищем худший MP4
            '-o', output_file,
            url
        ]
        
        try:
            subprocess.run(command, check=True)
            print(f"[DONE] Файл сохранен: {output_file}")
            
            # ТУТ МОЖНО ВСТАВИТЬ ВЫЗОВ ФУНКЦИИ ЗАГРУЗКИ НА YOUTUBE
            # upload_to_youtube(output_file, title)
            
            # После загрузки — УДАЛЯЕМ локальный файл, чтобы освободить место
            # os.remove(output_file)
            
        except Exception as e:
            print(f"[ERROR] Ошибка с видео {title}: {e}")

if __name__ == "__main__":
    migrate_batch('vimeo_migration_list.csv', start_index=0, batch_size=10)
```

---

### Почему это сработает за неделю:

1. **Минимальный вес:** Видео в 240p весит около **100-150 МБ на час**. 3000 часов — это ~450 ГБ. Любой современный жесткий диск это выдержит.
2. **Параллельная загрузка:** Вы можете запустить этот скрипт в 3-4 окнах терминала одновременно, указав разные `start_index` (например, 0, 500, 1000 и т.д.).
3. **Прямой транзит:** Если вы добавите функцию `upload_to_youtube` прямо внутрь цикла (сразу после `subprocess.run`), скрипт будет работать как конвейер: «Скачал — Залил — Удалил». Вам даже не понадобится много места на диске.



---

### Резюме по структуре данных (для вашего Агента):

* **Входные данные:** `VIMEO_TOKEN`.
* **Переменные:** `start_index` (с какого видео начинать), `batch_size` (сколько за раз).
* **Библиотеки:** `requests` (для API), `pandas` (для работы со списками), `yt-dlp` (движок скачивания).

**Ваш следующий шаг:**
Зарегистрируйте приложение на Vimeo и получите токен. После этого запустите первый скрипт, чтобы мы увидели полный список ваших 3000 видео. 

Хотите, чтобы я подготовил для вас **Bash-команду**, которая автоматически будет запускать этот процесс в несколько потоков, чтобы вам не пришлось делать это вручную?


Поскольку ваша задача — **локальный внутренний инструмент** для личного архива, мы будем запускать всё прямо на вашем компьютере (Mac или PC). Это даст вам 100% контроля, отсутствие лишних трат на сервера и максимальную скорость работы с вашим домашним интернетом.

Ниже — пошаговый план «подготовительных работ» и финальный набор команд.

---

### Шаг 1: Подготовка окружения (Terminal)

Откройте терминал (Terminal на Mac или PowerShell на Windows) и установите необходимые «движки». Мы будем использовать `yt-dlp` для скачивания и `ffmpeg` для обработки.

```bash
# Установка менеджера пакетов (если нет) и инструментов
brew install yt-dlp ffmpeg aria2

# Установка библиотек для Python
pip install pandas requests google-api-python-client google-auth-oauthlib
```
> **Зачем:** `aria2` — это ускоритель. Он позволяет качать видео в 16 потоков одновременно, что критично для 3000 файлов.

---

### Шаг 2: Получение Vimeo API Token

1. Зайдите на [Vimeo Developer](https://developer.vimeo.com/apps).
2. Нажмите **"Create an app"**. Название любое (например, "MyMigration").
3. В меню слева выберите **"Authentication"**.
4. Прокрутите вниз до **"Generate a personal access token"**.
5. Выберите галочки: `public`, `private`, `video_files`.
6. **Нажмите Generate.** Скопируйте этот длинный код. Это ваш пропуск к видео.

---

### Шаг 3: Мастер-скрипт «Vimeo-to-Local»

Этот скрипт сделает всю «черную работу». Он скачает видео в самом низком качестве, чтобы вы могли залить их на YouTube для анализа.

**Создайте файл `vimeo_downloader.py` и вставьте туда этот код:**

```python
import os
import subprocess
import requests
import pandas as pd
import time

# --- НАСТРОЙКИ ---
VIMEO_TOKEN = "ВАШ_ТОКЕН_ИЗ_ШАГА_2"
DOWNLOAD_FOLDER = "./vimeo_archives_lowres"
LOG_FILE = "migration_log.csv"

def get_vimeo_list():
    """Собирает список всех ваших видео через API"""
    url = "https://api.vimeo.com/me/videos"
    headers = {"Authorization": f"bearer {VIMEO_TOKEN}"}
    params = {"per_page": 100, "page": 1}
    video_list = []

    print("--- Сбор списка видео с Vimeo ---")
    while True:
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        for v in data['data']:
            video_list.append({'title': v['name'], 'url': v['link']})
        if 'next' in data['paging'] and data['paging']['next']:
            params['page'] += 1
        else: break
    
    df = pd.DataFrame(video_list)
    df.to_csv(LOG_FILE, index=False)
    print(f"Готово! Найдено {len(df)} видео. Список в {LOG_FILE}")
    return df

def download_batch(start_idx, end_idx):
    """Качает видео куском (batch) в низком качестве"""
    df = pd.read_csv(LOG_FILE)
    if not os.path.exists(DOWNLOAD_FOLDER): os.makedirs(DOWNLOAD_FOLDER)

    for i in range(start_idx, min(end_idx, len(df))):
        title = df.iloc[i]['title']
        url = df.iloc[i]['url']
        filename = f"{DOWNLOAD_FOLDER}/video_{i}.mp4"
        
        print(f"[{i+1}/{len(df)}] Качаю: {title}")
        
        # Команда для супер-быстрой выкачки в низком качестве
        cmd = [
            'yt-dlp',
            '-f', 'worst[ext=mp4]/worst', # Самое низкое качество
            '--external-downloader', 'aria2c',
            '--external-downloader-args', '-x 16 -s 16 -k 1M',
            '-o', filename,
            url
        ]
        subprocess.run(cmd)

if __name__ == "__main__":
    # 1. Сначала один раз соберите список:
    # get_vimeo_list() 
    
    # 2. Потом запускайте скачивание (например, первые 50 видео):
    download_batch(0, 50)
```

---

### Шаг 4: Команды для управления (Terminal)

Чтобы не запутаться в 3000 видео, используйте «порционный» подход. Запускайте скачивание частями.

**Как запустить процесс:**
1. Сначала в коде выше раскомментируйте `get_vimeo_list()` и закомментируйте `download_batch`. Запустите: `python vimeo_downloader.py`. Вы получите файл `migration_log.csv`.
2. Затем верните всё обратно и качайте частями.

**Для супер-скорости (Многопоточность):**
Вы можете открыть 3 окна Терминала и запустить в каждом разные диапазоны:
* Окно 1: `python -c "from vimeo_downloader import download_batch; download_batch(0, 500)"`
* Окно 2: `python -c "from vimeo_downloader import download_batch; download_batch(500, 1000)"`
* Окно 3: `python -c "from vimeo_downloader import download_batch; download_batch(1000, 1500)"`



---

### Почему это сработает для вас?

1. **Прозрачность:** Вы видите каждый скачанный файл в папке `vimeo_archives_lowres`.
2. **Низкое разрешение:** Видео 240p/360p весят копейки. Весь ваш архив на 3000 часов поместится на обычный внешний диск.
3. **Безопасность:** Ключи Vimeo не покидают ваш компьютер.
4. **Контроль:** Если интернет пропал — вы просто запускаете скрипт с того `start_idx`, на котором остановились.

### Что делать дальше?
Как только вы скачаете первую сотню видео, я дам вам скрипт-загрузчик, который по этой же логике («Скачал — Залил — Удалил») отправит их на ваш YouTube-канал для анализа.

**Начинаем с получения Токена на Vimeo?** Если возникнут сложности на сайте Vimeo, пишите — я подскажу, куда нажать.
