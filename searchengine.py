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

class SearchEngine():
    def __init__(self, container):
        self.container = container
        self.subEngraveList = []
        self.totalItemNum = -1
        self.totalPageIndex = 0
        self.curPageIndex = 0
        self.curItemIndex = 0
        self.loaPageSize = 10
        self.botPageSize = 5
    
    def make_search_option(self, pageNum=1):
        container = self.container
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
        curPageIndex = 0
        curItemIndex = 0
        if self.totalItemNum != 0:
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
    import DBmanager
    import datetime
    
    rst = []
    if len(api_list) == 0:
        raise Exception('Cannot find api list.')
    
    loaPageSize = 10
    
    curPageIndex = 0
    
    foundAllItem = False
    totalItemNum = 0
    totalPageIndex = None
    for api in api_list:
        
        getNextAPI = False
        headers = {
            'accept' : 'application/json',
            'authorization' : 'bearer ' + api[DBmanager.APITag.key]
        }
        
        if totalPageIndex == None:
            response = requests.post(url, headers=headers, json=preset[DBmanager.PresetTag.search_option][0])
            print('first response for getting total item num : ', response.status_code)
            if response.status_code != 200:
                getNextAPI = True
            else:
                try:
                    totalItemNum = response.json().get(ResponseJsonTagType.totalCount)
                    totalPageIndex = math.ceil(totalItemNum/loaPageSize)
                except:
                    print('Error has occured in get_preset_result. ', response.status_code)
        
        
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
                        itemAuctionInfo = items[idx].get(AuctionItemTagType.auctionInfo)
                        if preset[DBmanager.PresetTag.search_option][0].get('Sort') == SortOptionType.buyPrice:
                            itemPrice = itemAuctionInfo.get(AuctionInfoTagType.buyPrice)
                        else:
                            itemPrice = itemAuctionInfo.get(AuctionInfoTagType.startPrice)
    
                        if itemPrice > preset[DBmanager.PresetTag.condition]:
                            foundAllItem = True
                            break
                        
                        # subengrave list 확인
                        subengrave_list = preset[DBmanager.PresetTag.search_option][1]
                        if subengrave_list == [] and not items[idx] in rst:
                            rst.append(items[idx])
                        else:
                            item_options = items[idx].get(AuctionItemTagType.options)
                            for option in item_options:
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
        if getNextAPI:
            valid_time = datetime.datetime.now() + datetime.timedelta(seconds=60)
            time_str = valid_time.strftime("%Y-%m-%d %H:%M:%S")
            print("Change API valid time. ", time_str)
            api[DBmanager.APITag.valid_time] = time_str
            continue

    return rst

def check_api_validity(api_key):
    url = 'https://developer-lostark.game.onstove.com/news/events'
    headers = {
        'accept' : 'application/json',
        'authorization' : 'bearer ' + api_key
        }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return True
    return False
