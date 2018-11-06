from bs4 import BeautifulSoup
from urllib.parse import urlencode
import sys
from urllib.request import Request, urlopen
from datetime import datetime, timedelta
import math
import json
import os
import xmltodict
import pandas as pd
import re
import pymysql
from sqlalchemy import create_engine

RESULT_DIRECTORY = '../__result__/crawling'

#동물관리보호소  공공데이터 API 서비스키

# SURVICE_KEY = 'lPho2AedT94HdWcuLEqLx%2FxutLFprTW4diIv6lp%2FylcbEtT0TFuMSfWdSiWip2LcqZ3fRfZ4tTKNyZiU%2BKUfAw%3D%3D'
SURVICE_KEY = 'kjzgwf40zX1dWlcX1PKEw2r%2BUfP1YbASnaMYa5dQ6aOr9mFJOi%2FcDQB%2FRlvaWdCVVQ5uSS%2BWwXU1WJYDAFmmBA%3D%3D'    # 김민규
# SURVICE_KEY = 'EdieVeGWBCgcq7f02Z4gpx%2FEssqE8l151SGr%2FHYps1SvWYKgXvpn35kSxTQUhMkxyf9yOrp2SU%2Fr9xZjf7aWQA%3D%3D'    # 송수진
# SURVICE_KEY = 'FXCllNPKHcV69y%2FBSMoNxmHKoCNvPRagdDMlScSRSsNJLbGqp12VchucwYzzGf1jWKNrbyi%2BBDF0zJSL%2Bi4K3Q%3D%3D'  # 김신애
base_url='http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/abandonmentPublic'


def animal_url(base=base_url, **params):
    url = '%s?%s&ServiceKey=%s' % (base, urlencode(params), SURVICE_KEY)
    return url

def animal_crawling():
        year = datetime.now().strftime('%Y')
        year = int(year)
        date = datetime.now().date()
        date = date - timedelta(days=1)
        date = str(date).split('-')

        # for year in range(2018):  # 년도가 바뀔 때마다, pageNo, isnext 초기화

        bgnde = '%s%s%s' % (date[0], date[1], date[2])  # 주소값 시작일
        endde = '%s%s%s' % (date[0], date[1], date[2])  # 끝일
        pageNo = 1
        isnext = True
        datalist = []
        columns = []
        encoding = 'utf-8'
        numOfRows = '1'

        while isnext:
            url = animal_url(bgnde=bgnde, endde=endde, pageNo=pageNo, numOfRows=numOfRows)
            res = urlopen(url=url)

            if res is None:
                break

            xml_result = res.read().decode(encoding)
            xml_data = xmltodict.parse(xml_result)
            xml_dict = json.dumps(xml_data)
            dict_result = json.loads(xml_dict)
            xml_body = dict_result.get('response').get('body')
            print(xml_body)
            xml_nor = None if dict_result is None else xml_body.get('numOfRows')
            xml_tc = None if dict_result is None else xml_body.get('totalCount')
            lostData = xml_body.get('items').get('item')

            datalist.append(lostData)


            cnt = math.ceil(int(xml_tc)/int(xml_nor))   # 크롤링 횟수 확인

            if pageNo == cnt:
                isnext = False
            else:
                pageNo += 1

        df_crawling = pd.DataFrame(datalist)  # Dict -> DataFrame
        df_crawling.to_csv('{0}/{1}_realtime_data.csv'.format(RESULT_DIRECTORY, bgnde), encoding='euc-kr', mode='w', index=True)

