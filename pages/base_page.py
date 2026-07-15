# pages/base_page.py
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from .locators import OrderFormLocators
from selenium.webdriver.common.action_chains import ActionChains

class BasePage:
    
    def __init__(self, driver, base_url: str = ""):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)
        self.actions = ActionChains(driver)

    # для открытия браузера в тесте
    def open(self, url: str = ""):
        target = url or self.base_url
        if not target:
            raise ValueError("URL нет")
        self.driver.get(target)

    # убрал cookie
    def close_cookie_banner(self):
        locator = OrderFormLocators.CONFIRM_BUTTON 
        btn = self.wait_for_element_clickable(locator)
        btn.click()

    # для чистки и ввода
    def fill_field(self, locator, value: str):
        element = self.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(value)
        return element
    
    # метод одного элемента
    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    #  метод для поиска элементов
    def find_elements(self, *locator):
        return self.driver.find_elements(*locator)

    # жду появление элементов    
    def wait_for_element_all_visible(self, locator, timeout=15):
        self.wait = WebDriverWait(self.driver, timeout)  
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    # жду на клик
    def wait_for_element_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator)) 
        
    #  для клика js
    def click_with_fallback(self, locator):
        
        element = self.wait_for_element_clickable(locator)

        try:
            # Обычный клик 
            element.click()
        except Exception:
            
            self.actions.move_to_element(element).click().perform()

    # жду видимость
    def wait_for_element_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    # для скрола
    def scroll_into_view(self, element, block="center", behavior="auto"):
        script = f"""arguments[0].scrollIntoView({{block: "{block}",behavior: "{behavior}"}});"""
        self.driver.execute_script(script, element)

       # для проверки заполнение поле 
    def is_field_has_value(self, locator, expected_value):
        
            field = self.wait_for_element_visible(locator)
            
            # для input или text 
            raw_actual = field.get_attribute("value") or field.text or ""
            
            actual = raw_actual.replace("\u00A0", " ").strip()
            expected = str(expected_value).replace("\u00A0", " ").strip()
            
            return actual == expected
    
    
    # для навигации
    # текущее окно
    def get_current_handle(self):
        return self.driver.current_window_handle

    def get_all_handles(self):
        return self.driver.window_handles

    #№ новая вкладка
    def switch_to_new_window(self, original_handle: str | None = None):
        if original_handle is None:
            original_handle = self.get_current_handle()

        all_handles = self.get_all_handles()
       
        new_handle = next(h for h in all_handles if h != original_handle)
        self.driver.switch_to.window(new_handle)

    #  URL 
    def wait_for_url_contains(self, substring: str, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.url_contains(substring))

    def is_url_contains(self, substring: str):
        return substring in self.driver.current_url
