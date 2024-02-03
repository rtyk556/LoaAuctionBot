import json
import enum

#db manager에 필요한 내용
# 새 유저 등록, 프리셋 등록, api 등록, get 유저 데이터

def singleton(class_):
  instances = {}
  
  def get_instance(*args, **kwargs):
    if class_ not in instances:
      instances[class_] = class_(*args, **kwargs)
    return instances[class_]
  return get_instance

@singleton
class DBManager():
    def __init__(self):
        self.dataPath = './data.json'
        self.basicData = {
                    DBDataTag.user_id : 0,
                    DBDataTag.guild : [],
                    DBDataTag.api : [],
                    DBDataTag.preset : []
                }
    
    def add_new_user(self, userid):
        try:
            data = {}
            with open(self.dataPath, "r") as json_file:
                data = json.load(json_file)
            
            for user in data.get(DBDataTag.users):
                if user.get(DBDataTag.user_id) == userid:
                    return
            
            user_data = self.basicData
            user_data[DBDataTag.user_id] = userid
            data.get(DBDataTag.users).append(user_data)
            
            with open(self.dataPath, 'w') as outfile:
                json.dump(data, outfile, indent=4)
        except Exception as e:
            raise Exception("DBManager cannot edit json data. ", e)
    
    def add_preset(self, userid, preset:list):
        self.add_new_user(userid)
        
        try:
            data = {}
            with open(self.dataPath, 'r') as json_file:
                data = json.load(json_file)
            
            idx = 0
            for user in data.get(DBDataTag.users):
                if user.get(DBDataTag.user_id) == userid:
                    user_presets = user.get(DBDataTag.preset)
                    for i in range(len(user_presets)):
                        if user_presets[i][0] == preset[0]:
                            user_presets[i][1] == preset[1]
                            break
                    if preset not in user_presets:
                        user_presets.append(preset)
                    user[DBDataTag.preset] = user_presets
                    data.get(DBDataTag.users)[idx] = user
                    break
                idx += 1
            
            with open(self.dataPath, 'w') as outfile:
                json.dump(data, outfile, indent=4)
            
        except Exception as e:
            raise Exception("DBmanager cannot edit json file. ", e)

class DBDataTag(str, enum.Enum):
    users = "users"
    user_id = "user_id"
    guild = "guild"
    api = "api"
    preset = "preset"
