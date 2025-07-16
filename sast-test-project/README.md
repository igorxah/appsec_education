# Комплексный тестовый проект для SAST-тестирования
Обзор проекта
Этот проект предназначен для тестирования инструментов статического анализа безопасности приложений (SAST). Он содержит преднамеренно внедренные уязвимости для проверки возможностей SAST-инструментов.
_ _ _
/sast-test-project
│
├── /backend                 # Backend сервис (Python/Flask)
│   ├── /app
│   │   ├── __init__.py
│   │   ├── auth.py          # Модуль аутентификации (с уязвимостями)
│   │   ├── crud.py          # CRUD операции (с уязвимостями)
│   │   ├── discord.py       # Интеграция с Discord (с уязвимостями)
│   │   ├── models.py        # Модели данных
│   │   └── telegram.py      # Интеграция с Telegram (с уязвимостями)
│   ├── config.py            # Конфигурация (с hardcoded секретами)
│   ├── requirements.txt
│   └── Dockerfile
│
├── /frontend                # Frontend (React + Microfrontends)
│   ├── /main-app            # Основное приложение
│   ├── /auth-module         # Микрофронтенд аутентификации
│   ├── /profile-module      # Микрофронтенд профиля
│   ├── public/
│   ├── package.json
│   └── Dockerfile
│
├── /auth-server             # OAuth2/OIDC сервер
│   ├── /app
│   │   ├── __init__.py
│   │   └── oauth2.py        # Реализация OAuth2 (с уязвимостями)
│   ├── config.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml       # Конфигурация Docker Compose
├── README.md                # Документация
└── TESTING.md               # Инструкции по тестированию
