import discord


message = {
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
    embed = discord.Embed.from_dict(message["embeds"])
    def __init__(self):
        super().__init__()
        

    @discord.ui.button(label='API키', style=discord.ButtonStyle.primary)
    async def button_api(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="api 버튼 클릭됨", embed=None)
      ## 메시지 수정하면 content, embed, view는 따로 가져가는 것 같다. 필요한 요소인 embed와 view만 수정하는 방식으로 진행하면 될 듯

    @discord.ui.button(label='알림 설정', style=discord.ButtonStyle.primary)
    async def button_noti(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="알림 설정 버튼 클릭됨", embed=None)
    
    @discord.ui.button(label='매물 검색', style=discord.ButtonStyle.primary)
    async def button_search(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="매물 검색 버튼 클릭됨", embed=None)
        
        
class APIView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.embed = None

    @discord.ui.button(label='등록한 API 확인', style=discord.ButtonStyle.primary)
    async def button_api(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="api 버튼 클릭됨", embed=None)
      ## 메시지 수정하면 content, embed, view는 따로 가져가는 것 같다. 필요한 요소인 embed와 view만 수정하는 방식으로 진행하면 될 것


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

  
    