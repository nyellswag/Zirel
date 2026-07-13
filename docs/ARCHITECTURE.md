# Zirel: архитектура

## Общая структура

Zirel — Flask-монолит.

Основные директории:

- `app/` — основной пакет Flask-приложения.
- `app/templates/` — HTML-шаблоны Jinja2.
- `app/static/` — CSS и JavaScript.
- `migrations/` — миграции Flask-Migrate / Alembic.
- `docs/` — документация проекта и долгосрочный контекст.
- Корневые файлы: `config.py`, `run.py`, `wsgi.py`, `requirements.txt`.

## Серверная часть

Серверная часть использует:

- Python;
- Flask;
- Flask-SQLAlchemy;
- Flask-Migrate;
- Flask-Login;
- SQLite локально;
- PostgreSQL на деплое, если задан `DATABASE_URL`;
- Gunicorn через `wsgi.py` для production-запуска.

Фабрика приложения находится в `app/__init__.py`.

## Конфигурация

`config.py` читает:

- `SECRET_KEY`;
- `WISHLIST_MODE`;
- `BETA_APPLICATION_MODE` (новое имя режима; `WISHLIST_MODE` временно поддерживается как legacy alias);
- `BETA_PROJECT_LIMIT` (по умолчанию 2 для обычного beta-пользователя; администраторы не ограничены);
- `DATABASE_URL`.

Если `DATABASE_URL` не задан, используется локальная SQLite-база `zirel.db`.

## Модели базы данных

Модели определены в `app/models.py`.

Основные модели:

- `User` — аккаунт пользователя, роль, email, хеш пароля, флаг администратора, проекты.
- `Project` — пользовательский проект мира.
- `Character` — персонаж проекта.
- `Faction` — фракция проекта.
- `Event` — событие проекта.
- `Relation` — связь `source_type/source_id -> relation_type -> target_type/target_id`.
- `Feedback` — сообщение обратной связи: имя, email, роль, тема, текст, дата создания.
- `ContactMessage` — contact-сообщение: имя, email, причина, тема, текст, дата создания.
- `WishlistEntry` — заявка списка ожидания.

Связанные данные проекта удаляются каскадно вместе с проектом.

## Маршруты

Маршруты определены в `app/routes.py` внутри blueprint `main`.

Публичные маршруты:

- `/`
- `/beta/apply` (`/wishlist` перенаправляет сюда для обратной совместимости)
- `/beta`
- `/faq`
- `/whitepaper`
- `/roadmap`
- `/terms`
- `/privacy`
- `/feedback`
- `/contact`
- `/login`
- `/register`

Защищенные маршруты приложения:

- `/projects`
- страницы проекта;
- CRUD-маршруты проекта;
- маршруты персонажей, фракций, событий и связей;
- предупреждения;
- граф;
- импорт и экспорт.

Админские маршруты:

- `/admin`
- `/admin/users`
- `/admin/feedback`
- `/admin/contact`
- `/admin/applications` (`/admin/wishlist` сохранён как legacy URL)
- маршруты удаления пользователей, заявок wishlist, feedback-сообщений и contact-сообщений.

## Контроль доступа

Доступ к приложению защищен через Flask-Login.

Доступ к проекту проверяется функцией `get_project_or_404_for_current_user(project_id)`:

- обычный пользователь видит только свои проекты;
- администратор видит все проекты.

Админские страницы используют `admin_required`.

В режиме `BETA_APPLICATION_MODE=true` (или legacy `WISHLIST_MODE=true`):

- большинство публичных и внутренних маршрутов перенаправляются на `/beta/apply`;
- `/login` остается доступен;
- админские маршруты доступны только авторизованному администратору.

## Движок логики

`app/logic_engine.py` динамически анализирует проект и возвращает список предупреждений.

Предупреждения не сохраняются в базе данных.

Текущие проверки:

- персонаж участвует в событии после смерти;
- персонаж участвует в событии до рождения;
- уничтоженная фракция участвует в событии после уничтожения;
- односторонняя вражда;
- внутренний конфликт во фракции.

## Граф мира

Эндпоинт данных графа:

- `/projects/<project_id>/graph/data`

Он возвращает JSON для Graph Workspace:

- узлы для персонажей, фракций и событий;
- ребра на основе связей;
- стабильные процентные позиции узлов;
- визуальные данные для узлов и связей: цвет, подпись, знак;
- связи с отсутствующими сущностями пропускаются.

Graph Workspace использует fullscreen constellation map:

- верхняя панель проекта;
- левый sidebar с поиском, фильтрами, легендой и поиском пути;
- центральная HTML/SVG-карта с draggable-узлами;
- SVG-слой связей;
- canvas-слой звездного фона;
- миникарта, которая строится из тех же позиций, что и основная карта;
- правый inspector;
- нижняя status bar.

## Рабочие fullscreen-страницы

Некоторые страницы используют отдельный fullscreen layout и отключают общий navbar/footer в `base.html`:

- `/projects`;
- `/projects/create`, `/projects/import` и редактирование проекта;
- страницы Characters, Factions, Events и Relations;
- формы создания и редактирования сущностей и связей;
- `/projects/<project_id>/warnings`;
- `/projects/<project_id>/graph`;
- `/admin` и admin-подстраницы.

Длинные project workspace-страницы используют `projects-shell scrollable-projects-shell`: верхняя панель остается фиксированной, а `main` становится отдельным вертикальным scroll-контейнером. Фиксированные Dashboard, Graph и Warnings сохраняют собственную модель прокрутки.

## Интерфейс

Интерфейс использует:

- Jinja2 templates;
- Bootstrap CDN;
- основной CSS-файл `app/static/style.css`;
- `app/static/privacy_policy_reference.css` — изолированная визуальная система Privacy, перенесенная из подтвержденного HTML-референса;
- `app/static/terms_of_service_reference.css` — изолированная визуальная система Terms, перенесенная из подтвержденного HTML-референса;
- `app/static/list_filters.js`;
- `app/static/auth.js`;
- `app/static/entity_composer.js` — live preview форм сущностей;
- `app/static/record_workspace.js` — Grid/List и состояние bulk-selection;
- `app/static/story_tapestry.js` — интерактивная ткань данных проекта;
- `app/static/import_project.js` — состояние выбора JSON-файла и drag-and-drop импорта.

`base.html` предоставляет блок `extra_head`. Terms и Privacy используют его для подключения своих reference CSS после общего `style.css`, поэтому их утвержденный дизайн не зависит от последующих изменений общей визуальной системы приложения.

Текущий визуальный стиль:

- темный футуристичный SaaS;
- почти черный / темно-синий фон;
- фиолетовые и синие акценты;
- стеклянные карточки;
- светящиеся границы;
- fullscreen workspace-экраны для крупных рабочих разделов.

## Деплой

Production entry point:

- `wsgi.py`

Для Render может использоваться стартовая команда:

```bash
flask db upgrade && flask create-admin && gunicorn wsgi:app
```

После создания первого администратора стартовая команда может быть упрощена:

```bash
flask db upgrade && gunicorn wsgi:app
```
