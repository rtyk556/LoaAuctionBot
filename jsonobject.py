import enum
import asyncio

class SearchOptionContaitner():
  def __new__(cls, *args, **kwargs):
    if not hasattr(cls, "__instance"):
      cls.__instance = super().__new__(cls)
    return cls.__instance
  
  def __init__(self):
     self.acceType = []
     self.mainEngrave = None
     self.mainEngraveMin = 3
     self.mainEngraveMax = 6
     self.subEngraves = []
     self.subEngraveMin = 3
     self.subEngraveMax = 6
     self.mainStat = None
     self.lock = asyncio.Lock()
  
  def isNecklace(self):
    return AccesoryType.necklace in self.acceType

class AccesoryType(int, enum.Enum):
  necklace = 200010,
  earring = 200020,
  ring = 200030
  
  def __int__(self) -> int:
    return self.value

  
class TagType(str, enum.Enum):
  codeValue = "Value",
  text = "Text",
  className = "class"

classEngrave= [ {
          "Value": 125,
          "Text": "광기",
          "Class": "버서커"
        },
        {
          "Value": 127,
          "Text": "오의 강화",
          "Class": "배틀마스터"
        },
        {
          "Value": 129,
          "Text": "강화 무기",
          "Class": "데빌헌터"
        },
        {
          "Value": 130,
          "Text": "화력 강화",
          "Class": "블래스터"
        },
        {
          "Value": 188,
          "Text": "광전사의 비기",
          "Class": "버서커"
        },
        {
          "Value": 189,
          "Text": "초심",
          "Class": "배틀마스터"
        },
        {
          "Value": 190,
          "Text": "극의: 체술",
          "Class": "인파이터"
        },
        {
          "Value": 191,
          "Text": "충격 단련",
          "Class": "인파이터"
        },
        {
          "Value": 314,
          "Text": "권왕파천무",
          "Class": "브레이커"
        },
        {
          "Value": 315,
          "Text": "수라의 길",
          "Class": "브레이커"
        },
        {
          "Value": 192,
          "Text": "핸드거너",
          "Class": "데빌헌터"
        },
        {
          "Value": 193,
          "Text": "포격 강화",
          "Class": "블래스터"
        },
        {
          "Value": 194,
          "Text": "진실된 용맹",
          "Class": "바드"
        },
        {
          "Value": 195,
          "Text": "절실한 구원",
          "Class": "바드"
        },
        {
          "Value": 293,
          "Text": "점화",
          "Class": "소서리스"
        },
        {
          "Value": 294,
          "Text": "환류",
          "Class": "소서리스"
        },
        {
          "Value": 196,
          "Text": "분노의 망치",
          "Class": "디스트로이어"
        },
        {
          "Value": 197,
          "Text": "중력 수련",
          "Class": "디스트로이어"
        },
        {
          "Value": 198,
          "Text": "상급 소환사",
          "Class": "서머너"
        },
        {
          "Value": 199,
          "Text": "넘치는 교감",
          "Class": "서머너"
        },
        {
          "Value": 200,
          "Text": "황후의 은총",
          "Class": "아르카나"
        },
        {
          "Value": 201,
          "Text": "황제의 칙령",
          "Class": "아르카나"
        },
        {
          "Value": 224,
          "Text": "전투 태세",
          "Class": "워로드"
        },
        {
          "Value": 225,
          "Text": "고독한 기사",
          "Class": "워로드"
        },
        {
          "Value": 256,
          "Text": "세맥타통",
          "Class": "기공사"
        },
        {
          "Value": 257,
          "Text": "역천지체",
          "Class": "기공사"
        },
        {
          "Value": 258,
          "Text": "두 번째 동료",
          "Class": "호크아이"
        },
        {
          "Value": 259,
          "Text": "죽음의 습격",
          "Class": "호크아이"
        },
        {
          "Value": 276,
          "Text": "절정",
          "Class": "창술사"
        },
        {
          "Value": 277,
          "Text": "절제",
          "Class": "창술사"
        },
        {
          "Value": 278,
          "Text": "잔재된 기운",
          "Class": "블레이드"
        },
        {
          "Value": 279,
          "Text": "버스트",
          "Class": "블레이드"
        },
        {
          "Value": 280,
          "Text": "완벽한 억제",
          "Class": "데모닉"
        },
        {
          "Value": 281,
          "Text": "멈출 수 없는 충동",
          "Class": "데모닉"
        },
        {
          "Value": 282,
          "Text": "심판자",
          "Class": "홀리나이트"
        },
        {
          "Value": 283,
          "Text": "축복의 오라",
          "Class": "홀리나이트"
        },
        {
          "Value": 284,
          "Text": "아르데타인의 기술",
          "Class": "스카우터"
        },
        {
          "Value": 285,
          "Text": "진화의 유산",
          "Class": "스카우터"
        },
        {
          "Value": 286,
          "Text": "갈증",
          "Class": "리퍼"
        },
        {
          "Value": 287,
          "Text": "달의 소리",
          "Class": "리퍼"
        },
        {
          "Value": 289,
          "Text": "피스메이커",
          "Class": "건슬링어"
        },
        {
          "Value": 290,
          "Text": "사냥의 시간",
          "Class": "건슬링어"
        },
        {
          "Value": 291,
          "Text": "일격필살",
          "Class": "스트라이커"
        },
        {
          "Value": 292,
          "Text": "오의난무",
          "Class": "스트라이커"
        },
        {
          "Value": 305,
          "Text": "회귀",
          "Class": "도화가"
        },
        {
          "Value": 306,
          "Text": "만개",
          "Class": "도화가"
        },
        {
          "Value": 307,
          "Text": "질풍노도",
          "Class": "기상술사"
        },
        {
          "Value": 308,
          "Text": "이슬비",
          "Class": "기상술사"
        },
        {
          "Value": 309,
          "Text": "포식자",
          "Class": "슬레이어"
        },
        {
          "Value": 310,
          "Text": "처단자",
          "Class": "슬레이어"
        },
        {
          "Value": 311,
          "Text": "만월의 집행자",
          "Class": "소울이터"
        },
        {
          "Value": 312,
          "Text": "그믐의 경계",
          "Class": "소울이터"
        } ]

