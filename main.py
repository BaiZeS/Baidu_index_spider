import time, os, datetime
from get_baidu_index import get_feed_index, get_social_describe, get_search_index
from random import random, randint
from mysql_server import *


# 预定义默认参数
log_path = os.path.join(os.path.dirname(__file__), 'error_log.log')
Cipher_Text = '1659337210605_1659351285981_N3qnOnIhz1xe8id6yPQYjjZCehK6bVBVcZ0W+hkx8RbQwdd/5XXPuNv9xPAa1l9TNiq+n0rCgXl7Gr7AZtB9OfyPcUmKFrIw5bF9fZTOQsMxRf/9iCJEC1iY8XOV3alz7vO6PecHqBpmwDhMJlVUwKrJil0Kxg0SuIax6hObS62LX+f47hpcPnEv3rnnB2aU2v/uzn+ty3F0D9bvGJ+E741qR2SWVJpEE+6gGHf9XvjznaWCbl+Z7gA24aKe/79vqMm2SKN50J2cLmJzfhc9ZozZ64gNUoTW/OVZVlJ2ig92RvRAJkEBLc5weL9gSwT3B4nVz2NQrIuwcn6YtKZ8io6jbko2RRoTRn7IiyefND2hoBpr+zJ7xtJbYwvEd3lgInQaDovdbXJp9y1yNOHLH1EW9+gW/EokSV1x2a2Mmyc='
cookies = '__yjs_duid=1_0fe663a1123945dfda4fe82aa5e55fe91632706119900; BAIDUID=D9C58B588D6A9AB5743335E01333588A:FG=1; BIDUPSID=D9C58B588D6A9AB5743335E01333588A; PSTM=1634812464; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1635935198; MCITY=-289:; BAIDUID_BFESS=0194F9EC3BAB2BDE0E3BA8F6830274B0:FG=1; ZFY=h3sfUf:ALkhqnY42AfoSwyMqfWFhxvAS4L:AYE65RFFBo:C; BDUSS=01VLTRKRVNLTEtac3NQVk0zfmp3TU4xWXhvLWp3LXZ3a1RWZ35GLVJaTFVQUTlqSVFBQUFBJCQAAAAAAAAAAAEAAAB9DdNQtc~LucLtya3S1Mj2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANSw52LUsOdib; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a04093637011C3qIs3L2LUlNx86sWcVoAZaYtC8JnM05AMJYOeKBGEbKK2t/hHOWW3AuPeMwOo8QxXjSX/JIgpR9neBIOtTvSYtEcK8rx9QikL1NrKVbMZmZWsjXK8vhQlmgTlfgKzApqVDRorqw1UkAxoPd6KwT+wfcdmlcC08NqVod9IlHcTsILnt+0TAB9yk0zINm6H/eqVDRorqw1UkAxoPd6KwT+wfcdmlcC08NqVod9IlHcTs7AISwlcnM2YSfeYTwMGC9N9WFc3NI3S6Frl6M4OkQLMs+SQSXDLqjUAW0sxFYS8dyXrqo4RTmOz0Zt3WJ4ZBPAUB0AX1V4BwddYCaScbraCUtyMyamGXQWxwlY/dffKU=32438252368981359275114084110211; __cas__rn__=409363701; __cas__st__212=467e7f74bfeb54795c599626434883b79b77d732359fc22b264d7913546801e1ebf06e3195722c1cbaa59762; __cas__id__212=41049790; CPID_212=41049790; CPTK_212=2073575016; bdindexid=6th9k0vnctf7oknhffo4cu7um5; ab_sr=1.0.1_MDQwYTIwZjg4N2RhYzYxZTZiNmQ3MjUyMzE2ZGI3N2U0MDAzNjgyYzUwNmZhZjI1OTVjOWIwMDA4OWMxNTYwODZhZjhjNWQ3OWFiMjUxMDIxYmIzZThmMDQ3YTRjMDBiNjQ0YjEwMDNhMTliMjFjYjBjY2YwNGI4NmVkMDA2OGQzOWI0NGJkZWIzZWVlZWMwYTBlZDYwOGYyMDNiYjAwMQ==; RT="z=1&dm=baidu.com&si=5f5e5b4a-1ee7-4d65-b884-a333a9d0036f&ss=l6amvjli&sl=a&tt=dgc&bcn=https://fclog.baidu.com/log/weirwood?type=perf"; BDUSS_BFESS=01VLTRKRVNLTEtac3NQVk0zfmp3TU4xWXhvLWp3LXZ3a1RWZ35GLVJaTFVQUTlqSVFBQUFBJCQAAAAAAAAAAAEAAAB9DdNQtc~LucLtya3S1Mj2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANSw52LUsOdib'


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
        if time_now.hour == 19:
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
                        index_list.extend((search_index, feed_index, sex_rate['男'], sex_rate['女'], age_rate['0-19'], age_rate['20-29'], age_rate['30-39'], age_rate['40-49'], age_rate['50+'], keywords))
                        print('title %s, and the count of title: %s' % (keywords, index_list))

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
