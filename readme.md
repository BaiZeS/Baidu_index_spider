安装依赖包：
cd main.py 目录
pip install -r requirements.txt

参数配置：
main.py中配置预定义参数，如果参数过期，需要更新Cipher_Text和cookies
mysql_server.py中connect_mysql()函数，定义本地数据库
mysql_server.py中get_keywords()函数，更新数据库对应的表名称

运行说明：
定义为每天8点运行，每隔1小时查询一次
运行main.py,将从数据库中读取关键字查询百度指数，然后写回数据库中