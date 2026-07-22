# tests/test_order.py
import pytest
import allure
import json

from conftest import BASE_URL

@allure.feature("Оформление заказа")
@allure.story("Сценарий заполнения от Формы 1 до перехода к Форме 2")

class TestOrderFlow:

    @pytest.mark.parametrize(
    "entry_data_by_key",
    ["top", "bottom"],
    ids=["top_btn", "bottom_btn"],
    indirect=True,  
)
    @allure.title("Полный проход сценария: от Формы 1 до перехода к Форме 2 ({request.node.callspec.id})")
    def test_form_1_fills_and_transitions_to_form_2(self, entry_data_by_key, prepared_order_flow):
        data, button_location = entry_data_by_key  # данные уже готовы

        allure.attach(
            json.dumps(data, ensure_ascii=False, indent=2),
            f"Набор данных ({button_location})",
            allure.attachment_type.JSON
        )

        flow = prepared_order_flow
        main_page = flow["main"]
        page_order = flow["order"]

        with allure.step(f"Нажимаем кнопку «Заказать» ({button_location})"):
            main_page.click_order_button(button_location)

        with allure.step("Заполняем все поля Формы 1"):
            page_order.fill_form_1_full(data)

        with allure.step("Отправляем Форму 1"):
            page_order.submit_order()

        with allure.step("Проверяем, что появилась Форма 2"):
            assert page_order.wait_for_form_2_ready(), "Форма 2 не появилась после отправки Формы 1"


    @allure.feature("Оформление заказа")
    @allure.story("Полный позитивный сценарий заказа самоката")
    
    @pytest.mark.parametrize(
        "entry_data_by_key",
        ["top", "bottom"],
        ids=["top_btn", "bottom_btn"],
        indirect=True,
    )
    @allure.title("Полный проход сценария: Форма 2 и подтверждение заказа ({request.node.callspec.id})")
    def test_form_2_fills_and_confirms_order(self, entry_data_by_key, prepared_order_flow, request):
        data, button_location = entry_data_by_key

        allure.attach(
                    json.dumps(data, ensure_ascii=False, indent=2),
                    f"Набор данных ({button_location})",
                    allure.attachment_type.JSON
                )

        flow = prepared_order_flow
        main_page = flow["main"]
        page_order = flow["order"]

        # Переход к Форме 2 
        with allure.step(f"Старт сценария через кнопку: {button_location}"):
            main_page.click_order_button(button_location)

        with allure.step("Заполняем все поля Формы 1"):
            page_order.fill_form_1_full(data)

        with allure.step("Отправляем Форму 1 кнопкой «Оформить заказ»"):
            page_order.submit_order()

            #  с Формы 1 на Форму 2
        with allure.step("Проверяем, что появилась Форма 2"):
            assert page_order.wait_for_form_2_ready(), "Форма 2 не появилась после отправки Формы 1"

        # Заполнение Формы 2 
            
        with allure.step(f"Указываем дату заказа:{data['order_date']} день"):
            page_order.fill_order_date_from_calendar(data["order_date"])

        with allure.step(f"Указываем срок аренды:{data['duration']} "):
            page_order.select_duration(data["duration"])

        with allure.step(f"Указываем цвет:{data['scooter_color']} "):
            page_order.select_scooter_color(data["scooter_color"])

        with allure.step(f"Заполняю комментарии:{data['comments']} "):
            page_order.fill_comment(data["comments"])

        # Подтверждение заказа
        with allure.step("Подтверждаем заказ отправка формы 2"):
            page_order.click_order_button_2()

        with allure.step("Ждём появления модалки «Хотите оформить заказ?» с кнопкой «Да»"):
            modal_button = page_order.wait_for_modal_with_confirm_button()  # Получаем элемент
            
            allure.attach(
                f"Модалка найдена. Кнопка «Да» готова к клику. Текст кнопки: '{modal_button.text}'",
                "Статус модалки подтверждения",
                allure.attachment_type.TEXT
            )
        with allure.step("Подтверждаем заказ кнопкой ДА"):
            page_order.confirm_order_yes()
            




       
        
        # проверка 
        with allure.step("Проверяем появление окна «Заказ оформлен»"):
            assert page_order.is_order_success_visible(), "Модалка «Заказ оформлен» не появилась"

@allure.feature("Навигация")
@allure.story("Переходы по логотипам")
@pytest.mark.parametrize("entry_data_by_key", ["top", "bottom"], indirect=True, ids=["top_btn", "bottom_btn"])
class TestNavigationFlow:

    @allure.title("Клик по логотипу «Самокат» - переход на главную ")
    def test_click_self_logo_leads_to_main_page(self, flow_with_success_modal, entry_data_by_key):
        flow = flow_with_success_modal
        page = flow["order"]

        data, button_location = entry_data_by_key
        allure.attach(json.dumps(data, ensure_ascii=False, indent=2), f"Данные заказа (кнопка: {button_location})", allure.attachment_type.JSON)

        with allure.step("Переходим к просмотру статуса заказа"):
            page.click_view_status()

        with allure.step("Кликаем логотип «Самокат»"):
            page.click_logo()
            
        with allure.step("Проверяем переход на главную страницу"):
            current_url = page.driver.current_url
           
            assert current_url == BASE_URL or current_url.startswith(BASE_URL), \
                f"Ожидался URL главной ({BASE_URL}), но получили: {current_url}"
            
    @allure.title("Клик по логотипу Яндекса - переход на Дзен ")
    def test_yandex_logo_opens_dzen(self, flow_with_success_modal, entry_data_by_key):
        flow = flow_with_success_modal
        page = flow["order"]

        data, button_location = entry_data_by_key
        allure.attach(json.dumps(data, ensure_ascii=False, indent=2), f"Данные заказа (кнопка: {button_location})", allure.attachment_type.JSON)

        with allure.step("Переходим к просмотру статуса заказа"):
            page.click_view_status()

        with allure.step("Клик по логотипу Яндекса (переход на Дзен)"):
            page.click_yandex_logo_and_wait_for_dzen()
          
        with allure.step("Проверяем, что мы на Дзене"):
            page.wait_for_url_contains("dzen.ru")
            assert page.is_on_dzen(), "Ожидался Дзен, но URL не соответствует"

