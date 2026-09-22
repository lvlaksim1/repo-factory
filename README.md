# repo-factory

Приватная фабрика репозиториев для аккаунта `lvlaksim1`.

## Создание репозитория

Создать Issue с точным заголовком:

`[CREATE_REPOSITORY]`

Профиль теперь **обязателен**. Старый Context Capsule bootstrap удалён из текущей фабрики.

### Репозиторий проекта с Project Manager v2

```json
{
  "name": "my-project",
  "private": true,
  "description": "Project repository",
  "profile": "project-manager"
}
```

Фабрика создаёт репозиторий и выполняет clean install актуального Project Manager v2 из закреплённого Context Capsule Core.

### Репозиторий Service Agent

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

Для `service-agent` обязательны:

- `agent_id`
- `role`
- `specialization`

Фабрика выполняет clean install Minimal Service Agent Base.

## Context Capsule policy

`repo-factory` больше не содержит и не использует старый Context Capsule Core.

Оба поддерживаемых профиля устанавливаются из одного закреплённого актуального v2 Core:

- `project-manager` → `capsulectl.py install`
- `service-agent` → `capsulectl.py service-install`

Поле `profile` обязательно; неявного legacy/default bootstrap нет.

## Стандартные Telegram secrets

Поле `standard_secrets` опционально и по умолчанию равно `true`.

Если оно разрешено и secrets настроены в `repo-factory`, в новый репозиторий копируются:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Для сервисных агентов, которым они не нужны, следует явно использовать:

```json
{
  "standard_secrets": false
}
```

## Синхронизация стандартных secrets

Для уже существующего репозитория создать Issue с заголовком:

`[SYNC_STANDARD_SECRETS]`

и телом:

```json
{
  "name": "telegram-receiver"
}
```

## Удаление стандартных secrets

Используется Issue:

`[REMOVE_STANDARD_SECRETS]`

с телом:

```json
{
  "name": "telegram-receiver"
}
```

## Receiver-specific secret

Для Telegram receiver поддерживается отдельная команда:

`[SYNC_RECEIVER_SECRETS]`

с телом:

```json
{
  "name": "telegram-receiver"
}
```

Она копирует только `CONSUMER_DISPATCH_TOKEN`.

## Изменение видимости

Используется Issue:

`[SET_REPOSITORY_VISIBILITY]`

с телом:

```json
{
  "name": "telegram-receiver",
  "visibility": "public"
}
```

Допустимые значения: `public` и `private`.

## Обязательная настройка

В `repo-factory → Settings → Secrets and variables → Actions` должен существовать:

- `REPO_FACTORY_TOKEN`

Telegram-related secrets нужны только для соответствующих secret-sync функций:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `CONSUMER_DISPATCH_TOKEN`

Для `REPO_FACTORY_TOKEN` нужны как минимум:

- Repository permissions → Administration → Read and write
- Repository permissions → Contents → Read and write
- Repository permissions → Secrets → Read and write

Команды принимаются только от пользователя `lvlaksim1`.

Значения secrets не пишутся в код, Issue или комментарии workflow.

Удаление репозиториев фабрика не поддерживает.
