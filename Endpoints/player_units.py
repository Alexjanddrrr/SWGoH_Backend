from flask import Blueprint
import requests
from database import Player, Characters

all_units = Blueprint('units', __name__)


@all_units.route('/units/<string:ally_code>/', methods=['GET'])
def units_info(ally_code: str):
    """
    Регистрирует игрока и его склад, если игрок уже зарегистрирован, то возвращает
    склад игрока

    :param
        ally_code: Код союзника
    :return: Если игрок уже есть в базе, то возвращает список юнитов с уровнем реликвий.
    Если нет, то регистрирует
    """
    url = 'COMLINK_URL/player'
    payload = {
        "payload": {
            "allyCode": f'{ally_code}',
        },
        "enums": False
    }

    response = requests.post(url, json=payload)
    player_data = response.json()['rosterUnit']
    player_nickname = response.json()['name']

    output_dict = {}
    if Player.get_or_none(nickname=player_nickname, ally_code=ally_code):
        for char in Characters.select().where(Characters.ally_id == ally_code):
            output_dict[char.unit] = char.relic
        return output_dict

    else:
        Player.create(nickname=player_nickname, ally_code=ally_code)
        output = []
        for some_data in player_data:
            try:
                if some_data['currentTier'] < 13:
                    output.append(f'UNIT: {some_data['definitionId']}, GEAR LVL: {some_data['currentTier']}')
                else:
                    output.append(f'UNIT: {some_data['definitionId']}, RELIC LVL: {some_data['relic']['currentTier'] - 2}')
                    Characters.create(ally_id=ally_code,
                                          unit=f'{some_data['definitionId']}',
                                          relic=f'{some_data['relic']['currentTier'] - 2}')
            except TypeError as exc:
                output.append(f'FLEET UNIT: {some_data['definitionId']}')
        return output