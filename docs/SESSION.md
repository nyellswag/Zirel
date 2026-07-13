# Zirel: журнал сессии

## Базовое состояние

Zirel — Flask-монолит для worldbuilding workflow: пользователи, приватные проекты, персонажи, фракции, события, связи, предупреждения, граф, импорт/экспорт JSON, wishlist, feedback/contact и admin-панель.

Официальное название продукта: **Zirel**.

## Недавние подтвержденные изменения

- Создана базовая документация проекта в `docs/`.
- Страницы Sign In / Sign Up переработаны по modal-референсам и подтверждены как рабочая базовая версия.
- Terms и Privacy переработаны и подтверждены; общий Legal Center и Disclaimer убраны.
- Graph Workspace переработан по HTML-референсу и принят как временно приемлемая версия, но требует будущей полировки.
- Warnings Page переработана в fullscreen workspace.
- Projects Page переработана по HTML-референсу; лишний блок Quick links слева убран и подтвержден.
- Graph Workspace переведен на кастомную constellation map с HTML/SVG/canvas, draggable-узлами и миникартой по реальным позициям; текущая версия подтверждена как приемлемая.

## Изменения, ожидающие просмотра

- Google Tag Manager в `base.html` заменен на Google Analytics gtag.js с идентификатором `G-9JG8J2FMPP`; старый noscript-блок GTM удален.
- Начат новый редизайн внутренних workspace-страниц по HTML-референсам: Project Dashboard, Relations, Characters, Factions и Events переведены на новый темный dashboard/card workspace.
- Для Characters/Factions/Events добавлен общий шаблонный JS `app/templates/partials/entity_workspace.js` для client-side search, grid/list view и bulk-selection состояния.
- После просмотра пользователем первый вариант внутреннего редизайна признан недостаточно точным: внутренние меняющиеся nav-бары и отдельный мини-логотип убраны, страницы снова опираются на общий navbar из `base.html`.
- Relations cards увеличены и сделаны более выразительными, чтобы они не выглядели мелкими техническими блоками.
- Project Dashboard получил честный блок Recent activity / Latest project records на основе последних сущностей проекта.
- World completion на Project Dashboard переведен с маленьких MVP-нормативов на более реалистичные целевые значения: 15 characters, 10 factions, 15 events, 25 relations.
- Пользователь попросил разделить работу и начать заново только с Project Dashboard. Лишние изменения Relations/Characters/Factions/Events из этого пакета откатаны.
- Project Dashboard теперь переведен на тот же fullscreen `zpw-*` дизайн, что и `/projects`: общий topbar, sidebar, main area, right panel, bottombar, цветовая система и типографика страницы проектов.
- На Project Dashboard блок Recent activity изменен с карточного вида на компактную вертикальную branch/timeline-ленту.
- Выполнен общий редизайн v2 части публичных страниц: `/beta`, `/faq`, `/roadmap`, `/whitepaper`, `/feedback`, `/contact`.
- Главная страница `/` переработана; справа добавлен `partials/world_engine.html`, близкий к `ZirelWorldEngine.html`.
- Админские страницы переписаны под отдельный fullscreen admin workspace по `ZirelAdminDashboard.html`.
- Admin routes используют собственный topbar/tabbar и не показывают общий navbar/footer.
- В admin dashboard добавлены реальные последние wishlist-заявки.
- Лого в admin topbar заменено на общий ромбовый знак главной страницы.
- На admin-подстраницах показываются счетчики всех admin-разделов.
- Drawer-инспектор admin-страниц показывает данные структурированными строками.
- Feedback получил новое nullable-поле `topic`.
- Публичная форма `/feedback` получила выбор темы сообщения.
- Admin feedback list показывает тему feedback рядом с ролью отправителя.
- Добавлена миграция `4af6f4d6d5a2_add_feedback_topic.py`.
- На public Contact удален верхний ряд topic chips.
- На admin Contact удален неудачный верхний фильтр по reason.
- Локальная база была обновлена командой `flask db upgrade`; `/admin` проверен через Flask test client и возвращает 200.

## Что было исправлено в текущей сессии

