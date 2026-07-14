# tests/test_expand.py
import pytest
import allure
from pages.main_page import MainPage
from pages.data_main import EXPAND_TEXT

@allure.feature("FAQ: Аккордеон с вопросами")
@allure.story("Проверка раскрытия текстов вопросов аккордеона")
class TestAccordionQuestions:

    @allure.title("Проверка вопроса FAQ №{index}: {expected_text}")
    @pytest.mark.parametrize("index,expected_text", [
        (0, EXPAND_TEXT[0]),
        (1, EXPAND_TEXT[1]),
        (2, EXPAND_TEXT[2]),
        (3, EXPAND_TEXT[3]),
        (4, EXPAND_TEXT[4]),
        (5, EXPAND_TEXT[5]),
        (6, EXPAND_TEXT[6]),
        (7, EXPAND_TEXT[7]),
    ])
    def test_accordion_question(self, page: MainPage, index, expected_text):
        with allure.step(f"Открываем главную страницу"):
            page.open()

        with allure.step(f"Кликаем по заголовку вопроса №{index}"):
            page.click_accordion_header_by_index(index)

        with allure.step(f"Ожидаем и получаем текст панели №{index}"):
            actual_text = page.wait_for_text_by_index(index)

        with allure.step(f"Сравниваем полученный текст с ожидаемым"):
            assert actual_text == expected_text, (
                f"Текст не совпадает — ждал '{expected_text}', получил '{actual_text}'"
            )
