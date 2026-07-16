# conftest.py
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pages.main_page import MainPage
from pages.order_page import OrderFormPage

from tests.data import ENTRY_POINTS

BASE_URL = "https://qa-scooter.praktikum-services.ru"

@pytest.fixture(scope="function") 
def driver():
        options = Options()
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Firefox(options=options)
        yield driver
        driver.quit()

""" После обновления браузера появилась проблема - (60.06s teardown tests/test_order.py
    57.46s teardown tests/test_order.py) ИИ предлож. убрать driver.quit() и использовать killall в ->

import subprocess
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import os
@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    yield driver
    if os.name == "posix":
        subprocess.run(["killall", "-9", "firefox"], capture_output=True, check=False)
        subprocess.run(["killall", "-9", "geckodriver"], capture_output=True, check=False)
        
    после обновления OS и после команды pip install webdriver-manager - проблема  ушла похоже версии драйвера и бразера не совпадали
"""

# для главной страницы
@pytest.fixture
def page(driver):
    return MainPage(driver, base_url=BASE_URL)

# открыл страницу,закрыл куки, клик заказать, жду форму1
@pytest.fixture(params=["top", "bottom"], ids=["top_button", "bottom_button"])
def prepared_order_flow(driver, request):
    
    entry_key = request.param
    config = ENTRY_POINTS[entry_key]
    location = config["location"]
    data_set = config["data"]

    #  URL
    main_page = MainPage(driver, base_url=BASE_URL)
    page_order = OrderFormPage(driver, base_url=BASE_URL)

    with allure.step("Открываем главную страницу"):
        main_page.open()

    with allure.step("Закрыл куки "):
        # Метод должен быть с try/except внутри класса страницы!
        page_order.close_cookie_banner()

    with allure.step(f"Клик кнопка заказа: {location}"):
        main_page.click_order_button(location=location)

    with allure.step("Жду Форму1"):
        page_order.wait_for_form_1_ready()

    return {
        "main": main_page,
        "order": page_order,
        "data": data_set,
    }

# для заполнения формы 2
@pytest.fixture
def prepared_form_2(prepared_order_flow):
    flow = prepared_order_flow
    page_order = flow["order"]
    data = flow["data"]

    with allure.step("➡️ Доходим до Формы 2 (дозаполняем и отправляем Форму 1)"):
        # в форме1 заполнил
        page_order.fill_name(data["name"])
        page_order.fill_surname(data["surname"])
        page_order.fill_address(data["address"])
        page_order.fill_metro(data["metro"])
        page_order.fill_phone(data["phone"])

        page_order.submit_order()
        assert page_order.wait_for_form_2_ready(), "Форма 2 не появилась"

    return flow # вернул в тест

# для навигации
@pytest.fixture
def prepared_success_modal(prepared_form_2):
    flow = prepared_form_2
    page_order = flow["order"]
    data = flow["data"]
    
    # заполним форму2
    page_order.fill_order_date_from_calendar(data["order_date"])
    page_order.select_duration(data["duration"])
    page_order.select_scooter_color(data["scooter_color"])
    page_order.fill_comment(data["comments"])
    page_order.click_order_button_2()
    page_order.wait_for_modal_with_confirm_button()
    page_order.confirm_order_yes()
    
    #  модалка с посмотреть статус
    assert page_order.is_order_success_visible(), "Форма Посмотреть статус не появилась"
    page_order.click_view_status()

    yield flow # вернул в тест
