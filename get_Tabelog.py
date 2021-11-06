from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options

class get_Tabelog:
    '''
    呼び出し元に検索した食べ物の＜店名・url＞を返す
    '''
    def __init__(self,food,prace):
        self.food  = food
        self.prace = prace
        options = Options()
#        options.add_argument('--headless')
        self.browser01 = webdriver.Chrome(options=options)

    def re_shopInfo(self):
        #メインメソッド
        cur_url = self.input_info()
        self.shop_list = self.get_info()
        print('shop_list:',len(self.shop_list))
        return self.shop_list[0][0],cur_url,self.shop_list[0][1]  #1店舗目の＜店名・url＞を返す

    def input_info(self):
        self.browser01.get('https://tabelog.com/')
        food_name = self.browser01.find_element_by_xpath('//*[@id="sk"]')
        food_name.send_keys(self.food)
        area_station = self.browser01.find_element_by_xpath('//*[@id="sa"]')
        area_station.send_keys(self.prace)
        sarch_btn = self.browser01.find_element_by_xpath('//*[@id="js-global-search-btn"]')
        sarch_btn.click()
        return self.browser01.current_url

    def get_info(self):
        #1ページ分の店の＜店名・url＞を取得し配列に格納
        shop_list = []
        all_class = self.browser01.find_elements_by_class_name('list-rst__rst-data')
        for cnt,class_name in enumerate(all_class):
            aTag = class_name.find_element_by_tag_name("a")
            shop_name = aTag.text
            url = aTag.get_attribute("href")
            shop_list.append([shop_name,url])
            #print(cnt,':',shop_name,':\n',url,'\n')
        self.browser01.quit()
        return shop_list

if __name__ == "__main__":
    food  = 'オムライス'
    prace = '新宿' 
    shop,url = get_Tabelog(food,prace).re_shopInfo()
    print(shop,url)