import csv
import sys
import threading

import filter
import get_value
import scoring
import socket_connection

def file_load(url):
    data_file =[]

    with open(url, mode='r', encoding='utf8', errors='ignore') as f:
        csv_ = csv.reader(f)
        for i in csv_:
            data_file.append(i)
        return data_file

def input_title_to_search(search_title,data_movies):
    search_index = -1

    for index in range(len(data_movies)):
        if search_title.lower() == get_value.title(data_movies[index]).lower():
            search_index = index
            return data_movies[index]

    if search_index == -1:
        return None
        ## 영화가 데이터에 없음 

def recommend(search, data_movies, n, Mode= "G"):
    # search : 찾을 영화를 웹에서 입력해서 전달 받을 것
    # data_file = 영화 메타 데이터 정보를 DB에서 전달 받을 것
    # n : 추천할 영화 개수를 메인 서버에서 결정해서 전달 받을 것
    # return : 추천할 n개의 영화

    data = data_movies

    search_list = []
    search_list.append(search)

    ## 데이터에서 검색군 제거
    candidates = filter.sub_list(data, search_list)

    ## 필터로 언어, 시리즈, 장르 유사를 확인
    if Mode == "G":
        selected, candidates = filter.stream_filter(search,candidates, n)
    else:
        selected, candidates = filter.stream_filter_withoutGenre(search,candidates, n)

    n = n - len(selected)
    score_list = []

    ## 필터에서 선택된 선택군의 내용 유사 점수를 계산하여 추가

    overview_search = get_value.overview(search)
    s_overview_smi = scoring.similarites(overview_search, get_value.get_overviews(selected))

    for smi_score in s_overview_smi:
        smi_score = round(smi_score, 3) * 100
        score_list.append(smi_score)

    ## 남은 후보군을 내용 유사도 계산 후 선택군에 추가

    overview_candidates =get_value.get_overviews(candidates)
    overview_smi = scoring.similarites(overview_search, overview_candidates)

    ## 점수를 기준으로 정렬하여 선택군에 추가

    c_overview_smi = []
    for index in range(len(candidates)):
        temp = (index,overview_smi[index])
        c_overview_smi.append(temp)

    sorted_c_overview_smi = sorted(c_overview_smi, key = lambda x : x[1], reverse =True)

    for lot in range(n):
        smi_score = sorted_c_overview_smi[lot][1]
        smi_score = round(smi_score,3)*100
        score_list.append(smi_score)
        selected.append(candidates[lot])

    ## 반환은 선택군과, 점수표를 반환
    return selected, score_list

def refine_data(string):
    if type(string) is list:
        string = str(string)

    return string.replace('[',"").replace("]","").replace("\'","")

def print_result(number, movie, lines):
    title = get_value.title(movie)
    temp_line = str(number)+"."+ title
    #print(temp_line)

    lines.append(temp_line)
    
    languages = get_value.languages(movie)
    languages = refine_data(languages)
    
    temp_line = "languages : " + languages

    lines.append(temp_line)
    

    genres = get_value.genres_name(movie)
    genres = refine_data(genres)
    temp_line = "genres : " + genres

    lines.append(temp_line)

    series = get_value.series_name(movie)
    series = refine_data(series)
    if series != "":
        temp_line = "series : " + series
        lines.append(temp_line)
        
    companies = get_value.company_name(movie)
    companies = refine_data(companies)

    if companies != "":
        temp_line = "companies : " + companies

        lines.append(temp_line)

    overview = get_value.overview(movie)
    overview = refine_data(overview)

    if overview != "":
        temp_line = "overview : "+ overview

        lines.append(temp_line)

    vote_ave = get_value.vote_ave(movie)
    vote_ave = refine_data(vote_ave)

    if vote_ave != "":
        temp_line = "vote_ave : "+ vote_ave

        lines.append(temp_line)


    temp_line =""
    
    lines.append(temp_line)

def make_html(search, selected):
    lines = []

    temp_line = "[search]"
    lines.append(temp_line)
    #print(temp_line)

    print_result("S", search, lines)

    temp_line = "[selected]"
    lines.append(temp_line)
    #print(temp_line)

    for top in range(len(selected)):
        print_result(top+1, selected[top], lines)

    return lines

def rcv_load_metaData(client_socket, db_url):
    # 버젼과 캐시데이터 구현 추가 필요
    # version = socket_connection.get_file_version()
    # version check()

    # meta_data를 db에 저장, db에서 load
    file_url = socket_connection.file_receive(client_socket, db_url)

    socket_connection.msg_send(client_socket,"download_end")

    # 전달 받은 영화 데이터를 load / 소켓 종료
    db_data = file_load(file_url)
    data_file = db_data[1:]
    socket_connection.msg_send(client_socket,"fileLoad_end")
    socket_connection.socket_close(client_socket)

    return data_file

db = "C:/Users/luraw/OneDrive/Desktop/db/db.csv"
n =10

if __name__ == "__main__":

    ip = '127.0.0.1'
    port = 8888

    ### 연산 서버는 시작되면 최초 한번 DB를 받고, 연결이 끊김
    # 다시 연결되서 부터는 더 이상 종료 없이 제목만 받아 연산 처리
    # -> 소켓 서버가 연결된 상태에서 DB를 받고, spring app을 run 한 후, 앞선 소켓 서버를 사용하려면 중복된 ip라고 연결 종료.

    ## 연산 서버 시작 시 -> DB 저장
    # Spring server와 연산
    client_socket=socket_connection.connect(ip, port)
    if (client_socket)== None:
        print("connection Error")
        sys.exit(1)

    print("=== receive data ===")
    data_file = rcv_load_metaData(client_socket, db)
    
    # 추천 영화 수보다 데이터 수가 더 적으면 n을 데이터 수-1로. -> escape index out of range
    if len(data_file) < n:
        n = len(data_file)-1

    ## DB 저장되면, 연결을 끊었다가 재연결해서 이때 부턴 서버에서 보낸 데이터를 처리


    while True:
        print("=== wait for connection ===")
        client_socket = None
        while True:
            client_socket = socket_connection.connect(ip, port)
            if client_socket != None:
                break

        print("\n=== wait for title === ")

        # 영화 제목 입력 받음
        rcv_search_string = socket_connection.msg_receive(client_socket) ## title

        # 영화 제목을 meta_data에서 찾아서 line 추출
        search_line = input_title_to_search(rcv_search_string, data_file)

        isDataLive = True

        if search_line == None:
            isDataLive = False

        else:
            if get_value.genres(search_line) == "" and get_value.languages(search_line) == "":
                isDataLive = False
                ## 변수명 리팩토링?? 시급!!!

        # 추천 과정
        result_lines = []

        if isDataLive:
            selected, score_list = recommend(search_line, data_file, n)
            result_lines = make_html(search_line, selected)

        else:
            # 데이터 에러
            print("=== NO DATA ===")
            result_lines.append("!None")

        # 추천 영화 목록을 spring 서버에 전송
        socket_connection.send_result_lines(client_socket,result_lines)

         # 소켓 close
        socket_connection.socket_close(client_socket)

        