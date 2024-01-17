

class SearchOption():
    def __init__(self):
        self.searchOption = {
            'ItemGradeQuality' : 70,
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
        
class OptionLabel():
    def __init__(self):
        self.itemGradeQuality = 'ItemGradeQuality'
        self.sort = 'Sort'
        self.categoryCdoe = 'CategoryCode'
        self.etcOptions = 'EtcOptions'
        self.firstOption = 'FirstOption'
        self.secondOption = 'SecondOption'
        self.minValue = 'MinValue'
        self.maxValue = 'MaxValue'
        self.itemTier = 'ItemTier'
        self.ItemGrade = 'ItemGrade'
        self.sortCondition = 'SortCondition'
        self.pageNumber = 'PageNo'
        

class SortMethod():
    def __init__(self):
        self.BIDSTART_PRICE = 'BIDSTART_PRICE'
        
        