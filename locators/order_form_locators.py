# locators/order_locators.py

from selenium.webdriver.common.by import By

class OrderFormLocators:

    CONFIRM_BUTTON = (By.ID, "rcc-confirm-button") # для баннера cookie

    FORM_HEADER_1 = (By.XPATH, "//div[contains(text(), 'Для кого самокат')]") #для формы заполнения 1 (имя) Для кого самокат

    # Поля первого шага
    INPUT_NAME = (By.XPATH, "//input[contains(@placeholder, 'Имя')]") # поле Имя
    INPUT_SURNAME = (By.XPATH, "//input[contains(@placeholder, 'Фамилия')]") # поле Фамилия
    INPUT_ADDRESS = (By.XPATH, "//input[contains(@placeholder, 'Адрес: куда привезти заказ')]") # поле Адрес
    INPUT_PHONE = (By.XPATH, "//input[contains(@placeholder, 'Телефон: на него позвонит курьер')]") # поле Телефон

    # Метро
    INPUT_METRO_SEARCH = (By.CSS_SELECTOR, "input.select-search__input") # поле Метро
    METRO_OPTION = (By.CSS_SELECTOR, ".select-search__option") #  для опции метро
    
    BUTTON_NEXT = (By.XPATH, "//button[normalize-space()='Далее']") # копка Далее в первой форме ввода
    
    # Дата и календарь
    DATE_INPUT = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']") # поле выбора дата
    CALENDAR_DAY = (By.CSS_SELECTOR, ".react-datepicker__day:not(.react-datepicker__day--outside-month)") # раскрыть календарь

    #  срока аренды
    DURATION_TRIGGER = (By.CSS_SELECTOR, ".Dropdown-control[aria-haspopup='listbox']") # Триггер (область, по которой кликаем, чтобы открыть список)
    DURATION_MENU    = (By.CSS_SELECTOR, ".Dropdown-menu[aria-expanded='true']") # Меню (список опций)
    DURATION_OPTION  = (By.CSS_SELECTOR, ".Dropdown-option[role='option']") # Опции внутри меню

    DURATION_DROPDOWN = (By.CSS_SELECTOR, "div.Dropdown-root div.Dropdown-control[aria-haspopup='listbox']") # срок аренды про поле для проверок

    # Чекбоксы цвета
    CHECKBOX_BLACK = (By.ID, "black") # чек бокс черный
    CHECKBOX_GREY = (By.ID, "grey") # чек бокс серый

    COMMENT_FIELD = (By.CSS_SELECTOR, 'input[placeholder="Комментарий для курьера"]') # поле комментарий

    ORDER_BUTTON_IN_FORM_2 = (By.XPATH, '//div[contains(@class, "Order_Buttons")]//button[normalize-space()="Заказать"]') # кнопка заказать 2 формы ввода
    
    CONFIRM_BUTTON_YES_MODAL = (By.XPATH, "//*[contains(text(), 'Хотите оформить заказ?')]")
    
    
    CONFIRM_BUTTON_YES=(By.XPATH, "//button[normalize-space()='Да']")
    

    SUCCESS_MODAL_HEADER = (By.XPATH, '//div[contains(@class, "Order_Modal")]//div[contains(@class, "Order_ModalHeader")]') # окно создания заказа
    

    VIEW_STATUS_BUTTON = (By.XPATH, '//div[contains(@class, "Order_NextButton")]//button[normalize-space()="Посмотреть статус"]') # кнопка для статуса заказа