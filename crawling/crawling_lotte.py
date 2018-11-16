'''
롯데 시네마

http://www.lottecinema.co.kr/

'''

import random
import datetime, time
import urllib3  # pip install urllib3
import json
from jsonpath_rw import jsonpath, parse  # pip install jsonpath-rw      https://pypi.python.org/pypi/jsonpath-rw
from multiprocessing import Queue # python Setup.py build # exe 파일 생성을 위해 꼭 필요
import urllib3  # pip install urllib3


#########################################################################################################################################
# 공통 변수......
#
delayTime = 1

dicMovieData = {}  # 영화데이터 정보
dicCinemas = {}  # 극장 코드 정보
dicMovies = {}  # 영화 코드 정보

dicTicketingData = {}  # 티켓팅 정보

http = urllib3.PoolManager()

ostype    = "Chrome"
osversion = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.105 Safari/537.36 Swing/4.0.0.11"

#
#
#


#########################################################################################################################################
# 영화 / 박스 오피스(http://www.lottecinema.co.kr/LCHS/Contents/Movie/Movie-List.aspx) 에서 영화데이터를 가지고 온다. (dicMovieData)
#
def crawl_lotte_boxoffice(isPrnConsole):

    print('### 영화 / 박스 오피스(http://www.lottecinema.co.kr/LCHS/Contents/Movie/Movie-List.aspx) 에서 영화데이터를 가지고 온다. ###')

    movie_count = 0

    if isPrnConsole:  #################
        print( '-------------------------------------' )
        print( 'no, 코드, 영화명, 장르, 예매, 개봉일, 관람등급' )
        print( '-------------------------------------' )

    fields = {"paramList":
                          '{"MethodName":"GetMovies",'
                          '"channelType":"HO",'
                          '"osType":"' + ostype + '",'
                          '"osVersion":"' + osversion + '",'
                          '"multiLanguageID":"KR",'
                          '"division":1,'
                          '"moviePlayYN":"Y",'
                          '"orderType":"1",'
                          '"blockSize":100,'
                          '"pageNo":1'
                          '}'
                      }
    url = 'http://www.lottecinema.co.kr/LCWS/Movie/MovieData.aspx?nocashe=' + str( random.random() )
    r = http.request( 'POST', url, fields )
    time.sleep( delayTime )

    data = r.data.decode( 'utf-8' )
    # print(data)

    json_obj = json.loads( data )

    jsonpath_expr = parse( 'Movies.Items[*]' )

    for match in jsonpath_expr.find( json_obj ):
        representationmoviecode = str( match.value['RepresentationMovieCode'] )
        movienamekr             = str( match.value['MovieNameKR'] ).strip()
        moviegenrename          = str( match.value['MovieGenreName'] )
        bookingyn               = str( match.value['BookingYN'] )
        releasedate             = str( match.value['ReleaseDate'] )
        releasedate             = releasedate[0:4] + releasedate[5:7] + releasedate[8:10]
        viewgradenameus         = str( match.value['ViewGradeNameUS'] )

        if movienamekr == '' or movienamekr == 'AD': continue

        dicMovieData[representationmoviecode] = [movienamekr, moviegenrename, bookingyn, releasedate, viewgradenameus]  # 영화데이터 정보

        if isPrnConsole: #################
            movie_count += 1
            print( '{} : {},{}'.format( movie_count, representationmoviecode, movienamekr, moviegenrename, bookingyn, releasedate, viewgradenameus ) )

    fields = {"paramList":
                          '{"MethodName":"GetMovies",'
                          '"channelType":"HO",'
                          '"osType":"' + ostype + '",'
                          '"osVersion":"' + osversion + '",'
                          '"multiLanguageID":"KR",'
                          '"division":1,'
                          '"moviePlayYN":"N",'
                          '"orderType":"5",'
                          '"blockSize":100,'
                          '"pageNo":1'
                          '}'
                      }
    url = 'http://www.lottecinema.co.kr/LCWS/Movie/MovieData.aspx?nocashe=' + str( random.random() )
    r = http.request( 'POST', url, fields )
    time.sleep( delayTime )

    data = r.data.decode( 'utf-8' )
    # print(data)

    json_obj = json.loads( data )

    jsonpath_expr = parse( 'Movies.Items[*]' )

    for match in jsonpath_expr.find( json_obj ):
        representationmoviecode = str( match.value['RepresentationMovieCode'] )
        movienamekr             = str( match.value['MovieNameKR'] )
        moviegenrename          = str( match.value['MovieGenreName'] )
        bookingyn               = str( match.value['BookingYN'] )
        releasedate             = str( match.value['ReleaseDate'] )
        releasedate             = releasedate[0:4] + releasedate[5:7] + releasedate[8:10]
        viewgradenameus         = str( match.value['ViewGradeNameUS'] )

        if movienamekr == '' or movienamekr == 'AD': continue

        dicMovieData[representationmoviecode] = [movienamekr, moviegenrename, bookingyn, releasedate, viewgradenameus]  # 영화데이터 정보

        if isPrnConsole:  #################
            movie_count += 1
            print( '{} : {},{},{},{},{},{}'.format( movie_count, representationmoviecode, movienamekr, moviegenrename, bookingyn, releasedate, viewgradenameus ) )
