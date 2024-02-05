import token_value
from jsonobject import *
import requests
import math

Token = token_value.API_TOKEN

headers = {
    'accept' : 'application/json',
    'authorization' : Token
}

url = 'https://developer-lostark.game.onstove.com/auctions/items'

# 검색 엔진 활용법
# 검색 결과 뷰에서 검색 엔진 클래스 가져옴
# 검색 엔진 클래스는 init 될 때 각 검색 옵션들을 가져옴.
# 가져온 검색 결과에 따라 search option을 만들기
#   고정인 옵션 : 품질, 정렬 기준, 주스탯, 메인 각인, 아이템 티어, sortcondition
#   변동 옵션
#       - 악세 카테고리 -> 개수 확인하고 1개면 바로 입력, 여러개면 비우고 따로 검출할 리스트 만들기 -> 이건 고정하는게 나을듯? 안그러면 목걸이 매물이 말도 안될듯
#       - 부스탯 -> 목걸이고 입력된 값 있으면 추가
#       - 서브 각인들 -> 한개면 바로 검색옵션으로 추가, 아니면 비우고 따로 검출할 리스트 생성. 범위 값도 유도할 수 있도록
#       - 아이템 등급 -> 한개면 바로 검색옵션으로 추가, 여러개면 그냥 없애고 등급 상관없이 결과 보이면 될 것.
# 검색 옵션 생성 후에 request -> response 획득 -> response를 후처리 리스트에 다시 적용 -> 결과 페이지 도출
# 검색은 우선 한 페이지씩 시도. 여기서 한 페이지는 디코에서 보여줄 페이지. 다음 페이지 버튼 누를 시 그 다음 결과 도출 시도.
# 몇 개씩 끊어서 보여줄까.. 우선 이 점은 나중에 테스트 할듯. 지금 생각은 5개, 10개 정도.
# progress bar는 검색 진행도에 따라? 우선순위 낮음

# search engine이 하나의 인스턴스로서 검색 정보를 담고 있어야 한다.
# 한 순간의 정보를 프리셋 형태로 저장하기 위해서 init에서 정보를 담아야 한다. 이 때 pageNum은 좀 더 고려

# 알림 설정 버튼을 누르면, 해당 검색 엔진에 담긴 옵션 정보와 user_id, api_key를 저장해서 bot.loop를 통해 계속 task가 돌아가야 한다.


