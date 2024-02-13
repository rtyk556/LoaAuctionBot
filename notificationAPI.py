from DBmanager import DBManager, DBDataTag, get_valid_api
from searchengine import get_preset_result
import threading

from flask import Flask, jsonify

def noti_loop():
    dbmanger = DBManager()
    users = dbmanger.get_all_users()
    
    for user_idx in range(len(users)):
        # preset 존재하는지 확인
        # 추후엔 길드가 봇에게 있는 길드인지 확인
        if len(users[user_idx].get(DBDataTag.preset)) != 0:
            # check api validity
            api_list = get_valid_api(users[user_idx].get(DBDataTag.api))
            if len(api_list) == 0:
                continue
            
            user_presets = users[user_idx].get(DBDataTag.preset)
            
            for preset_idx in range(len(user_presets)):
                noti_rst = get_preset_result(user_presets[preset_idx], api_list)
                if len(noti_rst) != 0:
                    rst.append([users[user_idx], noti_rst])

            users[user_idx][DBDataTag.api] = api_list
            users[user_idx][DBDataTag.preset] = user_presets
            
    dbmanger.save_user_info(users)

    threading.Timer(60, noti_loop).start()

app = Flask(__name__)

rst = []

@app.route("/api/noti")
def get_notification_list():
    global rst
    noti_rst = rst
    rst = []
    return jsonify(noti_rst)


noti_loop()
app.run()