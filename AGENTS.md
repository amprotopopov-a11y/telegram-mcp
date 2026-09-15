# Telegram MCP

Наследуй `~/work/AGENTS.md` и platform overlay; это самостоятельный Git repo.
Публикация локального форка: remote `fork`, ветка `main`; `origin` — upstream.

## Source и зависимости

- `main.py` — MCP tools и Telethon client; CLI fallback: `~/work/scripts/tg_read.py`.
- `pyproject.toml` + `uv.lock` — локальное `.venv`, отслеживаемое dep watcher.
- `requirements.txt` — полный exact lock для Dockerfile. При обновлении пакета
  согласуй эти три файла, сохраняя остальные версии.
- `poetry.lock` — legacy upstream artifact; активные uv/Docker пути его не читают.
- Контейнер и stdio-MCP независимы. Карта и deploy boundary — `~/work/SYSTEM.md`.
  Обновление локальной зависимости не подтверждает обновление running container.

## Проверка dependency update

Запусти `uv lock --check`, `uv pip check --python .venv/bin/python` и существующие
`test_validation.py`, `test_file_path_security.py`, `test_container_dependencies.py`.
Для offline pytest/import smoke отключи `dotenv.load_dotenv` через mock до импорта
`main`, передай dummy API ID/hash, пустой session string и убери session name:
так клиент использует in-memory session и не читает live `.env`.
Проверь `main.mcp.list_tools()` без подключения к Telegram и сравни package
inventory до/после: меняется только согласованная зависимость.

## Проверено 15.09.2026 — 6a374acc

Telethon 1.44.0 → 1.45.0: 24 tests passed; 94 tool schemas; `uv pip check`
и `uv lock --check` успешны. Единственная inventory delta — Telethon.
Локальное `.venv` обновлено в `8ddfdbc`. После команды Андрея «доделай»
контейнер также пересобран штатным CLI:
`~/work/scripts/deploy.sh telegram-mcp --telethon-update 1.44.0:1.45.0`.
Корневой deploy code: `f6707a45`, independent plan/code review завершены.
15.09.2026 12:38:53 UTC: Telethon 1.45.0, MCP 1.30.0, все 45 distributions
совпадают с exact lock; main.py SHA256 совпадает с source, restart count = 0.
Лог подтвердил `Telegram client started. Running MCP server...`.
Image: `sha256:d33e815e8156a25f47305355795468abe7d4457c84fef432972fc2cabe4577dc`.
Полный rollout result и global health — `~/work/инфра/PLAN-telethon-6a374acc-live.md`.
Уже запущенные stdio consumers принадлежат своим клиентам и этим deploy не
перезапускаются; новый stdio process использует обновлённое `.venv`.
