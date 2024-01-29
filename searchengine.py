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
        self.totalItemNum = 0
        self.curPageIndex = 0
        self.curItemIndex = 0
    
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
            # {
            #     "FirstOption" : 3,
            #     "SecondOption" : 141, # 141은 예둔
            #     "MinValue" : 3,
            #     "MaxValue" : None
            # }
            ],
            'ItemTier': 3,
            # 'ItemGrade': '고대',
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
        
        if len(container.subEngraves) == 0:
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
        loaPageSize = 10
        botPageSize = 5
        
        if self.totalItemNum == 0:
            response = requests.post(url, headers=headers, json=self.make_search_option())
            try:
                self.totalItemNum = response.json().get(ResponseJsonTagType.totalCount)
            except Exception as e:
                print('Error has occured in get_search_results : ', e)
        rst = []
        
        if self.totalItemNum != 0:
            for curPageIndex in range(self.curPageIndex, math.ceil(self.totalItemNum/loaPageSize)):    
                response = requests.post(url, headers=headers, json=self.make_search_option(pageNum=curPageIndex+1))
                if response.status_code == 200:
                    json = response.json()
                    items = json.get('Items')
                    items = json.get(ResponseJsonTagType.items)
                    
                    for curItemIndex in range(self.curItemIndex, len(items)):
                        if self.subEngraveList == [] and not items[curItemIndex] in rst:
                            rst.append(items[curItemIndex])
                        else:
                            item_options = items[curItemIndex].get(AuctionItemTagType.options)
                            for option in item_options:
                                if option.get(ItemOptionTagType.type) == ItemOptionTagType.engrave and option.get(ItemOptionTagType.optionName) in self.subEngraveList and not items[curItemIndex] in rst:
                                    rst.append(items[curItemIndex])
                elif response.status_code == 429: # too much requests
                    raise Exception("API Requests has exceeded limits.")
                
                if len(rst) >= botPageSize:
                    self.curPageIndex = curPageIndex
                    self.curItemIndex = curItemIndex
                    break
        
        return rst
    
    def get_search_result(self):
        # 일단 한 페이지만 보여주는 식으로 할까? 그러려면 현재 페이지를 이 클래스 인스턴스가 기억해야한다.
        # 현재는 로아 경매장 페이지 사이즈인 10 으로 전체 넘버를 나눠서 모든 매물을 확인하는 중이다.
        # 이 방식보다는, 우선 한 페이지 확인해보고 결과 리스트의 숫자가 목표보다 작으면 다음 페이지로 넘어가서 만족 매물을 더하는 방식이 나은듯
        # 전체 매물 숫자 확인, loaPageSize=10으로 나누고 올림해서 api 몇 번 요구해야하는지 확인
        # 목표는 리스트에 사이즈 만큼 보여주는 것. 현재는 5개
        # 5개면 아마도 남은 매물 리스트가 있을 것. 이는 index로 하거나 리스트로 저장함. 그리고 현재 인덱스를 저장
        # 다음 페이지를 요구하면 이전 위치에서 이어서 진행. 여기서 문제 -> 만약 이 시간 동안에 매물이 업데이트 됐다면?
        # 매물이 업데이트 되어서 중복일 경우가 생긴다면 리스트에 넣을 때 동일한지만 확인해보자.
        # totalNum이 10에 딱 맞아 떨어지는 경우 ex. 30 -> 1, 2, 3   31 -> 4
        
        # 정리하면, 처음에는 전체 매물 갯수를 확인하고 페이지 수 확인 
        # 만족하는 결과물 5개 채울 때까지 페이지 수 loop -> 만족하면 break 하고 현재 index 정보들 저장 (전체 페이지 수, 10개 중 몇번째)
        # 만족하는 결과물 5개는? -> 처음에는 첫 5개, 그 다음에는 index 정보에 따른 이후부터 검색. 그렇다면 이 함수는 argument를 3개 받아야 한다.
        # argument = totalItemNum, pageIndex, itemIndex
        
        url = 'https://developer-lostark.game.onstove.com/auctions/items'
        response = requests.post(url, headers=headers, json=self.make_search_option())
        print('response code : ', response.status_code)
        rst = []
        if response.status_code == 200:
            json = response.json()
            totalNum = json.get('TotalCount')
            loaPageSize = 10
            
            if totalNum != 0:
                for i in range(math.ceil(totalNum/loaPageSize)):
                    response = requests.post(url, headers=headers, json=self.make_search_option(pageNum=i+1))
                    json = response.json()
                    
                    for obj in json.get('Items'):
                        if self.subEngraveList == []:
                            rst.append(obj)
                        else:
                            obj_options = obj.get('Options')
                            for opt in obj_options:
                                if opt.get('Type') == 'ABILITY_ENGRAVE' and opt.get('OptionName') in self.subEngraveList:
                                    rst.append(obj)
            else:
                print('Total count is 0 - no available item')
        for item in rst:
            print(item)
        return rst