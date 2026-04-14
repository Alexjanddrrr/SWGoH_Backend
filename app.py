from flask import Flask
from Endpoints.get_player_units import all_units
from Endpoints.cal_kestis_jedi import cal_kestis
from database import db, Player

app = Flask(__name__)
app.register_blueprint(all_units)
app.register_blueprint(cal_kestis)

with db:
    db.create_tables([Player])


app.run()