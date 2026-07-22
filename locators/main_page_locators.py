# locators/main_locators.py

from selenium.webdriver.common.by import By

class MainPageLocators:

    ACCORDION_HEADERS = (By.CSS_SELECTOR, "[data-accordion-component='AccordionItemButton']") # для списка заголовок
    PANEL_INDEX = "accordion__panel-{}" # для индекст заголовка

    ORDER_BUTTON_TOP = (By.XPATH, "//div[contains(@class,'Header_Nav')]//button[.='Заказать']") # кнопка заказать в шапке
    ORDER_FINISH_BUTTON = (By.XPATH, "//div[contains(@class,'Home_FinishButton')]//button[.='Заказать']") # кнопка заказать внизу

    LOGO_LINK_SAMOKAT = (By.CSS_SELECTOR, 'a[class*="Header_LogoScooter"]') # лого Самоката на ГС
    LOGO_YANDEX_LINK = (By.CSS_SELECTOR, 'a[class*="Header_LogoYandex"]') # лого Яндекса