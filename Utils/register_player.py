from database import Player, Characters, Fleet
from loguru import logger


def player_registration(nick: str, ally: str, player_info: list):
    """
    Создает профиль игрока и заполняет таблицу Characters и Fleet

    :param nick: Никнейм игрока
    :param ally: Код союзника игрока
    :param player_info: Необработанные данные, полученные от COMLINK
    :return: None
    """
    Player.create(nickname=nick, ally_code=ally)

    for some_data in player_info:
        if some_data['relic'] is None:
            Fleet.create(ally_id=ally,
                         ship=some_data['definitionId'])
        elif some_data['currentTier'] == 13:
            Characters.create(ally_id=ally,
                              unit=f'{some_data['definitionId']}',
                              relic=f'{some_data['relic']['currentTier'] - 2}')

    logger.info(f'New user {nick} are created')