# repo-factory

Приватная фабрика репозиториев для аккаунта `lvlaksim1`.

## Как работает

Создание нового Issue с точным заголовком:

`[CREATE_REPOSITORY]`

и JSON в теле:

```json
{
  "name": "telegram-receiver",
  "private": true,
  "description": "Reliable Telegram receiver"
}
```

запускает GitHub Actions workflow, который создаёт новый репозиторий через GitHub REST API.

Команды принимаются только от пользователя `lvlaksim1`.

## Обязательная настройка

В Settings → Secrets and variables → Actions → New repository secret создать:

- Name: `REPO_FACTORY_TOKEN`
- Value: fine-grained PAT владельца `lvlaksim1`
- Permission: Repository permissions → Administration → Read and write

Токен используется только внутри GitHub Actions и не хранится в коде.

## Ответ фабрики

Workflow пишет результат в исходный Issue:

- `CREATED: lvlaksim1/<name>`
- либо `FAILED: ...`

Удаление репозиториев фабрика не поддерживает.