class SearchEngine():
    def __init__(self):
        self.subEngraveList = []
        self.totalItemNum = -1
        self.totalPageIndex = 0
        self.curPageIndex = 0
        self.curItemIndex = 0
        self.loaPageSize = 10
        self.botPageSize = 5
    
    def make_search_option(self, pageNum=1):
        container = SearchOptionContainer()
        basic_search_option = {
        'ItemGradeQuality' : container.quality,
        'Sort': container.sort_option,
        'CategoryCode': container.acceType,
        'EtcOptions' : [
            {
                "FirstOption" : 2, # 2는 전투 특성
                "SecondOption" : container.mainStat, 
                "MinValue" : None,
                "MaxValue" : None
            },
            {
                "FirstOption" : 3, # 3은 각인
                "SecondOption" : container.mainEngrave, 
                "MinValue" : container.mainEngraveMin,
                "MaxValue" : container.mainEngraveMax,
            }
            ],
            'ItemTier': 3,
            'PageNo' : pageNum,
            'SortCondition': 'ASC',
        }
        
        if container.isNecklace() and container.subStat != None:
            basic_search_option['EtcOptions'].append({
                "FirstOption" : 2,
                "SecondOption" : container.subStat, 
                "MinValue" : None,
                "MaxValue" : None
            })
        
        if len(container.subEngraves) == 1:
            basic_search_option['EtcOptions'].append(
                {
                    "FirstOption" : 3,
                    "SecondOption" : container.subEngraves[0], 
                    "MinValue" : container.subEngraveMin,
                    "MaxValue" : container.subEngraveMax,
                }
            )
        else:
            engraveName = []
            for engrave in container.subEngraves:
                for x in classEngrave+publicEngrave:
                    if x.get(TagType.codeValue) == engrave:
                        engraveName.append(x.get(TagType.text))
            self.subEngraveList = engraveName
        
        if len(container.grade) == 1:
            basic_search_option['ItemGrade'] = container.grade[0]
        return basic_search_option
    
    def get_search_results(self):
        url = 'https://developer-lostark.game.onstove.com/auctions/items'
        
        if self.totalItemNum == -1:
            response = requests.post(url, headers=headers, json=self.make_search_option())
            try:
                self.totalItemNum = response.json().get(ResponseJsonTagType.totalCount)
                self.totalPageIndex = math.ceil(self.totalItemNum/self.loaPageSize)
            except Exception as e:
                print('Error has occured in get_search_results : ', e)
        rst = []
        
        if self.totalItemNum != 0:
            curPageIndex = 0
            curItemIndex = 0
            self.curPageIndex, self.curItemIndex = self.get_next_index()
            if self.curPageIndex == None or self.curItemIndex == None:
                return []
            for curPageIndex in range(self.curPageIndex, self.totalPageIndex):    
                response = requests.post(url, headers=headers, json=self.make_search_option(pageNum=curPageIndex+1))
                if response.status_code == 200:
                    json = response.json()
                    items = json.get(ResponseJsonTagType.items)
                    
                    for curItemIndex in range(self.curItemIndex, len(items)):
                        if self.subEngraveList == [] and not items[curItemIndex] in rst:
                            rst.append(items[curItemIndex])
                        else:
                            item_options = items[curItemIndex].get(AuctionItemTagType.options)
                            for option in item_options:
                                if option.get(ItemOptionTagType.type) == ItemOptionTagType.engrave and option.get(ItemOptionTagType.optionName) in self.subEngraveList and not items[curItemIndex] in rst:
                                    rst.append(items[curItemIndex])
                                    break
                        if len(rst) >= self.botPageSize:
                            self.curPageIndex = curPageIndex
                            self.curItemIndex = curItemIndex
                            return rst
                elif response.status_code == 429: # too much requests
                    raise Exception("API Requests has exceeded limits.")
        
        self.curPageIndex = curPageIndex
        self.curItemIndex = curItemIndex
        return rst
    
    def isFirstResult(self):
        return self.curItemIndex == 0 and self.curPageIndex == 0
    
    def isLastResult(self):
        return self.curItemIndex == None or self.curItemIndex == None
    
    def get_next_index(self):
        print('cur index : ', (self.curPageIndex, self.curItemIndex))
        if self.curPageIndex == 0 and self.curItemIndex == 0:
            return (0,0)
        elif ((self.curPageIndex)*self.loaPageSize + self.curItemIndex+1) == self.totalItemNum: # 마지막 아이템
            return (None, None)
        elif self.curItemIndex == (self.loaPageSize - 1): # 한 페이지 마지막 아이템
            return (self.curPageIndex+1, 0)
        return (self.curPageIndex, self.curItemIndex+1)