- Причина неработающего `/admin`: локальная база не имела новой колонки `feedback.topic` после изменения модели.
- Миграция успешно применена через `.venv`.
- Проверено, что таблица `feedback` содержит колонку `topic`.
- Проверено, что `/admin` открывается для существующего администратора в test client.
- С public Contact удален блок с надписями `Beta access`, `Bug report`, `Collaboration`, `Business / partnership`, `General question`.
- Восстановлены `ARCHITECTURE.md` и `SESSION.md` в нормальном русском UTF-8 после обнаружения повреждения кодировки рабочей копии.
- Graph Workspace начал переводиться на constellation map по новому HTML-референсу.
- `/projects/<project_id>/graph/data` теперь возвращает узлы, связи и стабильные позиции `positions`.
- В данные графа добавлены визуальные поля `color` и `glyph` для узлов, а также цвет связи.
- `graph.html` заменен на кастомную HTML/SVG-карту без Cytoscape на этой странице.
- Основная карта и миникарта теперь строятся из одних и тех же координат, поэтому миникарта отражает реальную структуру карты.
- Сохранены поиск, фильтры типов сущностей, фильтры типов связей, inspector, path finder, подсветка связей, режим connected-only и перетаскивание узлов.
- Inspector теперь показывает выбранный узел, прямые связи и выбранную связь в более компактном стиле с квадратными цветными отметками.
- Проверено: `routes.py` проходит AST-проверку.
- Проверено: `graph.html` проходит Jinja parse.
- Проверено: inline JavaScript страницы графа проходит `node --check`.
- Проверено через Flask test client: `/projects/<project_id>/graph/data` возвращает `nodes`, `edges`, `positions`.
- Проверено через Flask test client: `/projects/<project_id>/graph` возвращает 200.
- Project Dashboard заменен на более крупный dashboard с hero-блоком, workspace portals, world coverage, suggested next steps и project tools.
- Relations заменены на connection workspace с hero, real stat cards, chip-фильтрами, grid/list режимом, карточками связей и сохраненным bulk delete.
- Characters, Factions и Events переведены на общий entity workspace с hero, real stat cards, search, grid/list режимом, карточками сущностей и сохраненным bulk delete/delete all.
- У новых Relations/Entity страниц отключен старый `data-filter-list`, чтобы не конфликтовать с новым локальным JS.
- Проверено: `project_detail.html`, `relations.html`, `characters.html`, `factions.html`, `events.html` проходят Jinja parse.
- Проверено: `app/templates/partials/entity_workspace.js` проходит `node --check`.
- Проверено: `git diff --check` не нашел whitespace-ошибок.
- Проверено через Flask test client: `/projects/<project_id>`, `/relations`, `/characters`, `/factions`, `/events` возвращают 200.
- Исправлено по замечаниям пользователя: убраны внутренние `zdu-nav` из Project Dashboard, Relations, Characters, Factions и Events.
- Исправлено по замечаниям пользователя: actions перенесены в breadcrumb/subbar, чтобы не было второго конкурирующего navbar.
- Исправлено по замечаниям пользователя: relation cards стали крупнее; добавлены CSS-overrides для ширины workspace-страниц и relation card layout.
- Проверено повторно: `project_detail.html`, `relations.html`, `characters.html`, `factions.html`, `events.html` проходят Jinja parse.
- Проверено повторно: `app/templates/partials/entity_workspace.js` проходит `node --check`.
- Проверено повторно: `git diff --check` не нашел whitespace-ошибок.
- Проверено повторно через Flask test client: `/projects/<project_id>`, `/relations`, `/characters`, `/factions`, `/events` возвращают 200.
- После разделения задач изменен только Project Dashboard: `project_detail.html` переписан на структуру, близкую к `projects.html`.
- В `base.html` добавлен режим `project_dashboard_page`, чтобы `/projects/<project_id>` использовал тот же fullscreen shell, что `/projects`.
- В `style.css` добавлен небольшой слой `zpd-*` поверх существующей `zpw-*` системы.
- Проверено: `projects.html`, `project_detail.html`, `base.html` проходят Jinja parse.
- Проверено: `git diff --check` не нашел whitespace-ошибок.
- Проверено через Flask test client: `/projects` и `/projects/<project_id>` возвращают 200.
- Recent activity на Project Dashboard переоформлен через CSS как веточная timeline-лента: линия, точки, компактные строки, без тяжелых отдельных карточек.
- Проверено: `project_detail.html` проходит Jinja parse.
- Проверено: `git diff --check` не нашел whitespace-ошибок.

## Последняя рабочая сессия: формы сущностей и Story Tapestry

- Первый вариант Story Tapestry был отклонен пользователем: компонент выглядел как компактная версия Graph View и находился отдельным горизонтальным блоком, а сами list/dashboard-разделы сущностей оставались в старом дизайне.
- Отклоненный вариант не считается подтвержденным и не должен переноситься в `CHANGELOG.md`.
- Формы создания и редактирования персонажей, фракций и событий переведены на общий интерактивный `entity composer`.
- В формах добавлены живая карточка предварительного просмотра, индикатор заполнения записи, структурированные секции и пояснения о влиянии дат на Logic Warnings.
- Relation Builder сохранит существующий формат значений `type:id`, сгруппированные списки, live preview и подсказки, но получил общий с остальными формами визуальный язык.
- Для внутренних форм добавлена общая верхняя панель проекта, совпадающая с навигацией Projects и Project Dashboard; старые navbar и footer на этих экранах отключены.
- На Project Dashboard встроен интерактивный Story Tapestry по предоставленному HTML-референсу.
- Story Tapestry строит подписи и нити из реальных персонажей, фракций, событий и связей текущего проекта; вымышленные записи не используются.
- Фрагменты реагируют на наведение, открывают карточку записи, нити можно перестроить кнопкой `Weave again`; для пустого проекта предусмотрено стартовое состояние.
- Добавлены отдельные поддерживаемые файлы `app/static/entity_composer.js`, `app/static/story_tapestry.js`, `app/templates/_project_workspace_topbar.html` и `app/templates/_story_tapestry.html`.
- Все затронутые Jinja-шаблоны проходят разбор; Python-модули проходят `compileall`; оба новых JavaScript-файла проходят `node --check`; `git diff --check` не обнаружил ошибок.
- Защищенные маршруты dashboard и create/edit форм проверены через Flask test client и возвращают HTTP 200.
- Desktop и mobile-представления проверены во встроенном браузере: горизонтального переполнения нет, Relation Builder складывается в одну колонку, Story Tapestry сохраняет рабочую область.
- Проверены live preview персонажа и Relation Builder, открытие фрагмента Story Tapestry и отсутствие ошибок JavaScript в консоли.
- Временный локальный пользователь и тестовый проект, созданные исключительно для визуальной проверки, удалены после завершения теста.

