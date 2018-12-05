"""

MAGA BOX

http://www.megabox.co.kr/

pip가 최신인지 확인..
> python -m pip install --upgrade pip


"""

import re
import json
from jsonpath_rw import jsonpath, parse  # pip install jsonpath-rw      https://pypi.python.org/pypi/jsonpath-rw
from urllib.request import urlopen
from bs4 import BeautifulSoup  # pip install BeatifulSoup4
import requests # http://docs.python-requests.org/en/master/user/quickstart/ pip install requests
from multiprocessing import Queue # python Setup.py build # exe 파일 생성을 위해 꼭 필요
import urllib3  # pip install urllib3

########################################################################################################################
# 공통 변수......
#
dicMovies = {}   # 영화 코드 정보
dicRegions = {}  # 지역코드 정보
dicCinemas = {}  # 극장코드 정보

dicTicketingData = {}  # 티켓팅 정보

http = urllib3.PoolManager()

#
#
#


########################################################################################################################
# 영화(http://www.megabox.co.kr/?menuId=movie) 에서 영화데이터를 가지고 온다. (dicMovies)
#
def crawl_mega_movie(isPrnConsole):

    print( '### 영화(http://www.megabox.co.kr/?menuId=movie) 에서 영화데이터를 가지고 온다. ###' )

    mov_count = 0

    url = 'http://www.megabox.co.kr/pages/movie/Movie_List.jsp'
    fields = {"menuId": "movie"
            , "startNo": "0"
            , "count": "100"
            , "sort": "releaseDate"
              }
    r = requests.post( url, fields )
    # print( r.text )

    soup = BeautifulSoup( r.text, 'html.parser' )


    if isPrnConsole: #################
        print( '-------------------------------------' )
        print( 'no, 코드, 개봉일자, 구분, 영화명' )
        print( '-------------------------------------' )

    tags1 = soup.select( "li.item > div.front-info" )
    for tag1 in tags1:
        #print( tag1 )
        #print( '-------------------------------------------------------------' )


        releasedate = ''
        moviegbn = ''
        moviename = ''

        #tags2 = tag1.select( "div.d_day" )
        #for tag2 in tags2:
        #    releasedate = tag2.text.strip().split(' ')
        #    releasedate = releasedate[0][0:4] + releasedate[0][5:7] + releasedate[0][8:10]
            # print( releasedate )

        tags2 = tag1.select( "div.movie_info > h3.sm_film > span.film_rate" )
        for tag2 in tags2:
            moviegbn = tag2.text.strip()
            # print( moviegbn )


        tags2 = tag1.select( "div.movie_info > h3.sm_film > a.film_title" )
        for tag2 in tags2:
            moviename = tag2.text.strip()
            # print( moviename )

            moviecode = ''
            r = re.compile( '\d+' )
            results = r.findall( tag2['onclick'] )
            for result in results:
                moviecode = result
                #print( moviecode )

                url = 'http://www.megabox.co.kr/pages/movie/Movie_Detail.jsp'
                fields = {"code": moviecode}
                in_r = requests.post( url, fields )
                #print( in_r.text )

                in_soup = BeautifulSoup( in_r.text, 'html.parser' )

                in_tags1 = in_soup.select( "ul.info_wrap > li" )
                for in_tag1 in in_tags1:
                    #print(in_tag1)

                    item_value = ''

                    in_tags2 = in_tag1.select( "strong" )
                    for in_tag2 in in_tags2:
                        item_name = in_tag2.text.strip()
                        #print(item_name)

                        if item_name == '개봉일':
                            in_tag2.extract()  # 자식태그를 제거한다.
                            item_value = in_tag1.text.strip()
                            releasedate = item_value[2:6] +item_value[7:9] +item_value[10:12]
            #

            if isPrnConsole: #################
                mov_count += 1

            dicMovies[moviecode] = [releasedate, moviegbn, moviename]  # 영화데이터 정보

            if isPrnConsole: #################
                print( '{} : {}, {}, {}, {}'.format( mov_count, moviecode, releasedate, moviegbn, moviename) )
#
# 영화(http://www.megabox.co.kr/?menuId=movie) 에서 영화데이터를 가지고 온다. (dicMovies)
#


