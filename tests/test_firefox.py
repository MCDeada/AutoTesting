import allure

from selenium.webdriver import Firefox

from src.constants import ConnectionConfig
from tests.BaseTests import BaseTests


class TestFirefox(BaseTests):
    def create_driver_and_connect(self):
        self.driver = Firefox()
        self.driver.get(ConnectionConfig.BASE_URL)

    @allure.story("Тест наличия картины «Трамвайный путь» в списке, Firefox")
    def test_does_tramway_painting_exist(self):
        super().does_tramway_painting_exist()

    @allure.story(
        "Тест, что стиль картины «Трамвайный путь» - «Реализм», Firefox"
    )
    def test_is_style_realism(self):
        super().is_style_realism()

    @allure.story("Тест сохранения картины в стиле «Батик» в избранное, Firefox")
    def test_favorite_add(self):
        super().favorite_add()

    @allure.story(
        "Тест наличия слова «Жираф» у первой картины "
        "в списке найденных по слову «Жираф», Firefox"
    )
    def test_is_giraffe_in_title(self):
        super().is_giraffe_in_title()

    @allure.story(
        "Тест соответствия цены первого изделия в разделе "
        "«Ювелирное искусство» и цены этого изделия в корзине, Firefox"
    )
    def test_check_ordering(self):
        super().check_ordering()
