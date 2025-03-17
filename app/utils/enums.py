import enum


class Order(str, enum.Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class FieldBy(str, enum.Enum):
    LEVEL = 'level'
    DUE_DATE = 'due_date'