########################################################################################################################
# 영화관(http://www.megabox.co.kr/?menuId=theater)에서 지역데이터,영화관데이터를 가지고 온다. (dicRegions,dicCinemas)
#
def crawl_mega_cinema(isPrnConsole):

    print( '### 영화관(http://www.megabox.co.kr/?menuId=theater)에서 지역데이터,영화관데이터를 가지고 온다. ###' )

    region_count = 0
    cinema_count = 0

    if isPrnConsole: #################
        print( '-------------------------------------' )
        print( 'no, 코드, 지역명' )
        print( '+- no, 코드, 극장명' )
        print( '-------------------------------------' )

    url = urlopen( "http://www.megabox.co.kr/?menuId=theater" )
    data = url.read().decode( 'utf-8' )
    # print(data)

    soup = BeautifulSoup( data, 'html.parser' )

    tags1 = soup.select( "div.content_wrap > ul > li" )
    for tag1 in tags1:
        # print(tag1)

        tags2 = tag1.select( "a" )
        for tag2 in tags2:
            if tag2.text=='선호영화관':
                continue

            dicRegions[tag2['data-region']] = tag2.text # 지역코드 저장

        # print('-------------')

    for dicRegion in dicRegions:

        if isPrnConsole: #################
            region_count += 1
            print( '{} : {},{}'.format( region_count, dicRegion, dicRegions[dicRegion] ) )

        url = 'http://www.megabox.co.kr/DataProvider'
        fields = {"_command": 'Cinema.getCinemasInRegion'
                    ,"siteCode": '36'
                    ,"areaGroupCode": dicRegion
                    ,"reservationYn": 'N'
                  }
        r = requests.post( url, fields )

        json_obj = r.json()
        # print(json_obj)

        jsonpath_expr = parse( 'cinemaList[*]' )

        i = 0
        for match in jsonpath_expr.find( json_obj ):
            cinemaname    = str( match.value['cinemaName'] )
            cinemacode    = str( match.value['cinemaCode'] )
            kofcinemacode = str( match.value['kofCinemaCode'] )

            dicCinemas[cinemacode] = [dicRegion, cinemaname, kofcinemacode]

            if isPrnConsole:  #################
                cinema_count += 1
                print('{} : {}, {}'.format(cinema_count, cinemacode,cinemaname))
#
# 영화관(http://www.megabox.co.kr/?menuId=theater)에서 지역데이터,영화관데이터를 가지고 온다. (dicRegions,dicCinemas)
#

########################################################################################################################
# 영화관(http://www.megabox.co.kr/?menuId=theater)에서 영화관에 스케줄데이터를 가지고 온다. (dicRegions,dicCinemas)
#
def crawl_mega_schedule(isPrnConsole):

    print( '### 영화관(http://www.megabox.co.kr/?menuId=theater)에서 영화관에 스케줄데이터를 가지고 온다. ###' )

    if isPrnConsole:  #################
        print( '-------------------------------------' )
        print( '일자, 지역명, 극장명' )
        print( '-------------------------------------' )

    for count in range( 0, 4):  # 4일간

        dicPlaydate = {}

        for dicCinema in dicCinemas: # 극장들을 순환
            #print( dicRegions[dicCinemas[dicCinema][0]]+','+ dicCinemas[dicCinema][1] )

            #--#
            #if dicCinema != '6902':  continue # 제주아라....

            dicSchMovies = {}    # 스케쥴 > 극장 / 영화 정보
            dicSchRooms = {}     # 스케쥴 > 관 정보
            dicSchMovRooms = {}  # 스케쥴 > 극장 / 영화 / 관 정보

            url = 'http://www.megabox.co.kr/pages/theater/Theater_Schedule.jsp'
            fields = {"cinema": dicCinema, "count": count}

            r = requests.post( url, fields )
            # print(r.text)

            soup = BeautifulSoup( r.text, 'html.parser' )
            # print( '-------------------------------------------------------------' )

            tags1 = soup.select( "input#playDate" )
            for tag1 in tags1:
                val = [v[0:4] + v[5:7] + v[8:10]  for k,v in tag1.attrs.items() if (k=='value')]
                playdate = val[0]
                #print(playdate)

                if isPrnConsole:  #################
                    print( '{} : {}, {}'.format( playdate, dicRegions[dicCinemas[dicCinema][0]], dicCinemas[dicCinema][1] ) )

            moviecode = ''
            moviegbn = ''
            moviename = ''
            cinemaroom = ''
            moviegubun = ''

            noRooms = 0
            cntRoom = 1
            tags1 = soup.select( "table.movie_time_table > tr.lineheight_80" )
            for tag1 in tags1:
                # print(tag1)

                noRooms += 1

                tags2 = tag1.select( "th.title > div > span.age_m" )
                for tag2 in tags2:
                    # print(tag2.attrs.values())
                    if tag2.text != '':
                        moviegbn = tag2.text
                        # print( tag2 ) # 15세 관람가

                tags2 = tag1.select( "th.title > div > strong" )
                for tag2 in tags2:
                    if tag2.text == '\xa0':
                        cntRoom += 1 # 같은 영화가 반복 관이 추가
                    else:
                        cntRoom = 1
                        moviename = tag2.text
                        # print( tag2 ) # 겟 아웃


                tags2 = tag1.select( "th.room > div" )
                for tag2 in tags2:
                    cinemaroom = tag2.text
                    # print( tag2 ) # 4관

                tags2 = tag1.select( "th.room > small" )
                for tag2 in tags2:
                    moviegubun = tag2.text
                    # print( tag2 ) # 디지털(자막)

                dicHoverTime = {} #
                tags2 = tag1.select( "td > div.cinema_time" )
                for tag2 in tags2:

                    time = ''
                    type = ''
                    seat = ''

                    tags3 = tag2.select( "a" )
                    # print( tags3)

                    if len( tags3 ) > 0:   # print( '일반' )

                        for tag3 in tags3:
                            onclick = ''.join( tag3['onclick'].split() ) #  모든 공백 문자를 제거하는 경우
                            #print(onclick)
                            moviecode = onclick[29:35]

                            tags4 = tag3.select( "span.hover_time" )
                            # print(tags4)
                            for tag4 in tags4:
                                times = tag4.text.split( '~' )

                                dicHoverTime[times[0]] = [times[1], ]  ##############################

                    else:  # print( '예매마감' )

                        tags3 = tag2.select( "p.time_info" )
                        for tag3 in tags3:
                            tags4 = tag3.select( "span.time" )
                            for tag4 in tags4:
                                times = [tag4.text, '']
                                # print( tag4 )

                            tags4 = tag3.select( "span.seat" )
                            for tag4 in tags4:
                                seat = tag4.text # '예매마감'
                                # print( tag4 )

                        dicHoverTime[times[0]] = [times[1], '예매마감', seat ]  ##############################

                    tags3 = tag2.select( "p.time_info" )
                    for tag3 in tags3:
                        tags4 = tag3.select( "span.type" )
                        for tag4 in tags4:
                            type = tag4.text
                            # print( tag4 )

                        tags4 = tag3.select( "span.time" )
                        for tag4 in tags4:
                            time = tag4.text
                            # print( tag4 )

                        tags4 = tag3.select( "span.seat" )
                        for tag4 in tags4:
                            seat = tag4.text
                            # print( tag4 )

                        dicHoverTime[times[0]].append( type )
                        dicHoverTime[times[0]].append( seat )

                dicSchRooms[noRooms] = [moviecode, moviename, moviegbn, cntRoom, cinemaroom, moviegubun, dicHoverTime]  ####
                # print(cntRoom,moviename)

            # 영화별로 추려내고
            old_moviecode = ''
            for k, v in dicSchRooms.items():
                if old_moviecode != str( v[0] ):
                    dicSchMovies[str( v[0] )] = [v[1], v[2]]  #### playdate, moviename, moviegbn 만 이동..
                    old_moviecode = str( v[0] )

            # 다시 영화별/관별 로 loop를 돌아.. dicSchMovRooms생성..
            for dicSchMovie in dicSchMovies:
                for k, v in dicSchRooms.items():
                    if dicSchMovie == v[0] : # moviecode
                        dicSchMovRooms[k] = [dicSchMovie, v[3], v[4], v[5], v[6]]

            for dicSchMovie in dicSchMovies:
                dictmp = {} # 관별 시간표 임시 dictionary
                for k, v in dicSchMovRooms.items():
                    if v[0] == dicSchMovie:
                        dictmp[k] = v
                # print(dictmp )

                dicSchMovies[dicSchMovie].append(dictmp)

            dicPlaydate[dicCinema] = dicSchMovies

         # for dicCinema in dicCinemas:

        dicTicketingData[playdate] = dicPlaydate

    # for count in range( 0, 3 ):  # 3일간

