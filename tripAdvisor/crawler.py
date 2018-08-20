from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By #頁面等待
from selenium.webdriver.support.ui import WebDriverWait #頁面等待
from selenium.webdriver.support import expected_conditions as EC #頁面等待
from urllib.parse import urlparse, parse_qs
import time
import re
from tool import element_has_css_class,Not_equalto
from POI import POI
from Review import Review

class tripAdvisorCrawler:
    def __init__(self,db):
        self.driver=webdriver.Chrome()
        self.driver.get("https://www.tripadvisor.com.tw/Attractions")
        self.numberOfPOI = 0
        self.db = db

        ''' control data flow '''
        self.loop_all_page_gate=True
        self.loop_all_poi_gate=True

        # review
        self.reviews_gate=True
        self.loop_all_reviews_gate=True

        # need both to be true
        self.insertToDB_gate=True
        self.clickPOI_gate=True

        #如果db中存在，就不用再打開分頁查詢細節
        self.db_exit_gate=True

    def onlySaveReivew(self):
        ''' Step2 '''
        self.loop_all_page_gate=True
        self.loop_all_poi_gate=True

        # review
        self.reviews_gate=True
        self.loop_all_reviews_gate=True

        # need both to be true
        self.insertToDB_gate=True
        self.clickPOI_gate=True

        #如果db中存在，就不用再打開分頁查詢細節
        self.db_exit_gate=True
    def onlySavePOI(self):
        ''' STEP1 '''
        self.loop_all_page_gate=True
        self.loop_all_poi_gate=True

        # review
        self.reviews_gate=False
        self.loop_all_reviews_gate=False

        # need both to be true
        self.insertToDB_gate=True
        self.clickPOI_gate=True

        #如果db中存在，就不用再打開分頁查詢細節
        self.db_exit_gate=True

    def test1POI1pageReview(self):
        self.loop_all_page_gate=False
        self.loop_all_poi_gate=False
        self.reviews_gate=True
        self.loop_all_reviews_gate=False

        # need both to be true
        self.insertToDB_gate=True
        self.clickPOI_gate=True

    def search(self,city):
        all_input = self.driver.find_elements_by_tag_name("input")
        print("1.number of all_input:", len(all_input))
        searchInput = None
        print("2.list all_input:")
        for i, input in enumerate(all_input):
            placeholder = input.get_attribute("placeholder")
            print(i, placeholder)
            if (placeholder == "搜尋目的地、景點或活動"):
                searchInput = input
        print("3.find searchInput", searchInput.get_attribute("placeholder"))
        print("4.輸入",city)  # 宜蘭縣 台北市
        searchInput.send_keys(city)  # 宜蘭縣 台北市
        time.sleep(5)

        SUBMIT_THINGS_TO_DO = self.driver.find_element_by_id("SUBMIT_THINGS_TO_DO")
        print("5.find 尋找不可錯過的景點(button id:SUBMIT_THINGS_TO_DO)")
        SUBMIT_THINGS_TO_DO.send_keys(Keys.RETURN)
        print("6.click SUBMIT_THINGS_TO_DO")
        print("7.wait page load")

    def loop_all_page(self):
        poi_stop = True
        while (poi_stop):
            try:
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "HEADING"))
                )
            except:
                print("頁面加載失敗")

            print("8.pag loaded")
            all_ATTR_ENTRY_ = self.driver.find_elements_by_id("ATTR_ENTRY_")  ## 沒有詳細資料的poi:attraction_type_group
            print("9.number of ATTR_ENTRY_(POI):", len(all_ATTR_ENTRY_))
            print("10.list all_ATTR_ENTRY_:")

            self.loop_all_poi(all_ATTR_ENTRY_);
            if not self.loop_all_page_gate:
                break#loop_all_page
            print("14.next page")
            try:
                nextPage = self.driver.find_element_by_link_text("往下")
                nextPage.click()
            except:
                poi_stop = False
                print("over")

    def loop_all_poi(self,all_ATTR_ENTRY_):
        for i, ATTR_ENTRY_ in enumerate(all_ATTR_ENTRY_):
            self.numberOfPOI += 1
            data_locationid = ATTR_ENTRY_.get_attribute("data-locationid")
            listing_title_a = ATTR_ENTRY_.find_element_by_css_selector("div.listing_title a")
            print(self.numberOfPOI, i, data_locationid, listing_title_a.text)

            if self.db_exit_gate:
                if self.db.exit(listing_title_a.text,"poi"):
                    continue

            if self.clickPOI_gate:
                self.clickPOI(listing_title_a)
                self.closePage()
            if not self.loop_all_poi_gate:
                break#loop all poi

    def clickPOI(self,listing_title_a):
        print("11.click poi")
        listing_title_a.click()
        print("12.加載頁面(poi詳細資料)")
        handles = self.driver.window_handles
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "HEADING"))
            )
        except:
            print("頁面加載失敗")
        self.driver.switch_to_window(handles[1])  # 可能有錯誤!!!!!

        self.POIdetail()

    def closePage(self):
        handles = self.driver.window_handles
        self.driver.close()
        self.driver.switch_to_window(handles[0])

    def POIdetail(self,url=None):

        if(url!=None):
            self.driver.get(url)

        ##crawl detail data from here!!##

        '''-------------name-------------'''
        name=None
        try:
            HEADING = self.driver.find_element_by_css_selector("h1#HEADING").text
            altHEADING = self.driver.find_element_by_css_selector("h1#HEADING .altHead").text
            name=HEADING.replace(altHEADING,"")
        except:
            try:
                HEADING = self.driver.find_element_by_css_selector("h1#HEADING").text
                name = HEADING
            except:
                name=None

        '''-------------rating-------------'''
        rating=None
        try:
            rating = self.driver.find_element_by_css_selector(".rating_and_popularity span.ui_bubble_rating.bubble_40").get_attribute("content")
        except:
            rating = None

        '''-------------rank-------------'''
        rank=None
        try:
            rank =self.driver.find_element_by_css_selector(".rating_and_popularity b span").text.replace("第 ","")
        except:
            rank = None

        '''-------------detail_list-------------'''
        detail_list=None
        try:
            detail_list=[]
            detail=self.driver.find_elements_by_css_selector(".rating_and_popularity .detail a")
            for a in detail:
                detail_list.append(a.text)
            if len(detail_list)==0:
                detail_list = None
        except:
            detail_list = None

        '''-------------address-------------'''
        country_name=None
        try:
            country_name = self.driver.find_element_by_css_selector(".prw_rup.prw_common_atf_header_bl.headerBL .country-name").text
        except:
            country_name=None
        locality= None
        try:
            locality = self.driver.find_element_by_css_selector(".prw_rup.prw_common_atf_header_bl.headerBL .locality").text
        except:
            locality = None
        street_address=None
        try:
            street_address = self.driver.find_element_by_css_selector(".prw_rup.prw_common_atf_header_bl.headerBL .street-address").text
        except:
            street_address=None

        '''-------------phone-------------'''
        phone=None
        try:
            phone = self.driver.find_elements_by_css_selector(".prw_rup.prw_common_atf_header_bl.headerBL .phone span")[1].text
        except:
            phone = None

        '''-------------rating_chart_list-------------'''
        rating_chart_list=None
        try:
            rating_chart_list=[]
            rating_chart=self.driver.find_elements_by_css_selector(".ratings_chart .chart_row .row_count")
            for row in rating_chart:
                rating_chart_list.append(row.text)
        except:
            rating_chart_list = None

        '''-------------timeRange,dayRange-------------'''
        timeRange=None
        dayRange=None
        try:
            allhours=self.driver.find_element_by_css_selector(".allHoursContainer .allHoursCTA")
            allhours.click()#click first then scroll -->no error
            print("click allhours")
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".timeRange"))
            )
            timeRange = self.driver.find_element_by_css_selector(".timeRange").text
            dayRange = self.driver.find_element_by_css_selector(".dayRange").text
        except:
            timeRange = None
            dayRange = None

        '''-------------locations-------------'''
        '''
        locations=None
        try:
            # scroll to map
            prv_map = self.driver.find_element_by_css_selector(".overviewContent .prv_map.clickable img")
            self.driver.execute_script("arguments[0].scrollIntoView();", prv_map)
            element = WebDriverWait(self.driver, 30).until(Not_equalto("https://static.tacdn.com/img2/x.gif"))

            # parse map_url
            locations = []
            map_url=self.driver.find_element_by_css_selector(".overviewContent .prv_map.clickable img").get_attribute("src")
            print(map_url)
            map_url_parse=urlparse(map_url)
            map_url_query= parse_qs(map_url_parse.query)
            locations=map_url_query["center"][0].split(",",2)
        except:
            locations = None
        '''
        locations = None
        try:
            locations = [0]*2
            allscript=self.driver.find_elements_by_tag_name("script")
            for script in allscript:
                js_text=str(script.get_attribute("innerHTML"))
                find_window_mapDivId=js_text.find("window.mapDivId")
                if(find_window_mapDivId!=-1):
                    lat_index=js_text.find("lat")
                    lng_index=js_text.find("lng")
                    zoom_index=js_text.find("zoom")
                    lat=float(js_text[lat_index:lng_index-1].replace("lat: ","").replace(",",""))
                    lng=float(js_text[lng_index:zoom_index - 1].replace("lng: ","").replace(",",""))
                    # print(js_text[lat_index:lng_index-1])
                    # print(js_text[lng_index:zoom_index-1])
                    print(lat,",",lng,"↓")
                    locations[0]=lat
                    locations[1]=lng
        except:
            locations = None


        '''-------------duration-------------'''
        duration=None
        try:
            duration=self.driver.find_element_by_css_selector("div.section.hours .detail_section.duration").text
        except:
            duration=None

        '''-------------print all data-------------'''
        # print("name:",name,"rating:",rating,"rank:",rank,"detail_list:",detail_list,"address:",country_name+"/"+locality+"/"+street_address,"phone(未處理):",phone,"rating_chart_list:",rating_chart_list,"lat:",locations[0],"lng:",locations[1],"duration:",duration,"dayRange:",dayRange,"timeRange:",timeRange)


        '''-------------poi_url-------------'''
        poi_url=self.driver.current_url
        poi=POI(name,rating,rank,detail_list,country_name,locality,street_address,phone,rating_chart_list,timeRange,dayRange,locations,duration,poi_url)
        print(poi)
        poi_id =None
        if self.insertToDB_gate:
            poi_id=self.db.insert(poi,"poi")
            print("insert ",poi.name)

        if self.reviews_gate:
            self.loop_all_reviews(poi_id)



        ##crawl detail data end here!!##

    def loop_all_reviews(self, poi_id,url=None):
        if(url!=None):
            self.driver.get(url)
        ##評論start##
        reviews_sop = True
        while reviews_sop:
            try:
                element = WebDriverWait(self.driver, 10).until_not(
                    element_has_css_class((By.ID, 'REVIEWS'), "loading")
                )
            except:
                print("頁面加載失敗")
            all_review_container = self.driver.find_elements_by_class_name("review-container")
            for i, review_container in enumerate(all_review_container):
                self.reviewDetail(review_container,poi_id)

            if not self.loop_all_reviews_gate:
                break#loop_all_reviews
            try:
                nextPage = self.driver.find_element_by_css_selector("span.nav.next.taLnk")
                nextPage.click()
                print("next reviews")
            except:
                reviews_sop = False
                print("over")
                # 評論end#

    def reviewDetail(self,review_container,poi_id):
        """--------------------------"""

        '''-------------uid-------------'''
        uid = None
        try:
            try:
                original_uid=review_container.find_elements_by_css_selector(".memberOverlayLink")[0].get_attribute("id")
                #print(original_uid)
                long_uid=original_uid.split("_")[1]
                long_uid_split=long_uid.split("-")
                if len(long_uid_split)>0:
                    uid=long_uid_split[0]
                else:
                    uid=long_uid
            except:
                original_uid = review_container.find_elements_by_css_selector(".member_info div")[0].get_attribute("class")
                try:
                    long_uid = original_uid.split("_")[1]
                    uid=long_uid
                except:
                    uid=review_container.find_element_by_css_selector(".username.mo span").text
        except:
            uid = None

        '''-------------review_title-------------'''
        review_title=None
        try:
            review_title = review_container.find_element_by_css_selector("span.noQuotes").text
        except:
            review_title = None

        '''-------------review_rating-------------'''

        review_rating = None
        try:
            review_rating_string=review_container.find_element_by_css_selector(".rating span.ui_bubble_rating").get_attribute("class")
            review_rating=int(review_rating_string.split(" ")[1].split("_")[1])/10
        except:
            review_rating=None

        '''-------------ratingDate-------------'''
        ratingDate=None
        try:
            ratingDate = review_container.find_element_by_css_selector(".ratingDate.relativeDate").get_attribute("title")
        except:
            ratingDate=None

        '''-------------review-------------'''
        review=None
        try:
            review=review_container.find_element_by_css_selector(".entry .partial_entry").text
        except:
            review=None

        '''-------------print all data-------------'''
        # print("uid:",uid,"review_title:",review_title,"review_rating:",review_rating,"review:",review,"ratingDate:",ratingDate)
        review=Review(poi_id,uid,review_title,review_rating,review,ratingDate)
        print(review)
        if self.insertToDB_gate:
            self.db.insert(review,"review")
            print("insert ",review.review_title)


    def loop_all_url(self):
        gate=False
        for poi in self.db.findall("poi"):
            if poi["name"]=="慶和橋":
                gate=True
            if gate:
                self.loop_all_reviews(poi["_id"],poi["poi_url"])


