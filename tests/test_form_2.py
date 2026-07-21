# tests/test_form_2.py
import pytest
import allure
import json

from pages.locators import OrderFormLocators
from tests.data import ENTRY_POINTS

# Переход к форме 2
def _prepare_form_2(main_page, page_order, cfg):
    
    with allure.step("Клик по кнопке «Заказать»"):
        main_page.click_order_button(cfg["location"])

    with allure.step("Заполняем Форму 1 и отправляем заказ"):
        page_order.fill_form_1_full(cfg["data"])
        page_order.submit_order()

    with allure.step("Ждём появления Формы 2"):
        assert page_order.wait_for_form_2_ready(), "Форма 2 не появилась после отправки Формы 1"

FORM_2_FIELDS_CONFIG = {
    "order_date": ("Дата заказа", OrderFormLocators.DATE_INPUT, "fill_order_date_from_calendar", "is_date_filled"),
    "duration": ("Длительность аренды", OrderFormLocators.DURATION_DROPDOWN, "select_duration", "is_duration_selected"),
    "scooter_color": ("Цвет самоката", None, "select_scooter_color", "is_scooter_color_selected"),
    "comments": ("Комментарий", OrderFormLocators.COMMENT_FIELD, "fill_comment", None),
}

@allure.feature("Самокат: атомарные проверки полей Формы 2")
@allure.story("Проверка полей Формы 2: точка входа — ВЕРХНЯЯ кнопка")
@pytest.mark.parametrize("field_key", FORM_2_FIELDS_CONFIG.keys(), ids=FORM_2_FIELDS_CONFIG.keys())
@allure.title("Поле '{field_key}' через ВЕРХНЮЮ кнопку")

def test_top_entry_point(prepared_order_flow,  field_key):
    flow = prepared_order_flow
    main_page, page = flow["main"], flow["order"]
    cfg = ENTRY_POINTS["top"]

    _prepare_form_2(main_page, page, cfg)

    display_name, locator, fill_method_name, check_method_name = FORM_2_FIELDS_CONFIG[field_key]

    if field_key == "scooter_color":
        data_key = "scooter_color"
    elif field_key == "comment":
        data_key = "comments"
    else:
        data_key = field_key

    value = cfg["data"][data_key]  

    allure.attach(json.dumps(cfg["data"], ensure_ascii=False, indent=2), f"Данные (top)", allure.attachment_type.JSON)
    allure.attach(f"Поле: {display_name}\nЗначение: {value}", "Значение поля", allure.attachment_type.TEXT)

    with allure.step(f"Заполняем поле: {display_name}"):
        fill_method = getattr(page, fill_method_name)
        fill_method(value)

    with allure.step("Проверяем значение"):
        if check_method_name:
            check_method = getattr(page, check_method_name)
            
            if field_key == "duration":
                assert check_method(value), f"Поле '{field_key}' не содержит ожидаемого значения"
                
            elif field_key == "scooter_color":
                assert check_method(value), f"Цвет '{field_key}' не выбран"
         
            elif field_key == "order_date":
                
                allure.attach(
                    f"Ожидался день: {value}",
                    "Входные данные для проверки даты",
                    allure.attachment_type.TEXT
                )
               
                input_el = page.find_element(*OrderFormLocators.DATE_INPUT)
                actual_value = (input_el.get_attribute("value") or "").strip()
                    
                allure.attach(
                    f"Ожидался день: {value}\nПолучилось в поле: '{actual_value}'",
                    "Сравнение ожидаемого и фактического значения даты",
                    allure.attachment_type.TEXT
                )

                assert page.is_date_filled(), f"Поле даты осталось пустым. Фактическое значение: '{actual_value}'"

                
            else:
                assert check_method(), f"Поле '{field_key}' не заполнено"
        else:
            assert page.is_field_has_value(locator, value), f"Поле '{field_key}' не содержит ожидаемого значения"


@allure.feature("Самокат: атомарные проверки полей Формы 2")
@allure.story("Проверка полей Формы 2: точка входа — НИЖНЯЯ кнопка")
@pytest.mark.parametrize("field_key", FORM_2_FIELDS_CONFIG.keys(), ids=FORM_2_FIELDS_CONFIG.keys())
@allure.title("Поле '{field_key}' через НИЖНЮЮ кнопку")
def test_bottom_entry_point(prepared_order_flow, field_key):
    flow = prepared_order_flow
    main_page, page = flow["main"], flow["order"]
    cfg = ENTRY_POINTS["bottom"]

    _prepare_form_2(main_page, page, cfg)

    display_name, locator, fill_method_name, check_method_name = FORM_2_FIELDS_CONFIG[field_key]

    if field_key == "scooter_color":
        data_key = "scooter_color"
    elif field_key == "comment":
        data_key = "comments"
    else:
        data_key = field_key

    value = cfg["data"][data_key]  

    allure.attach(json.dumps(cfg["data"], ensure_ascii=False, indent=2), f"Данные (top)", allure.attachment_type.JSON)
    allure.attach(f"Поле: {display_name}\nЗначение: {value}", "Значение поля", allure.attachment_type.TEXT)

    with allure.step(f"Заполняем поле: {display_name}"):
        fill_method = getattr(page, fill_method_name)
        fill_method(value)

    with allure.step("Проверяем значение"):
        if check_method_name:
            check_method = getattr(page, check_method_name)
            
            if field_key == "duration":
                assert check_method(value), f"Поле '{field_key}' не содержит ожидаемого значения"
                
            elif field_key == "scooter_color":
                assert check_method(value), f"Цвет '{field_key}' не выбран"
                
            elif field_key == "order_date":
                
                allure.attach(
                    f"Ожидался день: {value}",
                    "Входные данные для проверки даты",
                    allure.attachment_type.TEXT
                )
               
                input_el = page.find_element(*OrderFormLocators.DATE_INPUT)
                actual_value = (input_el.get_attribute("value") or "").strip()
                    
                allure.attach(
                    f"Ожидался день: {value}\nПолучилось в поле: '{actual_value}'",
                    "Сравнение ожидаемого и фактического значения даты",
                    allure.attachment_type.TEXT
                )

                assert page.is_date_filled(), f"Поле даты осталось пустым. Фактическое значение: '{actual_value}'"

                
            else:
                assert check_method(), f"Поле '{field_key}' не заполнено"
        else:
            assert page.is_field_has_value(locator, value), f"Поле '{field_key}' не содержит ожидаемого значения"