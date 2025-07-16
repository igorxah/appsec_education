# SAST Test Project

Проект для тестирования инструментов статического анализа безопасности приложений (SAST). Содержит преднамеренно внедренные уязвимости для проверки возможностей SAST-инструментов.

## 📌 О проекте

Этот тестовый проект включает полный стек технологий с уязвимостями в различных компонентах:

- **Backend**: Python/Flask с REST API
- **Frontend**: React.js с микрофронтендами
- **Auth Server**: OAuth2/OIDC сервер
- **Базы данных**: PostgreSQL и S3-хранилище
- **Интеграции**: Discord и Telegram API

## 🚀 Быстрый старт

### Требования
- Docker 20.10+
- Docker Compose 1.29+

### Запуск
```bash
git clone https://github.com/your-repo/sast-test-project.git
cd sast-test-project
docker-compose up --build