#
# 영화 / 박스 오피스 (http://www.lottecinema.co.kr/LCHS/Contents/Movie/Movie-List.aspx) 에서 영화데이터를 가지고 온다. (dicMovieData)
#


#########################################################################################################################################
# 영화관 (http://www.lottecinema.co.kr/LCHS/Contents/Cinema) 에서 극장데이터를 가지고 온다. (dicCinemas)
#
def crawl_lotte_cinema(isPrnConsole):

    print( '### 영화관 (http://www.lottecinema.co.kr/LCHS/Contents/Cinema) 에서 극장데이터를 가지고 온다. ###' )

    cinema_count = 0

    if isPrnConsole:  #################
        print( '-------------------------------------' )
        print( 'no, 코드, 스페셜관, 정렬일련번호, 극장명' )
        print( '-------------------------------------' )

    specialcinemas = ["0300",  ## 스페셜관(샤롯데) 지정
                      "0941",  ## 스페셜관(수퍼플렉스 G) 지정
                      "0940",  ## 스페셜관(수퍼플렉스) 지정
                      "0930",  ## 스페셜관(수퍼 4D) 지정
                      "0910",  ## 스페셜관(수퍼바이브) 지정
                      "0960",  ## 스페셜관(씨네패밀리) 지정
                      "0200",  ## 스페셜관(씨네커플) 지정
                      "0950"   ## 스페셜관(씨네비즈) 지정
                      ]
    for specialcinema in specialcinemas:
        # print(specialcinema)

        fields = {"paramList":
                      '{"MethodName":"SpecialCinemaList",'
                      '"channelType":"HO",'
                      '"osType":"' + ostype + '",'
                      '"osVersion":"' + osversion + '",'
                      '"DetailDivisionCode":"' + specialcinema + '",'
                      '"Latitude":"37.5675451", "Longitude":"126.9773356"'
                      '}'
                  }
        url = 'http://www.lottecinema.co.kr/LCWS/Cinema/CinemaData.aspx?nocashe=' + str( random.random() )
        r = http.request( 'POST', url, fields )
        time.sleep( delayTime )

        data = r.data.decode( 'utf-8' )
        # print(data)

        json_obj = json.loads( data )

        jsonpath_expr = parse( 'Cinemas.Items[*]' )

        i = 0
        for match in jsonpath_expr.find( json_obj ):
            cinemaid     = str( match.value['CinemaID'] )
            cinemanamekr = match.value['CinemaNameKR']
            sortsequence = match.value['SortSequence']

            i = i + 1

            dicCinemas[cinemaid] = ['Y', sortsequence, cinemanamekr]  # 극장(스페셜괌)정보저장

            if isPrnConsole:  #################
                cinema_count += 1
                print( '{} : {},{},{},{}'.format( cinema_count, cinemaid, 'Y', sortsequence, cinemanamekr ) )

    detaildivisioncodes = ["1",   ## 서울
                           "2",   ## 경기/인천
                           "3",   ## 충청/대전
                           "4",   ## 전라/광주
                           "5",   ## 경북/대구
                           "101", ## 경남/부산/울산
                           "6",   ## 강원
                           "7"    ## 제주
                           ]
    for detaildivisioncode in detaildivisioncodes:

        fields = {"paramList":
                      '{"MethodName":"GetCinemaByArea",'
                      '"channelType":"HO",'
                      '"osType":"' + ostype + '",'
                      '"osVersion":"' + osversion + '",'
                      '"multiLanguageID":"KR",'
                      '"divisionCode":"1","detailDivisionCode":"' + detaildivisioncode + '"'
                      '}'
                  }
        url = 'http://www.lottecinema.co.kr/LCWS/Cinema/CinemaData.aspx?nocashe=' + str( random.random() )
        r = http.request( 'POST', url, fields )
        time.sleep( delayTime )

        data = r.data.decode( 'utf-8' )

        json_obj = json.loads( data )

        jsonpath_expr = parse( 'Cinemas.Items[*]' )

        i = 0
        for match in jsonpath_expr.find( json_obj ):
            cinemaid     = str( match.value['CinemaID'] )
            cinemaname   = match.value['CinemaName']
            sortsequence = match.value['SortSequence']

            i = i + 1

            dicCinemas[cinemaid] = ['N', sortsequence, cinemaname]  # 극장 정보저장

            if isPrnConsole:  #################
                cinema_count += 1
                print( '{} : {},{},{},{}'.format( cinema_count, cinemaid, 'N', sortsequence, cinemanamekr ) )