## Текущая реализация после исправления замечаний

- Story Tapestry перемещен в hero Project Dashboard справа от названия, описания, статистики и действий проекта.
- Композиция приведена ближе к исходному `StoryTapestry.html`: высокая карточка, свободные текстовые фрагменты, кубические SVG-нити, частицы, подсветка ближайших нитей и фрагментов, ripple при клике, tooltip записи и команда `Weave new`.
- Все подписи Story Tapestry берутся из реальных персонажей, фракций и событий текущего проекта; описания связей используются для содержимого нитей.
- Characters, Factions, Events и Relations полностью переведены на новый fullscreen record workspace с общей верхней панелью проекта.
- Во всех четырех разделах добавлены крупный hero, реальные stat-блоки, поиск, Grid/List-переключатель, счетчик выбранных записей и обновленные карточки.
- Relations получил отдельные крупные connection cards с направлением `source → relation → target`, фильтром типа связи и сохраненными bulk-действиями.
- Существующие маршруты, формы удаления, массовое удаление, поиск и фильтры сохранены без изменения моделей базы данных.
- Проверено через Flask test client: Project Dashboard, Characters, Factions, Events и Relations возвращают HTTP 200.
- Проверено в браузере: desktop-версии Project Dashboard, Characters и Relations; Story Tapestry показывает реальные фрагменты и открывает tooltip записи.
- Проверено в браузере: совместная работа поиска и relation-type filter, Grid/List, checkbox selection и счетчика выбранных записей.
- Проверено на мобильной ширине: горизонтального переполнения нет, hero и карточки складываются вертикально, tapestry сохраняет рабочую высоту.
- Jinja-шаблоны и новые JavaScript-файлы проходят синтаксическую проверку; ошибок JavaScript в консоли браузера не обнаружено.
- Временный локальный пользователь и тестовый проект для этой проверки удалены.

## Последняя рабочая сессия: Import, прокрутка и аудит страниц

- Исправлена общая причина отсутствующей прокрутки на Characters, Factions, Events, Relations и create/edit формах: для длинных project-страниц введен отдельный `scrollable-projects-shell` с вертикальным scroll-контейнером.
- Фиксированные Projects Dashboard, Graph и Warnings не переведены на этот режим и сохраняют собственное управление рабочей областью.
- Страница `/projects/import` полностью переведена на новый Project Setup дизайн.
- Import получил интерактивную upload-зону, drag-and-drop, отображение имени и размера файла, проверку расширения `.json`, состояние готовности и отключенную кнопку до выбора корректного файла.
- Create Project и Edit Project также переведены на общий Project Setup дизайн, чтобы после аудита не осталось старого project-form shell.
- Через браузер подтверждена прокрутка Import, Characters, Factions, Events, Relations, Character form и Relation Builder: `scrollTop` изменяется до фактического конца контейнера.
- Проведен браузерный аудит 30 маршрутов: публичные страницы, wishlist, legal, FAQ, Whitepaper, Roadmap, Beta, Feedback, Contact, все admin-разделы, Projects, project setup, dashboard, entity workspaces, forms, Warnings и Graph.
- Все проверенные страницы используют актуальные семейства интерфейса и не имеют горизонтального переполнения.
- `login.html` и `register.html` дополнительно проверены по шаблонам и анонимным GET-маршрутам; они используют текущий auth modal дизайн.
- Старые неиспользуемые шаблоны `contact_list.html` и `feedback_list.html` удалены. Их маршруты уже перенаправляют в актуальные `/admin/contact` и `/admin/feedback`.
- Все публичные GET-маршруты возвращают HTTP 200. Все защищенные страницы возвращают HTTP 200 для администратора; `/feedback/list` и `/contact/list` корректно возвращают redirect в admin-разделы.
- Ошибок JavaScript в консоли во время полного браузерного аудита не обнаружено.
- Модели базы данных и миграции в этой сессии не изменялись.

## Что требует уточнения

- Нужно проверить на production, что Google Analytics gtag.js корректно загружается и видит посещения.
- Нужно ли делать commit/push после подтверждения текущих admin/contact исправлений.
- Нужно ли запускать локальный сервер заново, если браузер все еще показывает старую ошибку `/admin`.
- Список дальнейших правок Graph Workspace.
- Финальная production-настройка домена и Render.
- Нужно визуально проверить новую карту в браузере: размеры узлов, читаемость подписей, работу drag, path finder и состояние миникарты после перемещения узлов.
- Позже стоит точечно вернуться к Graph Workspace для визуальной полировки на реальных проектах.
- Нужно визуально проверить новый Project Dashboard, Relations, Characters, Factions и Events в браузере на реальных данных.

