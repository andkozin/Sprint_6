# 1. Создаём __init__.py, чтобы импорты работали (иначе будет ModuleNotFoundError)
touch pages/__init__.py
touch tests/__init__.py

# 2. Настраиваем pytest.ini, чтобы результаты сразу падали в allure-results
cat > pytest.ini <<EOF
[pytest]
addopts = --alluredir=allure-results
testpaths = tests
python_files = test_*.py
EOF

# 3. Настраиваем .gitignore, чтобы не пушить мусор
cat > .gitignore <<EOF
__pycache__/
*.pyc
.pytest_cache/
allure-results/
allure-report/
.DS_Store
EOF

# 4. Исправляем conftest.py: добавляем путь к корню, чтобы видел constants/pages
sed -i.bak '1i import os\nimport sys\nroot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))\nif root_path not in sys.path:\n    sys.path.insert(0, root_path)\n' tests/conftest.py

# 5. Запускаем тест — данные сразу пишутся в allure-results
pytest tests/test_order.py -v -s

# создает папку aluure_report
allure generate allure-results -o allure-report --clean

# 6. Смотрим отчёт (он подтянет данные из шага 5)
allure serve allure-results

# создает папку aluure_report
allure generate allure-results -o allure-report --clean

# без pytest.ini
pytest tests/test_expand.py --alluredir=allure-results

pip freeze > requirements.txt

Шаг 1: запусти тесты с сохранением результатов для Allure
pytest --alluredir=allure-results

Шаг 2: сгенерируй HTML‑отчёт
allure generate allure-results --clean -o allure-report

Как посмотреть
open allure-report/index.html

Либо через сервер 
allure serve allure-results

#качай свежие данные с сервера, но не меняй файлы у меня на диске
git fetch origin

 Посмотри, какие коммиты есть локально, но нет на сервере
 git log --oneline origin/develop..develop 
 -Если вывод пустой — твоя локальная ветка полностью совпадает с удалённой.

  Быстро увидеть список файлов, которые отличаются
  git diff --name-status origin/develop develop

они покажут все строки с хардкодом локаторов и номера строк:
grep -rn "By\.ID" pages/ tests/
grep -rn "By\.CSS_SELECTOR" pages/ tests/
grep -rn "By\.XPATH" pages/ tests/
