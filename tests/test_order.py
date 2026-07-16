# tests/test_order.py
import time
import allure
from typing import Any
from pages.locators import OrderFormLocators

"""Разбил на 2 заполняемые формы (может лишнее) 
1я кнопка- 1я форма- 1е данные > 2я кнопка-1я форма- 2е данные > проверка появления 2й формы
{обьединяя формы  смотрелось как потеря - что и где} но тут же на каждое поле есть assert (лишний!?) 
оставлял один финальный появл. формы 2
но при выполнение работы помогали ососбенно при работе с календарем и списками
для заполнение 1формы перед тестом 2формы использовал фикстуру заполнения 1формы
и вынес навигацию 2шт(прозрачно!?) 2 кнопки через фикстру заполнения 2формы
использовал is_field_has_value в Base для проверки значений поля но не с кален., списки
"""

@allure.feature("Оформление заказа")
@allure.story("Сценарий заполнение от 1формы до подтверждения")
class TestOrderFlow:

    def test_form_1_fills_and_transitions_to_form_2(self,prepared_order_flow):
        flow = prepared_order_flow
        page_order: Any = flow["order"]
        data = flow["data"]

        # Подготовил в фикстурк

        # проверка по каждому полю) 
        with allure.step(f"Заполняю поле Имя : {data['name']}"):
            page_order.fill_name(data["name"])

        with allure.step("Проверяю поле Имя заполнено"):
            assert page_order.is_field_has_value(OrderFormLocators.INPUT_NAME, data["name"]), f"Поле Имя не заполнено '{data['name']}'"

        with allure.step(f"Заполняю поле Фамилия : {data['surname']}"):
            page_order.fill_surname(data["surname"])

        with allure.step("Проверяю поле Фамилия заполнено"):
            assert page_order.is_field_has_value(OrderFormLocators.INPUT_SURNAME, data["surname"]), f"Поле Фамилия не заполнено '{data['surname']}'"

        with allure.step(f"Заполняю поле Адрес : {data['address']}"):
            page_order.fill_address(data["address"])

        with allure.step("Проверяюполе Адрес заполнено"):
            assert page_order.is_field_has_value(OrderFormLocators.INPUT_ADDRESS, data["address"]), "Поле Адрес не заполнено"

        with allure.step(f"Заполняю поле Метро : {data['metro']}"):
            page_order.fill_metro(data["metro"])

        with allure.step("Проверяю Метро заполнено"):
            assert page_order.is_field_has_value(OrderFormLocators.INPUT_METRO_SEARCH, data["metro"]), " Метро не заполнено"

        with allure.step(f"Заполняю поле Телефон : {data['phone']}"):
            page_order.fill_phone(data["phone"])

        with allure.step("Проверяю поле Телефон Телефон"):
            assert page_order.is_field_has_value(OrderFormLocators.INPUT_PHONE, data["phone"]), "Поле Телефон не заполнено"

        # отправка формы
        with allure.step("Отправляю Форму 1кнопка Оформить"):
            page_order.submit_order()

        # Резул. теста первой формы
        with allure.step("Проверяю, что после отправки Формы 1 появилась Форма 2"):
            assert page_order.wait_for_form_2_ready(), "Форма 2 не появилась после отправки Формы 1"

#Только Форма 2

    def test_form_2_fills_and_confirms_order(self,prepared_form_2):
        flow = prepared_form_2
        page_order: Any = flow["order"]
        data = flow["data"]
        
        # форма 2 открыта
        #заполняю формы 2
        with allure.step(f"Устанавливаю дату заказа: {data['order_date']}"):
            page_order.fill_order_date_from_calendar(data["order_date"])

        with allure.step("дата заказа корректно установлена "):
            assert page_order.is_date_filled(), "Дата не установлена"

        with allure.step(f"Выбор срок аренды: {data['duration']}"):
            page_order.select_duration(data["duration"])

        with allure.step("Проверил срок аренды есть"):
            assert page_order.is_duration_selected(data["duration"]), "Не удалось выбрать срок"

        with allure.step(f"Выбираю цвет самоката: {data['scooter_color']}"):
            page_order.select_scooter_color(data["scooter_color"])

        with allure.step("Проверяю выбран цвет"):
            assert page_order.is_scooter_color_selected(data["scooter_color"]), f"Не удалось выбрать цвет '{data['scooter_color']}'"

        with allure.step(f"Заполняю поле комментарий значением: {data['comments']}"):
            page_order.fill_comment(data["comments"])

        with allure.step("Проверяю комментарий отображается "):
            assert page_order.is_field_has_value(OrderFormLocators.COMMENT_FIELD, data["comments"]), f"Комментарий не заполнен: '{data['comments']}'"

        # отпрвил форму2
        with allure.step("Клик на кнопку «Заказать» на форме 2"):
            page_order.click_order_button_2()

        with allure.step("жду появления окна с кнопкой «Да»"):
            page_order.wait_for_modal_with_confirm_button()

        # Подтверждение заказа 
        with allure.step("Подтверждаю заказ кнопкио «Да»"):
            page_order.confirm_order_yes()

        # результат теста 2 формы
        with allure.step("Проверяю появление окна «Заказ оформлен»"):
            assert page_order.is_order_success_visible(), "Модалки «Заказ оформлен» нет"

@allure.feature("Навигация")
@allure.story("Переходы по логотипам")
class TestNavigationFlow:

    def test_click_self_logo_leads_to_main_page(self,prepared_success_modal):
        flow = prepared_success_modal
        page = flow["order"]
        
        with allure.step("Клик на логотип «Самокат» в шапке"):
            page.click_logo()
            time.sleep(2)
        with allure.step("Преход на ГС (URL содержит 'scooter')"):
            assert page.is_url_contains("scooter"), "Ждал URL  'scooter'"
    

    def test_yandex_logo_opens_dzen(self,prepared_success_modal):
        flow = prepared_success_modal
        page = flow["order"]  

        with allure.step("Клик по логотипу Яндекса → переход на Дзен"):
            page.click_yandex_logo_and_wait_for_dzen()
            time.sleep(2)
        with allure.step("Проверяем, что мы на Дзене"):
            assert page.is_on_dzen(), "Ждал Дзен,  открыт  URL"
        
