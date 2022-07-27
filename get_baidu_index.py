import requests
import json


def get_social_describe(headers, keywords):
    '''获取用户画像（性别分布和年龄分布）'''
    # 构建请求地址
    url = 'https://index.baidu.com/api/SocialApi/baseAttributes?wordlist[]=' + keywords

    # 获取请求数据
    html = requests.get(url, headers=headers)
    social_data = json.loads(html.text)

    # 判断抓取状态
    status = social_data['status']
    if status == 0:
        # 根据关键词获取用户性别画像
        sex_data = {}
        for one in social_data['data']['result'][0]['gender']:
            sex_data[one['desc']] = round(one['rate'], 2)
        # 根据关键词获取用户年龄画像
        age_data = {}
        for one in social_data['data']['result'][0]['age']:
            age_data[one['desc']] = round(one['rate'], 2)
    else:
        # 抓取失败置空
        sex_data = {'男':'-1', '女':'-1'}
        age_data = {'0-19': '-1', '20-29': '-1', '30-39': '-1', '40-49': '-1', '50+': '-1'}

    return sex_data, age_data


def get_search_index(headers, keywords, days):
    '''获取搜索指数均值'''
    # 构建请求地址
    url = 'https://index.baidu.com/api/SearchApi/index?area=0&word=[[{"name":"%s","wordType":1}]]&days=%s' % (keywords, days)

    # 获取请求数据
    html = requests.get(url, headers=headers)
    search_data = json.loads(html.text)

    # 判断抓取状态
    status = search_data['status']
    if status == 0:
        # 根据关键词获取搜索指数均值
        search_index = search_data['data']['generalRatio'][0]['all']['avg']
    else:
        # 抓取失败置空
        search_index = '-1'
    return search_index


def get_feed_index(headers, keywords, days):
    '''获取资讯指数均值'''
    # 构建请求地址
    url = 'https://index.baidu.com/api/FeedSearchApi/getFeedIndex?word=[[{"name":"%s","wordType":1}]]&area=0&days=%s' % (keywords, days)

    # 获取请求数据
    html = requests.get(url, headers=headers)
    feed_data = json.loads(html.text)

    # 判断抓取状态
    status = feed_data['status']
    if status == 0:
        # 根据关键词获取咨询指数均值
        feed_index = feed_data['data']['index'][0]['generalRatio']['avg']
    else:
        # 抓取失败置空
        feed_index = '-1'
    return feed_index