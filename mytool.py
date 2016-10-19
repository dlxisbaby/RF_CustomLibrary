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
        
