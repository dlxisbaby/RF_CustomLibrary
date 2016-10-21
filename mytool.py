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
                                                dict2[i] = dict_key_value[i][j][0]
                                        else:
                                                dict2[i] = str(dict_key_value[i][j][0])
                                else:
                                        if type(dict_key_value[i][j]) == type(int()) or type(dict_key_value[i][j]) == type(float()):
                                                dict2[i] = str(dict_key_value[i][j])
                                        else:
                                                dict2[i] = dict_key_value[i][j]
                        expect_list.append(dict2)
                return expect_list
