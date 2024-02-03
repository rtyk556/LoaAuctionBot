import json
import enum

class DBManager():
    def __init__(self):
        self.dataPath = './data.json'
    
    def add_new_user(self, userid):
        try:
            data = {}
            with open(self.dataPath, "r") as json_file:
                data = json.load(json_file)
            
            for user in data.get(DBDataTag.users):
                if user.get(DBDataTag.user_id) == userid:
                    return
            
            data.get(DBDataTag.users).append(
                {
                    DBDataTag.user_id : userid,
                    DBDataTag.guild : [],
                    DBDataTag.api : [],
                    DBDataTag.preset : []
                }
            )
            
            with open(self.dataPath, 'w') as outfile:
                json.dump(data, outfile, indent=4)
        except Exception as e:
            raise Exception("DBManager cannot edit json data : ", e)

class DBDataTag(str, enum.Enum):
    users = "users"
    user_id = "user_id"
    guild = "guild"
    api = "api"
    preset = "preset"