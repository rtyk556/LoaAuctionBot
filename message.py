from typing import Optional
import discord


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
          "value": " >> 검색에 필요한 API키를 입력하고 조회할 수 있습니다. 서버에서 상시로 APi를 통해 검색을 시도하기 때문에 다른 사이트(ex. Icepeng)에서 사용되지 않는 API 키를 입력해주세요\n"
        },
        {
          "id": 940685081,
          "name": "매물 검색",
          "value": ">> 아직 미구현 입니다\n"
        },
        {
          "id": 559602059,
          "name": "알림 설정",
          "value": ">> 알림 설정한 매물이 나타나면 디스코드 봇이 메시지를 보냅니다.\n"
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

# button_components = [
#   [
#     discord.ui.Button(style=discord.ButtonStyle.blurple, label="파란 버튼"),
#     discord.ui.Button(style=discord.ButtonStyle.red, label="빨간 버튼"),
#   ]
# ]

# class FirstPage(discord.ui.View):
#   def __init__(self):
#     super().__init__()

#   @discord.ui.button(label='API키',  style=discord.ButtonStyle.primary)
#   async def button_api(self, button: discord.ui.Button, interaction: discord.Interaction):
#     await interaction.message.edit(content="api버튼 클릭됨")
    
  
#   @discord.ui.button(label='매물 검색', style=discord.ButtonStyle.primary)
#   async def button_search(self, button: discord.ui.Button, interaction: discord.Interaction):
#     await interaction.message.edit(content="매물 검색 버튼 클릭됨")
  
#   @discord.ui.button(label='알림 설정', style=discord.ButtonStyle.primary)
#   async def button_noti(self, button: discord.ui.Button, interaction: discord.Interaction):
#     await interaction.message.edit(content="알림 설정 버튼 클릭됨")

class FirstView(discord.ui.View):
  # __instance = None
  
  embed = discord.Embed.from_dict(first_message["embeds"])
  def __init__(self):
      # if FirstView.__instance:
      #   self.getInstance()
      super().__init__()
    
  # @classmethod
  # def getInstance(cls):
  #   if not cls.__instance:
  #     cls.__instance = FirstView()
  #   return cls.__instance

  @discord.ui.button(label='API키', style=discord.ButtonStyle.primary)
  async def button_api(self, interaction: discord.Interaction, button: discord.ui.Button):
    ## 메시지 수정하면 content, embed, view는 따로 가져가는 것 같다. 필요한 요소인 embed와 view만 수정하는 방식으로 진행하면 될 듯
    view = APIView()
    await interaction.response.edit_message(embed=view.embed, view=view)
    

  @discord.ui.button(label='알림 설정', style=discord.ButtonStyle.primary)
  async def button_notification(self, interaction: discord.Interaction, button: discord.ui.Button):
    await interaction.response.edit_message(content="알림 설정 버튼 클릭됨", embed=None)
  
  @discord.ui.button(label='매물 검색', style=discord.ButtonStyle.primary)
  async def button_search(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = NotiAcceTypeView()
    await interaction.response.edit_message(embed=view.embed, view=view)
        
        
class APIView(discord.ui.View):
    embed = discord.Embed.from_dict(api_message)
    def __init__(self):
        super().__init__()
        

    @discord.ui.button(label='API 조회', style=discord.ButtonStyle.primary)
    async def button_check_api(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="api 버튼 클릭됨", embed=None)
     
    @discord.ui.button(label='API 등록', style=discord.ButtonStyle.primary)
    async def button_register_api(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="api 버튼 클릭됨", embed=None)
    
    @discord.ui.button(label='처음 화면으로', style=discord.ButtonStyle.primary)
    async def button_home(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = FirstView()
        await interaction.response.edit_message(embed=view.embed, view=view)
    
class NotiAcceTypeView(discord.ui.View):
    # __instance = None
    embed = discord.Embed.from_dict(select_acce_type_message)
    def __init__(self):
      # if NotiAcceTypeView.__instance:
      #   self.getInstance()
      super().__init__()
    
    # @classmethod
    # def getInstance(cls):
    #   if not cls.__instance:
    #     cls.__instance = NotiAcceTypeView()
    #   return cls.__instance
    
    @discord.ui.select(placeholder="장신구 종류",
                       min_values=1, max_values=3,
                       options=[
                          discord.SelectOption(
                              label="목걸이",
                          ),
                          discord.SelectOption(
                              label="귀걸이",
                          ),
                          discord.SelectOption(
                              label="팔찌",
                          ),
                       ])
    async def select_callback(self, interaction, select): # the function called when the user is done selecting options
      # dataManager 받아와서 걔한테 데이터를 옮겨줘야 할 것 같다.
      pass
    
    
    @discord.ui.button(label='<--', style=discord.ButtonStyle.primary)
    async def button_prev(self, interaction: discord.Interaction, button: discord.ui.Button):
      view = FirstView()
      await interaction.response.edit_message(embed=view.embed, view=view)
      # view = FirstView.getInstance()
      # await interaction.response.edit_message(embed=view.embed, view = view)
    
    @discord.ui.button(label='-->', style=discord.ButtonStyle.primary)
    async def button_next(self, interaction: discord.Interaction, button: discord.ui.Button):
      view = NotiMainOptView()
      await interaction.response.edit_message(embed=view.embed, view=view)
      # await interaction.response.edit_message(content="Not implemented", embed=None)
    
    @discord.ui.button(label='처음 화면으로', style=discord.ButtonStyle.primary)
    async def button_home(self, interaction: discord.Interaction, button: discord.ui.Button):
      view = FirstView()
      await interaction.response.edit_message(embed=view.embed, view=view)

class NotiMainOptView(discord.ui.View):
  embed = discord.Embed.from_dict(get_main_opt_message())
  def __init__(self, engrave: str='미입력' ):
    super().__init__()
    self.embed=discord.Embed.from_dict(get_main_opt_message(engrave))
  
  def search_engrave(self, engrave):
    pass
  
  @discord.ui.select(placeholder="각인 최소값",
                       min_values=1, max_values=1,
                       options=[
                          discord.SelectOption(
                              label="제한 없음",
                          ),
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
      # dataManager 받아와서 걔한테 데이터를 옮겨줘야 할 것 같다.
      pass
  
  @discord.ui.select(placeholder="각인 최대값",
                       min_values=1, max_values=1,
                       options=[
                          discord.SelectOption(
                              label="제한 없음",
                          ),
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
      # dataManager 받아와서 걔한테 데이터를 옮겨줘야 할 것 같다.
      pass
  
  @discord.ui.button(label='각인 입력하기', style=discord.ButtonStyle.primary)
  async def button_main_engrave(self, interaction: discord.Interaction, button: discord.ui.Button):
      modal = MainOptModal()
      await interaction.response.send_modal(modal)

  @discord.ui.button(label='<--', style=discord.ButtonStyle.primary)
  async def button_prev(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = NotiAcceTypeView()
    await interaction.response.edit_message(embed=view.embed, view=view)
  
  @discord.ui.button(label='-->', style=discord.ButtonStyle.primary)
  async def button_next(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = NotiEtcOptView()
    await interaction.response.edit_message(embed=view.embed, view=view)
  
  @discord.ui.button(label='처음 화면으로', style=discord.ButtonStyle.primary)
  async def button_home(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = FirstView()
    await interaction.response.edit_message(embed=view.embed, view=view)

class NotiEtcOptView(discord.ui.View):
  embed = discord.Embed.from_dict(get_etc_opt_message())
  def __init__(self, subEngrave:list = []):
    super().__init__()
    self.embed = discord.Embed.from_dict(get_etc_opt_message(subEngrave))

  @discord.ui.select(placeholder="각인 최소값",
                       min_values=1, max_values=1,
                       options=[
                          discord.SelectOption(
                              label="제한 없음",
                          ),
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
      # dataManager 받아와서 걔한테 데이터를 옮겨줘야 할 것 같다.
      pass
  
  @discord.ui.select(placeholder="각인 최대값",
                       min_values=1, max_values=1,
                       options=[
                          discord.SelectOption(
                              label="제한 없음",
                          ),
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
      # dataManager 받아와서 걔한테 데이터를 옮겨줘야 할 것 같다.
      pass
  
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
      # dataManager 받아와서 걔한테 데이터를 옮겨줘야 할 것 같다.
      pass
  
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
      # dataManager 받아와서 걔한테 데이터를 옮겨줘야 할 것 같다.
      pass
  
  @discord.ui.button(label='각인 입력하기', style=discord.ButtonStyle.primary)
  async def button_sub_engrave(self, interaction: discord.Interaction, button: discord.ui.Button):
    modal = EtcOptModal()
    await interaction.response.send_modal(modal)

  @discord.ui.button(label='<--', style=discord.ButtonStyle.primary)
  async def button_prev(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = NotiMainOptView()
    await interaction.response.edit_message(embed=view.embed, view=view)
  
  @discord.ui.button(label='-->', style=discord.ButtonStyle.primary)
  async def button_next(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = Noti2ndEtcOptView()
    await interaction.response.edit_message(embed=view.embed, view=view)
  
  @discord.ui.button(label='처음 화면으로', style=discord.ButtonStyle.primary)
  async def button_home(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = FirstView()
    await interaction.response.edit_message(embed=view.embed, view=view)

class EtcOptModal(discord.ui.Modal, title="서브 각인"):
  sub_1 = discord.ui.TextInput(label="서브 각인 1", required=False, placeholder="검색에 포함될 서브 각인을 입력해 주세요.")
  sub_2 = discord.ui.TextInput(label="서브 각인 2", required=False, placeholder="검색에 포함될 서브 각인을 입력해 주세요.")
  sub_3 = discord.ui.TextInput(label="서브 각인 3", required=False, placeholder="검색에 포함될 서브 각인을 입력해 주세요.")
  
  async def on_submit(self, interaction: discord.Interaction):
    subEngrave_list = [self.sub_1.value, self.sub_2.value, self.sub_3.value]
    view = NotiEtcOptView(subEngrave=[x for x in subEngrave_list if x != ""])
    await interaction.response.edit_message(embed=view.embed, view=view)

class MainOptModal(discord.ui.Modal, title="메인 각인"):
    mainEngrave = discord.ui.TextInput(label="메인 옵션을 입력해 주세요.", placeholder="검색에 반드시 포함될 메인 각인을 입력해 주세요.")
    
    async def on_submit(self, interaction: discord.Interaction):
        view = NotiMainOptView(engrave=self.mainEngrave)
        await interaction.response.edit_message(embed=view.embed, view=view)
  
class Noti2ndEtcOptView(discord.ui.View):
  embed = discord.Embed.from_dict(etc_2nd_option_message)
  
  def __init__(self):
    super().__init__()
  
  @discord.ui.select(placeholder="품질",
                       min_values=1, max_values=1,
                       options=[
                          discord.SelectOption(
                              label="제한 없음",
                          ),
                          discord.SelectOption(
                              label="50 이상",
                          ),
                          discord.SelectOption(
                              label="60 이상",
                          ),
                          discord.SelectOption(
                              label="70 이상",
                          ),
                          discord.SelectOption(
                              label="80 이상",
                          ),
                          discord.SelectOption(
                              label="90 이상",
                          )
                       ])
  async def select_quality(self, interaction, select):
      # dataManager 받아와서 걔한테 데이터를 옮겨줘야 할 것 같다.
      pass
  
  @discord.ui.select(placeholder="아이템 등급 (복수 선택 가능)",
                       min_values=1, max_values=2,
                       options=[
                          discord.SelectOption(
                              label="유물",
                          ),
                          discord.SelectOption(
                              label="고대",
                          )
                       ])
  async def select_item_grade(self, interaction, select):
      # dataManager 받아와서 걔한테 데이터를 옮겨줘야 할 것 같다.
      pass
  
  @discord.ui.select(placeholder="정렬 기준",
                       min_values=1, max_values=1,
                       options=[
                          discord.SelectOption(
                              label="입찰가 기준",
                          ),
                          discord.SelectOption(
                              label="구입가 기준",
                          )
                       ])
  async def select_sort_option(self, interaction, select):
      # dataManager 받아와서 걔한테 데이터를 옮겨줘야 할 것 같다.
      pass
  
  @discord.ui.button(label='<--', style=discord.ButtonStyle.primary)
  async def button_prev(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = NotiEtcOptView()
    await interaction.response.edit_message(embed=view.embed, view=view)
  
  @discord.ui.button(label='-->', style=discord.ButtonStyle.primary)
  async def button_next(self, interaction: discord.Interaction, button: discord.ui.Button):
    await interaction.response.edit_message(content="Not implemented", embed=None)
  
  @discord.ui.button(label='처음 화면으로', style=discord.ButtonStyle.primary)
  async def button_home(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = FirstView()
    await interaction.response.edit_message(embed=view.embed, view=view)
  

# class SearchAuctionButton(discord.ui.view):
#   def __init__(self):
#     super.__init__()
  
#   @discord.ui.Button(label='매물 검색', style=discord.ButtonStyle.primary)
#   async def button_search(self, button: discord.ui.Button, interaction: discord.Interaction):
#     pass

# class SearchAuctionButton(discord.ui.view):
#   def __init__(self):
#     super.__init__()
  
#   @discord.ui.Button(label='알림 설정', style=discord.ButtonStyle.primary)
#   async def button_noti(self, button: discord.ui.Button, interaction: discord.Interaction):
#     pass

  
    