#
# 영화관 (http://www.lottecinema.co.kr/LCHS/Contents/Cinema) 에서 극장데이터를 가지고 온다. (dicCinemas)
#


#########################################################################################################################################
# 영화관 (http://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx) 에서 극장데이터를 가지고 온다. (dicTicketingData)
#
def crawl_lotte_ticketingdata(isPrnConsole):

    print( '### 영화관 (http://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx) 에서 극장데이터를 가지고 온다. ###' )

    movie_count = 0
    ticket_count = 0

    days = []

    date1 = datetime.date.today()  ## 오늘자 날짜객체
    date2 = date1 + datetime.timedelta( days=1 )
    date3 = date2 + datetime.timedelta( days=1 )
    date4 = date3 + datetime.timedelta( days=1 )

    days.append( '{:04d}-{:02d}-{:02d}'.format( date1.year, date1.month, date1.day ) )  ## 오늘의 날짜
    days.append( '{:04d}-{:02d}-{:02d}'.format( date2.year, date2.month, date2.day ) )  ## 오늘+1의 날짜
    days.append( '{:04d}-{:02d}-{:02d}'.format( date3.year, date3.month, date3.day ) )  ## 오늘+2의 날짜
    days.append( '{:04d}-{:02d}-{:02d}'.format( date4.year, date4.month, date4.day ) )  ## 오늘+3의 날짜

    # 4일간 자료 가져오기

    for today in days:
        #
        # 전체극장을 돌면서 각각의 정보를 가져온다.
        #

        dicTeather = {}

        for dicCinema in dicCinemas:
            # print(dicCinema +'//' +str(dicCinemas[dicCinema]))
            #if dicCinema != '9013': # 서귀포
            #  CinemaID=1013 #  가산디지컬
            #     continue
            #if dicCinema != '1013': #  가산디지컬
            #    continue

            fields = {"paramList":
                          '{"MethodName":"GetPlaySequence",'
                          '"channelType":"HO",'
                          '"osType":"' + ostype + '",'
                          '"osVersion":"' + osversion + '",'
                          '"playDate":"' + today + '",'
                          '"cinemaID":"1|1|' + dicCinema + '",'
                          '"representationMovieCode":""'
                          '}'
                      }
            url = 'http://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx?nocashe=' + str( random.random() )

            r = http.request( 'POST', url, fields )
            time.sleep( delayTime )
            # status = r.status
            data = r.data.decode( 'utf-8' )
            # print( data )

            json_obj = json.loads( data )
            # print(json_obj['PlaySeqsHeader'])

            jsonpath_expr1 = parse( 'PlaySeqsHeader.Items[*]' )
            jsonpath_expr2 = parse( 'PlaySeqs.Items[*]' )

            if isPrnConsole:  #################
                print( '-------------------------------------' )
                print( '일자, no, 코드, 영화명, 장르, 더빙/자막' )
                print( '-------------------------------------' )

            moviecode_old = ''
            for match1 in jsonpath_expr1.find( json_obj ):
                moviecode  = match1.value['MovieCode']

                if moviecode_old != moviecode :
                    moviename  = match1.value['MovieNameKR']                  # 영화명
                    filmnamekr = match1.value['FilmNameKR']                   # 필름종류
                    gubun      = match1.value['TranslationDivisionNameKR']  # 더빙/자막

                    dicMovies[moviecode] = [moviename, filmnamekr, gubun]  # 영화정보를 저장한다. 영화명 + 필름종류 + 더빙/자막

                    # for match1_1 in jsonpath_expr1.find( json_obj ):
                    # i = i + 1
                    # print( i)
                    if isPrnConsole:  #################
                        movie_count += 1
                        print( '{},{} : {},{},{},{}'.format( today, movie_count, moviecode, moviename, filmnamekr, gubun ) )

                    moviecode_old = moviecode
            #

            if isPrnConsole:  #################
                print( '-------------------------------------' )
                print( '일자, no, 티켓코드, 극장명, 상영관그룹명, 상영관명, 영화명, 영화구분, 개봉일, 시작시간, 끝시간, 예약좌석수, 총좌석수' )
                print( '-------------------------------------' )
            #


            ## dicScreen를 먼저구하기 위해 2번 돈다.
            dicScreen = {}
            for match2 in jsonpath_expr2.find( json_obj ):
                screenid       = match2.value['ScreenID']  # 상영관 코드
                screennamekr   = match2.value['ScreenNameKR']  # 상영관명
                totalseatcount = match2.value['TotalSeatCount']  # 총좌석수

                dicScreen[screenid] = [screennamekr, totalseatcount]

            screenid_old = None
            screenNo = 0
            degreeNo = 0
            for match2 in jsonpath_expr2.find( json_obj ):
                cinemanamekr          = match2.value['CinemaNameKR']            # 극장명
                sequencenogroupnamekr = match2.value['SequenceNoGroupNameKR']  # 상영관그룹명
                screenid              = match2.value['ScreenID']                 # 상영관 코드
                screennamekr          = match2.value['ScreenNameKR']             # 상영관명
                moviecode             = match2.value['MovieCode']                # 영화코드 [영화명 + 필름종류 + 더빙/자막]
                bookingseatcount      = match2.value['BookingSeatCount']        # 예약좌석수
                totalseatcount        = match2.value['TotalSeatCount']          # 총좌석수
                playdt                = match2.value['PlayDt']                   # 상영일자
                playdt                = playdt[0:4] + playdt[5:7] + playdt[8:10]  # 상영일자(조정)
                starttime             = match2.value['StartTime']               # 상영시간(시작)
                endtime               = match2.value['EndTime']                 # 상영시간(끝)
                # print(dicMovies[moviecode][1]+':'+dicMovies[moviecode][0])

                if  screenid_old != screenid:

                    if screenid_old is not None:
                        dicScreen[screenid_old].append(dicTime)
                    #

                    screenNo += 1
                    degreeNo = 0
                    dicTime = {}
                    screenid_old = screenid
                #

                degreeNo += 1
                dicTime[(screenNo*100) + degreeNo] = [starttime, endtime, bookingseatcount, moviecode, dicMovies[moviecode][1], dicMovies[moviecode][2]]
                #dicTime[degreeNo] = [starttime, endtime, bookingseatcount, moviecode, dicMovies[moviecode][0], dicMovies[moviecode][1], dicMovies[moviecode][2]]

                if isPrnConsole:  #################
                    ticket_count += 1
                    print( '{} : {},{},{},{},{},{},{},{},{},{},{}~{},{},{}'.format( today, (screenNo*100) + degreeNo, dicCinema, cinemanamekr, sequencenogroupnamekr, screennamekr, moviecode, dicMovies[moviecode][0], dicMovies[moviecode][1], dicMovies[moviecode][2], playdt, starttime, endtime, bookingseatcount, totalseatcount ) )

            if screenid_old is not None:
                dicScreen[screenid].append( dicTime )

            dicTeather[dicCinema] = [dicScreen]
        #

        dicTicketingData[today[0:4] + today[5:7] + today[8:10]] = [dicTeather]
    #

