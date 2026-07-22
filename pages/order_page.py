# pages/order_page.py
import allure
from .base_page import BasePage
from locators.main_page_locators import MainPageLocators
from locators.order_form_locators import OrderFormLocators


class OrderFormPage(BasePage):

    # тест на появление формы
    @allure.step("Ждём готовности Формы1")
    def wait_for_form_1_ready(self):
        self.wait_for_element_clickable(OrderFormLocators.FORM_HEADER_1)
        self.wait_for_element_clickable(OrderFormLocators.INPUT_NAME)
        return self
    
    # ввод поле ИМЯ
    @allure.step("Заполняем поле Имя: {name}")
    def fill_name(self, name: str):
        self.fill_field(OrderFormLocators.INPUT_NAME, name)
        
    #  ввод поле Фамилия
    @allure.step("Заполняем поле Фамилия: {surname}")
    def fill_surname(self, surname: str):
        self.fill_field(OrderFormLocators.INPUT_SURNAME, surname)
        
    #  ввод поле Адрес
    @allure.step("Заполняем поле Адрес: {address}")
    def fill_address(self, address: str):
        self.fill_field(OrderFormLocators.INPUT_ADDRESS, address)

    # ввод поля метро
    @allure.step("Заполняем поле Метро: {metro_name}")
    def fill_metro(self, metro_name: str):
        self.fill_field(OrderFormLocators.INPUT_METRO_SEARCH, metro_name)

        options = self.find_elements(*OrderFormLocators.METRO_OPTION)
        option = next((o for o in options if o.is_displayed()))

        if option:
            self.scroll_into_view(option)
            option.click()
        
    # ввод поля телефон
    @allure.step("Заполняем поле Телефон: {phone}")
    def fill_phone(self, phone: str):
        self.fill_field(OrderFormLocators.INPUT_PHONE, phone)


    @allure.step("Нажимаем кнопку Далее в Форме1")    
    def submit_order(self):
        btn = self.wait_for_element_clickable(OrderFormLocators.BUTTON_NEXT)
        self.click_with_fallback(btn)

#заполняет всю Форму 1
    @allure.step("Заполняем Форму1 полностью данными из словаря")
    def fill_form_1_full(self, data):
        self.fill_name(data["name"])
        self.fill_surname(data["surname"])
        self.fill_address(data["address"])
        self.fill_metro(data["metro"])
        self.fill_phone(data["phone"])



    @allure.step("Ждём готовности Формы2")
    def wait_for_form_2_ready(self):
        self.wait_for_element_clickable(OrderFormLocators.DATE_INPUT)
        self.wait_for_element_clickable(OrderFormLocators.DURATION_DROPDOWN)
        return self

    @allure.step("Выбираем дату заказа в календаре: день {day_number}")
    def fill_order_date_from_calendar(self, day_number: int):
        
        self.wait_for_element_clickable(OrderFormLocators.DATE_INPUT).click()

        days = self.wait_for_element_all_visible(OrderFormLocators.CALENDAR_DAY)

        target_day = next(
            (d for d in days
                if d.text.strip() == str(day_number)
                and "react-datepicker__day--outside-month" not in (d.get_attribute("class") or "")),None)

        self.wait_for_element_clickable(target_day).click()

    @allure.step("Проверяем, заполнено ли поле даты заказа")
    def is_date_filled(self):
        input_el = self.find_element(*OrderFormLocators.DATE_INPUT)
        value = input_el.get_attribute("value") or ""
        return bool(value and value.strip())

    @allure.step("Выбираем срок аренды: {expected_text}")
    def select_duration(self, expected_text: str):
        
        trigger = self.wait_for_element_clickable(OrderFormLocators.DURATION_TRIGGER)

        self.scroll_into_view(trigger)
        trigger.click()

        #  меню
        self.wait_for_element_clickable(OrderFormLocators.DURATION_MENU)

        options = self.find_elements(*OrderFormLocators.DURATION_OPTION)

        selected_option = None
        available_texts = []

        for opt in options:
            opt_text = opt.text.strip()
            if not opt_text:
                continue
            available_texts.append(opt_text)
            if opt_text.lower() == expected_text.lower() or expected_text.lower() in opt_text.lower():
                selected_option = opt
                break
        self.click_with_fallback(selected_option)
       
    @allure.step("Проверяем, выбрана ли срок аренды: {expected_text}")
    def is_duration_selected(self, expected_text: str):
        
        trigger = self.find_element(*OrderFormLocators.DURATION_DROPDOWN)
        actual_text = trigger.text.strip() or trigger.get_attribute("aria-label") or ""
        if expected_text.lower() in actual_text.lower():
                return True
        
     # для заполнения поля цвет
    @allure.step("Выбираем цвет самоката: {color}")
    def select_scooter_color(self, color: str):
        if color == "black":
            locator = OrderFormLocators.CHECKBOX_BLACK
        else:
            locator = OrderFormLocators.CHECKBOX_GREY
        
        checkbox = self.wait_for_element_clickable(locator)
        self.scroll_into_view(checkbox)
        self.click_with_fallback(checkbox)

    # для проверки заполнения поля цвет  
    @allure.step("Проверяем, выбран ли цвет самоката: {color}")
    def is_scooter_color_selected(self, color: str) -> bool:
       
        if color == "black":
            locator = OrderFormLocators.CHECKBOX_BLACK
        else:
            locator = OrderFormLocators.CHECKBOX_GREY
 
        checkbox = self.wait_for_element_clickable(locator) 
        
        return checkbox.is_selected()
        
    @allure.step("Заполняем поле Комментарий: {text}")
    def fill_comment(self, text: str):
        self.fill_field(OrderFormLocators.COMMENT_FIELD, text)
