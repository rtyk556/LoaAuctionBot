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



class SearchEngine():
    def __init__(self):
        self.subEngraveList = []
        self.currentPage = 1
    
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
    
    def get_search_result(self):
        # 일단 한 페이지만 보여주는 식으로 할까? 그러려면 현재 페이지를 이 클래스 인스턴스가 기억해야한다.
        # 현재는 로아 경매장 페이지 사이즈인 10 으로 전체 넘버를 나눠서 모든 매물을 확인하는 중이다.
        # 이 방식보다는, 우선 한 페이지 확인해보고 결과 리스트의 숫자가 목표보다 작으면 다음 페이지로 넘어가서 만족 매물을 더하는 방식이 나은듯
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