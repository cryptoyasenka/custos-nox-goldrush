# Custos Nox — Grant Submission Plan

## Приоритет подачи

### 1. SF Ukraine Grants — СДЕЛАТЬ СЕГОДНЯ
**$1K–$10K USDG | Rolling (~7 дней на решение) | Только Украина**

- URL: https://earn.superteam.fun/grants/solana-foundation-ukraine-grants
- Категория: Developer Tooling + DAO Tooling
- Контакт: andrew@kumeka.team
- Статус: [ ] не подано

**Что нужно:**
- [ ] Описание проекта (см. шаблон ниже)
- [ ] GitHub ссылка: https://github.com/cryptoyasenka/custos-nox
- [ ] Milestone план с бюджетом
- [ ] Объяснение "зачем деньги если open-source" (см. ниже)

---

### 2. Agentic Engineering Grant — ДЕДЛАЙН 4 МАЯ
**$200 USDG | ~10 минут на заявку**

- URL: https://earn.superteam.fun/grants/agentic-engineering
- Требует: описание + Colosseum submission link
- Статус: [ ] не подано

---

### 3. Colosseum Public Goods Award — ДЕДЛАЙН 11 МАЯ
**$10,000 | В рамках основного хакатона**

- URL: arena.colosseum.org (уже зарегистрированы)
- Действие: явно написать "open-source public good, MIT license" в описании проекта
- Статус: [ ] текст не добавлен

---

### 4. Ukrainian Track — ДЕДЛАЙН 11 МАЯ
**$10,000 USDG (1-е 5K / 2-е 3K / 3-е 2K)**

- URL: https://earn.superteam.fun/listing/frontier-hackathon-ukrainian-track
- Подаётся автоматически если в Colosseum профиле страна = Украина
- [ ] Проверить что country = Ukraine в профиле
- [ ] Зарегистрироваться на Online Demo Day

---

### 5. Solana Foundation Direct — ПОСЛЕ ХАКАТОНА
**Сумму указываешь сама | ~4 недели на решение**

- URL: https://share.hsforms.com/1GE1hYdApQGaDiCgaiWMXHA5lohw
- Категория в форме: Developer Tooling
- Статус: [ ] не подано

---

## Почему open-source проекту нужны деньги

Это стандартный вопрос для всех грантовых программ. Грантодатели прекрасно понимают open-source модель — именно для таких проектов гранты и существуют. Логика простая:

**Open-source ≠ бесплатная разработка.**
Разработчик тратит время. Время = деньги. Грант компенсирует это время чтобы проект развивался, а не умер через месяц.

### Конкретные статьи бюджета для Custos Nox

| Статья | Обоснование |
|---|---|
| Разработка (developer time) | Основная статья. Детекторы, тесты, web dashboard — это месяцы работы |
| Security audit | Сторонний аудит кода — доверие пользователей перед деплоем в production |
| Documentation | Написать нормальный onboarding чтобы non-technical DAO команди могли задеплоїти |
| Outreach | Звʼязатися з реальними DAO командами (Realms, Squads users) щоб вони спробували |

> Примечание: RPC и hosting — ответственность пользователя (self-hosted модель).
> Каждый деплоит на своём Helius аккаунте (free tier хватает для одного multisig).
> Yana не платит за инфраструктуру пользователей.

### Шаблон ответа на "зачем деньги"

> Custos Nox — public good для всего Solana ecosystem. Код MIT, self-hosted:
> каждый деплоит на своей инфраструктуре с собственным Helius ключом — без vendor lock-in
> и без инфраструктурных расходов для автора. Грант покрывает исключительно время разработчика:
> (1) следующие детекторы и web dashboard чтобы non-technical DAO могли использовать без CLI,
> (2) security audit для доверия перед production деплоями,
> (3) outreach чтобы реальные multisig команды узнали что инструмент существует.
> Цель: к концу гранта — 10+ реальных DAO которые используют Custos Nox для защиты treasury.

---

## Checklist перед каждой подачей

- [ ] GitHub repo public, CI зелений, README актуальний
- [ ] Live demo сайт: https://custos-nox.up.railway.app
- [ ] Colosseum submission link (потрібен для деяких програм)
- [ ] Milestone план готовий (конкретні суми і терміни)
- [ ] Email відправника: cryptoyasenka@gmail.com
