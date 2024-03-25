from time import sleep
from typing import Optional, Union
import allure
from allure_commons.types import AttachmentType

from selenium.webdriver import Chrome, Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from src.constants import Errors, ConnectionConfig, SelectorTypes, ActionTypes


class BaseTests:
    def create_driver_and_connect(self):
        self.driver = Chrome()
        self.driver.get(ConnectionConfig.BASE_URL)

    def close_driver(self):
        if self.driver:
            self.driver.close()
            self.driver.quit()

    def catch_error(self, error_name: str):
        with allure.step(error_name):
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="error",
                attachment_type=AttachmentType.PNG
            )
            self.close_driver()

    def get_element(self, selector_type: SelectorTypes, path: str) -> WebElement:
        if selector_type == SelectorTypes.CSS_SELECTOR:
            return self.driver.find_element(By.CSS_SELECTOR, path)
        elif selector_type == SelectorTypes.XPATH:
            return self.driver.find_element(By.XPATH, path)

    def allure_step(
        self,
        step_name: str,
        selector_type: SelectorTypes,
        path: str,
        action_type: ActionTypes,
        error_message: str,
        attribute: str = None
    ) -> Optional[Union[WebElement, str]]:
        """
        Проводит действие с использованием репортинга allure
        :param step_name: Наименование шага allure
        :param selector_type: Тип селектора для получения веб элемента
        :param path: Путь, по которому находится элемент
        :param action_type: Что нужно сделать с найденным элементом
        :param error_message: Сообщение об ошибке в случае не найденного элемента
        :param attribute: Если действие получить атрибут, то тут его имя
        :return:
        """
        with allure.step(step_name):
            try:
                element = self.get_element(selector_type, path)
                if action_type == ActionTypes.CLICK:
                    element.click()
                    return
                elif action_type == ActionTypes.ELEMENT:
                    return element
                elif action_type == ActionTypes.ATTRIBUTE and attribute:
                    return element.get_attribute(attribute)
                elif action_type == ActionTypes.TEXT:
                    return element.text
            except NoSuchElementException:
                self.catch_error(error_message)

    def allure_step_connection(self):
        with allure.step("Создание драйвера и переход на сайт"):
            try:
                self.create_driver_and_connect()
            except Exception:
                self.catch_error("Ошибка при открытии сайта")

    def cityscape_path_actions(self):
        self.allure_step(
            "Выбор пункта «Показать еще» в боковом меню",
            SelectorTypes.CSS_SELECTOR,
            '.menu-group.gids > div >span',
            ActionTypes.CLICK,
            "Ошибка при выборе пункта «Показать еще» в боковом меню"
        )

        self.allure_step(
            "Выбор пункта «Вышитые картины» в боковом меню",
            SelectorTypes.XPATH,
            '//a[text()=" Вышитые картины"]',
            ActionTypes.CLICK,
            "Ошибка при выборе пункта «Вышитые картины» в боковом меню"
        )

        self.allure_step(
            "Выбор жанра «Городской пейзаж»",
            SelectorTypes.CSS_SELECTOR,
            '#genre257',
            ActionTypes.CLICK,
            "Ошибка при выборе жанра «Городской пейзаж»"
        )

        self.allure_step(
            "Выбор кнопки для применения фильтрации",
            SelectorTypes.CSS_SELECTOR,
            '.a_button',
            ActionTypes.CLICK,
            "Ошибка при выборе кнопки для применения фильтрации"
        )
        sleep(1)  # Время на открытие новой страницы

    @allure.story("Тест наличия картины «Трамвайный путь» в списке, Chrome")
    def does_tramway_painting_exist(self):
        self.allure_step_connection()

        self.cityscape_path_actions()

        element_desc = self.allure_step(
            "Поиск элемента с картиной «Трамвайный путь»",
            SelectorTypes.XPATH,
            '//*[@alt="Трамвайный путь. Гвоздецкая Татьяна"]',
            ActionTypes.ATTRIBUTE,
            "Ошибка картины «Трамвайный путь» нет на странице",
            "alt"
        )

        is_found = True if element_desc else False
        assert is_found, Errors.PAINTING_NOT_FOUND.value
        # assert False, True
        self.close_driver()

    @allure.story(
        "Тест, что стиль картины «Трамвайный путь» - «Реализм», Chrome"
    )
    def is_style_realism(self):
        self.allure_step_connection()

        self.cityscape_path_actions()

        self.allure_step(
            "Поиск элемента с картиной «Трамвайный путь»",
            SelectorTypes.XPATH,
            '//*[@alt="Трамвайный путь. Гвоздецкая Татьяна"]',
            ActionTypes.CLICK,
            "Ошибка картины «Трамвайный путь» нет на странице"
        )

        painting_style = self.allure_step(
            "Получение информации о стиле картины «Трамвайный путь»",
            SelectorTypes.XPATH,
            '//*[text()="Стиль: "]/../a',
            ActionTypes.TEXT,
            "Ошибка при получении стиля картины «Трамвайный путь»"
        )

        assert painting_style == 'Реализм', Errors.WRONG_STYLE.value
        self.close_driver()

    @allure.story("Тест сохранения картины в стиле «Батик» в избранное, Chrome")
    def favorite_add(self):
        self.allure_step_connection()

        self.allure_step(
            "Выбор пункта «Показать еще» в боковом меню",
            SelectorTypes.CSS_SELECTOR,
            '.menu-group.gids > div >span',
            ActionTypes.CLICK,
            "Ошибка при выборе пункта «Показать еще» в боковом меню"
        )

        self.allure_step(
            "Выбор стиля «Батик» в боковом меню",
            SelectorTypes.XPATH,
            '//a[text()=" Батик"]',
            ActionTypes.CLICK,
            "Ошибка при выборе стиля «Батик» в боковом меню"
        )

        self.allure_step(
            "Добавление первой картины в стиле «Батик» в избранное",
            SelectorTypes.XPATH,
            '//*[@class="post"]/div[@class="heart"]',
            ActionTypes.CLICK,
            "Ошибка при добавлении первой картины в стиле «Батик» в избранное"
        )

        self.allure_step(
            "Добавление второй картины в стиле «Батик» в избранное",
            SelectorTypes.XPATH,
            '//*[@class="post"][2]/div[@class="heart"]',
            ActionTypes.CLICK,
            "Ошибка при добавлении второй картины в стиле «Батик» в избранное"
        )

        self.allure_step(
            "Добавление третьей картины в стиле «Батик» в избранное",
            SelectorTypes.XPATH,
            '//*[@class="post"][3]/div[@class="heart"]',
            ActionTypes.CLICK,
            "Ошибка при добавлении третьей картины в стиле «Батик» в избранное"
        )

        first_painting_title = self.allure_step(
            "Получение заголовка первой картины в стиле «Батик»",
            SelectorTypes.XPATH,
            '//*[@class="post"]/a/img',
            ActionTypes.ATTRIBUTE,
            "Ошибка при получении заголовка первой картины в стиле «Батик»",
            "alt"
        )

        self.allure_step(
            "Переход в избранное",
            SelectorTypes.XPATH,
            '//*[@alt="Избранное"]',
            ActionTypes.CLICK,
            "Ошибка при переходе в избранное"
        )
        sleep(1)

        # BROKEN
        # elem = self.allure_step(
        #     "Получение числа картин в избранном",
        #     SelectorTypes.XPATH,
        #     "//*[@id='sa_container']/div[@class='post']",
        #     ActionTypes.ELEMENT,
        #     "Ошибка при получении числа картин в избранном"
        # )
        # favorite_count = len(elem)
        with allure.step("Получение числа картин в избранном"):
            try:
                favorite_count = len(
                    self.driver.find_elements(
                        By.XPATH,
                        "//*[@id='sa_container']/div[@class='post']"
                    )
                )
            except NoSuchElementException:
                self.catch_error(
                    "Ошибка при получении числа картин в избранном"
                )

        with allure.step("Поиск целевой картины в избранном"):
            target_painting_added = False
            for i in range(favorite_count):
                try:
                    painting_title = self.driver.find_element(
                        By.XPATH,
                        f'//*[@id="sa_container"]/div[{i + 2}]/a/img'
                    ).get_attribute("alt")
                except Exception:
                    self.catch_error(
                        "Ошибка при получении имени картины в избранном"
                    )
                if painting_title in first_painting_title:
                    target_painting_added = True
                    break

        assert target_painting_added, Errors.FAVORITE_PAINTING_ADD_ERROR.value
        self.close_driver()

    @allure.story(
        "Тест наличия слова «Жираф» у первой картины "
        "в списке найденных по слову «Жираф», Chrome"
    )
    def is_giraffe_in_title(self):
        self.allure_step_connection()

        title_to_find = 'Жираф'
        input_element = self.allure_step(
            "Поиск в поисковой строке по слову «Жираф»",
            SelectorTypes.XPATH,
            '//input[@name="qs"]',
            ActionTypes.ELEMENT,
            "Ошибка элемент поисковой строки не найден"
        )
        input_element.send_keys(title_to_find)
        input_element.send_keys(Keys.ENTER)
        sleep(1)

        first_painting_title = self.allure_step(
            "Проверка что первая найденная картина содежит слово «Жираф» в названии",
            SelectorTypes.XPATH,
            '//*[@class="post"]/a/img',
            ActionTypes.ATTRIBUTE,
            "Ошибка картина не найдена",
            "alt"
        )

        assert title_to_find in first_painting_title, Errors.NO_SUCH_TITLE.value
        self.close_driver()

    @allure.story(
        "Тест соответствия цены первого изделия в разделе "
        "«Ювелирное искусство» и цены этого изделия в корзине, Chrome"
    )
    def check_ordering(self):
        self.allure_step_connection()

        self.allure_step(
            "Выбор пункта «Показать еще» в боковом меню",
            SelectorTypes.CSS_SELECTOR,
            '.menu-group.gids > div >span',
            ActionTypes.CLICK,
            "Ошибка при выборе пункта «Показать еще» в боковом меню"
        )

        self.allure_step(
            "Выбор пункта «Ювелирное искусство» в боковом меню",
            SelectorTypes.XPATH,
            '//a[text()=" Ювелирное искусство"]',
            ActionTypes.CLICK,
            "Ошибка при выборе пункта «Ювелирное искусство» в боковом меню"
        )

        first_element_buy_path = '//*[@id="CartButton1127052"]'
        first_element_price = self.allure_step(
            "Получение цены первого изделия в разделе «Ювелирное искусство»",
            SelectorTypes.XPATH,
            f'{first_element_buy_path}/../../div[@class="price"]',
            ActionTypes.TEXT,
            "Ошибка при получении цены первого изделия в разделе «Ювелирное искусство»"
        )

        self.allure_step(
            "Добавление первого изделия в разделе «Ювелирное искусство» в корзину",
            SelectorTypes.XPATH,
            first_element_buy_path,
            ActionTypes.CLICK,
            "Ошибка при добавлении первого изделия в разделе «Ювелирное искусство» в корзину"
        )

        self.allure_step(
            "Нажатие на всплывающую кнопку перехода в корзину",
            SelectorTypes.XPATH,
            '//*[@class="ok-button"]',
            ActionTypes.CLICK,
            "Ошибка при нажатии на всплывающую кнопку перехода в корзину"
        )
        sleep(1)  # Ждем пока прогрузится корзина

        price_when_buy = self.allure_step(
            "Получение цены товара в корзине",
            SelectorTypes.XPATH,
            '//*[@class="shop"]/div[@class="price"]',
            ActionTypes.TEXT,
            "Ошибка при получении цены товара в корзине"
        )

        assert price_when_buy == first_element_price, Errors.PRICES_MISSMATCH.value
        self.close_driver()