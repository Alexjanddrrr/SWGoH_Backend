from peewee import *


db = SqliteDatabase('users_base')


class BaseModel(Model):
    """
    Базовый класс для всех наследников для работы с базой данных,
    наследник от Model
    """
    class Meta:
        database = db


class Player(BaseModel):
    """
    Модель игрока в системе

    :param
        nickname: Имя пользователя
        ally_code: Код союзника пользователя

    """
    nickname = CharField()
    ally_code = IntegerField(primary_key=True)