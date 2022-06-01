import pandas as pd
import numpy as np
import re
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.python.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

def sentiment(reply):
    
    tfidf_save_model = joblib.load('tfidf.pkl')
    LSTM_savemodel = load_model("sentiment_analysis123.h5")
    
    content = reply
    content_list = [content]
    tokenizer = Tokenizer(3758)
    tokenizer.fit_on_texts(content_list)
    content_list = tokenizer.texts_to_sequences(content_list)
    max_len = 70
    content_list = pad_sequences(content_list, maxlen = max_len)
    output = np.argmax(LSTM_savemodel.predict(content_list), axis = 1)

    sentiment_result_label = int(output)
    
    text = content
    music_list_df = pd.read_csv('music_remove_dup.csv', encoding="utf-8")
    # 동일 감정 label 확인
    same_label_music = music_list_df[music_list_df['label'] == sentiment_result_label][['title', 'artist', 'Lyric']]
    same_label_music.loc['crawl_data'] = ['crawling_data', 'user', text]

    # word embedding 후 유사도 측정
    tfidf_matrix = tfidf_save_model.fit_transform(same_label_music['Lyric'])
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix)
    recommendation_need = cosine_sim[-1]

    # 첫 번째 문서와 타 문서 간 유사도가 큰 순으로 정렬한 인덱스를 추출하되 자기 자신은 제외
    sorted_index = np.argsort(recommendation_need)[::-1]
    recommend_index = sorted_index[2:11]

    recommend_music_list = same_label_music.iloc[recommend_index]

    return recommend_music_list
