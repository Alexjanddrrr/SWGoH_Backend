from flask import Blueprint
from database import Player, Characters

cal_kestis = Blueprint('cal_kestis_jedi', __name__)


@cal_kestis.route('/all/cal_jedi/', methods=['GET'])
def cal_kestis_jedi():
    """
    Собирает словарь с игроком, персонажем и его уровнем реликвий

    :return: Словарь с игроками и персонажем и уровнем реликвий
    """
    output_dict = {}

    for char in Characters.select().where(Characters.unit.ilike('JEDIKNIGHTCAL%')):
        player_nick = Player.get(Player.ally_code == char.ally_id).nickname
        output_dict.setdefault(player_nick, {char.unit: char.relic})

    return output_dict