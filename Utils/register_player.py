from database import Player, Characters, Fleet


def player_registration(nick: str, ally: str, player_info: list):
    Player.create(nickname=nick, ally_code=ally)

    for some_data in player_info:
        if some_data['relic'] is None:
            Fleet.create(ally_id=ally,
                         ship=some_data['definitionId'])
        elif some_data['currentTier'] == 13:
            Characters.create(ally_id=ally,
                              unit=f'{some_data['definitionId']}',
                              relic=f'{some_data['relic']['currentTier'] - 2}')