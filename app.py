from flask import Flask
from Endpoints.player_units import all_units
from Endpoints.cal_kestis_jedi import cal_kestis
from database import db, Player, Characters, Fleet
from Utils.update_units import background_task



app = Flask(__name__)
app.register_blueprint(all_units)
app.register_blueprint(cal_kestis)

with db:
    db.create_tables([Player, Characters, Fleet])

if __name__ == '__main__':
    background_task()
    app.run(use_reloader=False)