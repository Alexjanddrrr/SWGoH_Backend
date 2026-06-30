from flask import Blueprint
import requests
from database import Player, Characters, Fleet
from Utils.register_player import player_registration

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
    output_dict = {
        'UNITS': {},
        'FLEET': []
    }
    payload = {
        "payload": {
            "allyCode": f'{ally_code}',
        },
        "enums": False
    }

    response = requests.post(url, json=payload)
    player_data = response.json()['rosterUnit']
    player_nickname = response.json()['name']
    player = Player.get_or_none(nickname=player_nickname, ally_code=ally_code)

    if player is None:
        player_registration(player_nickname, ally_code, player_data)

    for char in Characters.select().where(Characters.ally_id == ally_code):
        output_dict['UNITS'][char.unit] = char.relic
    for ships in Fleet.select().where(Fleet.ally_id == ally_code):
        output_dict['FLEET'].append(ships.ship)
    return output_dict