# pages/base_page.py
import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from locators.order_form_locators import OrderFormLocators

from selenium.webdriver.common.action_chains import ActionChains

class BasePage:
    
    def __init__(self, driver, base_url: str = ""):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)
        self.actions = ActionChains(driver)

    # для открытия браузера в тесте
    @allure.step("Открываем страницу по URL")
    def open(self, url: str = ""):
        target = url or self.base_url
        if not target:
            raise ValueError("URL нет")
        self.driver.get(target)

    # убрал cookie
    @allure.step("Закрываем баннер с куки")
    def close_cookie_banner(self):
        locator = OrderFormLocators.CONFIRM_BUTTON 
        btn = self.wait_for_element_clickable(locator)
        btn.click()

    # для чистки и ввода
    @allure.step("Заполняем поле  значением: {value}")
    def fill_field(self, locator, value: str):
        element = self.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(value)
        return element
    
    # метод одного элемента 
    @allure.step("Находим один элемент")
    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    #  метод для поиска элементов
    @allure.step("Находим несколько элементов:")
    def find_elements(self, *locator):
        return self.driver.find_elements(*locator)

    # жду появление элементов    
    @allure.step("Ждём, что ВСЕ элементы {locator} видны (таймаут: {timeout} сек)") # выводит в отчет локатора путь наверно можно через имена 
    def wait_for_element_all_visible(self, locator, timeout=15):
        self.wait = WebDriverWait(self.driver, timeout)  
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    # жду на клик
    @allure.step("Ждём, что элемент {locator} кликабелен")
    def wait_for_element_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator)) 
        
    #  для клика js
    @allure.step("Кликаем по элементу {locator} - fallback ")
    def click_with_fallback(self, locator):
        
        element = self.wait_for_element_clickable(locator)

        try:
            # Обычный клик 
            element.click()
        except Exception:
            
            self.actions.move_to_element(element).click().perform()

    # жду видимость
    @allure.step("Ждём, что элемент {locator} виден") 
    def wait_for_element_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    # для скрола
    @allure.step("Скроллим к элементу")
    def scroll_into_view(self, element, block="center", behavior="auto"):
        script = f"""arguments[0].scrollIntoView({{block: "{block}",behavior: "{behavior}"}});"""
        self.driver.execute_script(script, element)

       # для проверки заполнение поле 

       # pages/order_form_page.py
    @allure.step("Проверяем, что в поле {locator} значение совпадает с ожидаемым: '{expected_value}'")
    def is_field_has_value(self, locator, expected_value):
        field = self.wait_for_element_visible(locator)
        
        raw_actual = field.get_attribute("value") or field.text or ""
        actual = raw_actual.replace("\u00A0", " ").strip()
        expected = str(expected_value).replace("\u00A0", " ").strip()

        if actual != expected:
           
            raise AssertionError(
                f"\n НЕСОВПАДЕНИЕ В is_field_has_value\n"
                f"Ожидалось: '{expected}'\n"
                f"Получено:   '{actual}'"
            )
    
        return True

    
    
    # для навигации
    # текущее окно
    @allure.step("Получаем текущий значение окна")
    def get_current_handle(self):
        return self.driver.current_window_handle

    @allure.step("Получаем все значения  окон")
    def get_all_handles(self):
        return self.driver.window_handles

    #№ новая вкладка
    @allure.step("Переключаемся на новое окно (исходный : {original_handle})")
    def switch_to_new_window(self, original_handle: str | None = None):
        if original_handle is None:
            original_handle = self.get_current_handle()

        all_handles = self.get_all_handles()
       
        new_handle = next(h for h in all_handles if h != original_handle)
        self.driver.switch_to.window(new_handle)

    #  URL 
    @allure.step("Ждём, что URL содержит подстроку: '{substring}' (таймаут: {timeout} сек)")
    def wait_for_url_contains(self, substring: str, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.url_contains(substring))

    @allure.step("Проверяем, что URL содержит подстроку: '{substring}'")
    def is_url_contains(self, substring: str):
        return substring in self.driver.current_url
