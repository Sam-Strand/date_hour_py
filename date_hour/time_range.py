from datetime import datetime
from typing import Union
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler
from date_hour import DateHour


class TimeRange:
    '''
    Класс для работы с временными диапазонами.
    start и stop - это DateHour объекты (точки в времени).
    Диапазон: [start, stop) - включая start, исключая stop.
    '''

    def __init__(self, start: Union[str, datetime, DateHour],
                 stop: Union[str, datetime, DateHour] = None):
        '''
        Создает временной диапазон.

        Args:
            start: Начало диапазона
            stop: Конец диапазона (опционально)
                  Если не указан, создается диапазон из одного часа
        '''
        self.start = DateHour(start)

        if stop is None:
            self.stop = self.start + 1
        else:
            self.stop = DateHour(stop)

    def __str__(self) -> str:
        return f"TimeRange({self.start} - {self.stop})"

    def __len__(self) -> int:
        '''Количество часов в диапазоне'''
        start_dt = self.start._get_datetime()
        stop_dt = self.stop._get_datetime()

        diff = (stop_dt - start_dt).total_seconds() / 3600
        return max(0, int(diff))

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type,
        handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        def validate(value) -> 'TimeRange':
            if isinstance(value, cls):
                return value
            return cls(value)

        return core_schema.no_info_plain_validator_function(
            function=validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda v: {
                    'start': str(v.start),
                    'stop': str(v.stop)
                }
            )
        )