publicEngrave = [{
          "Value": 118,
          "Text": "원한",
          "Class": ""
        },
        {
          "Value": 123,
          "Text": "굳은 의지",
          "Class": ""
        },
        {
          "Value": 237,
          "Text": "실드 관통",
          "Class": ""
        },
        {
          "Value": 243,
          "Text": "강령술",
          "Class": ""
        },
        {
          "Value": 247,
          "Text": "저주받은 인형",
          "Class": ""
        },
        {
          "Value": 255,
          "Text": "각성",
          "Class": ""
        },
        {
          "Value": 111,
          "Text": "안정된 상태",
          "Class": ""
        },
        {
          "Value": 140,
          "Text": "위기 모면",
          "Class": ""
        },
        {
          "Value": 238,
          "Text": "달인의 저력",
          "Class": ""
        },
        {
          "Value": 240,
          "Text": "중갑 착용",
          "Class": ""
        },
        {
          "Value": 242,
          "Text": "강화 방패",
          "Class": ""
        },
        {
          "Value": 245,
          "Text": "부러진 뼈",
          "Class": ""
        },
        {
          "Value": 248,
          "Text": "승부사",
          "Class": ""
        },
        {
          "Value": 249,
          "Text": "기습의 대가",
          "Class": ""
        },
        {
          "Value": 251,
          "Text": "마나의 흐름",
          "Class": ""
        },
        {
          "Value": 254,
          "Text": "돌격대장",
          "Class": ""
        },
        {
          "Value": 107,
          "Text": "약자 무시",
          "Class": ""
        },
        {
          "Value": 109,
          "Text": "정기 흡수",
          "Class": ""
        },
        {
          "Value": 110,
          "Text": "에테르 포식자",
          "Class": ""
        },
        {
          "Value": 121,
          "Text": "슈퍼 차지",
          "Class": ""
        },
        {
          "Value": 134,
          "Text": "구슬동자",
          "Class": ""
        },
        {
          "Value": 141,
          "Text": "예리한 둔기",
          "Class": ""
        },
        {
          "Value": 235,
          "Text": "불굴",
          "Class": ""
        },
        {
          "Value": 239,
          "Text": "여신의 가호",
          "Class": ""
        },
        {
          "Value": 244,
          "Text": "선수필승",
          "Class": ""
        },
        {
          "Value": 142,
          "Text": "급소 타격",
          "Class": ""
        },
        {
          "Value": 236,
          "Text": "분쇄의 주먹",
          "Class": ""
        },
        {
          "Value": 241,
          "Text": "폭발물 전문가",
          "Class": ""
        },
        {
          "Value": 246,
          "Text": "번개의 분노",
          "Class": ""
        },
        {
          "Value": 253,
          "Text": "바리케이드",
          "Class": ""
        },
        {
          "Value": 168,
          "Text": "마나 효율 증가",
          "Class": ""
        },
        {
          "Value": 167,
          "Text": "최대 마나 증가",
          "Class": ""
        },
        {
          "Value": 202,
          "Text": "탈출의 명수",
          "Class": ""
        },
        {
          "Value": 288,
          "Text": "결투의 대가",
          "Class": ""
        },
        {
          "Value": 295,
          "Text": "질량 증가",
          "Class": ""
        },
        {
          "Value": 296,
          "Text": "추진력",
          "Class": ""
        },
        {
          "Value": 297,
          "Text": "타격의 대가",
          "Class": ""
        },
        {
          "Value": 298,
          "Text": "시선 집중",
          "Class": ""
        },
        {
          "Value": 299,
          "Text": "아드레날린",
          "Class": ""
        },
        {
          "Value": 300,
          "Text": "속전속결",
          "Class": ""
        },
        {
          "Value": 301,
          "Text": "전문의",
          "Class": ""
        },
        {
          "Value": 302,
          "Text": "긴급구조",
          "Class": ""
        },
        {
          "Value": 303,
          "Text": "정밀 단도",
          "Class": ""
        }]

penaltyEngrave = [
    {
          "Value": 800,
          "Text": "공격력 감소",
          "Class": ""
        },
        {
          "Value": 802,
          "Text": "공격속도 감소",
          "Class": ""
        },
        {
          "Value": 801,
          "Text": "방어력 감소",
          "Class": ""
        },
        {
          "Value": 803,
          "Text": "이동속도 감소",
          "Class": ""
        }
]

stat = [
        {
          "Value": 15,
          "Text": "치명",
          "Class": ""
        },
        {
          "Value": 16,
          "Text": "특화",
          "Class": ""
        },
        {
          "Value": 17,
          "Text": "제압",
          "Class": ""
        },
        {
          "Value": 18,
          "Text": "신속",
          "Class": ""
        },
        {
          "Value": 19,
          "Text": "인내",
          "Class": ""
        },
        {
          "Value": 20,
          "Text": "숙련",
          "Class": ""
        }
]