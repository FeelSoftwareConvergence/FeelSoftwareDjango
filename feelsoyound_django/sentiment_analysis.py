import pandas as pd
import numpy as np
import re
import joblib

def sentiment() :
    
    lgbm_clf_save_model = joblib.load('sentiment_analysis.pkl')
    tfidf_save_model = joblib.load('tfidf.pkl')
    
    comment =  "귀여워❤️ 언니 올해는 5월이나 종강할때 꼭 시간내봐요 ㅎㅎ선배 넘 넘 귀엽다!!..."
    content = "#하루필름"
    hashtag = "하루필름"

    if comment != "" :
        comment_sentiment = list(lgbm_clf_save_model.predict(tfidf_save_model.transform([comment])))
    if content != "":
        comment_sentiment.append(lgbm_clf_save_model.predict(tfidf_save_model.transform([content])))
    if hashtag != "" :
        comment_sentiment.append(lgbm_clf_save_model.predict(tfidf_save_model.transform([hashtag])))

    comment_sentiment_result = int(max(comment_sentiment,key = comment_sentiment.count))

    return comment_sentiment_result