## Рекомендуемые следующие шаги

1. После deploy проверить Google Analytics в режиме реального времени.
2. Проверить `/admin` в браузере после refresh или перезапуска сервера.
3. Проверить `/contact`, что верхние chips исчезли.
4. Проверить `/feedback`, что выбор темы сохраняется.
5. Проверить `/admin/feedback`, что тема видна в списке и drawer.
6. После подтверждения обновить `CHANGELOG.md`.
7. После push проверить production-deploy и открыть `/projects/<project_id>/graph` на реальном проекте.
8. После просмотра production-версии собрать следующий пакет правок.
9. После подтверждения текущего варианта зафиксировать формы сущностей и Story Tapestry в `CHANGELOG.md`, затем подготовить commit/push для beta-развертывания.
# Последняя рабочая сессия: возврат Terms и Privacy к предоставленным дизайн-референсам

## Что исправлено после просмотра

- После последнего замечания пользователя предыдущая адаптация legal-дизайна признана недостаточно точной и заменена полностью.
- Из приложенных `PrivacyPolicy.html` и `TermsOfService.html` напрямую выделены исходные CSS-системы в отдельные `privacy_policy_reference.css` и `terms_of_service_reference.css`.
- `terms.html` и `privacy.html` полностью переписаны на структуру исходных макетов, включая их top navigation, hero, mobile anchor bar, sidebar TOC, document sections, tables, callouts, rights panel, footer, progress bar и back-to-top.
- JavaScript-интерактивность также перенесена по структуре референсов: scroll progress, IntersectionObserver для активного раздела, smooth anchors, mobile TOC и back-to-top.
- В `base.html` добавлен блок `extra_head`, чтобы reference CSS загружался последним и не переопределялся общими стилями приложения.
- Адаптированы только бренд, реальные маршруты и фактическое содержание Zirel; вымышленные subscriptions, AI, SOC 2, AWS, Stripe и другие отсутствующие возможности из исходных демонстрационных документов не перенесены.
- После сообщения о том, что изменения не отображаются, обнаружено отсутствие запущенного сервера на порту `5000` и обновлен cache-buster `style.css`, чтобы браузер не использовал предыдущую копию стилей.
- Пользователь отклонил визуальную интерпретацию Terms и Privacy из предыдущего варианта: содержание было полезным, но оформление недостаточно точно повторяло предоставленные `TermsOfService.html` и `PrivacyPolicy.html`.
- Terms и Privacy возвращены к композиции референсов: легкая fixed-навигация, центральный document hero, двухколоночный layout, sticky TOC, нумерованные разделы, отдельный legal-footer и back-to-top.
- Подключена типографика референсов: `Inter`, `Instrument Serif` и `JetBrains Mono` только через соответствующие legal-стили.
- Privacy дополнена визуальными компонентами из референса: glass-таблица категорий данных, callout провайдеров и rights panel с переходом к Contact.
- После повторного замечания пользователя интеграция доведена до полного набора компонентов референсов: отдельные таблицы категорий данных, cookies и retention, security-callout, provider pills, rights panel, собственный legal-footer и различающиеся back-to-top элементы Terms/Privacy.
- Сохранена интерактивность референсов: scroll progress, active section в desktop/mobile TOC, smooth back-to-top, hover-состояния, print и внутренняя горизонтальная прокрутка таблиц на мобильных устройствах.
- Сохранена ранее подтвержденная текстовая кнопка `Print` без иконки.
- Фактическое содержание Zirel сохранено: отсутствуют вымышленные платежи, AI, сертификаты безопасности, юридическое лицо и инфраструктура, которых нет в продукте.

## Измененные файлы текущего исправления

- `app/templates/base.html`
- `app/templates/terms.html`
- `app/templates/privacy.html`
- `app/static/style.css`
- `docs/SESSION.md`

## Ожидает подтверждения

- Точность визуального совпадения Terms и Privacy с предоставленными HTML-референсами.
- Содержание legal-документов и дата обновления.

## Рекомендуется дальше

1. Проверить Terms и Privacy рядом с исходными референсами на desktop.
2. Проверить горизонтальную прокрутку таблицы Privacy на мобильной ширине.
3. После подтверждения обновить `CHANGELOG.md` и подготовить commit/push.

---

## Global destructive confirmation dialog — 13 July 2026

- Добавлен единый адаптивный Zirel confirm-dialog вместо верхнего browser `confirm()`.
- Компонент автоматически перехватывает delete forms и delete buttons во всех публичных, пользовательских и административных шаблонах.
- Покрыты: projects, characters, factions, events, relations, bulk/delete-all, Users, Contact, Feedback и Beta Applications.
- `Discard application` использует тот же компонент с отдельным текстом действия.
- Диалог поддерживает Escape, клик по backdrop, возврат focus, индивидуальный текст предупреждения и mobile layout.
- Проверены JavaScript syntax, Python compilation и глобальное подключение dialog assets через `base.html`.

---

## Beta application review and identity fixes — 13 July 2026

