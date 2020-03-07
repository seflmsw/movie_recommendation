import csv
import filter
import get_value
import scoring

meta_file_url_D = "C:/Users/luraw/OneDrive/Desktop/data/movies_metadata.csv"
meta_file_url_L = "C:/Users/user/Desktop/data/test_meta.csv"

rating_file_url_D = "C:/Users/luraw/OneDrive/Desktop/data/test_ratings.csv"
rating_file_url_L = "C:/Users/user/Desktop/data/test_ratings.csv"

def temp_db_load(url):
    data_file =[]

    with open(url, mode='r', encoding='utf8', errors='ignore') as f:
        csv_ = csv.reader(f)
        for i in csv_:
            data_file.append(i)
        return data_file

def recommend(search, data_file, n):
    # search : 찾을 영화를 웹에서 입력해서 전달 받을 것
    # data_file = 영화 메타 데이터 정보를 DB에서 전달 받을 것
    # n : 추천할 영화 개수를 메인 서버에서 결정해서 전달 받을 것

    # return : 추천할 n개의 영화
    data = data_file[1:]

    index = input("search movie index : ")
    search = data[int(index)]

    search_list = []
    search_list.append(search)
    candidates = filter.sub_list(data, search_list)

    selected, candidates = filter.stream_filter(search,candidates, n)

    def test_filter_works(selected, search):
        ## Test filter works 
        print("s",get_value.languages(search),get_value.series(search),get_value.genres(search), get_value.vote_ave(search))
        rank = 1
        for line in selected:
            print(rank, get_value.languages(line),get_value.series(line),get_value.genres(line), get_value.vote_ave(line))
            rank+=1

    n = n - len(selected)

    score_list = []

    overview_search = get_value.overview(search)
    overview_candidates =get_value.get_overviews(candidates)

    overview_smi = scoring.similarites(overview_search, overview_candidates)

    #batman_series 
    print("search : ",get_value.title(search))
    print("\n")
    print("selected : ")

    for s in selected:
        print(get_value.title(s))

    print("\n")
    print("candidates : ")

    titles = get_value.get_titles(candidates)

    i =0
    for o in overview_smi:
        if o> 0.05:
            if titles[i] != None:
                print(titles[i])
        i+=1

data_temp = temp_db_load(meta_file_url_D)

recommend("temp_search", data_temp, 10)