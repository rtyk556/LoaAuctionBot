from typing import Optional
import discord
from discord.interactions import Interaction
from jsonobject import *
from searchengine import SearchEngine, check_api_validity, OptionLabel
import pyllist
import DBmanager

first_message = {
  "embeds": 
    {
      "id": 652627557,
      "title": "로스트아크 매물 검색기",
      "color": 2326507,
      "fields": [
        {
          "id": 811547707,
          "name": "API",
          "value": " > 검색에 필요한 API키를 입력하고 조회할 수 있습니다. 서버에서 상시로 APi를 통해 검색을 시도하기 때문에 다른 사이트(ex. Icepeng)에서 사용되지 않는 API 키를 입력해주세요\n"
        },
        {
          "id": 940685081,
          "name": "알림 목록",
          "value": "> 알림 설정한 프리셋 목록을 확인하고 삭제할 수 있습니다.\n"
        },
        {
          "id": 559602059,
          "name": "매물 검색",
          "value": "> 다양한 조건으로 매물을 검색하고 일정 가격 이하일 때 알림을 설정할 수 있습니다.\n"
        }
      ]
    }
  ,
  "components": [
    {
      "id": 28594786,
      "type": 1,
      "components": [
        {
          "id": 608864451,
          "type": 2,
          "style": 1,
          "label": "API키",
          "action_set_id": "756636785"
        },
        {
          "id": 420977314,
          "type": 2,
          "style": 1,
          "label": "매물 검색",
          "action_set_id": "642948001"
        },
        {
          "id": 867872496,
          "type": 2,
          "style": 1,
          "label": "알림 설정",
          "action_set_id": "987717787"
        }
      ]
    }
  ],
  "actions": {
    "642948001": {
      "actions": []
    },
    "756636785": {
      "actions": []
    },
    "987717787": {
      "actions": []
    }
  }
}

api_message = {
      "id": 373725794,
      "description": "⛔ API를 알림 설정용으로 사용하게 되면 서버 상에서 상시로 경매장 검색이 돌아가기 때문에 100회 제한에 계속 걸리게 됩니다.\n알림 설정을 하신다면 그 용도로 따로 API를 분리해서 사용하시고 다른 사이트에선 다른 API를 사용하시는 걸 추천 드립니다. ⛔",
      "fields": [
        {
          "id": 253592701,
          "name": "API 조회",
          "value": "등록한 API의 이름과 값을 확인할 수 있습니다. "
        },
        {
          "id": 346272862,
          "name": "API 등록",
          "value": "API의 이름과 값을 등록합니다."
        }
      ],
      "author": {
        "name": "API 관리"
      }
    }


select_acce_type_message = {
      "id": 373725794,
      "description": "⛔ 알림 설정 용으로 등록된 API는 계속 100회 제한까지 사용하니 전용 API로 따로 구분하시길 바랍니다.\n\n검색하고자 하는 장신구 종류를 골라 주세요 (동시 선택 가능)",
      "fields": [],
      "title": "경매장 매물 알림 설정"
    }

def get_main_opt_message(engrave:str = '미입력'):
  main_option_message = {
      "description": f"⛔ 알림 설정 용으로 등록된 API는 계속 100회 제한까지 사용하니 전용 API로 따로 구분하시길 바랍니다.\n\n반드시 검색에 포함될 메인 각인과 최소값, 최대값을 입력해 주세요.\n\n",
      "fields": [
        {
          "id": 531054326,
          "name": "현재 입력된 메인 각인",
          "value": f"**{engrave}**"
        }
      ],
      "title": "필수 각인 검색 설정"
    }
  return main_option_message

def get_etc_opt_message(engrave_list:list = []):
  etc_option_message = {
      "description": f"⛔ 알림 설정 용으로 등록된 API는 계속 100회 제한까지 사용하니 전용 API로 따로 구분하시길 바랍니다.\n\n검색에 포함될 다른 각인(복수 선택 가능)과 스탯을 입력해 주세요.\n\n",
      "fields": [
        {
          "id": 531054327,
          "name": "현재 입력된 각인 목록",
          "value": f"**{engrave_list}**"
        }
      ],
      "title": "부가 요소 검색 설정 ( 1/2 )"
  }
  return etc_option_message

etc_2nd_option_message = {
      "description": f"⛔ 알림 설정 용으로 등록된 API는 계속 100회 제한까지 사용하니 전용 API로 따로 구분하시길 바랍니다.\n\n품질과 아이템 등급, 정렬 기준을 선택해 주세요.\n\n",
      "fields": [],
      "title": "부가 요소 검색 설정 ( 2/2 )"
  }

