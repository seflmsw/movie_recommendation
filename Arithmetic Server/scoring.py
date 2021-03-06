import pandas as pd
import csv
import get_value

## 코드에 사용될 유사도 반환 함수
def similarites(search_overview, candidates_overviews):
    from numpy import dot
    from numpy.linalg import norm
    import numpy as np

    from sklearn.feature_extraction.text import TfidfVectorizer

    tfidf = TfidfVectorizer(stop_words='english')

    candidates_overviews.insert(0,search_overview)

    data_tfidf = tfidf.fit_transform(candidates_overviews)

    similarities =  data_tfidf.toarray()[0] * data_tfidf[1:,].T


    return similarities

# tfidf 공부
def tfidf():
    from numpy import dot
    from numpy.linalg import norm
    import numpy as np

    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf = TfidfVectorizer(stop_words='english')

    search_string = "he is jin hwan kim"
    data_file = ["he is jin", "he is hwan","she is hong", "metrix is fake"]

    # 검색 데이터와 후보군 데이터를 합침
    data_file.insert(0, search_string)

    # tfidf matrix를 만듦
    data_tfidf = tfidf.fit_transform(data_file)

    # 전체 행렬을 곱할 필요가 없으므로 검색 열[0]을 분리하고, 후보군 행렬([1:,])의 transposed와 곱함.
    # 문자-단어 idf * 단어-문자 idf

    similarities =  data_tfidf.toarray()[0] * data_tfidf[1:,].T

    # 큰 순으로 정렬
    similarities = sorted(similarities, reverse=True)
    print(similarities)

## linear_kernel 공부
def overview_score(search, candidates):
    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf = TfidfVectorizer(stop_words='english')

    candidates.insert(0,search)
    tfidf_matrix = tfidf.fit_transform(candidates)

    from sklearn.metrics.pairwise import linear_kernel
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    sim_scores = list(enumerate(cosine_sim[idx]))

    return list(cosine_sim)
