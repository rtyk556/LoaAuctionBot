from discord.ext import tasks, commands
from DBmanager import DBManager, PresetData, PresetTag, DBDataTag, get_valid_api


@tasks.loop(seconds=60)
async def noti_loop(bot:commands.Bot):
    dbmanger = DBManager()
    users = dbmanger.get_all_users()
    
    for user in users:
        # preset 존재하는지 확인
        # 추후엔 길드가 봇에게 있는 길드인지 확인
        if len(user.get(DBDataTag.preset)) != 0:
            # check api validity
            api = get_valid_api(user.get(DBDataTag.api))
            if len(api) == 0:
                continue
            
            user_presets = user.get(DBDataTag.preset)
            for preset in user_presets:
                pass
                # 모든 프리셋 검색 시작.
                # 한 프리셋의 경우, 우선 가능한 api key 찾기.
                # 가능한 api key로 새로운 search_engine 만들기
                # search_engine에서 프리셋과 api키를 입력받음. -> [ 결과 리스트 ]
                #   valid한 키인지 리턴은 api 쪽이 알려줌. 그 값으로 preset으로 검색 -> 결과 넣기
                #   중간에 429 request -> 다음 api 얻어내기. 유효한 값 없다면 다음 유저
    # user = await bot.fetch_user(332152344060100608) # 사용자 ID를 통해 사용자 객체를 가져옵니다.
    # if user:
    #     channel = await user.create_dm() # 사용자와의 DM 채널을 생성합니다.
    #     await channel.send('테스트 메시지 30초 반복')