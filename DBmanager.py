import json
import enum
import datetime

#db manager에 필요한 내용
# 새 유저 등록, 프리셋 등록, api 등록, get 유저 데이터

class DBDataTag(str, enum.Enum):
    users = "users"
    user_id = "user_id"
    guild = "guild"
    api = "api"
    preset = "preset"
    
class PresetTag(str, enum.Enum):
    search_option = 'search_option'
    condition = 'condition'
    search_history = 'search_history'
    
class PresetData():
    def __init__(self, input = {PresetTag.search_option : None,
            PresetTag.condition : None,
            PresetTag.search_history : []}):
        self.preset_data = {
            PresetTag.search_option : input[PresetTag.search_option],
            PresetTag.condition : input[PresetTag.condition],
            PresetTag.search_history : input[PresetTag.search_history]
        }
    
    def get_search_option(self):
        return self.preset_data[PresetTag.search_option]
    
    def get_condition(self):
        return self.preset_data[PresetTag.condition]
    
    def get_search_history(self):
        return self.preset_data[PresetTag.search_history]
    
    def edit_preset(self, tag:PresetTag, changed_value):
        if tag == PresetTag.search_option:
            self.preset_data[PresetTag.search_option] = changed_value
        elif tag == PresetTag.condition:
            try:
                self.preset_data[PresetTag.condition] = int(changed_value)
            except ValueError as e:
                raise Exception('Condition must be int type.', e)
        elif tag == PresetTag.search_history:
            self.preset_data[PresetTag.search_history] = changed_value

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
        self.basicUserData = {
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
            
            user_data = self.basicUserData
            user_data[DBDataTag.user_id] = userid
            data.get(DBDataTag.users).append(user_data)
            
            with open(self.dataPath, 'w') as outfile:
                json.dump(data, outfile, indent=4)
        except Exception as e:
            raise Exception("DBManager cannot edit json data. ", e)
    
    def add_preset(self, userid, preset:PresetData):
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
                        exist_preset = PresetData(user_presets[i])
                        if exist_preset.get_search_option() == preset.get_search_option():
                            exist_preset.edit_preset(PresetTag.condition, preset.get_condition())
                            exist_preset.edit_preset(PresetTag.search_history, preset.get_search_history())
                            user_presets[i] = exist_preset.preset_data
                            break
                    if not preset.preset_data in user_presets:
                        user_presets.append(preset.preset_data)
                    user[DBDataTag.preset] = user_presets
                    data.get(DBDataTag.users)[idx] = user
                    break
                idx += 1
            
            with open(self.dataPath, 'w') as outfile:
                json.dump(data, outfile, indent=4)
            
        except Exception as e:
            raise Exception("DBmanager cannot edit json file. ", e)
    
    def get_all_users(self):
        try:
            data = {}
            with open(self.dataPath, 'r') as json_file:
                data = json.load(json_file)
            return data.get(DBDataTag.users)
        except Exception as e:
            raise Exception("DBmanager cannot edit json file. ", e)
    
    def save_user_info(self, users):
        try:
            data = {}
            with open(self.dataPath, 'r') as json_file:
                data = json.load(json_file)
            data[DBDataTag.users] = users
            
            with open(self.dataPath, 'w') as outfile:
                json.dump(data, outfile, indent=4)
        except Exception as e:
            raise Exception("DBmanager cannot edit json file. ", e)
                

def get_valid_api(api_list:list):
    rst = []
    for api in api_list:
        now = datetime.datetime.now()
        if api[APITag.valid_time] == None:
            rst.append(api)
        else:
            valid_time = datetime.datetime.strptime(api[APITag.valid_time], "%Y-%m-%d %H:%M:%S")
            if now > valid_time:
                rst.append(api)
    return rst
        
class APITag(str, enum.Enum):
    key = 'key',
    valid_time = 'valid_time'