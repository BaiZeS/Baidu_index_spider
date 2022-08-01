import time, os, datetime
from get_baidu_index import get_feed_index, get_social_describe, get_search_index
from random import random, randint
from mysql_server import *


# 预定义默认参数
log_path = os.path.join(os.path.dirname(__file__), 'error_log.log')
Cipher_Text = '1658214009400_1658223740218_OLfvqUFw/ZzscbkL/KDpmvjFgFkFdgCro5si+uhDOxjs5+WSszjIhs+9NwFc4heAodSCUdemQ5QAtx+cb0f8MNJHAUH42D31enVRDo4MWI4CGjBfHgyxzsnSY42rHl5noFc61HQZf1/Clj6dkxLsuchviWZxbogVWoXHXIM6z4K++o30VdXw0CfjuP9IDKYlAdoh/rqX2F/5FM3wBz6RNG3EHu4CZU436lII0pOsqDebcy/nEREQ3+g58I7Mbe0Nr5nEx8XubP43OHPHWhrvbWMjKwySJJLyo4d75Jtm/Kw4o2hioTf3H7Sd5t0UvAm+FhbanxL6BD/K9rBHZRJKCWYnGrKmbFx3DALeVy/Al7o03ok0/eyux6jO1EWb98RQL+DU3j10CxtWLM9Habun4+/fEM8lpD8Vel+D9xS+LK1EODpeRMKH6gecAGYPwVXKTSq39ujQW9kOP/8MXKYz8fXJaLoasNLrutih3lE9e5d8BiIvvZz1chrzr5sB92DG'
cookies = '__yjs_duid=1_0fe663a1123945dfda4fe82aa5e55fe91632706119900; BAIDUID=D9C58B588D6A9AB5743335E01333588A:FG=1; BIDUPSID=D9C58B588D6A9AB5743335E01333588A; PSTM=1634812464; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1635935198; MCITY=-289:; BAIDUID_BFESS=0194F9EC3BAB2BDE0E3BA8F6830274B0:FG=1; ZFY=h3sfUf:ALkhqnY42AfoSwyMqfWFhxvAS4L:AYE65RFFBo:C; BDUSS=FPTTV4ZXVMVVMySkpDYUIzV3hsUnJZNFBwVnB4dWp4REhFRG1yQ0VVelVsdnhpSVFBQUFBJCQAAAAAAAAAAAEAAAB9DdNQtc~LucLtya3S1Mj2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANQJ1WLUCdViNG; bdindexid=bnfoldk0kar4b370m6tqpmie51; ab_sr=1.0.1_NmI2MDMzZDE2YzY2ZWE4YWZmMDUzNDgyNDMwOGQ0N2U0MTgzMGFmNGVlNDY0YzFhMTgwNTQ3N2RlYjE5OTdlNTUxMjVhMzllZGIzM2E3NTQxZTE3MmE2ZGM0Yzg1ZGM4MTMwYjkwZjc5MTA3MzljZDY3ZWFlOWQzYjU0ZGE2OGUxNTU3Y2VjMDBiOWU4NmY1MWYwZWQ0YzQ0NDQyYTgxMg==; RT="z=1&dm=baidu.com&si=20fdbae5-c2ea-4c69-b747-58dbd99b7d03&ss=l5rzkhhc&sl=5&tt=9zm&bcn=https://fclog.baidu.com/log/weirwood?type=perf"; BDUSS_BFESS=FPTTV4ZXVMVVMySkpDYUIzV3hsUnJZNFBwVnB4dWp4REhFRG1yQ0VVelVsdnhpSVFBQUFBJCQAAAAAAAAAAAEAAAB9DdNQtc~LucLtya3S1Mj2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANQJ1WLUCdViNG'


def define_header(cookies, Ciper_Text):
    '''定义请求头'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Cipher-Text': Cipher_Text,
        'Cookie': cookies,
        'Host': 'index.baidu.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    return headers

if __name__ == "__main__":
    # 获取请求头
    headers = define_header(cookies, Cipher_Text)
    # 默认查询最近三十天数据
    days = 30
    # 初始化查询次数
    count = 0
    # 定义写入的表名称
    tables_name = ['film_all', 'teleplay_all', 'variety_all']
    # 定义写入字段名
    title_col = ['影名', '剧名', '综艺名']

    while True:
        # 获取当前小时
        time_now = datetime.datetime.now()
        # 定时每天8点运行
        if time_now.hour == 17:
            # 从数据库中获取搜索关键字
            data_list = get_keywords()
            # 标记写入数据库位置
            count = count % 3

            # 抓取对应关键词的百度指数
            for keywords_list in data_list:
                # 分别存入对应数据表单
                for keywords in keywords_list:
                    # 定义百度指数数据列表
                    index_list = []
                    try:
                        sex_rate, age_rate = get_social_describe(headers, keywords)
                        feed_index = get_feed_index(headers, keywords, days)
                        search_index = get_search_index(headers, keywords, days)

                        # 拼接更新数据表
                        index_list.append(search_index, feed_index, sex_rate['男'], sex_rate['女'], age_rate['0-19'], age_rate['20-29'], age_rate['30-39'], age_rate['40-49'], age_rate['50+'], keywords)
                        print('title %s, and the count of title: %s' % (keywords, len(index_list)))

                    except Exception as e:
                        # 记录错误日志
                        error_log = open(log_path, 'a+', encoding='utf-8')
                        error_log.write('spider error of %s at %s because %s\n' % (keywords, str(time_now), repr(e)))
                        
                    finally:
                        # 将百度指数写入数据库
                        insert_result(index_list, tables_name[count], title_col[count])
                        # 每次爬取间隔随机时间(10~15s)
                        sleep_time = round(randint(10, 15)+random(), 3)
                        print('sleep time is %s' % sleep_time)
                        time.sleep(sleep_time)
                
                # 计数器自加
                count = count + 1
        else:
            # 每隔1小时查询一次时间
            print('check time now: %s' % str(time_now))
            time.sleep(60*60)
