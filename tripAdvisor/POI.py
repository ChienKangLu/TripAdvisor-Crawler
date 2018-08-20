import json
'''
name: 國立傳統藝術中心 
rating: 4 
rank: 5 
detail_list: ['美術館', '博物館', '購物']
address: 台灣/宜蘭縣/五結鄉季新村五濱路二段201號 
phone(未處理): +886 800 868 676 
rating_chart_list: ['34%', '47%', '15%', '3%', '1%'] 
lat: 24.685297 
lng: 121.823708 
duration: 建議時間長度： 1-2 小時 
dayRange: 日 - 六 
timeRange: 上午9:00 - 下午6:00
'''
'''
{
    "name": "國立傳統藝術中心",
    "rating": "4",
    "rank": "5",
    "detail_list": [
        "美術館",
        "購物",
        "博物館"
    ],
    "country_name": "台灣",
    "locality": "宜蘭縣",
    "street_address": "五結鄉季新村五濱路二段201號",
    "phone": "+886 800 868 676",
    "rating_chart_list": [
        "34%",
        "47%",
        "15%",
        "3%",
        "1%"
    ],
    "timeRange": "上午9:00 - 下午6:00",
    "dayRange": "星期日 - 星期六",
    "locations": {
        "lat": "24.685297",
        "lng": "121.823708"
    },
    "duration": "建議時間長度： 1-2 小時
'''
'''
{
    "name": "國立傳統藝術中心",
    "rating": "4",
    "rank": "5",
    "detail_list": [
        "美術館",
        "購物",
        "博物館"
    ],
    "country_name": "台灣",
    "locality": "宜蘭縣",
    "street_address": "五結鄉季新村五濱路二段201號",
    "phone": "+886 800 868 676",
    "rating_chart_list": [
        0.34,
        0.47,
        0.15,
        0.03,
        0.01
    ],
    "dayRange": "星期日 - 星期六",
    "timeRange": "上午9:00 - 下午6:00",
    "locations": {
        "lat": "24.685297",
        "lng": "121.823708"
    },
    "duration": "建議時間長度： 1-2 小時"
}
'''
'''
{
    "name": "柯氏蔥油餅",
    "rating": "4",
    "rank": "4",
    "detail_list": null,
    "country_name": "台灣",
    "locality": "宜蘭縣",
    "street_address": "礁溪路四段128號",
    "phone": "+886 972 158 603",
    "rating_chart_list": [
        0.35,
        0.5,
        0.15,
        0.0,
        0.0
    ],
    "dayRange": null,
    "timeRange": null,
    "locations": {
        "lat": "24.821327",
        "lng": "121.769875"
    },
    "duration": null
}
'''

class POI:
    def __init__(self,name,rating,rank,detail_list,country_name,locality,street_address,phone,rating_chart_list,timeRange,dayRange,locations,duration,poi_url):
        self.name=name
        self.rating=rating
        self.rank=rank
        self.detail_list=detail_list
        self.country_name=country_name
        self.locality=locality
        self.street_address=street_address
        self.phone=phone
        self.convert_rating_chart_list(rating_chart_list)
        self.dayRange=dayRange
        self.timeRange=timeRange
        self.locations={}
        if(locations!=None):
            self.locations["lat"]=locations[0]
            self.locations["lng"]=locations[1]
        else:
            self.locations["lat"]=None
            self.locations["lng"]=None
        self.duration=duration
        self.poi_url=poi_url

    def convert_rating_chart_list(self,rating_chart_list):
        """convert "34%"-->0.34 """
        self.rating_chart_list =[0]*len(rating_chart_list)
        for index,s in enumerate(rating_chart_list):
            self.rating_chart_list[index]=int(s.replace("%",""))/100

    # def convert_duration(self,duration):
    #
    #     """convert "建議時間長度： 1-2 小時-->"short":1 "long":2"""
    #     self.duration={}
    #     duration_split=duration.replace("建議時間長度： ", "").replace(" 小時", "").split("-")
    #     self.duration["short"]=duration_split[0]
    #     self.duration["long"] = duration_split[1]

    def toJson(self):
        # return json.dumps(self.__dict__,indent=4,ensure_ascii=False)
        return json.dumps(self.__dict__, ensure_ascii=False)

    def __str__(self):
        return self.toJson()