# 
    # клик заказать на второй форме
    @allure.step("Нажимаем кнопку Заказать на Форме2")
    def click_order_button_2(self):
        button = self.wait_for_element_clickable(OrderFormLocators.ORDER_BUTTON_IN_FORM_2)
        button.click()

#заполняет всю Форму 2
    @allure.step("Заполняем Форму2 полностью данными из словаря")
    def fill_form_2_full(self, data):
        self.fill_order_date_from_calendar(data["order_date"])
        self.select_duration(data["duration"])
        self.select_scooter_color(data["scooter_color"])
        self.fill_comment(data["comments"])

    @allure.step("Ждём появления модального окна с кнопкой ДА")
    def wait_for_modal_with_confirm_button(self):
        
        element = self.wait_for_element_clickable(OrderFormLocators.CONFIRM_BUTTON_YES_MODAL)
        return element 
        
    
    # подтверждение заказа  после второй формы 
    @allure.step("Подтверждаем заказ кнопкой Да")
    def confirm_order_yes(self):
        
        button = self.click_with_fallback(OrderFormLocators.CONFIRM_BUTTON_YES)
        return button


    # смотрю заголово окно
    @allure.step("Проверяем видимость сообщения об успешном оформлении заказа")
    def is_order_success_visible(self):
        el = self.wait_for_element_visible(OrderFormLocators.SUCCESS_MODAL_HEADER)
        return "Заказ оформлен" in el.text

    @allure.step("Нажимаем кнопку Посмотреть статус")
    def click_view_status(self):
        btn = self.wait_for_element_clickable(OrderFormLocators.VIEW_STATUS_BUTTON)
        btn.click()

    # переход на ГС
    @allure.step("Переходим на ГС через логотип Самоката")
    def click_logo(self):
        btn = self.wait_for_element_clickable(MainPageLocators.LOGO_LINK_SAMOKAT)
        btn.click()

    # яндекс через BasePage
    @allure.step("Кликаем логотип Яндекса и ждём открытия Дзена ")
    def click_yandex_logo_and_wait_for_dzen(self, timeout=10):
        btn = self.wait_for_element_clickable(MainPageLocators.LOGO_YANDEX_LINK)
        btn.click()

        original_handle = self.get_current_handle()

        #  на новую вкладку (через BasePage)
        self.switch_to_new_window(original_handle)

        # жду URL через BasePage
        self.wait_for_url_contains("dzen.ru", timeout)

    @allure.step("Проверяем, что находимся на Дзене")
    def is_on_dzen(self):
        return self.is_url_contains("dzen.ru")

   