def db_save():
    year = datetime.now().strftime('%Y')
    year = int(year)
    date = datetime.now().date()
    date = date - timedelta(days=1)
    date = str(date).split('-')
    bgnde = '%s%s%s' % (date[0], date[1], date[2])  # 주소값 시작일

    df = pd.read_csv('{0}/{1}_realtime_data.csv'.format(RESULT_DIRECTORY, bgnde),encoding="euc-kr")
    df = df.drop("Unnamed: 0", 1)
    df = df.fillna("NaN")

    # df = pd.read_csv('{0}/{1}_realtime_data.csv'.format(RESULT_DIRECTORY, bgnde),encoding="euc-kr")
    #         df = df.drop("Unnamed: 0", 1)
    #         print(df)

    # ------------------------------------------- 컬럼을 리스트로 변환
    a = [df.loc[i, j] for i in df.index for j in df[['weight']]]
    b = [df.loc[i, j] for i in df.index for j in df[['age']]]

    temp_weight = []
    temp_age = []

    # ------------------------------------ weight 에러단어만 검출
    for i in a:
        pattern = re.compile(r'\d[.]\d\(Kg\)+|\d\(Kg\)+|\d\d\(Kg\)+|\d?\d[.]\d?\d?\(Kg\)')  # 형식에 맞는 패턴 인식
        no_error_weight_word = pattern.findall(i)  # 패턴값과 맞는 값을 반환
        temp_weight += no_error_weight_word  # 임시리스트에 추가
    error_word_weight = list(set(a) - set(temp_weight))  # 차집합
    print("에러다 시버펄\n")
    print(temp_weight)
    print(no_error_weight_word,'\n')

    print("임시 weight 리스트 반환\n")
    print(temp_weight,'\n')

    print("임시 에러weight 초기화\n")
    del temp_weight[:]
    print(temp_weight)

    print(error_word_weight)

    # ------------------------------------ age 에러단어만 검출
    for j in b:
        pattern2 = re.compile(r'20+[0-1]+[0-9]\(년생\)')  # 형식에 맞는 패턴 인식
        no_error_age_word = pattern2.findall(j)  # 패턴값과 맞는 값을 반환
        temp_age += no_error_age_word  # 임시리스트에 추가
    error_word_age = list(set(b) - set(temp_age))  # 차집합
    print(no_error_age_word, "패턴값 반환")
    print(temp_age, "임시 age 리스트 반환")
    del temp_age[:]
    print(temp_age, "임시 에러age 초기화")
    print(error_word_age)
    conn = pymysql.connect(host='localhost', user='root', password='mkyu0917', db='animaldb', charset='utf8mb4', )
    curs = conn.cursor()
    # -----------------------테이블이 없을시에 테이블 생성

    SQL_QUERY = '''
               CREATE TABLE IF NOT EXISTS animaldb.weight_error(
                   id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
                   weight VARCHAR(30) NOT NULL,
                   PRIMARY KEY(id)
                   )DEFAULT CHARSET=utf8mb4 '''
    SQL_QUERY2 = """
        CREATE TABLE IF NOT EXISTS animaldb.age_error(
            id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
            age VARCHAR(30) NOT NULL,
            PRIMARY KEY(id)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 
        """

    curs.execute(SQL_QUERY)
    conn.commit()

    curs.execute(SQL_QUERY2)
    conn.commit()

    # === 에러단어만 각 테이블에 insert ===

    sql1 = """insert into age_error(age) values (%s)"""
    sql2 = """insert into weight_error(weight) values (%s)"""

    # === 에러단어만 들어있는 리스트를 통채로 db에 적재 ===
    curs.executemany(sql1, error_word_age)
    conn.commit()

    curs.executemany(sql2, error_word_weight)
    conn.commit()

    # === 적제된 에러문자의 데이터를 select문으로 불러옴
    sql_a = """ select * from weight_error """
    sql_b = """ select * from age_error"""

    curs.execute(sql_a)
    result_weight_error = curs.fetchall()
    print(result_weight_error, "db_weight 에러단어\n")

    curs.execute(sql_b)
    result_age_error = curs.fetchall()
    print(result_age_error, "db_age 에러단어\n")

    list_temp = []  # weight에러가 있는 로우가 들어갈 리스트
    list_temp2 = []  # weight,age오류가 없는 로우가 들어갈 리스트

    # ------불러온 에러단어리스트 속 튜플에서 속성값 i값의 1번째를 가져옴
    if len(result_weight_error) != 0:
        for i in result_weight_error:
            error = i[1]
            for j in df.itertuples():

                if j.__contains__(error):
                    list_temp.append(j)
                else:
                    list_temp2.append(j)

        list_temp2 = list(set(list_temp2))
    else:
        for j in df.itertuples():
            list_temp2.append(j)

        list_temp2 = list(set(list_temp2))
        print("weight 에러단어가 없습니다.")
        # print(list_temp2,'에러없는 데이터')
        # print(list_temp,'에러있는 데이터')

    if len(result_age_error) != 0:
        for i in result_age_error:
            error = i[1]
            for j in list_temp2:

                if j.__contains__(error):
                    list_temp.append(j)
    else:
        print("age에러단어가 없습니다.")

    engine = create_engine("mysql+pymysql://root:" + "mkyu0917" + "@localhost:3306/animaldb?charset=utf8mb4",
                           encoding='utf8')
    conn = engine.connect()

    if len(set(list_temp)) != 0:
        realdata = list(set(list_temp2) - set(list_temp))
    else:
        realdata = list(set(list_temp2))
        print(realdata)

    if len(set(list_temp)) != 0:
        error_df = pd.DataFrame(list_temp).drop('Index', 1).drop_duplicates()  # index 컬럼제거 row중복값 제거
        print("error_df", error_df)
        error_df.to_sql(name='animal_realtime_2018_error', con=engine, if_exists='append', index=False)
        del error_df
    else:
        print("에러데이터가 없기때문에 저장하지 않습니다.")

    if len(realdata) != 0:
        no_error_df = pd.DataFrame(realdata).drop('Index', 1).drop_duplicates()  # index 컬럼제거 row중복값 제거
        print("에러가 없는 데이터를 저장했습니다.", no_error_df)
        no_error_df.to_sql(name='animal_realtime_2018', con=engine, if_exists='append', index=False)

    conn.close()

    del list_temp[:]
    del list_temp2[:]
    print(list_temp2)


if not os.path.exists(RESULT_DIRECTORY):
    os.makedirs(RESULT_DIRECTORY)

if __name__ == '__main__':
    animal_crawling()
    db_save()