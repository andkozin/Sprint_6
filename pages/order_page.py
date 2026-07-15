# pages/order_page.py

from .base_page import BasePage
from .locators import OrderFormLocators 

class OrderFormPage(BasePage):

    # тест на появление формы
    def wait_for_form_1_ready(self):
        self.wait_for_element_clickable(OrderFormLocators.FORM_HEADER_1)
        self.wait_for_element_clickable(OrderFormLocators.INPUT_NAME)
        return self
    
    # ввод поле ИМЯ
    def fill_name(self, name: str):
        self.fill_field(OrderFormLocators.INPUT_NAME, name)
        
    #  ввод поле Фамилия
    def fill_surname(self, surname: str):
        self.fill_field(OrderFormLocators.INPUT_SURNAME, surname)
        
    #  ввод поле Адрес
    def fill_address(self, address: str):
        self.fill_field(OrderFormLocators.INPUT_ADDRESS, address)

    # ввод поля метро
    def fill_metro(self, metro_name: str):
        self.fill_field(OrderFormLocators.INPUT_METRO_SEARCH, metro_name)

        options = self.find_elements(*OrderFormLocators.METRO_OPTION)
        option = next((o for o in options if o.is_displayed()))

        if option:
            self.scroll_into_view(option)
            option.click()
        
    # ввод поля телефон
    def fill_phone(self, phone: str):
        self.fill_field(OrderFormLocators.INPUT_PHONE, phone)
        
    def submit_order(self):
        btn = self.wait_for_element_clickable(OrderFormLocators.BUTTON_NEXT)
        self.click_with_fallback(btn)

    def wait_for_form_2_ready(self):
        self.wait_for_element_clickable(OrderFormLocators.DATE_INPUT)
        self.wait_for_element_clickable(OrderFormLocators.DURATION_DROPDOWN)
        return self

    def fill_order_date_from_calendar(self, day_number: int):
        
        self.wait_for_element_clickable(OrderFormLocators.DATE_INPUT).click()

        days = self.wait_for_element_all_visible(OrderFormLocators.CALENDAR_DAY)

        target_day = next(
            (d for d in days
                if d.text.strip() == str(day_number)
                and "react-datepicker__day--outside-month" not in (d.get_attribute("class") or "")),None)

        self.wait_for_element_clickable(target_day).click()

    def is_date_filled(self):
        input_el = self.find_element(*OrderFormLocators.DATE_INPUT)
        value = input_el.get_attribute("value")
        return bool(value and value.strip())

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
       
    def is_duration_selected(self, expected_text: str):
        
        trigger = self.find_element(*OrderFormLocators.DURATION_DROPDOWN)
        actual_text = trigger.text.strip() or trigger.get_attribute("aria-label") or ""
        if expected_text.lower() in actual_text.lower():
                return True
     # для заполнения поля цвет
    def select_scooter_color(self, color: str):
        if color == "black":
            locator = OrderFormLocators.CHECKBOX_BLACK
        else:
            locator = OrderFormLocators.CHECKBOX_GREY
        
        checkbox = self.wait_for_element_clickable(locator)
        self.scroll_into_view(checkbox)
        self.click_with_fallback(checkbox)

    # для проверки заполнения поля цвет  
    def is_scooter_color_selected(self, color: str) -> bool:
       
        if color == "black":
            locator = OrderFormLocators.CHECKBOX_BLACK
        else:
            locator = OrderFormLocators.CHECKBOX_GREY
 
        checkbox = self.wait_for_element_clickable(locator) # можно через атрибутcheckbox = checkbox.get_attribute("checked")
        
        return checkbox.is_selected()
        
    def fill_comment(self, text: str):
        self.fill_field(OrderFormLocators.COMMENT_FIELD, text)
# 
    # клик заказать на второй форме
    def click_order_button_2(self):
        button = self.wait_for_element_clickable(OrderFormLocators.ORDER_BUTTON_IN_FORM_2)
        button.click()

    def wait_for_modal_with_confirm_button(self):
        self.wait_for_element_clickable(OrderFormLocators.CONFIRM_BUTTON_YES)

    # подтверждение заказа  после второй формы 
    def confirm_order_yes(self):
        button = self.wait_for_element_clickable(OrderFormLocators.CONFIRM_BUTTON_YES)
        button.click()

    # смотрю заголово окно
    def is_order_success_visible(self):
        el = self.wait_for_element_visible(OrderFormLocators.SUCCESS_MODAL_HEADER)
        return "Заказ оформлен" in el.text

    def click_view_status(self):
        btn = self.wait_for_element_clickable(OrderFormLocators.VIEW_STATUS_BUTTON)
        btn.click()

    # переход на ГС
    def click_logo(self):
        btn = self.wait_for_element_clickable(OrderFormLocators.LOGO_LINK_SAMOKAT)
        btn.click()

    # яндекс через BasePage
    def click_yandex_logo_and_wait_for_dzen(self, timeout=10):
        btn = self.wait_for_element_clickable(OrderFormLocators.LOGO_YANDEX_LINK)
        btn.click()

        original_handle = self.get_current_handle()

        #  на новую вкладку (через BasePage)
        self.switch_to_new_window(original_handle)

        # жду URL через BasePage
        self.wait_for_url_contains("dzen.ru", timeout)

    def is_on_dzen(self):
        return self.is_url_contains("dzen.ru")

   
