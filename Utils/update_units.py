from apscheduler.schedulers.background import BackgroundScheduler
from database import Player, Characters, Fleet
from loguru import logger
import requests


def player_update():
    """
    Проходит по списку игроков для работы с ними

    :return: None
    """
    for player in Player.select():
        clean_and_update(player.ally_code)


def clean_and_update(ally: str):
    """
    Очищает и добавляет свежие данные по игроку

    :param ally: Код союзника
    :return: None
    """
    url = 'COMLINK_URL/player'
    payload = {
        "payload": {
            "allyCode": f'{ally}',
        },
        "enums": False
    }

    response = requests.post(url, json=payload)
    player_data = response.json()['rosterUnit']

    Fleet.delete().where(Fleet.ally_id == ally).execute()
    logger.info(f'Fleet for {ally} are cleaned')
    Characters.delete().where(Characters.ally_id == ally).execute()
    logger.info(f'Units for {ally} are cleaned')

    for some_data in player_data:
        if some_data['relic'] is None:
            Fleet.create(ally_id=ally,
                         ship=some_data['definitionId'])
            logger.info(f'Fleet {some_data['definitionId']} for {ally} are added')
        elif some_data['currentTier'] == 13:
            Characters.create(ally_id=ally,
                              unit=f'{some_data['definitionId']}',
                              relic=f'{some_data['relic']['currentTier'] - 2}')
            logger.info(f'Unit {some_data['definitionId']} for {ally} are added')

    logger.info('All updated are done!')


def background_task():
    """
    Создает задачу в фоновом потоке, не блокируя основной

    :return: None
    """
    work = BackgroundScheduler()
    work.add_job(player_update, 'cron', hour='10-23', minute='14')
    work.start()