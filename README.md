# repo-factory

Приватная фабрика репозиториев для аккаунта `lvlaksim1`.

## Создание репозитория

Создать Issue с точным заголовком:

`[CREATE_REPOSITORY]`

и JSON в теле:

```json
{
  "name": "telegram-receiver",
  "private": true,
  "description": "Reliable Telegram receiver"
}
```

Workflow создаёт репозиторий через GitHub REST API.

После успешного создания фабрика автоматически копирует в новый репозиторий стандартные secrets:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

если они настроены в `repo-factory`.

## Синхронизация стандартных secrets

Для уже существующего репозитория создать Issue с заголовком:

`[SYNC_STANDARD_SECRETS]`

и телом:

```json
{
  "name": "telegram-receiver"
}
```

Фабрика заново устанавливает оба Telegram secrets в целевом репозитории.

## Изменение видимости

Поддерживается команда:

`[SET_REPOSITORY_VISIBILITY]`

с JSON:

```json
{
  "name": "telegram-receiver",
  "visibility": "public"
}
```

Допустимые значения: `public` и `private`.

## Обязательная настройка

В `repo-factory → Settings → Secrets and variables → Actions` должны существовать:

- `REPO_FACTORY_TOKEN`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Для `REPO_FACTORY_TOKEN` нужны как минимум:

- Repository permissions → Administration → Read and write
- Repository permissions → Secrets → Read and write

Команды принимаются только от пользователя `lvlaksim1`.

Значения secrets не пишутся в код, Issue или комментарии workflow.

Удаление репозиториев фабрика не поддерживает.