class FirstView(discord.ui.View):
  
  embed = discord.Embed.from_dict(first_message["embeds"])
  def __init__(self):
      super().__init__()
      self.container = SearchOptionContainer()

  @discord.ui.button(label='API키', style=discord.ButtonStyle.primary)
  async def button_api(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = APIView()
    await interaction.response.edit_message(embed=view.embed, view=view)
    
  @discord.ui.button(label='알림 목록', style=discord.ButtonStyle.primary)
  async def button_notification_lists(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = NotificationListView(interaction.user.id)
    await interaction.response.edit_message(embed=view.embed, view=view)
  
  @discord.ui.button(label='매물 검색', style=discord.ButtonStyle.primary)
  async def button_search(self, interaction: discord.Interaction, button: discord.ui.Button):
    self.container.userid = interaction.user.id
    view = NotiAcceTypeView(self.container)
    await interaction.response.edit_message(embed=view.embed, view=view)

class NotificationListView(discord.ui.View):
  embed = discord.Embed(title="등록된 알림 설정 목록")

  def __init__(self, user_id):
    super().__init__()
    self.presets = DBmanager.DBManager().get_user_presets(user_id)
    
    text = ''
    for preset in self.presets:
      search_option = preset.get(DBmanager.PresetTag.search_option)[0]
      option = SearchOptionParser(search_option)
      subengraves = preset.get(DBmanager.PresetTag.search_option)[1]
      text += f'### 장신구 종류\n> {option.acceType}\n    '
      text += f'### 메인각인\n> {option.engrave[0][0]}\n최소 : {option.engrave[0][1]}, 최대 : {option.engrave[0][2]}\n'
      if len(option.engrave) == 1 and len(subengraves) == 0:
        text += f'### 서브각인\n> 없음\n'
      elif len(option.engrave) == 2:
        sub = option.engrave[1]
        text += f'### 서브각인\n> {sub[0]}\n최소 : {sub[1]}, 최대 : {sub[2]}\n'
      elif len(subengraves) != 0:
        text += f'### 서브각인\n> {subengraves}\n'
      text += f'### 스탯\n> {option.stats}\n'
      text += f'### 품질\n> {option.quality} 이상\n'
      text += f'### 아이템 등급\n> {option.grade}\n'
      text += f'### 알림 설정 가격\n> {option.sort} {preset[DBmanager.PresetTag.condition]} 이하\n'
      text += '-----------------------------------\n'

    self.embed.description = text
    # userid에 등록된 preset 목록은 embed로 보여줌
    # 프리셋 삭제 버튼, 처음으로 버튼
    # 프리셋 삭제 버튼 누르면 새로운 view로 삭제할 프리셋 선택

  @discord.ui.button(label='프리셋 삭제', style=discord.ButtonStyle.primary)
  async def button_delete_preset(self, interaction: discord.Interaction, button: discord.ui.Button):
    view=NotificationDeleteView(self.presets)
    await interaction.response.edit_message(embed=view.embed, view=view)
    
  @discord.ui.button(label='처음 화면으로', style=discord.ButtonStyle.primary)
  async def button_home(self, interaction: discord.Interaction, button: discord.ui.Button):
      view = FirstView()
      await interaction.response.edit_message(embed=view.embed, view=view)

class NotificationDeleteView(discord.ui.View):
  embed = discord.Embed(title="삭제할 프리셋 선택", description="삭제할 프리셋을 선택하고 삭제 버튼을 눌러주세요.")
  delete_list = []
  preset_list = []
  def __init__(self, presetList:list):
    super().__init__()
    presetOptions = []
    self.preset_list = presetList

    description_txt = ''
    idx = 0
    for preset in presetList:
      search_option = preset[DBmanager.PresetTag.search_option][0]
      subengraves = preset[DBmanager.PresetTag.search_option][1]
      option = SearchOptionParser(search_option)
      if len(option.engrave) == 1:
        description_txt += f'{idx+1}. 등급-{option.grade} 종류-{option.acceType}, 스탯-{option.stats}, 각인-{option.engrave[0][0]}, 서브각인-{subengraves}, {option.sort} {preset[DBmanager.PresetTag.condition]} 이상\n'
      elif len(option.engrave) == 2:
        description_txt += f'{idx+1}. 등급-{option.grade} 종류-{option.acceType}, 스탯-{option.stats}, 각인-{option.engrave[0][0]}, 서브각인-{option.engrave[1][0]}, {option.sort} {preset[DBmanager.PresetTag.condition]} 이상\n'
      presetOptions.append(discord.SelectOption(
        label=f'{idx+1}번',
        value=idx
      ))
      idx += 1
    self.select_delete_preset.options = presetOptions
    self.embed.description = description_txt

  @discord.ui.select(placeholder="알림 프리셋")
  async def select_delete_preset(self, interaction:discord.Interaction, select: discord.ui.Select):
    for option in self.select_delete_preset.options:
      option.default = False
    
    d_list = []
    for presetIdx in select.values:
      d_list.append(self.preset_list[int(presetIdx)])
    self.delete_list = d_list
    
    options = self.select_delete_preset.options
    for i in range(len(options)):
      if options[i].value in select.values:
        options[i].default = True
    
    self.select_delete_preset.options = options
    await interaction.response.edit_message(embed=self.embed, view=self)
  
  @discord.ui.button(label='프리셋 삭제', style=discord.ButtonStyle.red)
  async def button_delete_preset(self, interaction: discord.Interaction, button: discord.ui.Button):
      dbManager = DBmanager.DBManager()
      
      for preset in self.delete_list:
        dbManager.delete_preset(interaction.user.id, preset)
      
      await interaction.response.edit_message(content='알림 프리셋 삭제 완료', embed=None, view=None)
    
  @discord.ui.button(label='처음 화면으로', style=discord.ButtonStyle.primary)
  async def button_home(self, interaction: discord.Interaction, button: discord.ui.Button):
      view = FirstView()
      await interaction.response.edit_message(embed=view.embed, view=view)

class APIView(discord.ui.View):
    embed = discord.Embed.from_dict(api_message)
    def __init__(self):
        super().__init__()
        
    @discord.ui.button(label='API 조회', style=discord.ButtonStyle.primary)
    async def button_check_api(self, interaction: discord.Interaction, button: discord.ui.Button):
      view = APICheckView(interaction.user.id)
      await interaction.response.edit_message(embed=view.embed, view=view)
    
    @discord.ui.button(label='API 등록', style=discord.ButtonStyle.primary)
    async def button_register_api(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = APIRegisterModal()
        await interaction.response.send_modal(modal)        
    
    @discord.ui.button(label='처음 화면으로', style=discord.ButtonStyle.primary)
    async def button_home(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = FirstView()
        await interaction.response.edit_message(embed=view.embed, view=view)

class APIRegisterModal(discord.ui.Modal, title="API 등록"):
  label = discord.ui.TextInput(label="라벨명을 입력해 주세요. ", placeholder="기존에 등록된 API 라벨명과 달라야 합니다.")
  key = discord.ui.TextInput(label="API 키를 입력해 주세요.", placeholder="유효한 API인지 1회 확인합니다. 로스트아크 점검 시간이면 등록이 불가능합니다.")

  async def on_submit(self, interaction: discord.Interaction):
    dbManager = DBmanager.DBManager()
    api_list = dbManager.get_user_api(interaction.user.id)
    for api in api_list:
      if api.get(DBmanager.APITag.label) == self.label.value or api.get(DBmanager.APITag.key) == self.key.value:
        return await interaction.response.edit_message(content='이미 등록된 라벨명이나 값이 존재합니다.', embed=None, view=None)
    if not check_api_validity(self.key.value):
      return await interaction.response.edit_message(content='사용 가능한 API가 아닙니다. 키 값과 점검 여부를 확인해 주세요.', embed=None, view=None)
    dbManager.add_new_api(interaction.user.id, self.label.value, self.key.value)
    await interaction.response.edit_message(content='API 등록 완료!', embed=None, view=None)

class APICheckView(discord.ui.View):
  embed = discord.Embed(title='등록된 API 조회')
  curAPI = []
  def __init__(self, user_id):
    super().__init__()
    dbManager = DBmanager.DBManager()
    self.curAPI = dbManager.get_user_api(user_id)
    description = ''
    for api in self.curAPI:
      description += f'### 라벨명\n```\n{api.get(DBmanager.APITag.label)}\n```\n### Key\n```\n{api.get(DBmanager.APITag.key)}\n```\n\n'
    self.embed.description = description
  
  @discord.ui.button(label='API 삭제', style=discord.ButtonStyle.primary)
  async def button_delete_api(self, interaction: discord.Interaction, button: discord.ui.Button):
      view = APIDeleteView(self.curAPI)
      await interaction.response.edit_message(embed=view.embed, view=view)
    
  @discord.ui.button(label='처음 화면으로', style=discord.ButtonStyle.primary)
  async def button_home(self, interaction: discord.Interaction, button: discord.ui.Button):
      view = FirstView()
      await interaction.response.edit_message(embed=view.embed, view=view)

class APIDeleteView(discord.ui.View):
  embed = discord.Embed(title="삭제할 API 선택", description='삭제할 API를 선택하고 삭제 버튼을 눌러주세요')
  delete_list = []
  def __init__(self, apiList:list):
    super().__init__()
    apiOptions=[]
    for api in apiList:
      apiOptions.append(discord.SelectOption(
        label=api.get(DBmanager.APITag.label)
      ))
    self.select_delete_API.options = apiOptions
  
  @discord.ui.select(placeholder="API 라벨")
  async def select_delete_API(self, interaction:discord.Interaction, select: discord.ui.Select):
    for option in self.select_delete_API.options:
      option.default = False
    
    self.delete_list = select.values
    
    options = self.select_delete_API.options
    for i in range(len(options)):
      if options[i].label in select.values:
        options[i].default = True
    
    self.select_delete_API.options = options
    await interaction.response.edit_message(embed=self.embed, view=self)
  
  @discord.ui.button(label='API 삭제', style=discord.ButtonStyle.red)
  async def button_delete_api(self, interaction: discord.Interaction, button: discord.ui.Button):
      dbManager = DBmanager.DBManager()
      
      for api_label in self.delete_list:
        dbManager.delete_api_by_label(interaction.user.id, api_label)
      
      await interaction.response.edit_message(content='API 삭제 완료', embed=None, view=None)
    
  @discord.ui.button(label='처음 화면으로', style=discord.ButtonStyle.primary)
  async def button_home(self, interaction: discord.Interaction, button: discord.ui.Button):
      view = FirstView()
      await interaction.response.edit_message(embed=view.embed, view=view)
  
class NotiAcceTypeView(discord.ui.View):
    embed = discord.Embed.from_dict(select_acce_type_message)
    def __init__(self, container):
      super().__init__()
      self.container = container
    
    @discord.ui.select(placeholder="장신구 종류",
                       min_values=1, max_values=1,
                       options=[
                          discord.SelectOption(
                              label="목걸이",
                              value=AccessoryType.necklace,
                              default=False
                          ),
                          discord.SelectOption(
                              label="귀걸이",
                              value=AccessoryType.earring,
                              default=False
                          ),
                          discord.SelectOption(
                              label="반지",
                              value=AccessoryType.ring,
                              default=False
                          ),
                       ])
    async def select_acce_type(self, interaction:discord.Interaction, select: discord.ui.Select): # the function called when the user is done selecting options
      # dataManager 받아와서 걔한테 데이터를 옮겨줘야 할 것 같다.
      # 선택한 값을 가져옴 (목걸이, 귀걸이, 팔찌) -> 검색 옵션 중에 저장함(dict 형태?). -> 나중에 검색 옵션 다 가져오면 그 값대로 검색
      #   dict를 하면 장점 - 저장이 쉽다. 단점 - key를 text로 하거나 enum으로 입력해야함. 나중에 문제 일으키기 쉬움
      #   class로 하면 장점 - 내가 직접 요소들 다 지정하면 문제 발견 쉬움 단점 - 하나의 인스턴스로 만들어서 계속 가지고 관리해야함. 싱글톤하면 처음 화면으로 돌아갈 때 문제가 될 것. 그냥 인스턴스면 어떻게 다음 과정으로 옮겨줄지 난감
      # 선택을 해야 다음 버튼 활성화. 선택 값을 조회해서 값이 유효하면 활성화 하는 방식으로 진행. 아니면 disable로 만들기
      for option in self.select_acce_type.options:
          option.default = False
      if len(select.values) != 0:
        self.button_next.disabled = False
        value = select.values[0]
        self.container.acceType = int(value)

        if int(value) == AccessoryType.necklace:
          self.select_acce_type.options[0].default = True
        elif int(value) == AccessoryType.earring:
          self.select_acce_type.options[1].default = True
        elif int(value) == AccessoryType.ring:
          self.select_acce_type.options[2].default = True
      await interaction.response.edit_message(embed=self.embed, view=self)
      # await interaction.response.defer()
    
    
    @discord.ui.button(label='<--', style=discord.ButtonStyle.primary)
    async def button_prev(self, interaction: discord.Interaction, button: discord.ui.Button):
      view = FirstView()
      await interaction.response.edit_message(embed=view.embed, view=view)
    
    @discord.ui.button(label='-->', style=discord.ButtonStyle.primary, disabled=True)
    async def button_next(self, interaction: discord.Interaction, button: discord.ui.Button):
      view = NotiMainOptView(self.container)
      await interaction.response.edit_message(embed=view.embed, view=view)
    
    @discord.ui.button(label='처음 화면으로', style=discord.ButtonStyle.primary)
    async def button_home(self, interaction: discord.Interaction, button: discord.ui.Button):
      view = FirstView()
      await interaction.response.edit_message(embed=view.embed, view=view)

class NotiMainOptView(discord.ui.View):
  embed = discord.Embed.from_dict(get_main_opt_message())
  def __init__(self, container, engrave: str='미입력' ):
    super().__init__()
    self.container = container
    self.input_engrave = self.search_engrave(engrave)
    self.embed=discord.Embed.from_dict(get_main_opt_message(self.input_engrave))
  
  def search_engrave(self, engrave):
    # 각인 값을 입력받고 스페이스 제거 후에 jsonobject에 있는지 확인
    # 없으면 다시 각인을 입력해달라고 리턴
    # 있으면 그 각인 이름으로 리턴
    if engrave == '미입력':
      return engrave

    classEngraveStr = [ x.get(TagType.text).replace(" ", "") for x in classEngrave]
    input_engrave = engrave.replace(" ", "")
    publicEngraveStr = [ x.get(TagType.text).replace(" ", "") for x in publicEngrave]
    
    if input_engrave in classEngraveStr:
      self.container.mainEngrave = classEngrave[classEngraveStr.index(input_engrave)].get(TagType.codeValue)
      return classEngrave[classEngraveStr.index(input_engrave)].get(TagType.text)
    elif input_engrave in publicEngraveStr:
      self.container.mainEngrave = publicEngrave[publicEngraveStr.index(input_engrave)].get(TagType.codeValue)
      return publicEngrave[publicEngraveStr.index(input_engrave)].get(TagType.text)
    wrong_message = "각인을 찾을 수 없습니다. 정확한 이름을 입력해주세요."
    return wrong_message

  
  @discord.ui.select(placeholder="각인 최소값",
                       min_values=1, max_values=1,
                       options=[
                          discord.SelectOption(
                              label="3",
                          ),
                          discord.SelectOption(
                              label="4",
                          ),
                          discord.SelectOption(
                              label="5",
                          ),
                          discord.SelectOption(
                              label="6",
                          ),
                       ])
  async def select_minEngrave(self, interaction, select):
    for option in self.select_minEngrave.options:
      option.default = False
    
    if len(select.values) != 0:
      self.container.mainEngraveMin = int(select.values[0])
      for option in self.select_minEngrave.options:
        if option.label == select.values[0]:
          option.default = True
    await interaction.response.edit_message(embed=self.embed, view=self)
  
  @discord.ui.select(placeholder="각인 최대값",
                       min_values=1, max_values=1,
                       options=[
                          discord.SelectOption(
                              label="3",
                          ),
                          discord.SelectOption(
                              label="4",
                          ),
                          discord.SelectOption(
                              label="5",
                          ),
                          discord.SelectOption(
                              label="6",
                          ),
                       ])
  async def select_maxEngrave(self, interaction, select):
    for option in self.select_maxEngrave.options:
      option.default = False
      
    if len(select.values) != 0:
      self.container.mainEngraveMax = int(select.values[0])
      for option in self.select_maxEngrave.options:
        if option.label == select.values[0]:
          option.default = True
    await interaction.response.edit_message(embed=self.embed, view=self)
  
  @discord.ui.button(label='각인 입력하기', style=discord.ButtonStyle.green)
  async def button_main_engrave(self, interaction: discord.Interaction, button: discord.ui.Button):
      modal = MainOptModal(self.container)
      await interaction.response.send_modal(modal)

  @discord.ui.button(label='<--', style=discord.ButtonStyle.primary)
  async def button_prev(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = NotiAcceTypeView(self.container)
    await interaction.response.edit_message(embed=view.embed, view=view)
  
  @discord.ui.button(label='-->', style=discord.ButtonStyle.primary)
  async def button_next(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = NotiEtcOptView(self.container)
    await interaction.response.edit_message(embed=view.embed, view=view)
  
  @discord.ui.button(label='처음 화면으로', style=discord.ButtonStyle.primary)
  async def button_home(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = FirstView()
    await interaction.response.edit_message(embed=view.embed, view=view)

class NotiEtcOptView(discord.ui.View):
  embed = discord.Embed.from_dict(get_etc_opt_message())
  def __init__(self, container, subEngrave:list = []):
    super().__init__()
    self.container = container
    self.embed = discord.Embed.from_dict(get_etc_opt_message(self.search_engraves(subEngrave)))
    self.select_subStat.disabled = not(self.container.isNecklace())
    
  def search_engraves(self, engraves:list):
    # 각인 값들을 입력받고 스페이스 제거 후에 jsonobject에 있는지 확인
    # 발견된 각인들을 리스트에 넣기. 없으면 리스트 비우기
    # 빈 리스트라면 입력된 각인이 없습니다.
    # 메인과 다른 점은 서브는 굳이 입력하지 않아도 된다는 점.
    # 따라서 처음에 빈 결과값 리스트를 만들고 검색되면 넣다가 마지막에 결과 리스트를 컨테이너로 전달. 여기서 컨테이너는 코드 리스트를 저장
    rst_code = []
    rst_text = []
    
    classEngraveStr = [ x.get(TagType.text).replace(" ", "") for x in classEngrave]
    input_engraves = [engrave.replace(" ", "") for engrave in engraves]
    publicEngraveStr = [ x.get(TagType.text).replace(" ", "") for x in publicEngrave]
    
    for input in input_engraves:
      if input in classEngraveStr:
        rst_code.append(classEngrave[classEngraveStr.index(input)].get(TagType.codeValue))
        rst_text.append(classEngrave[classEngraveStr.index(input)].get(TagType.text))
      elif input in publicEngraveStr:
        rst_code.append(publicEngrave[publicEngraveStr.index(input)].get(TagType.codeValue))
        rst_text.append(publicEngrave[publicEngraveStr.index(input)].get(TagType.text))
    self.container.subEngraves = rst_code
    if len(rst_text) == 0:
      return "입력된 각인이 없습니다."
    return rst_text
  
  @discord.ui.select(placeholder="각인 최소값",
                       min_values=0, max_values=1,
                       options=[
                          discord.SelectOption(
                              label="3",
                          ),
                          discord.SelectOption(
                              label="4",
                          ),
                          discord.SelectOption(
                              label="5",
                          ),
                          discord.SelectOption(
                              label="6",
                          ),
                       ])
  async def select_minEngrave(self, interaction, select):
    for option in self.select_minEngrave.options:
      option.default = False
    
    if len(select.values) != 0:
      self.container.subEngraveMin = int(select.values[0])
      for option in self.select_minEngrave.options:
        if option.label == select.values[0]:
          option.default = True
    else:
      self.container.subEngraveMin = 3
    await interaction.response.edit_message(embed=self.embed, view=self)
  
  @discord.ui.select(placeholder="각인 최대값",
                       min_values=0, max_values=1,
                       options=[
                          discord.SelectOption(
                              label="3",
                          ),
                          discord.SelectOption(
                              label="4",
                          ),
                          discord.SelectOption(
                              label="5",
                          ),
                          discord.SelectOption(
                              label="6",
                          ),
                       ])
  async def select_maxEngrave(self, interaction, select):
    for option in self.select_maxEngrave.options:
      option.default = False
      
    if len(select.values) != 0:
      self.container.subEngraveMax = int(select.values[0])
      for option in self.select_maxEngrave.options:
        if option.label == select.values[0]:
          option.default = True
    else:
      self.container.subEngraveMax = 6
    await interaction.response.edit_message(embed=self.embed, view=self)
  
  @discord.ui.select(placeholder="스탯",
                       min_values=1, max_values=1,
                       options=[
                          discord.SelectOption(
                              label="치명",
                          ),
                          discord.SelectOption(
                              label="특화",
                          ),
                          discord.SelectOption(
                              label="제압",
                          ),
                          discord.SelectOption(
                              label="신속",
                          ),
                          discord.SelectOption(
                              label="인내",
                          ),
                          discord.SelectOption(
                              label="숙련",
                          )
                       ])
  async def select_mainStat(self, interaction, select):
    for option in self.select_mainStat.options:
      option.default = False
    
    if len(select.values) != 0:
      rst = [ stat.get(TagType.codeValue) for stat in stat if select.values[0] == stat.get(TagType.text)]
      if len(rst) != 0:
        for option in self.select_mainStat.options:
          if option.label == select.values[0]:
            option.default = True
        self.container.mainStat = rst[0]
      else:
        raise IndexError("Main Stat result is not found in EtcOptView")
    await interaction.response.edit_message(embed=self.embed, view=self)
  
  @discord.ui.select(placeholder="목걸이용 서브 스탯",
                       min_values=1, max_values=1,
                       options=[
                          discord.SelectOption(
                              label="치명",
                          ),
                          discord.SelectOption(
                              label="특화",
                          ),
                          discord.SelectOption(
                              label="제압",
                          ),
                          discord.SelectOption(
                              label="신속",
                          ),
                          discord.SelectOption(
                              label="인내",
                          ),
                          discord.SelectOption(
                              label="숙련",
                          )
                       ])
  async def select_subStat(self, interaction, select):
    for option in self.select_subStat.options:
      option.default = False
    
    if len(select.values) != 0:
      rst = [ stat.get(TagType.codeValue) for stat in stat if select.values[0] == stat.get(TagType.text)]
      if len(rst) != 0:
        for option in self.select_subStat.options:
          if option.label == select.values[0]:
            option.default = True
        self.container.subStat = rst[0]
      else:
        raise IndexError("Sub Stat result is not found in EtcOptView")
    await interaction.response.edit_message(embed=self.embed, view=self)
  
  @discord.ui.button(label='각인 입력하기', style=discord.ButtonStyle.green)
  async def button_sub_engrave(self, interaction: discord.Interaction, button: discord.ui.Button):
    modal = EtcOptModal(self.container)
    await interaction.response.send_modal(modal)

  @discord.ui.button(label='<--', style=discord.ButtonStyle.primary)
  async def button_prev(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = NotiMainOptView(self.container)
    await interaction.response.edit_message(embed=view.embed, view=view)
  
  @discord.ui.button(label='-->', style=discord.ButtonStyle.primary)
  async def button_next(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = Noti2ndEtcOptView(self.container)
    await interaction.response.edit_message(embed=view.embed, view=view)
  
  @discord.ui.button(label='처음 화면으로', style=discord.ButtonStyle.primary)
  async def button_home(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = FirstView()
    await interaction.response.edit_message(embed=view.embed, view=view)

class EtcOptModal(discord.ui.Modal, title="서브 각인"):
  sub_1 = discord.ui.TextInput(label="서브 각인 1", required=False, placeholder="검색에 포함될 서브 각인을 입력해 주세요.")
  sub_2 = discord.ui.TextInput(label="서브 각인 2", required=False, placeholder="검색에 포함될 서브 각인을 입력해 주세요.")
  sub_3 = discord.ui.TextInput(label="서브 각인 3", required=False, placeholder="검색에 포함될 서브 각인을 입력해 주세요.")
  
  def __init__(self, container):
      super().__init__()
      self.container = container
  
  async def on_submit(self, interaction: discord.Interaction):
    subEngrave_list = [self.sub_1.value, self.sub_2.value, self.sub_3.value]
    view = NotiEtcOptView(self.container, subEngrave=[x for x in subEngrave_list if x != ""])
    await interaction.response.edit_message(embed=view.embed, view=view)

class MainOptModal(discord.ui.Modal, title="메인 각인"):
    mainEngrave = discord.ui.TextInput(label="메인 옵션을 입력해 주세요.", placeholder="검색에 반드시 포함될 메인 각인을 입력해 주세요.")
    
    def __init__(self, container):
      super().__init__()
      self.container = container

    async def on_submit(self, interaction: discord.Interaction):
        view = NotiMainOptView(self.container, engrave=self.mainEngrave.value)
        await interaction.response.edit_message(embed=view.embed, view=view)
  
class Noti2ndEtcOptView(discord.ui.View):
  embed = discord.Embed.from_dict(etc_2nd_option_message)
  
  def __init__(self, container):
    super().__init__()
    self.container = container
  
  @discord.ui.select(placeholder="품질",
                       min_values=1, max_values=1,
                       options=[
                          discord.SelectOption(
                              label="50 이상",
                              value=ItemGradeQuality.over50
                          ),
                          discord.SelectOption(
                              label="60 이상",
                              value=ItemGradeQuality.over60
                          ),
                          discord.SelectOption(
                              label="70 이상",
                              value=ItemGradeQuality.over70
                          ),
                          discord.SelectOption(
                              label="80 이상",
                              value=ItemGradeQuality.over80
                          ),
                          discord.SelectOption(
                              label="90 이상",
                              value=ItemGradeQuality.over90
                          )
                       ])
  async def select_quality(self, interaction, select):
    for option in self.select_quality.options:
      option.default = False
    
    if len(select.values) != 0:
      self.container.quality = select.values[0]
      for option in self.select_quality.options:
        if option.value == select.values[0]:
          option.default = True
    await interaction.response.edit_message(embed=self.embed, view=self)
  
  @discord.ui.select(placeholder="아이템 등급 (복수 선택 가능)",
                       min_values=1, max_values=2,
                       options=[
                          discord.SelectOption(
                              label="유물",
                              default = False
                          ),
                          discord.SelectOption(
                              label="고대",
                              default = False
                          )
                       ])
  async def select_item_grade(self, interaction, select):
    for i in range(len(self.select_item_grade.options)):
      self.select_item_grade.options[i].default = False
    
    if len(select.values) != 0:
      self.container.grade = select.values
      for i in range(len(self.select_item_grade.options)):
        if self.select_item_grade.options[i].label in select.values:
          self.select_item_grade.options[i].default = True
    await interaction.response.edit_message(embed=self.embed, view=self)
  
  @discord.ui.select(placeholder="정렬 기준",
                       min_values=1, max_values=1,
                       options=[
                          discord.SelectOption(
                              label="입찰가 기준",
                              value = SortOptionType.bidPrice
                          ),
                          discord.SelectOption(
                              label="구매가 기준",
                              value = SortOptionType.buyPrice,
                              default=True
                          )
                       ])
  async def select_sort_option(self, interaction, select):
    for option in self.select_sort_option.options:
      option.default = False
    
    if len(select.values) != 0:
      self.container.sort_option = select.values[0]
      if select.values[0] == SortOptionType.bidPrice:
        self.select_sort_option.options[0].default = True
      elif select.values[0] == SortOptionType.buyPrice:
        self.select_sort_option.options[1].default = True
    await interaction.response.edit_message(embed=self.embed, view=self)
  
  @discord.ui.button(label='<--', style=discord.ButtonStyle.primary)
  async def button_prev(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = NotiEtcOptView(self.container)
    await interaction.response.edit_message(embed=view.embed, view=view)
  
  @discord.ui.button(label='-->', style=discord.ButtonStyle.primary)
  async def button_next(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = OptionResultView(self.container)
    await interaction.response.edit_message(embed=view.embed, view=view)
  
  @discord.ui.button(label='처음 화면으로', style=discord.ButtonStyle.primary)
  async def button_home(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = FirstView()
    await interaction.response.edit_message(embed=view.embed, view=view)

class OptionResultView(discord.ui.View):  
  def __init__(self, container):
    super().__init__()
    self.container = container
    self.embed = discord.Embed(title="검색 옵션", description="다음과 같은 옵션으로 검색합니다.", color=discord.Color.random()) 
    self.embed.add_field(name="악세서리 종류", value=[x.get(AccessoryTagType.codeName) for x in accessory if x.get(AccessoryTagType.code) == self.container.acceType], inline=False)
    embMainEng=""
    for engrave in classEngrave+publicEngrave:
      if self.container.mainEngrave == engrave.get(TagType.codeValue):
        embMainEng = engrave.get(TagType.text)
    self.embed.add_field(name="메인 각인", value=embMainEng, inline=True)
    self.embed.add_field(name="각인 값 범위", value=f"{self.container.mainEngraveMin} ~ {self.container.mainEngraveMax}", inline=True)
  
    embSubEng=[]
    for engrave in publicEngrave+classEngrave:
      if engrave.get(TagType.codeValue) in self.container.subEngraves:
        embSubEng.append(engrave.get(TagType.text))
    self.embed.add_field(name="서브 각인", value=embSubEng if len(self.container.subEngraves) != 0 else "미입력" , inline=False)
    if len(self.container.subEngraves) != 0:
      self.embed.add_field(name="각인 값 범위", value=f"{self.container.subEngraveMin} ~ {self.container.subEngraveMax}", inline=True)
    
    self.embed.add_field(name="스탯", value=[x.get(TagType.text) for x in stat if x.get(TagType.codeValue) == self.container.mainStat], inline=False)
    if self.container.isNecklace():
      self.embed.add_field(name="부스탯", value=[x.get(TagType.text) for x in stat if x.get(TagType.codeValue) == self.container.subStat], inline=True)
    
    self.embed.add_field(name="품질", value=f"{int(self.container.quality)} 이상", inline = False)
    self.embed.add_field(name="아이템 등급", value=self.container.grade, inline=True)
    self.embed.add_field(name="정렬 기준", value="구매가 기준" if self.container.sort_option == SortOptionType.buyPrice else "입찰가 기준", inline=True)
  
  @discord.ui.button(label='검색', style=discord.ButtonStyle.green)
  async def button_search(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = SearchResultView(self.container)
    await interaction.response.edit_message(embed=view.embed, view=view)

  @discord.ui.button(label='처음 화면으로', style=discord.ButtonStyle.primary)
  async def button_home(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = FirstView()
    await interaction.response.edit_message(embed=view.embed, view=view)

class SearchResultView(discord.ui.View):
  def __init__(self, container):
    super().__init__()
    self.container = container
    self.embed = discord.Embed(title="검색 결과", description="\n\n", color=discord.Color.random())
    self.engine = SearchEngine(self.container)
    self.embed_list = pyllist.dllist()
    if self.engine.totalItemNum == 0:
      self.embed.add_field(name="검색 결과가 없습니다.", value=" ")
      self.button_next_rst.disabled = True
      self.button_prev_rst.disabled = True
    else:
      self.add_result_field()
        
  def add_result_field(self):
    if len(self.embed_list) != 0 and not self.embed in self.embed_list:
      raise IndexError('Cannot find embed message in SearchResultView')
    if len(self.embed_list) != 0 and self.embed != self.embed_list[-1]:
      embed_node = [n for n in self.embed_list.iternodes() if n.value == self.embed][0]
      self.embed = embed_node.next.value
      return

    results = self.engine.get_search_results()
    self.embed = discord.Embed(title="검색 결과", description="\n\n", color=discord.Color.random())
    
    if len(results) == 0:
      self.embed.add_field(name="검색 결과가 없습니다.", value=" ")
      return

    for result in results:
      print('results is : ', result)
      stats = []
      engraves = []
      for option in result.get(AuctionItemTagType.options):
        if option.get(ItemOptionTagType.type) == ItemOptionTagType.stat:
          stats.append(option)
        elif option.get(ItemOptionTagType.type) == ItemOptionTagType.engrave:
          engraves.append(option)
      
      if len(stats) < 1 or len(engraves) < 3:
        raise Exception("Cannot find stats or engraves in search results.")
      
      text =  f'입찰가 : {result.get(AuctionItemTagType.auctionInfo).get(AuctionInfoTagType.startPrice)} \t 구매가 : {result.get(AuctionItemTagType.auctionInfo).get(AuctionInfoTagType.buyPrice)} \n'
      text += f'품질 : {result.get(AuctionItemTagType.quality)}     {stats[0].get(ItemOptionTagType.optionName)} : {stats[0].get(ItemOptionTagType.values)}     '
      if len(stats) == 2:
        text += f'{stats[1].get(ItemOptionTagType.optionName)} : {stats[1].get(ItemOptionTagType.values)}'
      engraves.reverse() # 페널티가 맨 앞에 있어서 맨 마지막으로 변경. 이러면 3, 6, 페널티 각인 순서
      for engrave in engraves:
          text += f'\n{engrave.get(ItemOptionTagType.optionName)} : {engrave.get(ItemOptionTagType.values)}'

      self.embed.add_field(name=result.get(AuctionItemTagType.name), value = text, inline=False)
    
    self.embed_list.append(self.embed)
    
    

  @discord.ui.button(label='알림 설정', style=discord.ButtonStyle.green)
  async def button_noti(self, interaction: discord.Interaction, button: discord.ui.Button):
    modal = NotificationModal(self.container)
    await interaction.response.send_modal(modal)
    
  @discord.ui.button(label='이전 검색 결과', style=discord.ButtonStyle.primary, disabled=True)
  async def button_prev_rst(self, interaction: discord.Interaction, button: discord.ui.Button):
    if self.embed == self.embed_list[0]:
      raise IndexError("Cannot go previous result in SearchResultView")
    self.button_next_rst.disabled = False
    self.button_prev_rst.disabled = False
    
    embed_nodes = [n for n in self.embed_list.iternodes() if n.value == self.embed]
    if len(embed_nodes) == 0: # 검색 결과 없음이라 list에 없는 embed일 경우
      self.embed = self.embed_list.last()
      self.button_next_rst.disabled = True
    else:
      self.embed = embed_nodes[0].prev.value
    
    if self.embed == self.embed_list[0]:
      self.button_prev_rst.disabled=True
    if self.engine.isLastResult():
      self.button_next_rst.disabled = True
    await interaction.response.edit_message(embed=self.embed, view=self)
  
  @discord.ui.button(label='다음 검색 결과', style=discord.ButtonStyle.primary)
  async def button_next_rst(self, interaction: discord.Interaction, button: discord.ui.Button):
    self.add_result_field()
    self.button_next_rst.disabled = False
    self.button_prev_rst.disabled = False
    if self.engine.isLastResult():
      self.button_next_rst.disabled = True
    await interaction.response.edit_message(embed=self.embed, view=self)

  
class NotificationModal(discord.ui.Modal, title="알림 조건 가격"):
  price_condition = discord.ui.TextInput(label="알림 설정 가격", required=True, placeholder="해당 가격 이하인 매물이 생길 경우 메시지를 보냅니다.")
  
  def __init__(self, container):
    super().__init__()
    self.container = container

  async def on_submit(self, interaction: discord.Interaction):
    import DBmanager
    dbmanager = DBmanager.DBManager()
    
    try:
      price = int(self.price_condition.value)
    except ValueError:
      await interaction.response.send_message(content='숫자로만 입력해주세요', ephemeral=True)
    
    preset = DBmanager.PresetData()
    engine = SearchEngine(self.container)
    preset.edit_preset(DBmanager.PresetTag.search_option, [engine.make_search_option(), engine.subEngraveList])
    preset.edit_preset(DBmanager.PresetTag.condition, price)
    dbmanager.add_preset(interaction.user.id, preset)
    await interaction.response.send_message(content=f"알림 설정 완료!",  ephemeral=True)