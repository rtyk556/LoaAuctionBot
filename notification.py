from discord.ext import tasks, commands
from DBmanager import DBManager, PresetData, PresetTag, DBDataTag, get_valid_api
from searchengine import SearchEngine, get_preset_result
import discord
from jsonobject import AuctionItemTagType, ItemOptionTagType, AuctionInfoTagType

import requests

@tasks.loop(seconds=60)
async def noti_loop(bot:commands.Bot):
    response = requests.get('http://localhost:5000/api/noti')
    
    if response.status_code == 200:
       noti_list = response.json()
       for noti in noti_list:
          await send_rst_dm(bot, noti[0], noti[1])      
    else:
       raise Exception('Cannot get response from api')

async def send_rst_dm(bot:commands.Bot, user, rst):
    user = await bot.fetch_user(user.get(DBDataTag.user_id))
    embed = discord.Embed(title="검색 결과", description="\n\n", color=discord.Color.random())
    
    for result in rst:
      stats = []
      engraves = []
      for option in result.get(AuctionItemTagType.options):
        if option.get(ItemOptionTagType.type) == ItemOptionTagType.stat:
          stats.append(option)
        elif option.get(ItemOptionTagType.type) == ItemOptionTagType.engrave:
          engraves.append(option)
      
      text =  f'입찰가 : {result.get(AuctionItemTagType.auctionInfo).get(AuctionInfoTagType.startPrice)} \t 구매가 : {result.get(AuctionItemTagType.auctionInfo).get(AuctionInfoTagType.buyPrice)} \n'
      text += f'품질 : {result.get(AuctionItemTagType.quality)}     {stats[0].get(ItemOptionTagType.optionName)} : {stats[0].get(ItemOptionTagType.values)}     '
      if len(stats) == 2:
        text += f'{stats[1].get(ItemOptionTagType.optionName)} : {stats[1].get(ItemOptionTagType.values)}'
      engraves.reverse() # 페널티가 맨 앞에 있어서 맨 마지막으로 변경. 이러면 3, 6, 페널티 각인 순서
      for engrave in engraves:
          text += f'\n{engrave.get(ItemOptionTagType.optionName)} : {engrave.get(ItemOptionTagType.values)}'
      embed.add_field(name=result.get(AuctionItemTagType.name), value = text, inline=False)
    
    if user.dm_channel:
        await user.dm_channel.send(content=f'알림 설정 매물 발견! \n', embed=embed)
    else:
        channel = await user.create_dm()
        await channel.send(content=f'알림 설정 매물 발견! \n', embed=embed)