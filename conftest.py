# conftest.py
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pages.main_page import MainPage
from pages.order_page import OrderFormPage

from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import os
import subprocess


@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--window-size=1920,1080")

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    yield driver
    """ После обновления браузера появилась проблема - (60.06s teardown tests/test_order.py
    57.46s teardown tests/test_order.py) ИИ предлож. убрать driver.quit() и использовать killall в
    @pytest.fixture(scope="function") 
    def driver():
        options = Options()
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Firefox(options=options)
        yield driver
        driver.quit()"""
    if os.name == "posix":
        subprocess.run(["killall", "-9", "firefox"], capture_output=True, check=False)
        subprocess.run(["killall", "-9", "geckodriver"], capture_output=True, check=False)

@pytest.fixture(scope="function")
def page(driver):
    base_url = "https://qa-scooter.praktikum-services.ru"
    return MainPage(driver, base_url=base_url)

    # подговил открыл страницу -банер закрыл- кликал на точку входа в
@pytest.fixture
def prepared_order_flow(driver, page, location, data_set):
    
    page.open()
    main_page = MainPage(driver)
    page_order = OrderFormPage(driver)

    #  закрываем куки
    with allure.step("Закрываю баннер с куки"):
        page_order.close_cookie_banner()

    #  кликаем (top или bottom)
    with allure.step(f"Кликаю кнопку заказа: {location}"):
        main_page.click_order_button(location=location)

    # ждём, пока форма будет готова
    with allure.step("Ожидаю готовности формы 1"):
        page_order.wait_for_form_1_ready()

    # вернул все тесту
    return {
        "main": main_page,
        "order": page_order,
        "data": data_set,
        "page": page
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
