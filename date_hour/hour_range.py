from datetime import datetime
from typing import Union
from pydantic_core import core_schema
from date_hour import DateHour
from pydantic import GetCoreSchemaHandler


class HourRange(dict):
    '''
    Класс для работы с временными диапазонами.
    start и stop - это DateHour объекты (точки в времени).
    Диапазон: [start, stop) - включая start, исключая stop.
    '''

    def __init__(self, start: Union[str, datetime, DateHour],
                 stop: Union[str, datetime, DateHour] = None):
        start_dh = DateHour(start)
        stop_dh = start_dh + 1 if stop is None else DateHour(stop)
        super().__init__(start=str(start_dh), stop=str(stop_dh))

    @property
    def start(self) -> DateHour:
        return DateHour(self['start'])

    @property
    def stop(self) -> DateHour:
        return DateHour(self['stop'])

    def __str__(self) -> str:
        return f"HourRange({self.start} - {self.stop})"

    def __repr__(self) -> str:
        return f"HourRange({self.start} - {self.stop})"

    def hours(self) -> int:
        '''Количество часов в диапазоне'''
        diff = (self.stop._get_datetime() - self.start._get_datetime()).total_seconds() / 3600
        return max(0, int(diff))
    
    def __len__(self) -> int:
        diff = (self.stop._get_datetime() - self.start._get_datetime()).total_seconds() / 3600
        return max(0, int(diff))
    
    def __bool__(self) -> bool:
        return self.__len__() > 0

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type,
        handler: GetCoreSchemaHandler
    ):
        return core_schema.no_info_plain_validator_function(
            function=cls._validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda v: {'start': str(v.start), 'stop': str(v.stop)}
            ),
        )

    @classmethod
    def _validate(cls, v):
        if isinstance(v, cls):
            return v
        if isinstance(v, dict):
            return cls(v['start'], v.get('stop'))
        if isinstance(v, (list, tuple)):
            return cls(*v)
        return cls(v)
