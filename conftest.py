# conftest.py
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.options import Options # # from selenium.webdriver.chrome.options import Options

from pages.main_page import MainPage
from pages.order_page import OrderFormPage

from tests.data import ENTRY_POINTS

BASE_URL = "https://qa-scooter.praktikum-services.ru"

# @pytest.fixture(scope="function") 
# def driver():
#         options = Options()
#         options.add_argument("--window-size=1920,1080")
#         driver = webdriver.Firefox(options=options) # driver = webdriver.Chrome(options=options)
#         yield driver
#         driver.quit()

""" После обновления браузера появилась проблема - (60.06s teardown tests/test_order.py
    57.46s teardown tests/test_order.py) ИИ предлож. убрать driver.quit() и использовать killall в ->"""

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
    if os.name == "posix": #
        subprocess.run(["killall", "-9", "firefox"], capture_output=True, check=False) #
        subprocess.run(["killall", "-9", "geckodriver"], capture_output=True, check=False)#
"""    
после обновления OS и после команды pip install webdriver-manager - проблема  ушла похоже версии драйвера и бразера не совпадали
"""

# для главной страницы
@pytest.fixture
def page(driver):
    return MainPage(driver, base_url=BASE_URL)

# открывает главную, закрывает куки.
   
@pytest.fixture(scope="function")
def prepared_order_flow(driver):
    
    main_page = MainPage(driver, base_url=BASE_URL)
    page_order = OrderFormPage(driver, base_url=BASE_URL)

    with allure.step("Открываем главную страницу"):
        main_page.open()

    with allure.step("Закрываем баннер с куки"):
        page_order.close_cookie_banner()

    return {
        "main": main_page,
        "order": page_order,
    }

# для навигации 

@pytest.fixture
def flow_with_success_modal(prepared_order_flow, entry_data_by_key):
    flow = prepared_order_flow
    main_page = flow["main"]
    page_order = flow["order"]

    data, location = entry_data_by_key

    # ДО теста
    with allure.step(f"Нажимаем кнопку «Заказать» ({location})"):
        main_page.click_order_button(location)

    with allure.step("Заполняем Форму 1 и отправляем"):
        page_order.fill_form_1_full(data)
        page_order.submit_order()

    with allure.step("Заполняем Форму 2 и подтверждаем заказ"):
        page_order.fill_form_2_full(data)
        page_order.click_order_button_2()
        page_order.wait_for_modal_with_confirm_button()
        page_order.confirm_order_yes()

    return flow

@pytest.fixture
def entry_data_by_key(request):
    key = request.param
    entry = ENTRY_POINTS[key]
    return entry["data"], entry.get("button_location", key)

