from flask import request, Blueprint
import requests
from database import db, Player

all_units = Blueprint('units_info', __name__)


@all_units.route('/units_info', methods=['GET'])
def units_info():
    url = 'COMLINK_URL/player'
    get_ally_code = request.args.get('allycode')
    payload = {
        "payload": {
            "allyCode": f'{get_ally_code}',
        },
        "enums": False
    }
    response = requests.post(url, json=payload)
    player_data = response.json()['rosterUnit']

    output = []

    for some_data in player_data:
        try:

            if some_data['currentTier'] < 13:
                output.append(f'UNIT: {some_data['definitionId']}, GEAR LVL: {some_data['currentTier']}')

            else:
                output.append(f'UNIT: {some_data['definitionId']}, RELIC LVL: {some_data['relic']['currentTier'] - 2}')

        except TypeError as exc:
            output.append(f'FLEET UNIT: {some_data['definitionId']}, RELIC LVL: NONE')

    return f'<pre>{'\n'.join(output)}</pre>'