#
# 영화관(http://www.megabox.co.kr/?menuId=theater)에서 영화관에 스케줄데이터를 가지고 온다. (dicRegions,dicCinemas)
#


########################################################################################################################
# MAGA 클로링 정보 올리기..
#
def crawl_mega_upload():

    print( '### 서버 전송 시작 ###' )

    fields = { "movies": str( dicMovies )
             , "regions": str( dicRegions )
             , "cinemas": str( dicCinemas )
             , "ticketingdata": str( dicTicketingData )
             }
    url = 'http://www.mtns7.co.kr/totalscore/upload_mega.php'

    r = http.request( 'POST', url, fields )

    data = r.data.decode( 'utf-8' )

    print( '[', data, ']' )

    print( '### 서버 전송 종료 ###' )
#
# MAGA 클로링 정보 올리기..
#


########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################


if __name__ == '__main__':

    crawl_mega_movie(True) # 영화(http://www.megabox.co.kr/?menuId=movie) 에서 영화데이터를 가지고 온다. (dicMovies)

    crawl_mega_cinema(True) # 영화관(http://www.megabox.co.kr/?menuId=theater)에서 지역데이터,영화관데이터를 가지고 온다. (dicRegions,dicCinemas)

    crawl_mega_schedule(True) # 영화관(http://www.megabox.co.kr/?menuId=theater)에서 영화관에 스케줄데이터를 가지고 온다. (dicRegions,dicCinemas)

    # print( '-------------------------------------------------------------dicRegions' )
    # for k, v in dicRegions.items():
    #     print( '{} {}'.format( k, v ) )
    # print( '-------------------------------------------------------------' )
    #
    # print( '-------------------------------------------------------------dicMovies' )
    # for k, v in dicMovies.items():
    #     print( '{} {}'.format( k, v ) )
    # print( '-------------------------------------------------------------' )
    #
    # print( '-------------------------------------------------------------dicSchRoom' )
    # for k, v in dicSchRooms.items():
    #     print( '{} {}'.format( k, v ) )
    # print( '-------------------------------------------------------------' )
    #
    # print( '-------------------------------------------------------------dicCinemas' )
    # for k, v in dicCinemas.items():
    #     print( '{} {}'.format( k, v ) )

    crawl_mega_upload()

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
