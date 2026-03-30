# Automations

В этой папке собраны документы про автоматизацию медиаконтента и построение вспомогательных knowledge-пайплайнов вокруг видеоархива.

Это не готовый production-код, а набор проектных и архитектурных материалов:

- сценарии автоматической публикации;
- сценарии миграции видеотеки;
- документы про подготовку базы для RAG и семантического индекса;
- заготовки для будущих скриптов и конвейеров.

## Кейсы: какой файл под какую задачу

- Если вам нужно автоматизировать публикацию видео на YouTube с AI-генерацией метаданных, описаний, таймкодов и обложек, откройте [video-youtube.md](/Users/alexeykrolmini/Code/essays/automations/video-youtube.md).
- Если ваша задача — быстро увидеть общий roadmap миграции большого Vimeo-архива в YouTube и далее в knowledge base, начните с [vimeo-migration.md](/Users/alexeykrolmini/Code/essays/automations/vimeo-migration.md).
- Если вам нужен именно инженерный transport pipeline Vimeo → YouTube, с `yt-dlp`, batching и Python-примерами, используйте [vimeo-youtube.md](/Users/alexeykrolmini/Code/essays/automations/vimeo-youtube.md).
- Если ваша цель — превратить YouTube-архив в RAG-ready knowledge base, а не просто перелить видео между платформами, откройте [RAGprepare.md](/Users/alexeykrolmini/Code/essays/automations/RAGprepare.md).
- Если у вас уже есть большой массив Markdown-файлов и вы хотите построить над ним semantic layer, controlled vocabulary и индексный слой, идите в [semantic_index.md](/Users/alexeykrolmini/Code/essays/automations/semantic_index.md).
- Если вы хотите собирать не архив и не индекс, а фабрику автоматической генерации учебных видеокурсов, начните с [Video-Course-Generator.md](/Users/alexeykrolmini/Code/essays/automations/Video-Course-Generator.md).

## Что здесь лежит

- [video-youtube.md](/Users/alexeykrolmini/Code/essays/automations/video-youtube.md)  
  Большой design-документ про автоматическую публикацию видео на YouTube. Внутри описаны:
  - watcher / intelligence / transport-архитектура;
  - использование Gemini для генерации названия, описания, таймкодов и промптов для обложек;
  - два варианта загрузки: через YouTube Data API и через Playwright;
  - пример оркестрации и развёрнутый Python-скелет.

- [vimeo-migration.md](/Users/alexeykrolmini/Code/essays/automations/vimeo-migration.md)  
  Короткий roadmap миграции большого Vimeo-архива в YouTube и далее в Markdown/RAG-базу. Это high-level README-план: стек, модули конвейера, недельный график и общий замысел.

- [vimeo-youtube.md](/Users/alexeykrolmini/Code/essays/automations/vimeo-youtube.md)  
  Более подробный инженерный документ про транспортный слой миграции Vimeo → YouTube. Внутри:
  - выгрузка списка видео через Vimeo API;
  - скачивание в низком качестве или только аудио через `yt-dlp`;
  - батчинг, параллелизм и локальный pipeline;
  - Python-примеры для inventory и transit-этапов.

- [RAGprepare.md](/Users/alexeykrolmini/Code/essays/automations/RAGprepare.md)  
  Документ про подготовку YouTube-архива к превращению в knowledge base. Фокус не на миграции, а на полном конвейере:
  - extraction списка видео;
  - transcription;
  - превращение транскриптов в Markdown-отчёты;
  - последующая загрузка в векторную базу или RAG-систему.

- [semantic_index.md](/Users/alexeykrolmini/Code/essays/automations/semantic_index.md)  
  Концептуальный проект инвентаризации большого массива Markdown-файлов и построения над ним семантического слоя. Это уже не только про видео, а про более общий knowledge-инженерный подход:
  - inventory;
  - индексные Markdown-слои;
  - нормализация тегов;
  - controlled vocabulary;
  - embeddings и semantic search.

- [Video-Course-Generator.md](/Users/alexeykrolmini/Code/essays/automations/Video-Course-Generator.md)
  Техническая спецификация системы автоматической генерации видеоуроков. Это уже кейс не про публикацию готового архива, а про production-пайплайн с talking-head аватарами, B-roll, инфографикой и финальной сборкой видео.

## Как читать

Если нужен маршрут по папке:

1. Начни с [vimeo-migration.md](/Users/alexeykrolmini/Code/essays/automations/vimeo-migration.md), чтобы увидеть общую дорожную карту.
2. Затем открой [vimeo-youtube.md](/Users/alexeykrolmini/Code/essays/automations/vimeo-youtube.md), если нужен детальный транспортный pipeline Vimeo → YouTube.
3. После этого читай [video-youtube.md](/Users/alexeykrolmini/Code/essays/automations/video-youtube.md), если нужен уже полноценный publish-пайплайн для YouTube.
4. Открой [RAGprepare.md](/Users/alexeykrolmini/Code/essays/automations/RAGprepare.md), если задача состоит в превращении видеоархива в RAG-ready базу знаний.
5. Затем читай [semantic_index.md](/Users/alexeykrolmini/Code/essays/automations/semantic_index.md), если хочешь построить более общий semantic layer над большим документным архивом.
6. Отдельно переходи к [Video-Course-Generator.md](/Users/alexeykrolmini/Code/essays/automations/Video-Course-Generator.md), если тебя интересует уже фабрика генерации учебных видео, а не архив и не миграция.

## Практический смысл раздела

Эта папка полезна, если нужно спроектировать или собрать:

- pipeline миграции большого видеоархива;
- автоматическую публикацию видео с AI-генерацией метаданных;
- Markdown-first knowledge base из видео и транскриптов;
- semantic indexing и подготовку базы для будущих AI-агентов.

Если позже здесь появится исполняемый код, его имеет смысл держать рядом с этими design-документами, но отделять от описаний через подпапки вроде `scripts/`, `specs/` или `examples/`.
