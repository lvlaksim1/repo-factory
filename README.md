# repo-factory

Приватная фабрика репозиториев для аккаунта `lvlaksim1`.

## Создание репозитория

Создать Issue с точным заголовком:

`[CREATE_REPOSITORY]`

Профиль **обязателен**.

### Репозиторий проекта с Project Manager v2

```json
{
  "name": "my-project",
  "private": true,
  "description": "Project repository",
  "profile": "project-manager"
}
```

Фабрика создаёт репозиторий и выполняет clean install закреплённого Project Manager v2 из отдельного источника `lvlaksim1/context-capsule-project-manager`, передавая ему отдельные immutable provenance pins для Project Manager и Context Capsule Core.

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

Фабрика выполняет clean install из отдельного закреплённого источника `lvlaksim1/service-agent-base`.

### Инфраструктурный репозиторий без агента

```json
{
  "name": "agent-control-plane",
  "private": true,
  "description": "Durable control plane for persistent agents",
  "profile": "infrastructure",
  "standard_secrets": false
}
```

Профиль `infrastructure` создаёт обычный репозиторий без Context Capsule и без агентской идентичности. Он предназначен для общих очередей, реестров, control-plane state и другой инфраструктуры, которая сама не является Project Manager или Service Agent.

## Component source policy

Агентские профили имеют раздельные закреплённые источники:

- Context Capsule Core compatibility → `lvlaksim1/context-capsule`;
- `project-manager` → `lvlaksim1/context-capsule-project-manager` → `pmctl.py install`;
- `service-agent` → `lvlaksim1/service-agent-base` → `servicectl.py install`;
- `infrastructure` → агентская идентичность и Context Capsule не устанавливаются.

Для профиля `project-manager` фабрика передаёт в `pmctl.py` два разных SHA:
`--context-capsule-commit` для Core и `--project-manager-commit` для PM. Исторический
`--core-commit` больше не используется фабрикой.

Таким образом, ни Project Manager, ни Service Agent Base больше не берутся из исторической ветки `context-capsule:v2-manager-runtime`.
Каждый источник закрепляется точным immutable commit SHA в `components.lock.json`. Этот файл является единственным каноническим distribution lock; workflow читает repository/commit только из него.

Изменение component pin считается допустимым только после успешной CI самого компонента и успешного `Component Contract Smoke` фабрики. Поле `profile` обязательно; профиль всегда задаётся явно.

## Миграция существующего Project Manager на split provenance

Миграция существующих v2-репозиториев выполняется только явно, без массовой фоновой перезаписи.

Создать Issue с точным заголовком:

`[MIGRATE_PROJECT_MANAGER_PROVENANCE]`

и телом:

```json
{
  "name": "my-project",
  "branch": "main",
  "expected_head": "40-character-exact-current-commit-sha"
}
```

`expected_head` обязателен и работает как optimistic concurrency guard: если указанная ветка
успела измениться, миграция прекращается без push.

Workflow:

- берёт Core и Project Manager только из `components.lock.json`;
- проверяет, что цель уже является Project Manager v2;
- выполняет `pmctl.py repair` с отдельными `--context-capsule-commit` и
  `--project-manager-commit`;
- требует успешные `validate`, `ready` и `recover`;
- проверяет итоговые provenance coordinates через `jq`;
- публикует только обычный fast-forward commit в указанную ветку;
- ничего не меняет, если репозиторий уже соответствует текущим pins.

## Миграция standalone Context Capsule Core

Для существующих standalone Context Capsule v1.3.x без Project Manager используется отдельная
guarded-команда:

`[MIGRATE_CONTEXT_CAPSULE_CORE]`

Тело Issue:

```json
{
  "name": "my-repository",
  "branch": "main",
  "expected_head": "40-character-exact-current-commit-sha"
}
```

Workflow берёт Core только из `components.lock.json`, принимает только уже установленный
`lvlaksim1/context-capsule` v1.3.x, выполняет non-destructive `capsulectl repair`, требует
`validate → ready → recover`, проверяет итоговые `version/core_commit` и публикует только
fast-forward commit. При изменившемся `expected_head` запись запрещена.

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


## Проверка приватных репозиториев без расходования приватных Actions minutes

Для приватных инфраструктурных репозиториев стандартные GitHub-hosted runners больше не являются каноническим способом проверки: они расходуют месячную квоту приватных Actions minutes.

Проверка выполняется из этого публичного `repo-factory`, где стандартный GitHub-hosted runner для публичного репозитория не расходует приватную квоту.

Создать Issue с точным заголовком:

`[VERIFY_PRIVATE_REPOSITORY]`

Для Agent Control Plane:

```json
{
  "name": "agent-control-plane",
  "commit": "40-character-exact-commit-sha",
  "profile": "agent-control-plane"
}
```

Для Supervisor:

```json
{
  "name": "supervisor",
  "commit": "40-character-exact-commit-sha",
  "profile": "supervisor"
}
```

Инварианты процесса:

- проверяется только точный immutable commit SHA;
- пары repository/profile разрешены явно и не принимают произвольную команду;
- `REPO_FACTORY_TOKEN` используется только на отдельном шаге чтения приватного репозитория и не передаётся шагам тестирования;
- исходный remote удаляется до исполнения тестов;
- артефакты и Actions cache не загружаются;
- результат фиксируется комментарием `VERIFICATION_OK` или `VERIFICATION_FAILED`;
- приватные репозитории не должны использовать `ubuntu-latest`, `windows-latest` или `macos-latest` для обычной CI-проверки, если для них предусмотрен этот механизм.


Дополнительные профили обычной проверки без производственных секретов:

```json
{
  "name": "evrasia-bot-max",
  "commit": "40-character-exact-commit-sha",
  "profile": "evrasia-bot-max"
}
```

```json
{
  "name": "fgis-fsa-site",
  "commit": "40-character-exact-commit-sha",
  "profile": "fgis-fsa-site"
}
```

Эти профили заменяют прежние приватные `ubuntu-latest` проверки: MAX выполняет статическую валидацию, а сайт устанавливает зависимости на Node 22 и выполняет production-сборку. Производственные секреты не передаются.


## Component lock

`components.lock.json` — единственный источник истины для версий компонентов, устанавливаемых фабрикой.

В lock schema v2 отдельно закрепляются:
- Context Capsule Core — repository + exact immutable commit;
- Project Manager — repository + exact immutable commit;
- Service Agent Base — repository + exact immutable commit.

`Component Contract Smoke` проверяет существование всех трёх immutable SHA, выполняет временную установку Project Manager с раздельными provenance coordinates и валидирует оба агентских профиля без создания тестовых репозиториев.
