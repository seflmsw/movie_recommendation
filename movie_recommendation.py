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
14. release
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
    'vote_cnt':23 }

import csv
data_file =[]

with open("C:/Users/user/Desktop/data/test.csv", mode='r', encoding='utf8', errors='ignore') as f:
    csv= csv.reader(f)    
    for i in csv:
        data_file.append(i)
        #print(i[3].split('}, {'))

def print_list(list_):
    for line in list_:
        print(line,'\n')

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

def get_genres_by_line(line):
    return find_value_tag(line[data_hash['genres']], 'id', 3, char_last=',')

def get_series_by_line(line):
    return find_value_tag(line[data_hash['series']], 'id', 3, char_last=',')

def get_languages_by_line(line):
    return find_value_tag(line[data_hash['spoken_language']], 'iso_639_1', pad_lan=4, data_lan=2)

def get_company_by_line(line):
    return find_value_tag(line[data_hash['production_company']], 'id', pad_lan=3, char_last='}')

def get_vote_ave_by_line(line):
    return line[data_hash['vote_ave']]

def get_vote_cnt_by_line(line):
    return line[data_hash['vote_cnt']]

    vote_cnt = []
    for i in predict_set:
        vote_cnt.append(get_vote_cnt_by_line(i))
    return vote_cnt

def isExist(main_set, compare_set):
    for feature in main_set:
        for c in compare_set:
            if feature==c:
                return True
    
    return False

def sub_list(pre, post):
    for p in post:
        pre.remove(p)
    return pre

def same_language(search_line, compare_set):
    search_language = get_languages_by_line(search_line)

    new_compare_set = [] 
    for line in compare_set:
        compare_language = get_languages_by_line(line)
        if isExist(search_language,compare_language):
            new_compare_set.append(line)
    
    return new_compare_set

def same_series(search_line, compare_set):
    search_series = get_series_by_line(search_line)

    if search_series != []:   
        same_series_set = [] 
        for line in compare_set:
            compare_series = get_series_by_line(line)
            if isExist(search_series,compare_series):
                same_series_set.append(line)
        return same_series_set
    
    else:
        return compare_set    

def same_genre_score(search_line, compare_set):
    search_genre = get_genres_by_line(search_line)

    score_set = []
    for line in compare_set:
        score = 0
        compare_genre = get_genres_by_line(line)
        for sg in search_genre:
            for cg in compare_genre:
                if sg==cg:
                    score += 1
        score_set.append(score)

    return score_set

def filt(same_movies, candidates, n, selected):
    r = len(same_movies)

    if  r < n:
        sorted(same_movies, key = lambda x : x[data_hash['vote_ave']], reverse =True)
        for movie in same_movies:
            selected.append(movie)
        n= n-r
        candidates = sub_list(candidates, same_movies)
    
    elif r == n:
        sorted(same_movies, key = lambda x : x[data_hash['vote_ave']], reverse =True)
        for movie in same_movies:
            selected.append(movie)
        return None,0

    else:
        candidates = same_movies

    return candidates,n

def filt_genre(search, candidates, n, selected):
    genre_score = same_genre_score(search, candidates)
    max_score = max(genre_score)
    
    dif_score=0
    while(True):
        exprected_score = max_score - dif_score
       
        if exprected_score ==0:
            return candidates,n
        
        r = genre_score.count(exprected_score)
        
        index_list = []
        lines_list = [] 

        for index, value in enumerate(genre_score):
            if value == exprected_score:
                index_list.append(index)

        for index in index_list:
            lines_list.append(candidates[index])

        if r < n :
            sorted(lines_list, key = lambda x : x[data_hash['vote_ave']], reverse =True)
            for movie in lines_list:
                selected.append(movie)
            n = n-r
            dif_score+=1
        
        elif r == n :
            sorted(lines_list, key = lambda x : x[data_hash['vote_ave']], reverse =True)
            for movie in lines_list:
                selected.append(movie)
            return None,0

        else:
            candidates = lines_list
            return candidates, n

def stream_filter(search, data_file, n):
    selected = []

    search_list = []
    search_list.append(search)
    
    candidates = sub_list(data_file, search_list)
    
    print("number of data : ", len(candidates))

    ## filter same language 

    same_languages_movies = same_language(search,candidates)
    candidates,n = filt(same_languages_movies, candidates, n, selected)
    same_language_cnt = len(candidates)
    
    if n == 0:
        print("selecting complete")
        return selected,0 
    else:
        print("number of same languages : ", same_language_cnt)

    ## find same series

    same_series_movies = same_series(search, candidates)
    candidates,n = filt(same_series_movies, candidates, n, selected)
    
    n_series_cnt = len(candidates)
    same_series_cnt = same_language_cnt - n_series_cnt
    
    left_temp = n

    if n == 0:
        print("selecting complete")
        return selected,0 
    else:
        print("number of same series : ", same_series_cnt)
        print("left candidates : ", n_series_cnt)

    ## get same genre movies

    candidates, n = filt_genre(search, candidates, n, selected)
    
    same_genre_number = left_temp - n

    if n == 0:
        print("selecting complete")
        return selected,0 
    else:
        print("number of same genre : ", same_genre_number)
        print("left candidates : ", len(candidates))

    return candidates, n

index = input("search movie index : ")

search_movie = data_file[int(index)]

candidates, selected_n = stream_filter(search_movie,data_file, 10)

print("selected : ",selected_n)

