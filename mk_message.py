import requests
import pprint
import get_Tabelog as gt

def Tabelog_recommend(food_list,similar_list):
    message='<あなたにおすすめの食べ物>\n'+\
        ' 1.'+food_list[0]+'\n'\
        '    ('+str(round(similar_list[0],3))+')\n'\
        ' 2.'+food_list[1]+'\n'\
        '    ('+str(round(similar_list[1],3))+')\n'\
        ' 3.'+food_list[2]+'\n'\
        '    ('+str(round(similar_list[2],3))+')'
    return message 

def Tabelog_shopInfo(food,place):
    #get_Tabelogクラスを呼び出し、＜店名・url＞を取得
    shop,cur_url,shop_url = gt.get_Tabelog(food,place).re_shopInfo()
    message1=place+'周辺の'+food+'を含む店\n'+\
            '⇒'+'\n\n'+\
            cur_url

    message2='下記のお店はいかがでしょうか'+'\n'+\
            '⇒'+'\n\n'+\
            '【店名】\n'+\
            shop+'\n\n'+\
            shop_url

    return message1,message2
