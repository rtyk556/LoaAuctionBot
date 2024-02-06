from discord.ext import tasks, commands
from DBmanager import DBManager, PresetData, PresetTag, DBDataTag, get_valid_api
from searchengine import SearchEngine, get_preset_result
import discord
from jsonobject import AuctionItemTagType, ItemOptionTagType, AuctionInfoTagType

@tasks.loop(seconds=60)
async def noti_loop(bot:commands.Bot):
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
                    await send_rst_dm(bot, users[user_idx], noti_rst)
            
            users[user_idx][DBDataTag.api] = api_list
            users[user_idx][DBDataTag.preset] = user_presets
            
    dbmanger.save_user_info(users)

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
        await channel.send(content=f'첫 알림 - 알림 설정 매물 발견! \n', embed=embed)