from configparser import ConfigParser
import os
cp = ConfigParser()
current_path = os.path.dirname(__file__)
print(current_path)
cp.read(current_path+'/db_config/db.cfg')
d=cp.get('mysql_k8s_test',"host")
print(d)

# section = cp.sections()
# print('得到所有的section，以列表的形式返回 -->',section)
# print('得到该section的所有option-->',cp.options('mysql_k8s_test'))
# print('得到该section中的所有键值对-->',cp.items('mysql_k8s_test'))
# print('得到该section中option的值-->',cp.get('mysql_k8s_test',"host"))

