import requests
import json
import searchoption
import math
import token_value

Token = token_value.API_TOKEN

headers = {
    'accept' : 'application/json',
    'authorization' : Token
}

url = 'https://developer-lostark.game.onstove.com/auctions/items'

search_option = searchoption.SearchOption().searchOption
label = searchoption.OptionLabel()

search_option = {
    'ItemGradeQuality' : 80,
    'Sort': 'BIDSTART_PRICE',
    'CategoryCode': 200030, # 200000 - 장신구, 200030 - 반지
    'EtcOptions' : [
        {
            "FirstOption" : 2, # first 2면 스탯, 3이면 각인, 6이면 감소 효과
            "SecondOption" : 16, # 16은 특화
            "MinValue" : None,
            "MaxValue" : None
        },
        {
            "FirstOption" : 3,
            "SecondOption" : 129, # 129는 강화무기
            "MinValue" : 5,
            "MaxValue" : None,
        },
        # {
        #     "FirstOption" : 3,
        #     "SecondOption" : 141, # 141은 예둔
        #     "MinValue" : 3,
        #     "MaxValue" : None
        # }
        ],
        'ItemTier': 3,
        'ItemGrade': '고대',
        'PageNo' : 0,
        'SortCondition': 'ASC',
    }

# search_option = {
#     'ItemGradeQuality' : 80,
#     'Sort': 'BIDSTART_PRICE',
#     'CategoryCode': 200010, # 200000 - 장신구, 200030 - 반지
#     'EtcOptions' : [
#         {
#             "FirstOption" : 2, # first 2면 스탯, 3이면 각인, 6이면 감소 효과
#             "SecondOption" : 16, # 16은 특화
#             "MinValue" : None,
#             "MaxValue" : None
#         },
#         {
#             "FirstOption" : 2, # first 2면 스탯, 3이면 각인, 6이면 감소 효과
#             "SecondOption" : 15, # 16은 특화
#             "MinValue" : None,
#             "MaxValue" : None
#         },
#         {
#             "FirstOption" : 3,
#             "SecondOption" : 299, # 129는 강화무기
#             "MinValue" : 6,
#             "MaxValue" : None,
#         },
#         # {
#         #     "FirstOption" : 3,
#         #     "SecondOption" : 141, # 141은 예둔
#         #     "MinValue" : 3,
#         #     "MaxValue" : None
#         # }
#         ],
#         'ItemTier': 3,
#         'ItemGrade': '고대',
#         'PageNo' : 0,
#         'SortCondition': 'ASC',
#     }

def get_search_option(ItemGradeQuality = 70, Sort = 'BIDSTART_PRICE', Category = 200030, pageNo=0 ,mainStat=None, mainOption=None, subOption=None):
    
    search_option['ItemGradeQuality'] = ItemGradeQuality
    search_option['Sort'] = Sort
    search_option['CategoryCode'] = Category
    search_option['PageNo'] = pageNo
    # search_option['EtcOptions'].append(subOption)
    return search_option

def get_response_json(search_option):
    response = requests.post(url, headers=headers, json=search_option)
    jsonObject = response.json()
    
    return jsonObject

jsonObject = get_response_json(search_option)

totalNum = jsonObject.get('TotalCount')
print(' total num : ', totalNum)
pageSize = 10

# subOption = ["저주받은 인형", "예리한 둔기"]
subOption = ["예리한 둔기", "저주받은 인형"]
rst = []

if totalNum != 0:
    for i in range(math.ceil(totalNum/pageSize)):
        print(i)
        # option = get_search_option(pageNo=i+1)
        option = get_search_option(ItemGradeQuality=80, pageNo=i+1, Category=200030)
        jsonObject = get_response_json(option) ## 1분 100회 제한 생각 -> 1분에 1000개 리밋으로 매물 검색 가능할듯

        for obj in jsonObject.get('Items'):
            obj_options = obj.get('Options')
            for opt in obj_options:
                if subOption == []:
                    rst.append(obj)
                elif opt.get('Type') == 'ABILITY_ENGRAVE' and opt.get('OptionName') in subOption:
                    rst.append(obj)
                    
else:
    print("Total Count is 0 - No available item")

for item in rst:
    print(item)

