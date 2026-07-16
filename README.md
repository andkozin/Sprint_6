# Яндекс Самокат — Автотесты (Спринт 6)

Автотесты для «Яндекс Самокат» на Selenium + pytest. 

## Главное 

- **Запустить тесты:** `pytest`
- **Allure‑отчёт:** `pytest --alluredir=allure-results` → `allure serve allure-results`
- **Покрытие кода:** `python -m coverage run -m pytest` → `python -m coverage report -m`
- **Мёртвый код:** `vulture pages/ tests/ --min-confidence 100`

## Стек
Python, Selenium, pytest, Allure, webdriver-manager, coverage, vulture.

## Структура
- `pages/` — PO
- `tests/` — тесты.
- `locators.py` — локаторы.
- `conftest.py` — фикстуры.

## Git 

- Создать и переключиться на ветку `develop`:  
  `git checkout -b develop`
- Отправить ветку на GitHub:  
  `git push -u origin develop`
- Посмотреть последние 10 коммитов:  
  `git log --oneline -10`


