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
    def close_cookie_banner(self, timeout: int | None = None):
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
    def wait_for_element_clickable(self, locator, timeout=15):
        return self.wait.until(EC.element_to_be_clickable(locator),
            message=f"Элемент {locator} не стал клик.  за {timeout} сек.")
        
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