- В Admin Applications рядом с `Save review` добавлена отдельная `Delete application` с подтверждением и постоянным удалением записи.
- Recent applications теперь показывает имя в формате `Имя Ф.` вместо технического номера `0001`.
- Удалён `novalidate`, поэтому browser email validation снова активна; дополнительно добавлена независимая server-side проверка длины, local-part, домена, точек и domain labels.
- Проверено: `nonsense`, `a@b`, `a..b@example.com` и пустой local-part отклоняются; корректные адреса и `+alias` принимаются.

---

## Beta Application reference rebuild — 13 July 2026

- `/beta/apply` полностью перестроен по `ZirelBetaApplicationForm.html`: editorial hero, Recent applications, пять секций, capsule/radio controls и sticky live-preview `Your Application`.
- По запросу не перенесены Workspace sidebar и публичный Wave; wave остаётся только административным полем.
- Сохранены кастомные dropdown Zirel/Contact и ссылка Privacy Policy в обязательном consent.
- Добавлены Current Tools, optional product updates, character counters, Save draft, Discard и Application Strength.
- Recent applications публично показывают только внутренний номер и инициал, без email или полного имени.
- Добавлена миграция `c93e82fa1b21` для `current_tools` и `product_updates`; локальная база обновлена.
- Проверено на desktop и `390×844`: два custom selects активны, overflow отсутствует, console errors отсутствуют.

---

## Beta application UI corrections — 13 July 2026

- Beta Application selects подключены к общей кастомной `zf-select` системе вместо нативного browser dropdown.
- Feedback cadence capsules получили устойчивую сетку, увеличенную внутреннюю высоту и отдельный mobile layout.
- `Cookie settings` визуально выровнен с остальными ссылками публичного footer.
- Повреждённые кодировкой символы удаления в Users и Contact заменены CSS-крестиком, не зависящим от текстовой кодировки.
- Legacy `/wishlist` намеренно сохранён как `301` redirect на `/beta/apply`: это переводит старые поисковые результаты и внешние ссылки на новую страницу; удаление route дало бы 404 и замедлило переиндексацию.

---

## Beta applications, consent and project limits — 13 July 2026

- Wishlist UI полностью заменён публичной формой `/beta/apply`; старый `/wishlist` теперь выполняет постоянный redirect для совместимости.
- `WISHLIST_MODE=true` временно работает как alias нового `BETA_APPLICATION_MODE=true`, чтобы существующий Render environment не сломался при деплое.
- Существующие wishlist email не удаляются: миграция расширяет таблицу до beta applications и маркирует прежние записи как `legacy`.
- Новая заявка хранит имя, уникальный нормализованный email, роль, timezone, опыт, словесное количество активных проектов, проблему workflow, готовность к alpha, цель теста, источник и короткий feedback cadence.
- Администратор управляет status, wave и private notes через `/admin/applications`; wave не показывается и не выбирается заявителем.
- Для всех `input[type=number]` скрыты браузерные spinner arrows; в beta application количество проектов выбирается словесно.
- Добавлен Basic Consent Mode: GA4 не загружается до явного согласия. Доступны Necessary only, Accept analytics, Customize и повторное открытие Cookie settings из footer.
- Privacy Policy обновлена до версии 1.1 от 13 July 2026 и описывает работающий consent control.
- Обычным beta-пользователям разрешено максимум 2 проекта, включая импорт; администраторы не ограничены. Значение настраивается через `BETA_PROJECT_LIMIT`.
- Добавлена миграция `b82d71e9fa10`; локальная база обновлена.

### Проверки

- Первая beta application сохраняется, повторный email отклоняется.
- Третий проект блокируется server-side.
- На viewport `390×844` форма не имеет горизонтального overflow.
- До consent Google tag отсутствует; Necessary only скрывает баннер и не загружает GA; Cookie settings повторно открывает preferences.

---

## Mobile public layout fixes — 12 July 2026

- Исправлен селектор графического preview на главной: после добавления beta capacity strip стили больше не применяются к ошибочному последнему элементу hero.
- Для мобильных публичных страниц навбар сделан непрозрачным без backdrop blur, поэтому прокручиваемый контент не просвечивает и не создаёт пустую размытую полосу.
- Уплотнены hero, графический preview и первые интерактивные блоки главной на ширине телефона без изменений desktop-компоновки.
- Privacy и Terms ограничены шириной viewport; широкие legal-таблицы теперь прокручиваются внутри собственного блока и не растягивают документ.
- Проверено при viewport `390×844`: главная, Privacy и Terms не имеют горизонтального переполнения; фиксированные/sticky навбары остаются в границах экрана.

### Изменённые файлы

- `app/static/style.css`
- `app/static/mobile_public_fixes.css`
- `app/templates/base.html`
- `docs/SESSION.md`

---

## Favicon — 12 July 2026

- Пользовательский знак с соединёнными узлами подготовлен для маленького масштаба: встроенная шахматная подложка удалена и заменена настоящей прозрачностью.
- Подключены `favicon.ico`, PNG `32×32` и Apple Touch Icon `180×180` через общий `base.html`.

---

## Closed beta capacity and invitations — 12 July 2026

