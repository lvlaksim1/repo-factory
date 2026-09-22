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

По умолчанию фабрика сохраняет прежнее поведение: выполняет штатный clean install Project Manager Context Capsule в default branch нового репозитория.

Для репозиториев постоянных сервисных агентов поддерживается профиль `service-agent`:

```json
{
  "name": "supervisor",
  "private": true,
  "description": "Persistent Supervisor service agent",
  "profile": "service-agent",
  "agent_id": "ecosystem-supervisor",
  "role": "Supervisor",
  "specialization": "Portfolio and agent-system supervision",
  "standard_secrets": false
}
```

Для `service-agent` обязательны `agent_id`, `role` и `specialization`. Фабрика устанавливает Minimal Service Agent Base из закреплённого Core commit. Старые вызовы без `profile` продолжают использовать прежний Project Manager bootstrap.

Поле `standard_secrets` опционально и по умолчанию равно `true`. Для сервисных агентов, которым Telegram secrets не нужны, его следует явно устанавливать в `false`.

После успешного создания фабрика при разрешённом `standard_secrets` также автоматически копирует в новый репозиторий стандартные secrets:

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
- Repository permissions → Contents → Read and write
- Repository permissions → Secrets → Read and write

Команды принимаются только от пользователя `lvlaksim1`.

Значения secrets не пишутся в код, Issue или комментарии workflow.

Удаление репозиториев фабрика не поддерживает.


## Receiver-specific secret

For Telegram receiver repositories, `repo-factory` also supports a separate explicit command:

`[SYNC_RECEIVER_SECRETS]`

with body:

```json
{
  "name": "telegram-receiver"
}
```

This copies only:

- `CONSUMER_DISPATCH_TOKEN`

from `repo-factory` to the named receiver repository.

It is intentionally not part of automatic secret propagation to every new repository.
