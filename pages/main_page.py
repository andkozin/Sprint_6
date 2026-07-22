# pages/main_page.py
import allure
from selenium.webdriver.common.by import By
from .base_page import BasePage
from locators.main_page_locators import MainPageLocators

class MainPage(BasePage):

    # собрал по индексу
    
    @staticmethod
    @allure.step("Получаем локатор панели по индексу {index}")
    def _get_panel_locator(index: int):
        panel_id = MainPageLocators.PANEL_INDEX.format(index)
        return By.ID, panel_id

    # "top" или "bottom"
    @allure.step("Кликаем кнопку заказа: расположение = {location}")
    def click_order_button(self, location: str):
            
            if location == "top":
                locator = MainPageLocators.ORDER_BUTTON_TOP
            else: 
                locator = MainPageLocators.ORDER_FINISH_BUTTON
            
            self.click_with_fallback(locator)

    @allure.step("Кликаем заголовок аккордеона по индексу: {index}")
    def click_accordion_header_by_index(self, index: int)-> None:
        self.close_cookie_banner()

        headers = self.wait_for_element_all_visible(MainPageLocators.ACCORDION_HEADERS)
        
        if not 0 <= index < len(headers):
            raise IndexError(f"Индекс {index}  Всего: {len(headers)}")

        header = headers[index]

        self.scroll_into_view(header)
        self.click_with_fallback(header)

    @allure.step("Ждём и получаем текст панели по индексу: {index}")
    def wait_for_text_by_index(self, index: int): #str
        panel_loc = self._get_panel_locator(index) # взял по индексу
        panel = self.wait_for_element_visible(panel_loc) # ghjdthbk
        return panel.text.strip()
