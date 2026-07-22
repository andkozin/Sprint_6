# tests/form_1_1.py

import pytest
import allure
import json
from locators.order_form_locators import OrderFormLocators

from tests.data import ENTRY_POINTS

class TestForm1:

    FIELD_CONFIG = {
        "name": ("Имя", OrderFormLocators.INPUT_NAME, "fill_name"),
        "surname": ("Фамилия", OrderFormLocators.INPUT_SURNAME, "fill_surname"),
        "address": ("Адрес", OrderFormLocators.INPUT_NAME, "fill_address"), # INPUT_ADDRESS
        "metro": ("Метро", OrderFormLocators.INPUT_METRO_SEARCH, "fill_metro"), # INPUT_METRO_SEARCH
        "phone": ("Телефон", OrderFormLocators.INPUT_PHONE, "fill_phone"),
    }

    def _prepare_form_1(self,main_page, page_order, cfg):
        with allure.step(f"Клик по кнопке «Заказать» ({cfg['location']})"):
            main_page.click_order_button(cfg["location"])
            page_order.wait_for_form_1_ready()

    @allure.feature("Самокат: проверки полей Формы 1")
    @allure.story("Проверка полей формы: точка входа — ВЕРХНЯЯ кнопка")
    @pytest.mark.parametrize("field_key", FIELD_CONFIG.keys(), ids=FIELD_CONFIG.keys())
    @allure.title("Поле '{field_key}' через ВЕРХНЮЮ кнопку")
    def test_top_entry_point(self,prepared_order_flow, field_key):
        flow = prepared_order_flow
        main_page, page = flow["main"], flow["order"]
        cfg = ENTRY_POINTS["top"]

        self._prepare_form_1(main_page, page, cfg)

        with allure.step("Ждём появления Формы 2"):
                assert page.wait_for_form_1_ready(), "Форма 1 не появилась "

        display_name, locator, method_name = self.FIELD_CONFIG[field_key]
        value = cfg["data"][field_key]

        allure.attach(json.dumps(cfg["data"], ensure_ascii=False, indent=2), "Данные (top)", allure.attachment_type.JSON)
        allure.attach(f"Поле: {display_name}\nЗначение: {value}", "Значение", allure.attachment_type.TEXT)

        with allure.step(f"Заполняем поле: {display_name}"):
            getattr(page, method_name)(value)

        with allure.step("Проверяем значение"):
            assert page.is_field_has_value(locator, value), f"Поле '{field_key}' не содержит ожидаемого значения"

    @allure.feature("Самокат:  проверки полей Формы 1") 
    @allure.story("Проверка полей формы: точка входа — НИЖНЯЯ кнопка")
    @pytest.mark.parametrize("field_key", FIELD_CONFIG.keys(), ids=FIELD_CONFIG.keys())
    @allure.title("Поле '{field_key}' через НИЖНЮЮ кнопку")
    def test_bottom_entry_point(self,prepared_order_flow, field_key):
        flow = prepared_order_flow
        main_page, page = flow["main"], flow["order"]
        cfg = ENTRY_POINTS["bottom"]

        # для другой кнопки
        self._prepare_form_1(main_page, page, cfg)

        with allure.step("Ждём появления Формы 2"):
                assert page.wait_for_form_1_ready(), "Форма 1 не появилась "

        display_name, locator, method_name = self.FIELD_CONFIG[field_key]
        value = cfg["data"][field_key]

        allure.attach(json.dumps(cfg["data"], ensure_ascii=False, indent=2), "Данные (bottom)", allure.attachment_type.JSON)
        allure.attach(f"Поле: {display_name}\nЗначение: {value}", "Значение", allure.attachment_type.TEXT)

        with allure.step(f"Заполняем поле: {display_name}"):
            getattr(page, method_name)(value)

        with allure.step("Проверяем значение"):
            assert page.is_field_has_value(locator, value), f"Поле '{field_key}' не содержит ожидаемого значения"        






