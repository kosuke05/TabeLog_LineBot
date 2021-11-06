from gensim.models import KeyedVectors

def relevance(w):
    try:
        model = KeyedVectors.load_word2vec_format('TabelogAdd.vec.pt', binary=True)
        food = w
        results = model.most_similar(positive = [food,'食べ物'])
        food_list = [results[0][0],results[1][0],results[2][0],results[3][0],results[4][0],results[5][0],results[6][0],results[7][0],results[8][0],results[9][0]]
        similar_list = [results[0][1],results[1][1],results[2][1],results[3][1],results[4][1],results[5][1],results[6][1],results[7][1],results[8][1],results[9][1]]
        return food_list,similar_list,0

    except KeyError as e:
        print('error:コーパスにありません')
        return e,1

    except FileNotFoundError as e:
        print('error:モデルが見つかりません')
        return e,2

if __name__ == "__main__":
    word='ラーメン'
    print(relevance(word))