- Добавлен закрытый набор на 100 обычных аккаунтов; лимит настраивается через `BETA_ACCOUNT_LIMIT`, а обязательность приглашений — через `CLOSED_BETA_INVITES`.
- Публичные страницы остаются доступными всем. Регистрация требует одноразовый код или ссылку с `?invite=...`; обычный вход после регистрации работает без кода.
- На первом экране главной добавлен адаптивный индикатор заполнения беты в цветовой гамме Zirel. Администраторы и уже авторизованные пользователи в счётчик не входят.
- Добавлены модель `BetaInvite`, миграция `7a31b6e4c2d9`, блокировка конкурентной регистрации при достижении лимита и административная страница `/admin/invites` для выпуска и отзыва приглашений.
- Проверены: одноразовое использование кода, отказ без кода, повторное использование, создание кодов администратором, Python/JavaScript syntax и миграция локальной базы.

### Эксплуатация

1. После развёртывания выполнить `flask db upgrade`.
2. Войти администратором и открыть `Admin → Invites`.
3. Указать количество кодов, срок действия и необязательную заметку, затем нажать `Generate invites`.
4. Передать тестировщику полную персональную ссылку регистрации. Каждый код рассчитан на один аккаунт; скомпрометированный неиспользованный код следует отозвать.

### Изменённые файлы

- `config.py`
- `app/models.py`
- `app/routes.py`
- `app/templates/index.html`, `register.html`, `admin_invites.html` и административная навигация
- `app/static/beta_access.css`, `beta_access_hero.css`, `beta_access.js`
- `migrations/versions/7a31b6e4c2d9_add_beta_invites.py`

---

# Latest working session: entity creation refresh

## Implemented

- Adapted the production-safe parts of `ZirelCreateEntities.html` into the existing Character, Faction, Event, and Relation creation flows without changing database models, routes, or submitted field names.
- Added shared create-type tabs linking the four real project routes, with the current type highlighted and a horizontally scrollable mobile layout.
- Preserved the existing project topbar, breadcrumbs, server validation, Relation Builder, live previews, record-depth progress, and factual Logic Warning guidance.
- Added `entity_create_refresh.css` and `entity_create_refresh.js`: current Zirel typography, refined section numbering, calmer panels, preview live indicator, description counters, invalid-field feedback, and Ctrl/Cmd+Enter submission.
- Explicitly deferred unsupported reference concepts such as drafts, autosave, quick relation creation inside entity forms, affiliation/member multiselects, fake success screens, and additional entity fields.
- Jinja parsing, JavaScript syntax, and diff checks pass for all four creation templates and the shared tabs include.

## Closed beta access recommendation

- Do not use one-device-one-account as the primary gate: device fingerprints are unreliable, privacy-sensitive, easy to bypass, and can block legitimate users after browser/device changes.
- Prefer invite-only registration with single-use codes or an approved-email allowlist, plus a configurable total account cap enforced server-side.
- Keep normal email uniqueness and add basic rate limiting; consider email verification only if operationally ready.
- No registration restriction was implemented in this session, per the user's request.

## Awaiting confirmation

- Visual confirmation in an authenticated project before updating `CHANGELOG.md` and preparing a release commit.

---

# Latest working session: shared form system redesign

## Implemented

- Adapted the form language from `ZirelForms.html` into a shared project-wide form system while preserving each existing form workflow and the project's Inter, Instrument Serif, and JetBrains Mono typography.
- Added `form_system.css` and `form_system.js` globally through `base.html` for Contact, Feedback, registration, entity composers, relation builder, project forms, and the embedded Beta feedback form.
- Replaced targeted native select presentation with an accessible custom popup: styled trigger, animated dark option panel, optgroup labels, selected checkmark, keyboard arrows/Escape, outside-click closing, native value synchronization, change events, reset support, and screen-reader labeling.
- Kept real native selects in the form for normal submission; the custom control only replaces their visual interaction.
- Redesigned Contact and Feedback as separate reference-inspired pages using `public_forms.css`: editorial hero, glowing card, responsive two-column context layout, unified fields/buttons, auto-growing 1000-character message area, and live counter.
- Corrected Feedback role values to match server validation, including `Worldbuilder` and `Narrative Designer`.
- Verified Contact, Feedback, and Register return HTTP 200; custom select selection updates native values, Feedback creates two correct controls, Register creates one, and no console or horizontal-overflow errors were found.

## Awaiting confirmation

- Visual confirmation across authenticated project/entity forms before updating `CHANGELOG.md` and preparing a commit.

---

# Latest working session: FAQ interactive redesign

## Implemented

- Replaced the previous Bootstrap/zv2 FAQ with a project-specific adaptation of `ZirelFaqSection.html`.
- Reviewed and consolidated the content into 21 current questions across General, Data & Ownership, Beta & Safety, Features, and Future Plans.
- Corrected unsupported reference claims: no self-service account deletion yet, no guaranteed beta-data survival, no fixed beta waves or response times, no saved warning state in export, and no misleading future cloud-sync promise.
- Added factual answers for the five current Logic Warnings, Graph Workspace, Story Tapestry, JSON portability, current absence of AI processing, payments, and collaboration.
- Added isolated `faq_manual.css` and `faq_manual.js` with independent accordions, sidebar scroll-spy, reading progress, full-text search, live result count, Escape-to-clear, empty state, and mobile category chips.
- Verified `/faq` returns HTTP 200 with 21 items; accordion, search, empty state, and mobile 390px layout work without horizontal overflow or console errors.
- Follow-up: removed the complete `Try a small world and see how it feels` FAQ CTA block; the sidebar contact link now routes directly to `/contact` instead of the removed anchor.

