import pytest
from pydantic import BaseModel
from date_hour import HourRange, DateHour


class Event(BaseModel):
    name: str
    period: HourRange


def test_valid_dict_still_works():
    # dict с start/stop проходит
    e = Event.model_validate({
        'name': 'x',
        'period': {'start': '2024-01-01 00', 'stop': '2024-01-01 03'},
    })
    assert isinstance(e.period, HourRange)
    assert len(e.period) == 3


def test_dict_without_start_raises_keyerror_not_validationerror():
    # ЛОМАЕТСЯ: вместо ValidationError получаем KeyError из _validate,
    # потому что HourRange теперь dict и попадает в ветку isinstance(v, dict)
    with pytest.raises(Exception) as exc:
        Event.model_validate({
            'name': 'x',
            'period': {'stop': DateHour('2024-01-01 03')},  # нет 'start'
        })
    # после наследования от dict:
    assert isinstance(exc.value, KeyError), type(exc.value)
    # ожидалось бы:
    # assert isinstance(exc.value, ValidationError)


def test_extra_keys_silently_pass():
    # ЛОМАЕТСЯ: лишние ключи не отбрасываются, т.к. dict их принимает
    e = Event.model_validate({
        'name': 'x',
        'period': {
            'start': '2024-01-01 00',
            'stop': '2024-01-01 03',
            'evil': 'payload',
        },
    })
    assert 'evil' not in dict(e.period)   # упадёт: evil там есть


def test_roundtrip_model_dump_python():
    # ЛОМАЕТСЯ: model_dump() возвращает dict-наследника,
    # повторная валидация идёт не по __get_pydantic_core_schema__,
    # а по dict-ветке, теряя DateHour
    e = Event.model_validate({
        'name': 'x',
        'period': {'start': '2024-01-01 00', 'stop': '2024-01-01 03'},
    })
    dumped = e.model_dump()
    assert isinstance(dumped['period'], dict)

    e2 = Event.model_validate(dumped)
    assert isinstance(e2.period, HourRange)
    # сравнение уходит в dict.__eq__: dict == dict → True
    # но start/stop как DateHour потеряны
    assert isinstance(e2.period.start, type(e.period.start))


def test_equality_with_plain_dict():
    # ЛОМАЕТСЯ семантика: HourRange теперь равен обычному словарю
    tr = HourRange('2024-01-01 00', '2024-01-01 03')
    assert tr == {'start': DateHour('2024-01-01 00'), 'stop': DateHour('2024-01-01 03')}  # True


def test_bool_is_false_for_single_hour():
    # ЛОМАЕТСЯ: __len__ возвращает 0 для диапазона без часов? нет —
    # для одного часа len == 1, bool True. Но для пустого диапазона:
    tr = HourRange('2024-01-01 00', '2024-01-01 00')
    # dict с двумя ключами всегда truthy, а __len__ говорит 0
    assert bool(tr) is False   # упадёт: dict.__bool__ → True


def test_start_attribute_sync():
    # ЛОМАЕТСЯ: ключ и атрибут живут раздельно
    tr = HourRange('2024-01-01 00', '2024-01-01 03')
    tr['start'] = DateHour('1999-01-01 00')
    assert str(tr.start) == tr['start']  # упадёт


def test_copy_loses_attributes():
    # ЛОМАЕТСЯ: dict.copy() не тащит self.start/self.stop
    import copy
    tr = HourRange('2024-01-01 00', '2024-01-01 03')
    c = copy.copy(tr)
    assert hasattr(c, 'start')  # упадёт для некоторых реализаций
    str(c)                       # AttributeError


if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main([__file__, '-v']))
