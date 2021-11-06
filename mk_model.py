from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import logging
import time
import requests

class mk_model:
    """
    分かち書きされたテキストからモデルを作成
    Doc2Vecの使い方:https://qiita.com/asian373asian/items/1be1bec7f2297b8326cf
    """
    def __init__(self):
        self.make_model()

    def make_model(self):
        start_time = time.time()
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        f = open(text_path,'r',encoding="utf-8") 

        #１文書ずつ、単語に分割してリストに入れていく[([単語1,単語2,単語3],文書id),...]こんなイメージ
        #words：文書に含まれる単語のリスト（単語の重複あり）
        # tags：文書の識別子（リストで指定．1つの文書に複数のタグを付与できる）
        trainings = [TaggedDocument(words = data.split(),tags = [i]) for i,data in enumerate(f)]

        # トレーニング（パラメータについては後日）
        m = Doc2Vec(documents= trainings, size=300, window=8, min_count=10)

        # モデルのセーブ
        m.save(model_path + model_name)

        time_min = int((time.time()-start_time)/60)
        time_sec = int(time.time()-start_time)%60
        self.PythonNotify('size=' + str(size) + '\nmin_count=' + str(min_count) + '\nwindow=' + str(window) +'\nモデル作成完了\n\nかかった時間\n' + str(time_min)+'分\n'+str(time_sec)+'秒')

    def PythonNotify(self,message, *args):
        # 諸々の設定
        line_notify_api = 'https://notify-api.line.me/api/notify'
        line_notify_token = 'epKP9NKi4XqepL0Q6CE11CzVXVJa4MIGo8yWXSkt9Yx' #メモしておいたアクセストークンに置換
        headers = {'Authorization': 'Bearer ' + line_notify_token}
        # メッセージ
        payload = {'message': message}
        # 画像を含むか否か
        if len(args) == 0:
            requests.post(line_notify_api, data=payload, headers=headers)
        else:
            # 画像
            files = {"imageFile": open(args[0], "rb")}
            requests.post(line_notify_api, data=payload, headers=headers, files=files)

if __name__ == "__main__":
    #3箇所変える必要がある
    wakati_text = 'wiki_wakati.txt'
    model_name  = 'wiki_all.model'
    folder_name = 'Doc2vec_'
    text_path = 'C:/Users/shine/OneDrive/prog/Xedge03/wakati_text/' + wakati_text
    model_path = 'C:/Users/shine/OneDrive/prog/Xedge03/model/'

    size, min_count,window = 300,10,8
    mk_model()

#Tabelog_wakati_genre(1-10).txt
#
#