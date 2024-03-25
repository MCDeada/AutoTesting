from enum import Enum


class Errors(Enum):
    PAINTING_NOT_FOUND = "Картина «Трамвайный путь» не найдена"
    WRONG_STYLE = "Стиль картины «Трамвайный путь» - не реализм"
    FAVORITE_PAINTING_ADD_ERROR = ("Первая картина выполненная с помощью "
                                   "«Батик» не попала в «Избранное»")
    NO_SUCH_TITLE = "Название первой картины не содержит желаемого слова"
    PRICES_MISSMATCH = "Цена при добавлении в корзину и в корзине не совпадают"


class ConnectionConfig:
    BASE_URL: str = "https://artnow.ru/"


class SelectorTypes:
    XPATH = "XPATH"
    CSS_SELECTOR = "CSS_SELECTOR"


class ActionTypes:
    TEXT = "TEXT"
    ATTRIBUTE = "ATTRIBUTE"
    ELEMENT = "ELEMENT"
    CLICK = "CLICK"
