from flask import request, Blueprint
import requests

cal_kestis = Blueprint('cal_kestis_jedi', __name__)


@cal_kestis.route('/cal_jedi_check', methods=['GET'])
def cal_kestis_jedi():
    url = 'COMLINK_URL/player'
    get_ally_code = request.args.get('allycode')
    payload = {
        "payload": {
            "allyCode": f'{get_ally_code}',
        },
        "enums": False
    }
    response = requests.post(url, json=payload)
