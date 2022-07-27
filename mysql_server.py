import pymysql


def connect_mysql(data_name):
    '''连接数据库'''
    try:
        conn = pymysql.connect(
            host='localhost',  # 连接服务器mysql
            user='root',  # 用户名
            passwd='123456',  # 密码
            port=3306,  # 端口，默认为3306
            db=data_name,  # 数据库名称
            charset='utf8',  # 字符编码
        )
    except:
        print('error in connecting to mysql')
    return conn


def close_mysql(conn):
    '''
    关闭数据库
    '''
    conn.close()    # 关闭数据连接


def query_mysql(conn, sql):
    '''
    定义查询:
    conn:数据库对象; sql:查询语句;
    ->data:查询结果; col_data:字段名;
    '''
    cur = conn.cursor()  # 生成游标对象
    cur.execute(sql)  # 执行SQL语句
    data = cur.fetchall()  # 通过fetchall方法获得数据
    cur.close()  # 关闭游标
    return data


def execute_mysql(conn, sql, param=[]):
    '''
    定义执行:
    conn:数据库对象;sql:查询语句;
    '''
    try:
        cur = conn.cursor()  # 生成游标对象
        if len(param) > 0:
            print('executemang mysql replace~')
            cur.executemany(sql, param)  # 执行插入的sql语句,多条数据
        else:
            print('execute mysql insert~')
            cur.execute(sql)        # 执行单挑查询
        conn.commit()  # 提交到数据库执行
    except:
        conn.rollback()  # 如果发生错误则回滚
    finally:
        cur.close() # 关闭游标


def get_keywords():
    '''获取关键字列表:film_list, tv_list, show_list'''
    # 获取爱奇艺数据
    conn = connect_mysql('aiqiyi_data')
    # 获取电影名称列表
    film_list = [one[0] for one in query_mysql(conn, 'select name from 爱奇艺_电影榜')]
    # 获取电视剧名称列表
    tv_list = [one[0] for one in query_mysql(conn, 'select name from 爱奇艺_剧集榜')]
    # 获取综艺称列表
    show_list = [one[0] for one in query_mysql(conn, 'select name from 爱奇艺_综艺榜')]
    # 关闭数据库连接
    close_mysql(conn)
    
    # 获取芒果tv数据
    conn = connect_mysql('mgtv_data')
    film_list.extend([one[0] for one in query_mysql(conn, 'select name from 芒果tv_电影榜')])
    tv_list.extend([one[0] for one in query_mysql(conn, 'select name from 芒果tv_剧集榜')])
    show_list.extend([one[0] for one in query_mysql(conn, 'select name from 芒果tv_综艺榜')])
    close_mysql(conn)

    # 获取腾讯数据
    conn = connect_mysql('tx_data')
    film_list.extend([one[0] for one in query_mysql(conn, 'select name from 腾讯视频_电影榜')])
    tv_list.extend([one[0] for one in query_mysql(conn, 'select name from 腾讯视频_剧集榜')])
    show_list.extend([one[0] for one in query_mysql(conn, 'select name from 腾讯视频_综艺榜')])
    close_mysql(conn)

    return film_list, tv_list, show_list


def insert_result(res_list, table_name, title_col):
    '''将百度指数写入mysql
    -----------------------------------
    res_list:将写入数据库的数据;
    table_name:存入数据库的表名称;
    title_col:存入数据库的字段名;
    '''
    # 连接数据库
    conn = connect_mysql('mediadata')
    # 查询总表中已存在数据
    title_list = [one[0] for one in query_mysql(conn, 'select name from %s' % table_name)]
    # 判断是否在数据库里
    if title_col not in title_list:
        # 写入数据库
        if table_name == 'teleplay_all':
            execute_mysql(conn, 'replace into %s (%s, 演员, 腾讯视频_总讨论数, 百度_平均搜索指数, 百度_平均资讯指数, 百度_男比例, 百度_女比例, 百度_0到19年龄比例, 百度_20到29年龄比例, 百度_30到39年龄比例, 百度_40到49年龄比例, 百度_50以上年龄比例) values' % (table_name, title_col) + "(%s, 'Null', '-1', "+(("%"+"s,")*9)[0:-1]+")", res_list)
        else:
            execute_mysql(conn, 'replace into %s (%s, 百度_平均搜索指数, 百度_平均资讯指数, 百度_男比例, 百度_女比例, 百度_0到19年龄比例, 百度_20到29年龄比例, 百度_30到39年龄比例, 百度_40到49年龄比例, 百度_50以上年龄比例) values' % (table_name, title_col) + "("+(("%"+"s,")*10)[0:-1]+")", res_list)
    else:
        # 更新数据库（keywords需要放在最后）
        execute_mysql(conn,'update %s set 百度_平均搜索指数=%s, 百度_平均资讯指数=%s, 百度_男比例=%s, 百度_女比例=%s, 百度_0到19年龄比例=%s, 百度_20到29年龄比例=%s, 百度_30到39年龄比例=%s, 百度_40到49年龄比例=%s, 百度_50以上年龄比例=%s where %s=%s' % (table_name, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', title_col, '%s'), res_list)
    # 关闭数据库连接
    close_mysql(conn)