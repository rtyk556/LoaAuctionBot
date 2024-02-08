import discord
from discord.ext import commands, tasks
import token_value
import message
import notification

TOKEN = token_value.BOT_TOKEN

# discord Client class를 생성합니다.
# client = discord.Client(intents=discord.Intents.default())
intents = discord.Intents.all()

class AuctionBot(commands.Bot):
    def __init__(self, prefix, intents):
        super().__init__(command_prefix=prefix ,intents=intents)
    
    async def setup_hook(self):
        await self.tree.sync()

bot = AuctionBot('>', intents=intents)

@bot.event
async def on_ready():
    print('Start Auction Bot')
    notification.noti_loop.start(bot)

@bot.tree.command(name='start', description='경매장 봇 명령어 테스트')
async def start(interaction:discord.Interaction):
    from message import FirstView
    view = FirstView()
    await interaction.response.send_message(embed=view.embed, view=view, ephemeral=True)

@bot.event
async def on_message(message):
    # 명령어가 봇 자신의 메시지일 경우 무시
    if message.author == bot.user:
        return

    # 명령어 처리를 위해 필요한 코드 추가
    await bot.process_commands(message)

bot.run(TOKEN)