#
# 영화관 (http://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx) 에서 극장데이터를 가지고 온다. (dicTicketingData)
#


#########################################################################################################################################
# LOTTE 클로링 정보 올리기..
#
def func_lotte_upload():

    print( '### 서버 전송 시작 ###' )

    fields = { "moviedata": str( dicMovieData )
             , "cinemas": str( dicCinemas )
             , "ticketingdata": str( dicTicketingData )
             }
    url = 'http://www.mtns7.co.kr/totalscore/upload_lotte.php'

    r = http.request( 'POST', url, fields )

    data = r.data.decode( 'utf-8' )

    print( '[', data, ']' )

    print( '### 서버 전송 종료 ###' )
#
# LOTTE 클로링 정보 올리기..
#



#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################

if  __name__ == '__main__':

    crawl_lotte_boxoffice(False) # 영화 / 박스 오피스(http://www.lottecinema.co.kr/LCHS/Contents/Movie/Movie-List.aspx) 에서 영화데이터를 가지고 온다. (dicMovieData)

    crawl_lotte_cinema(False) # 영화관 (http://www.lottecinema.co.kr/LCHS/Contents/Cinema) 에서 극장데이터를 가지고 온다. (dicCinemas)

    crawl_lotte_ticketingdata(True) # 영화관 (http://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx) 에서 극장데이터를 가지고 온다. (dicTicketingData1)

    func_lotte_upload()







#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
