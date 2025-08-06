from copy import deepcopy
from enum import Enum
from typing import Self

from fastapi import HTTPException


class Error(Enum):
    """Перечисление ошибок с поддержкой неизменяемости, add_info и up_raise."""
    # Предопределённые ошибки
    NO_ERROR = (0, "", 200)  # Код, сообщение, HTTP-код
    ER_NOT_ITEM = (1, "Нет объекта в БД", 404)
    ER_SERVER = (4, "Ошибка сервера", 400)
    ER_DUPLICATE_CREATE_ATTEMPT = (11, "В базе данных уже объект с таким id - возможно повторный запрос. Пропускаем", 200)
    ERROR = (15, "Ошибка: ", 400)

    ER_NOT_BUILDING = (16, "Пользователь не входит в состав участников встречи", 403)
    ER_NOT_ACTIVITY = (16, "Summary не найдено", 404)
    ER_NOT_ORGANIZATION = (16, "MeetingFile не найдено", 404)
    ER_NOT_ORGANIZATION_PHONE = (16, "Задача не найдена", 404)
    ER_NOT_ORGANIZATION_ACTIVITY = (16, "Встреча не найдена", 404)
    NOT_ER = (0, "", 200)

    def __init__(self, code: int, msg: str, http_code: int):
        super().__setattr__('_code', code)
        super().__setattr__('_msg', msg)
        super().__setattr__('_http_code', http_code)
        super().__setattr__('_extra_info', "")
        super().__setattr__('_initializing', True)
        self._initializing = False  # Сбрасываем флаг после инициализации

    @property
    def code(self) -> int:
        return self._code

    @property
    def msg(self) -> str:
        return self._msg + self._extra_info

    @property
    def http_code(self) -> int:
        return self._http_code

    def add_info(self, info: str = "") -> Self:
        """
        Создаёт новый объект ошибки с добавленной информацией.
        
        Args:
            info (str): Дополнительная информация для сообщения.
        
        Returns:
            Self: Новый объект ошибки с обновлённым сообщением.
        """
        new_error = deepcopy(self)
        if info:
            new_error._extra_info = f": {info}"
        return new_error

    def up_raise(self, msg="", detail="", http_code=None) -> HTTPException:
        return HTTPException(status_code=http_code or self.http_code, detail=detail or self.msg + msg)

    def __bool__(self) -> bool:
        return self.code != 0

    @property
    def as_dict(self) -> dict[str, int | str]:
        return {"code": self.code, "msg": self.msg} if self.code else {}


E = Error

