#coding:utf-8
from decimal import Decimal
import time,sys,hashlib,xmltodict,operator
from xml.dom.minidom import parse
from collections import OrderedDict
import xml.dom.minidom
reload(sys)
sys.setdefaultencoding('utf8')

class mytool():
	def __init__(self):
                pass

        def dlx_check_contain_chinese(self,check_str):
                for ch in check_str.decode('utf-8'):
                        if u'\u4e00' <= ch <= u'\u9fff':
                                return True
                return False

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
                                                if mytool().dlx_check_contain_chinese(dict_key_value[i][j][0]) == True:
                                                        dict2[i.encode("utf8")] = dict_key_value[i][j][0]
                                                else:
                                                        dict2[i.encode("utf8")] = dict_key_value[i][j][0].encode("utf8")
                                        elif type(dict_key_value[i][j][0]) == type(int()) or type(dict_key_value[i][j][0]) == type(float()):
                                                dict2[i.encode("utf8")] = str(dict_key_value[i][j][0]).encode("utf8")
                                        else:
                                                dict2[i.encode("utf8")] = str(dict_key_value[i][j][0]).encode("utf8")
                                else:
                                        if type(dict_key_value[i][j]) == type(unicode()):
                                                if mytool().dlx_check_contain_chinese(dict_key_value[i][j]) == True:
                                                        dict2[i.encode("utf8")] = dict_key_value[i][j]
                                                else:
                                                        dict2[i.encode("utf8")] = dict_key_value[i][j].encode("utf8")
                                        elif type(dict_key_value[i][j]) == type(int()) or type(dict_key_value[i][j]) == type(float()):
                                                dict2[i.encode("utf8")] = str(dict_key_value[i][j]).encode("utf8")
                                        else:
                                                dict2[i.encode("utf8")] = str(dict_key_value[i][j]).encode("utf8")
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

        def dlx_db_list_to_standard_list(self,db_list,mode="1"):
                '''
                将查询数据库的列表，如：
                [(1,), (3,), (15,), (16,), (17,), (18,), (19,), (20,)]
                转化为标准列表
                [1, 3, 15, 16, 17, 18, 19, 20](mode=1时)
                [u'1',u'3',u'15',u'17',u'18',u'19',u'20'](mode=2时)
                
                '''
                list1 = []
                for i in db_list:
                        if mode == "1":
                                if type(i[0]) == type(int()) or type(i[0]) == type(Decimal()):
                                        list1.append(i[0])
                                elif type(i[0]) == type(unicode()):
                                        for ch in i[0]:
                                                #判断是否为中文
                                                if u'\u4e00' <= ch <= u'\u9fff':
                                                        list1.append(i[0])
                                                        break
                                                else:
                                                        list1.append(i[0].encode("utf8"))
                                                        break
                                else:
                                        list1.append(i[0].encode("utf8"))
                        elif mode == "2":
                                list1.append(str(i[0]).decode("utf-8"))
                return list1

        def dlx_get_current_unix_time_string(self):
                '''
                获得当前时间的unix时间戳字符串
                '''
                format1 = '%Y-%m-%d %H:%M:%S'
                time1 = time.localtime()
                value = time.strftime(format1,time1)
                s = time.mktime(time1)
                return str(int(s))

        def dlx_md5_32_lowercase(self,string):
                '''
                对字符串进行32位小写的MD5加密
                '''
                m = hashlib.md5()
                m.update(string)
                encrypted_string = m.hexdigest()
                return encrypted_string

	def dlx_get_xml_resp_code(self,xml_resp,tag_name,unique_name="",unique_value="",res_code=""):
                '''
                解析返回的XML，返回所输入标签的内容\n
                1、后面3个参数都为空时，如:<tag_name>123</tag_name>,则返回123\n
                2、如果后面3个参数同时不为空，则返回res_code的值\
                unique_name为唯一标识标签名，unique_value为唯一标识的值\
                res_code为与unique_name同级的标签的值\n
                3、如果只有后面2个参数为空，则返回tag_name标签的下级，unique_name
                标签值的列表
                '''
                xml_data = xml.dom.minidom.parseString(xml_resp)
                Results = xml_data.getElementsByTagName(tag_name)
                if unique_value == '' and res_code == '' and unique_name == '':
                        for Result in Results:
                                if len(Result.childNodes) != 0:
                                        return Result.childNodes[0].data
                                else:
                                        return ''
                elif unique_value == '' and res_code == '':
                        value_list = []
                        for Result in Results:
                                if Result.getElementsByTagName(unique_name)[0].childNodes[0].data != None:
                                         value_list.append(Result.getElementsByTagName(unique_name)[0].childNodes[0].data)
                                         continue
                                else:
                                        break
                        return value_list
                elif unique_value != '' and res_code != '' and unique_name != '':
                        for Result in Results:
                                unique_id = Result.getElementsByTagName(unique_name)[0].childNodes[0].data
                                if unique_id == unique_value:
                                        return Result.getElementsByTagName(res_code)[0].childNodes[0].data
                                        break

	def dlx_sql_result_to_dict(self,tag_name_list,mode="",OrderedDict_dict={},*tag_value_lists):
		'''
		tag_value_lists = [list1,list2,list3,……]\n
		value_lists的长度应等于tag_list的长度\n
		将value_lists中每个列表的第一个值赋值给tag_list列表，\
		形成字典，以此类推，最后生成值为字典的列表\n
		OrderedDict_list为需要转化为有序字典的字典，格式为：\
		{"level_name_list":["Films","Film"],\
		"level_tag_name_list":["FilmNo","FilmName","FilmType","Language"],\
		"level_tag_value_list":[FilmNo_list,FilmName_list,FilmType_list,Language_list]}
		level_name_list为层级名称列表，tag_name_list为标签内容列表，\
		tag_value_list为每个标签内容列表的集合,列表中的内容必须为同一类型\n
		mode为模式，"outside"模式为有部分内容在固定标签外，"inside"\
		模式为所有内容都在固定标签下
		'''
		list_final = []
		dict_final = {}
		order_list = []
		length = len(tag_name_list)
		if len(OrderedDict_dict) != 0 and mode == "inside":
			length2 = len(OrderedDict_dict["level_tag_name_list"])
			order_dict = OrderedDict()
			order_dict3 = OrderedDict()
			dict4 = {}
			if type(OrderedDict_dict["level_tag_value_list"][0]) == list:
				for k in range(0,len(OrderedDict_dict["level_tag_value_list"][0])):
					i = 0
					while i < length2:
						order_dict[OrderedDict_dict["level_tag_name_list"][i]] = OrderedDict_dict["level_tag_value_list"][i][k]
						i = i + 1
					order_dict2 = order_dict.copy()
					length3 = len(OrderedDict_dict["level_name_list"])
					for j in range(0,length3):
						if j == length3-1:
							dict4[OrderedDict_dict["level_name_list"][0]] = order_dict2
						else:
							order_dict3[OrderedDict_dict["level_name_list"][length3-1-j]] = order_dict2
							order_dict2 = order_dict3.copy()
							order_dict3 = OrderedDict()
							continue
					dict5 = dict4.copy()
					order_list.append(dict5)
					continue
			else:
				i = 0
				while i < length2:
					if type(OrderedDict_dict["level_tag_value_list"][i]) == unicode:
						order_dict[OrderedDict_dict["level_tag_name_list"][i]] = OrderedDict_dict["level_tag_value_list"][i]
					if type(OrderedDict_dict["level_tag_value_list"][i]) == str:
						order_dict[OrderedDict_dict["level_tag_name_list"][i]] = OrderedDict_dict["level_tag_value_list"][i].decode("utf-8")
					if type(OrderedDict_dict["level_tag_value_list"][i]) == int or type(OrderedDict_dict["level_tag_value_list"][i]) == float:
						order_dict[OrderedDict_dict["level_tag_name_list"][i]] = str(OrderedDict_dict["level_tag_value_list"][i]).decode("utf-8")                    
					i = i + 1
				order_dict2 = order_dict.copy()
				length3 = len(OrderedDict_dict["level_name_list"])
				for j in range(0,length3):
					if j == length3-1:
						dict4[OrderedDict_dict["level_name_list"][0]] = order_dict2
					else:
						order_dict3[OrderedDict_dict["level_name_list"][length3-1-j]] = order_dict2
						order_dict2 = order_dict3.copy()
						order_dict3 = OrderedDict()
						continue
				dict5 = dict4.copy()
				order_list.append(dict5)
		elif len(OrderedDict_dict) != 0 and mode == "outside":
			length2 = len(OrderedDict_dict["level_tag_name_list"])
			order_dict = OrderedDict()
			order_dict3 = OrderedDict()
			dict4 = {}
			order_list2 = []
			for k in range(0,len(OrderedDict_dict["level_tag_value_list"][0])):
				i = 0 
				while i < length2:
					order_dict[OrderedDict_dict["level_tag_name_list"][i]] = str(OrderedDict_dict["level_tag_value_list"][i][k]).decode("utf-8")
					i = i + 1
				order_dict2 = order_dict.copy()
				if k != len(OrderedDict_dict["level_tag_value_list"][0])-1:
					order_list2.append(order_dict2)
					continue
				else:
					order_list2.append(order_dict2)
					order_dict2 = OrderedDict()
	
					length3 = len(OrderedDict_dict["level_name_list"])
					for j in range(0,length3):
						if j == length3-1:
							dict4[OrderedDict_dict["level_name_list"][0]] = order_dict2
						else:
							order_dict3[OrderedDict_dict["level_name_list"][length3-1-j]] = order_list2
							order_dict2 = order_dict3.copy()
							order_dict3 = OrderedDict()
							continue
					dict5 = dict4.copy()
					order_list.append(dict5)
		if type(tag_value_lists[0]) == list:
			for k in range(0,len(tag_value_lists[0])):
				i = 0
				while i < length:
					dict_final[tag_name_list[i]] = str(tag_value_lists[i][k]).decode("utf-8")
					i = i+1
				dict2 = dict_final.copy()
				if order_list != []:
					dict2 = dict(dict2.items()+order_list[k].items())
				list_final.append(dict2)
				continue
			for i in list_final:
				i[tag_name_list[0]] = int(i[tag_name_list[0]])
			list_final.sort(key=operator.itemgetter(tag_name_list[0]))
			for i in list_final:
				i[tag_name_list[0]] = str(i[tag_name_list[0]]).decode("utf-8")
			return list_final
		else:
			for k in range(0,len(tag_value_lists)):
				dict_final[tag_name_list[k]] = str(tag_value_lists[k]).decode("utf-8")
			dict2 = dict_final.copy()
			if order_list != []:
				dict2 = dict(dict2.items()+order_list[0].items())
			list_final.append(dict2)
			for i in list_final:
				i[tag_name_list[0]] = int(i[tag_name_list[0]])
			list_final.sort(key=operator.itemgetter(tag_name_list[0]))
			for i in list_final:
				i[tag_name_list[0]] = str(i[tag_name_list[0]]).decode("utf-8")
			return list_final
	

	def dlx_xml_to_dict(self,xml_resp,order_by='',pass_tag=[],*level_tag_names):
		'''
		将XML型的响应结果转化为字典，level_tag_names为
		需要获取的XML的层级,按照order_by的值进行排序,默认可不填。
		pass_tag为需要忽略的tag列表
		'''
		convert_string = xmltodict.parse(xml_resp)
		length = len(level_tag_names)
		final_list = []
		for i in range(0,length):
			convert_string = convert_string[level_tag_names[i]]
			if length == 1:
				convert_string.pop("@xmlns:xsi")
				convert_string.pop("@xmlns:xsd")
		if type(convert_string) == OrderedDict:
			convert_string = [convert_string]
		for i in convert_string:
			final_dict = dict(i)
			if len(pass_tag) != 0:
				for j in pass_tag:
					final_dict.pop(j)
			final_list.append(final_dict)
		if order_by != '':
			for i in final_list:
				i[order_by] = int(i[order_by])
			final_list.sort(key=operator.itemgetter(order_by))
			for i in final_list:
				i[order_by] = str(i[order_by]).decode("utf-8")
		return final_list
