from crawler import  tripAdvisorCrawler
from DB import DB


db = DB()
db.connectToDB("tripAdvisor")
tripAdvisor= tripAdvisorCrawler(db)

def main():
    print("start")

    tripAdvisor.search("宜蘭縣,亞洲,台灣")
    tripAdvisor.loop_all_page()

    #國立傳統藝術中心National Center for Traditional Arts
    # tripAdvisor.POIdetail("https://www.tripadvisor.com.tw/Attraction_Review-g608526-d2303982-Reviews-National_Center_for_Traditional_Arts-Yilan_County.html")

    #柯氏蔥油餅
    # tripAdvisor.POIdetail("https://www.tripadvisor.com.tw/Restaurant_Review-g608526-d9762233-Reviews-Ke_s_Chongyoubing-Yilan_County.html")

    #蘭陽博物館Lanyang Museum
    # tripAdvisor.POIdetail("https://www.tripadvisor.com.tw/Attraction_Review-g608526-d1992522-Reviews-Lanyang_Museum-Yilan_County.html")

    #蘇澳冷泉Suao Cold Spring
    # tripAdvisor.POIdetail("https://www.tripadvisor.com.tw/Attraction_Review-g608526-d2228822-Reviews-Suao_Cold_Spring-Yilan_County.html")

    #湯圍溝礁溪溫泉公園Tangweigou Jiaosi Hot Spring Park
    # tripAdvisor.POIdetail("https://www.tripadvisor.com.tw/Attraction_Review-g608526-d6974361-Reviews-or10-Tangweigou_Jiaosi_Hot_Spring_Park-Yilan_County.html")

    # tripAdvisor.loop_all_url()
def step1():
    tripAdvisor.onlySavePOI()#control data flow
    tripAdvisor.search("宜蘭縣,亞洲,台灣")
    tripAdvisor.loop_all_page()
def step2():
    tripAdvisor.onlySaveReivew()
    tripAdvisor.loop_all_url()
if __name__ == "__main__":
    main()