def get_preset_result(preset:dict, api_list:list):
    # preset에서는 search_option, subengraves, condition, history 존재
    # api는 key와 valid_time 존재
    # api에 맞는 header를 생성
    import DBmanager
    import datetime
    
    rst = []
    if len(api_list) == 0:
        raise Exception('Cannot find api list.')
    headers = {
        'accept' : 'application/json',
        'authorization' : 'bearer ' + api_list[0][DBmanager.APITag.key]
    }
    loaPageSize = 10
    #가능한 api 하나로 작업하다가 안되면 다음으로 넘어가야 한다. 어떻게 429마다 시도하고 넘어가는게 좋을까?
    # 1. api list에서 for문으로 작성하고, response에서 429가 뜨면 continue, 그 다음 api 가져와서 이어 나가는건?
    # pageIndex와 itemIndex를 for문 밖에 저장, loop 돌면서 기억. 아마 다음 pageIndex 가져올 때 오류가 날 것이기 때문에 itemIndex는 필요 없을듯
    # 가격 조건보다 더 큰 매물이 다음 매물이면 break든 리턴이든 해도 됨
    # 가격 조건 맞는 매물 확인되면 검색 기록에 있는지 확인, 검색 기록
    # 검색기록 업데이트는? 조건 아래 매물들 따로 리스트 만들고 이후 검색 기록과 비교 -> 검색 기록 매물이 현 매물 리스트에 없으면 검색 기록 삭제, 일치하면 최종 결과 리스트에서도 삭제
    # ex) 검색 기록 [ 1, 2, 3] 최근 [ 2, 3, 4, 5] -> 1은 최근에 없으니 검색 기록에서 삭제. 2는 최근에 있으니 최근에서 2는 삭제. 3은 최근에 있으니 최근에서 삭제. 결과 -> 4, 5 알림 올리기, 검색 기록 - [2, 3, 4, 5]
    response = requests.post(url, headers=headers, json=preset[DBmanager.PresetTag.search_option][0])
    print('first response for getting total item num : ', response.status_code)
    try:
        totalItemNum = response.json().get(ResponseJsonTagType.totalCount)
        totalPageIndex = math.ceil(totalItemNum/loaPageSize)
    except:
        print('Error has occured in get_preset_result. ', response.status_code)
    
    curPageIndex = 0
    
    foundAllItem = False
    for api in api_list:
        getNextAPI = False
        headers = {
            'accept' : 'application/json',
            'authorization' : 'bearer ' + api[DBmanager.APITag.key]
        }
        if totalItemNum != 0:
            print('total item num is : ', totalItemNum)
            for curPageIndex in range(curPageIndex, totalPageIndex):
                response = requests.post(url, headers=headers, json=preset[DBmanager.PresetTag.search_option][0])
                print('response status : ', response.status_code)
                if response.status_code == 429:
                    getNextAPI = True
                    break
                elif response.status_code == 200:
                    json = response.json()
                    items = json.get(ResponseJsonTagType.items)
                    
                    for idx in range(0, len(items)):
                        # 가격 조건보다 높아진 매물이 등장하면 loop 탈출
                        itemOptions = items[idx].get(AuctionItemTagType.auctionInfo)
                        if preset[DBmanager.PresetTag.search_option][0].get('Sort') == SortOptionType.buyPrice:
                            itemPrice = itemOptions.get(AuctionInfoTagType.buyPrice)
                        else:
                            itemPrice = itemOptions.get(AuctionInfoTagType.startPrice)
    
                        if itemPrice > preset[DBmanager.PresetTag.condition]:
                            foundAllItem = True
                            break
                        
                        # subengrave list 확인
                        subengrave_list = preset[DBmanager.PresetTag.search_option][1]
                        if subengrave_list == [] and not items[idx] in rst:
                            rst.append(items[idx])
                        else:
                            for option in itemOptions:
                                if option.get(ItemOptionTagType.type) == ItemOptionTagType.engrave and option.get(ItemOptionTagType.optionName) in subengrave_list and not items[idx] in rst:
                                    rst.append(items[idx])
                                    break
                else:
                    raise Exception('Cannot get response from API. ', response.status_code)
                if foundAllItem:
                    break
            # 결과 비교 및 기록 업데이트
            search_history = preset[DBmanager.PresetTag.search_history]
            for history in search_history:
                if history in rst:
                    # 이미 알린 적 있는 매물이니 rst에서 삭제
                    rst.remove(history)
                elif history not in rst:
                    # 최근 매물에 해당 기록이 없으니 검색 기록에서 해당 기록 삭제
                    search_history.remove(history)
            search_history.extend(rst)
            # api, preset 관련 json 파일 수정 필요
            preset[DBmanager.PresetTag.search_history] = search_history
            return rst
        elif totalItemNum == 0:
            return rst        
        if getNextAPI:
            valid_time = datetime.datetime.now() + datetime.timedelta(seconds=60)
            time_str = valid_time.strftime("%Y-%m-%d %H:%M:%S")
            api[DBmanager.APITag.valid_time] = time_str
            continue

    return rst