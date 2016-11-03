#coding:utf-8

class mytool():
	def __init__(self):
                pass

        def dlx_repeated_key_to_post_data(self,num,key_name,from_list):
                '''
                将列表转化为post类型的数据
                '''
                string_list = str(from_list)
                string = ''
                if ",)" in string_list:
                        for i in from_list[:int(num)]:
                                string = string + "{0}={1}&".format(key_name,i[0])
                else:
                        for i in from_list[:int(num)]:
                                string = string + "{0}={1}&".format(key_name,i)
                return string[:-1]
        
        def dlx_add_dict_to_list(self,num,**dict_key_value):
                '''
                将从数据库中查询出的字典列表转换为可对比的字典列表
                如：
                dict1 = {'a':[1,3,5,7,9],'b':[2,4,6,8,10]}
                如果num=3，则转化为:
                [{'a':1,'b':2},{'a':3,'b':4},{'a':5,'b':6}]
                '''
                num_list = range(0,int(num))
                expect_list = []

                for j in num_list:
                        dict2 = {}
                        for i in dict_key_value:
                                if ',)' in str(dict_key_value[i]):
                                        if type(dict_key_value[i][j][0]) == type(unicode()):
                                                dict2[i.encode("utf8")] = dict_key_value[i][j][0].encode("utf8")
                                        else:
                                                dict2[i.encode("utf8")] = str(dict_key_value[i][j][0]).encode("utf8")
                                else:
                                        if type(dict_key_value[i][j]) == type(int()) or type(dict_key_value[i][j]) == type(float()):
                                                dict2[i.encode("utf8")] = str(dict_key_value[i][j]).encode("utf8")
                                        else:
                                                dict2[i.encode("utf8")] = dict_key_value[i][j].encode("utf8")
                        expect_list.append(dict2)
                return expect_list

        def dlx_select_db_json_to_tuple(self,DB_list):
                '''
                将从数据库中查询出来列表（json）转化为元组，作为IN关键字后的条件
                如：
                [(u'["S20160927766190","S20160927159910"]',), (u'["S20160927766190","S20160927825520","S20160927936647","S20160927159910","P20160927764039"]',), (u'["P20161018158611"]',)]
                转化为：
                (u'S20160927766190', u'S20160927159910', u'S20160927766190', u'S20160927825520', u'S20160927936647', u'S20160927159910', u'P20160927764039', u'P20161018158611')
                '''
                final_list = []
                for i in DB_list:
                        string  = i[0][2:-2]
                        list1 = string.split('","')
                        for j in list1:
                                final_list.append(j.encode("utf8"))
                return tuple(final_list)

        def dlx_get_length_equal_n_list(self,num,list_value):
                '''
                num为3，list_value为group
                则生成一个列表为[group,group,group]
                '''
                list1 = []
                num_list = range(0,int(num))
                for i in num_list:
                        list1.append(list_value)
                return list1

        def dlx_list_subtract_list(self,list1,list2):
                '''
                列表1减去列表2，返回新的列表
                '''
                for i in list2:
                        list1.remove(i)
                return list1

        def dlx_db_list_to_standard_list(self,db_list):
                '''
                将查询数据库的列表，如：

                [(1,), (3,), (15,), (16,), (17,), (18,), (19,), (20,)]

                转化为标准列表

                [1, 3, 15, 16, 17, 18, 19, 20]
                '''
                list1 = []
                for i in db_list:
                        if type(i[0]) == type(int()):
                                list1.append(i[0])
                        else:
                                list1.append(i[0].encode("utf8"))
                return list1
