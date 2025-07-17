# SAST Test Project

Проект для тестирования инструментов статического анализа безопасности приложений (SAST). Содержит преднамеренно внедренные уязвимости для проверки возможностей SAST-инструментов.

## О проекте

Это тестовое приложение, включающее:

- **Backend API** на Python/Flask
- **Frontend** на React.js с микрофронтендами
- **Auth Server** с реализацией OAuth2/OIDC
- **Data Storage**: PostgreSQL и Amazon S3 (MinIO)
- **Интеграции**: Discord и Telegram API

## Архитектура

![88915c61d8c13108ef2709a51ed83f1935324ba3](https://github.com/user-attachments/assets/83bbf2fc-aee3-432e-8366-222cfc3e716a)


### Требования для запуска
- Docker 20.10+
- Docker Compose 1.29+


### Важное предупреждение
⚠️ Этот проект содержит преднамеренные уязвимости только для тестирования SAST-инструментов. Не используйте в production!


### Запуск
```bash
git clone https://github.com/your-repo/sast-test-project.git
cd sast-test-project
docker-compose up --build
