from datetime import datetime, timedelta
from typing import Union
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler


class DateHour(str):
    '''
    Класс для работы с временными метками с часовой дискретностью.
    Всегда хранит начало часа.
    '''

    def __new__(cls, value: Union[str, datetime]) -> 'DateHour':
        if isinstance(value, datetime):
            dt = value.replace(minute=0, second=0, microsecond=0)
            value = dt.strftime('%Y-%m-%d %H:%M:%S')

        if not isinstance(value, str):
            raise ValueError(
                f'Ожидалась строка, получен {type(value)}: {value}')

        dt = cls._parse_string(value)
        normalized_dt = dt.replace(minute=0, second=0, microsecond=0)
        normalized_str = normalized_dt.strftime('%Y-%m-%d %H:%M:%S')

        instance = super().__new__(cls, normalized_str)
        return instance

    @classmethod
    def _parse_string(cls, value: str) -> datetime:
        '''Парсит строку в datetime.'''
        formats = [
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M',
            '%Y-%m-%dT%H',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M',
            '%Y-%m-%d %H',
            '%Y-%m-%d',
            '%Y-%m',
            '%Y',
        ]

        for fmt in formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue

        raise ValueError(
            f'Не удалось распарсить дату: "{value}".\n'
            f'Поддерживаемые форматы: год, месяц, день, час'
        )

    def __sub__(self, hours: int) -> 'DateHour':
        dt = self._get_datetime() - timedelta(hours=hours)
        return DateHour(dt)

    def __add__(self, hours: int) -> 'DateHour':
        dt = self._get_datetime() + timedelta(hours=hours)
        return DateHour(dt)

    def _get_datetime(self) -> datetime:
        return datetime.strptime(self, '%Y-%m-%d %H:%M:%S')

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type,
        handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        def validate(value: Union[str, datetime]) -> 'DateHour':
            if isinstance(value, cls):
                return value
            return cls(value)

        return core_schema.no_info_plain_validator_function(
            function=validate,
            serialization=core_schema.plain_serializer_function_ser_schema(str)
        )
