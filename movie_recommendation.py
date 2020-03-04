"""
0: adult
1: siries
2: buget
3: genre
4: homepage
5: id
6: imdb_id
7: original lan
8. original title
9. overview
10. popularity
11. poster
12. production company
13. production lan
14. ##
16. revenue
17. runtime
18. spoken lan
19. status
20. tag
21. title
22. video
23. vote_ave
24. vote_cnt
"""

data_hash ={
    'adult' :0,
    'series' : 1,
    'budget' : 2,
    'genres' :3,
    'homepage' :4,
    'id':5,
    'imdb_id':6,
    'original_language':7,
    'original_titile' :8,
    'overview' :9,
    'popularity':10,
    'poster':11,
    'production_company':12,
    'production_country':13,
    'release':14,
    'revenue':15,
    'runtime':16,
    'spoken_language':17,
    'status':18,
    'tagline':19,
    'title':20,
    'video':21,
    'vote_ave':22,
    'vote_cnt':23
}

import csv
data_file =[]

with open("C:/Users/user/Desktop/data/test.csv", mode='r', encoding='utf8', errors='ignore') as f:
    csv= csv.reader(f)    
    for i in csv:
        data_file.append(i)
        #print(i[3].split('}, {'))

def find_value_tag(string, char_tag, pad_lan, char_last= None, data_lan =None):
    value = []

    while(True):
        tag_index = string.find(char_tag)

        if tag_index==-1:
            return value

        if data_lan != None:
            start_index = tag_index+pad_lan+len(char_tag)
            last_index = start_index+data_lan
        
        else:
            start_index = tag_index+pad_lan+len(char_tag)
            last_index = string.find(char_last)

        result_value = string[start_index:last_index]
        value.append(result_value)
        
        next_data_index = string.find(", {")

        if next_data_index == -1:
            break
        string = string[next_data_index+1:]

    return value

def get_genres(predict_set):
    genre_list = []
    for i in predict_set:
        genre_list.append(find_value_tag(i[data_hash['genres']], 'id', 3, char_last=','))
    return genre_list

def get_series(predict_set):
    series_list = []
    for i in predict_set:
        series_list.append(find_value_tag(i[data_hash['series']], 'id', 3, char_last=','))
    return series_list

def get_languages(predict_set):
    series_list = []
    for i in predict_set:
        series_list.append(find_value_tag(i[data_hash['spoken_language']], 'iso_639_1', pad_lan=4, data_lan=2))
    return series_list

def get_company(predict_set):
    company_list = []
    for i in predict_set:
        company_list.append(find_value_tag(i[data_hash['production_company']], 'id', pad_lan=3, char_last='}'))
    return company_list

def get_vote_ave(predict_set):
    company_list = []
    for i in predict_set:
        company_list.append(find_value_tag(i[data_hash['vote_ave']])
    return company_list

print(get_genres(data_file))