## Awaiting confirmation

- Final visual and wording approval before updating `CHANGELOG.md` and preparing a commit.

---

# Latest working session: Whitepaper editorial redesign

## Implemented

- Replaced the previous `zv2` Whitepaper layout with a project-specific adaptation of `ZirelWhitepaper.html`.
- Preserved and reviewed twelve factual sections covering the problem, principles, workflow, data model, five current rule checks, Graph Workspace, Story Tapestry, ownership, MVP, beta validation, future research, and boundaries.
- Kept AI explicitly outside the current core product and removed the reference's duplicated future-direction paragraph and misleading Story Tapestry timeline claim.
- Added the reference's editorial hero, disclaimer, sticky desktop contents, horizontally scrollable mobile TOC chips, numbered section headers, drop cap, pull quote, structured principles, and final thesis CTA.
- Integrated Zirel gradient buttons, violet/blue glow, gradient italic accents, dot-grid atmosphere, and shared public header/footer.
- Added isolated assets `app/static/whitepaper_manual.css` and `app/static/whitepaper_manual.js` with reading progress, active TOC state, and section reveal behavior.
- Verified `/whitepaper` returns HTTP 200; desktop and 390px layouts have no horizontal page overflow or console errors.
- Follow-up: fixed the `Product Principles` grid where descriptions were auto-placed into the 34px numbering column. Titles and descriptions now stay in the full-width second column, and all five principle rows render at equal compact heights; stylesheet cache bumped to `v2`.

## Awaiting confirmation

- Final visual and wording approval before updating `CHANGELOG.md` and preparing a commit.

---

# Latest working session: Roadmap manual redesign

## Implemented

- Replaced the previous `zv2` Roadmap layout with a project-specific adaptation of `ZirelRoadmap.html`.
- Preserved all documented roadmap phases and factual product priorities without adding dates, release promises, or unsupported capabilities.
- Added the reference's narrow editorial column, four connected phase cards, desktop vertical phase navigation, reading progress, reveal behavior, disclaimer, and evidence-based priority section.
- Integrated Zirel's current rounded gradient buttons, violet/blue glow, dot-grid atmosphere, and site-wide header/footer.
- Applied the requested Zirel violet-to-blue gradient to selected italic words in the hero, phase titles, and priority statement.
- Added isolated assets `app/static/roadmap_manual.css` and `app/static/roadmap_manual.js`.
- Verified `/roadmap` returns HTTP 200, phase navigation and reading progress work, cards reveal correctly, and the 390px mobile layout has one-column lists with no horizontal overflow or console errors.

## Awaiting confirmation

- Final visual approval before adding the Roadmap redesign to `CHANGELOG.md` and preparing a commit.

---

# Latest working session: Beta Field Manual redesign

## Implemented

- Replaced the previous public Beta page with a project-specific adaptation of `ZirelBetaFieldManual.html`.
- Kept the reference's field-manual hierarchy, reading progress, chapter navigation, live transmission, pinnable capability cards, ten-minute test protocol, limitations accordion, data-safety terminal, and feedback area.
- Excluded the reference graph visualization and timeline. The page instead points testers to Zirel's existing constellation-style Graph Workspace and uses a compact entity/relation starter universe.
- Removed unsupported claims and fictional metrics. All capability and limitation copy follows the documented MVP: private projects, core entities, typed relations, five rule-based warnings, Graph Workspace, JSON portability, basic account controls, no active AI core feature, and early-beta backup guidance.
- Embedded feedback posts to the existing `/feedback` route with server-valid role and topic values.
- Added isolated responsive assets `app/static/beta_field_manual.css` and `app/static/beta_field_manual.js`.
- Verified `/beta` returns HTTP 200, Jinja and JavaScript parse successfully, interactive controls work, and desktop/mobile layouts have no horizontal overflow or console errors.

## Awaiting confirmation

- Final visual approval of the new Beta page before adding it to `CHANGELOG.md` and preparing a commit.

## Follow-up correction

