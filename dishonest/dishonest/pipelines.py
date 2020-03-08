# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .settings import MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DB

"""

实现管道类
步骤：
    1.在open_spider方法中简历数据库链接，获取操作的数据的cursor
    2.在close_spider中，关闭cursor，关闭数据库链接
    3.在process_item中，如果数据存在，保存数据
"""

class DishonestPipeline(object):

    def open_spider(self,spider):
        self.connection=pymysql.connect(host=MYSQL_HOST,port=MYSQL_PORT,
                                        db=MYSQL_DB,user=MYSQL_USER,password=MYSQL_PASSWORD)
        #获取操作的数据的cursor
        self.cursor=self.connection.cursor()
    def process_item(self, item, spider):
        #3.在process_item中，如果数据存在，保存数据
        #3.1先判断数据是否存在，
        # 如果是自然人根据证件号
        #如果是企业/组织：企业名称和区域进行判断
        #如果年龄为0，为企业，否则为自然人
        if item['age']==0:
            #如果是企业，会根据企业名称 和区域进行判断是否重复
            select_count_sql="SELECT COUNT(1) from dishonest WHERE name = '{}' and area = '{}'".format(
                item['name'],item['area'])
        else:
            #如如果证件号码是18位的，那么就倒数第七到倒数第四位（不包含），三个数使用×××代替,信息保护
            card_num=item['card_num']
            if len(card_num)==18:
                card_num=card_num[:-7]+'****'+card_num[-4:]
                item['card_num']=card_num


            #否则为自然人，自然人通过号码card_num判断
            select_count_sql="SELECT COUNT(1) from dishonest WHERE card_num = '{}'".format(item['card_num'])
        #执行查询sql
        self.cursor.execute(select_count_sql)
        #返回的是一个元组
        """
        fetchone() ：
        返回单个的元组，也就是一条记录(row)，如果没有结果 则返回 None
        fetchall() ：
        返回多个元组，即返回多个记录(rows),如果没有结果 则返回 ()
        获取前n行数据
        row_2 = cursor.fetchmany(3)  获取前三行数据，元组包含元组
        """
        count=self.cursor.fetchone()[0]
        #如果count等于0说明数据不存在，需要插入数据
        if count==0:

            keys,values=zip(*dict(item).items())#把item子安转成字典然后使用zip函数把键与值分成两个列表
            #zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，
            # 然后返回由这些元组组成的列表。
            #如果各个迭代器的元素个数不一致，则返回列表长度与最短的对象相同，
            # 利用 * 号操作符，可以将元组解压为列表。
            insert_sql = "INSERT INTO dishonest ({}) VALUES ({})".format(
                ','.join(keys),
                ','.join(['%s'] * len(values))#%s占位
            )
            #执行sql
            self.cursor.execute(insert_sql,values)
            #提交事物
            self.connection.commit()
            spider.logger.info('插入数据')
        else:
            #重复就不需要插入了，可以在日志中说明
            spider.logger.info('数据重复')


        return item

    def close_spider(self,spider):
        #1.mysql数据库先关闭cursor
        self.cursor.close()
        #2.关闭数据库链接
        self.connection.close()
