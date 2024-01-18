import discord
from discord.ext import commands

TOKEN = 'MTE5NTk5OTk4NzU1ODAwMjcyOA.GD_GwW.dfcIp2XED8wAv_J53rw0qnb7VXPWGXtU1eCx1U'

# discord Client class를 생성합니다.
# client = discord.Client(intents=discord.Intents.default())
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='>', intents=intents)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        for channel in guild.text_channels:
            await channel.send('디코 봇 이제 켜짐')


embed = discord.Embed(
    title="Embed Title",
    description="Embed Description",
    color=0x42F56C  # Embed 색상 (16진수)
)

# 필요한 다양한 속성 추가 가능
embed.set_author(name="Author Name")
embed.add_field(name="Field Name 1", value="Field Value 1", inline=False)
embed.add_field(name="Field Name 2", value="Field Value 2", inline=True)
embed.set_footer(text="Embed Footer")

emb_Test = {
  "content": "Welcome to **Embed Generator**! 🎉 Create stunning embed messages for your Discord server with ease!\n\nIf you're ready to start, simply click on the \"Clear\" button at the top of the editor and create your own message.\n\nShould you need any assistance or have questions, feel free to join our [support server](/discord) where you can connect with our helpful community members and get the support you need.\n\nWe also have a [complementary bot](/invite) that enhances the experience with Embed Generator. Check out our [Discord bot](/invite) which offers features like formatting for mentions, channels, and emoji, creating reaction roles, interactive components, and more.\n\nLet your creativity shine and make your server stand out with Embed Generator! ✨",
  "tts": False,
  "embeds": 
    {
      "id": 10674342,
      "title": "Discord Bot Integration",
      "description": "Embed Generator offers a Discord bot integration that can further enhance your the functionality. While it is not mandatory for sending messages, having the bot on your server gives you access to a lot more features!\n\nHere are some key features of our bot:",
      "color": 2326507,
      "fields": [
        {
          "id": 472281785,
          "name": "Interactive Components",
          "value": "With our bot on your server you can add interactive components like buttons and select menus to your messages. Just invite the bot to your server, select the right server here on the website and you are ready to go!"
        },
        {
          "id": 608893643,
          "name": "Special Formatting for Mentions, Channels, and Emoji",
          "value": "With the /format command, our bot provides special formatting options for mentions, channel tags, and ready-to-use emoji. No more manual formatting errors! Simply copy and paste the formatted text into the editor."
        },
        {
          "id": 724530251,
          "name": "Recover Embed Generator Messages",
          "value": "If you ever need to retrieve a previously sent message created with Embed Generator, our bot can assist you. Right-click or long-press any message in your server, navigate to the apps menu, and select Restore to Embed Generator. You'll receive a link that leads to the editor page with the selected message."
        },
        {
          "id": 927221233,
          "name": "Additional Features",
          "value": "Our bot also supports fetching images from profile pictures or emojis, webhook management, and more. Invite the bot to your server and use the /help command to explore all the available features!"
        }
      ]
    }
  ,
  "components": [
    {
      "id": 807981180,
      "type": 1,
      "components": [
        {
          "id": 589661424,
          "type": 2,
          "style": 1,
          "label": "1번",
          "action_set_id": "600702400"
        },
        {
          "id": 507700772,
          "type": 2,
          "style": 1,
          "label": "2번",
          "action_set_id": "872029258"
        }
      ]
    }
  ],
  "actions": {
    "600702400": {
      "actions": []
    },
    "872029258": {
      "actions": []
    }
  }
}


class MyButtonView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # 버튼 생성
        self.add_item(discord.ui.Button(label='1번 버튼', custom_id='button_1'))
        self.add_item(discord.ui.Button(label='2번 버튼', custom_id='button_2'))

@bot.command()
async def button_command(ctx):
    # 메시지 생성
    message = await ctx.send('버튼 메시지입니다.', embed = embed, view=MyButtonView())

    # 버튼이 클릭될 때 실행될 콜백 함수
    async def button_callback(interaction: discord.Interaction):
        await interaction.response.send_message(f'버튼 {interaction.component.label}이(가) 클릭되었습니다!', ephemeral=True)

    # 버튼에 콜백 함수 등록
    bot.add_view(MyButtonView(), message, button_callback)

@bot.command()
async def test(ctx:commands.context):
    print(ctx)
    await ctx.send(content=emb_Test["content"],embed=discord.Embed.from_dict(emb_Test["embeds"]))

@bot.event
async def on_message(message):
    # 명령어가 봇 자신의 메시지일 경우 무시
    if message.author == bot.user:
        return

    # 명령어 처리를 위해 필요한 코드 추가
    await bot.process_commands(message)

bot.run(TOKEN)

# # event decorator를 설정하고 on_ready function을 할당해줍니다.
# @client.event
# async def on_ready():  # on_ready event는 discord bot이 discord에 정상적으로 접속했을 때 실행됩니다.
#     print('We have logged in as {}'.format(client))
#     print('Bot name: {}'.format(client.user.name))  # 여기서 client.user는 discord bot을 의미합니다. (제가 아닙니다.)
#     print('Bot ID: {}'.format(client.user.id))  # 여기서 client.user는 discord bot을 의미합니다. (제가 아닙니다.)

# # event decorator를 설정하고 on_message function을 할당해줍니다.
# @client.event
# async def on_message(message):
#     # message란 discord 채널에 올라오는 모든 message를 의미합니다.
#     # 따라서 bot이 보낸 message도 포함이되죠.
#     # 아래 조건은 message의 author가 bot(=clinet.user)이라면 그냥 return으로 무시하라는 뜻입니다.
#     if message.author == client.user:
#         return

#     # message를 보낸 사람이 bot이 아니라면 message가 hello로 시작하는 경우 채널에 Hello!라는 글자를 보내라는 뜻입니다.
#     elif message.content.startswith('hello'):
#         await message.channel.send('Hello!')

# 위에서 설정한 client class를 token으로 인증하여 실행합니다.

# client.run(discord_token)