- Removed the complete `Use a small test universe first` demo chapter and its side-navigation entry at the user's request.
- Rebuilt capability cards to match the reference interaction: first activation expands details, second activation pins the card, and another activation unpins it; the three-card limit remains enforced.
- Corrected missing generated-element classes that had prevented checklist and limitation styles from applying.
- Restored reference-like chapter reveal, typewriter transmission, checklist completion state, confetti, severity accordion styling, and a working clipboard interaction using a factual JSON-backup reminder.
- Kept the existing integrated feedback form unchanged.
- Performed a second direct visual comparison against `ZirelBetaFieldManual.html` after the user reported that the first screen still differed.
- Corrected hero typography from the oversized adaptation to the reference scale, rebuilt the transmission panel spacing and 60px oscilloscope, restored the reference dot grid, animated background orb, grain texture, cursor glow, and desktop custom cursor behavior.
- Matched the reference chapter spacing and mobile behavior, including hiding the transmission panel below 900px while preserving the project's shared navigation and factual product copy.
- Rebuilt the `What you can test`, `Test Zirel in 10 minutes`, and `Known limitations` chapters against the reference geometry: chapter rules and number tails, compact glass capability chips, 140px gradient timer, two-column protocol, reference checklist rows, severity badges, pulse indicators, and chevrons.
- Fixed a browser-visible checklist markup bug where step descriptions were rendered in the number column, and corrected the limitations control order to pulse, severity, summary, chevron.
- Reverified capability expand/pin, timer start, and accordion expansion in the browser with no console errors or horizontal overflow.
- Follow-up: normalized the Beta `What you can test` capability cards into an equal-height grid (3 columns desktop, 2 tablet, 1 mobile) while preserving expand and pin behavior; bumped the Beta stylesheet cache key to `v8`.

---

# Последняя рабочая сессия: интерактивные блоки Landing Page

## Что изменено

- `ZirelLandingPageOne.html` адаптирован вместо прежних отдельных секций `For creators` и `Current beta` на главной странице.
- Новый объединенный блок получил переключаемые роли создателей, фактические описания сценариев использования Zirel и beta-карточку с реальными маршрутами Beta, Roadmap, Whitepaper и Feedback.
- `ZirelLandingPageTwo.html` адаптирован вместо старого статичного блока `How it works`, поскольку оба блока описывали одинаковую последовательность `Create → Connect → Analyze → Refine`.
- Новый workflow использует раскрывающиеся шаги, журнал фактических операций, сводные показатели, autoplay, ручное переключение и клавиатурное управление.
- В демонстрационном содержании не перенесены отсутствующие функции референса: templates, versioning, Markdown export и game-engine export.
- Повторный финальный CTA `Start small` удален: после крупной beta-карточки он не добавлял новой информации и дублировал переход в Beta.
- Добавлены поддерживаемые файлы `app/static/landing_creators.js` и `app/static/landing_workflow.js`.
- `ZirelLandingPageThree.html` адаптирован вместо прежнего статичного блока `Core workspace`, поскольку оба раздела описывали один и тот же набор доступных возможностей.
- Новый Feature Explorer показывает шесть подтвержденных возможностей через боковой список и сменяемый inspector: private projects, core entities, relation builder, Logic Warnings, Graph Workspace и JSON portability.
- Для Explorer добавлен поддерживаемый файл `app/static/landing_explorer.js`; демонстрационное содержимое не изменяет данные и не заявляет отсутствующие функции.
- Главная страница проверена на desktop и mobile: горизонтального переполнения и JavaScript-ошибок не обнаружено.

## Ожидает подтверждения

- Визуальная композиция двух новых Landing Page блоков и решение о фиксации их в `CHANGELOG.md`.

---

# Предыдущая рабочая сессия: Roadmap, Whitepaper, Terms и Privacy

## Что сделано

- Публичный Roadmap переведен с устаревшей схемы Q1-Q4 на этапы: доступно сейчас, готовность к бете, глубина анализа и исследовательские направления.
- Убраны вымышленные сроки и неподтвержденные обещания; добавлены реальные приоритеты надежности, приватности, удаления данных, onboarding и тестирования.
- Whitepaper полностью актуализирован по текущему Zirel: описаны фактическая модель мира, основной workflow, пять существующих правил Logic Engine, Graph Workspace, Story Tapestry, владение контентом и вопросы для бета-проверки.
- Terms of Service расширены разделами об аккаунтах, разрешенном и запрещенном использовании, владении контентом, beta availability, выводах Logic Engine, экспорте, удалении, сторонних сервисах и ограничениях ответственности.
- Privacy Policy приведена в соответствие с текущей реализацией: аккаунты, проектные данные, feedback/contact/wishlist, Google Analytics 4, Render/PostgreSQL, сроки хранения, права пользователей, экспорт, удаление, безопасность и отсутствие активных AI-функций.
- В legal-документы добавлены общие списки с разделителем `-`, сохранившие утвержденный визуальный стиль и печатную версию.

## Измененные файлы

- `app/templates/roadmap.html`
- `app/templates/whitepaper.html`
- `app/templates/terms.html`
- `app/templates/privacy.html`
- `app/static/style.css`
- `docs/ROADMAP.md`
- `docs/SESSION.md`

## Требует подтверждения

- Содержание и формулировки четырех публичных документов.
- Публикация даты обновления `10 July 2026` на Terms и Privacy.
- Решение о добавлении отдельного consent/preferences интерфейса для Google Analytics перед широкой публичной бетой.
- Формальные данные оператора, юрисдикция и прямой privacy-контакт перед коммерческим или широким публичным запуском.

## Рекомендуется дальше

1. Просмотреть все четыре страницы на desktop и mobile.
2. Перед широкой бетой реализовать analytics consent control для регионов, где он требуется.
3. Определить и добавить официальные данные оператора и privacy-контакт.
4. После подтверждения обновить `CHANGELOG.md` и подготовить commit/push.

---
