from api_auto_test.read_excel import GetData
from api_auto_test.get_response import Request_method
from api_auto_test.read_database import get_mysql
import unittest,json,time,random,string


api_name = 'updatePlaylist'
# params这句放函数里会报警告
params = GetData().get_excel(api_name)

class updatePlaylist(unittest.TestCase):
    '''这个接口只能修改标题'''
    def setUp(self):
        self.playlist_uuid_df = get_mysql(db='playlist', sql='select ppl_uuid,title from playlist_data limit 2')
        dt = time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))
        self.title = dt + ''.join(random.sample(string.digits + string.ascii_letters, 5))
    def test_01_updata_title(self):
        '''修改playlist的名称是否正确'''
        uuid = self.playlist_uuid_df['ppl_uuid'][0]
        # print(uuid,)
        params['get_url_param'] = uuid
        params['data']['title'] =self.title
        d = Request_method(params)
        response = d.send_request()
        # print(response)
        self.assertEqual(response.status_code,200,msg='修改标题不成功')
    def test_02_title_exist(self):
        '''修改title时，是否判断重复标题不可新增'''
        uuid = self.playlist_uuid_df['ppl_uuid'][0]
        repeat_title = self.playlist_uuid_df['title'][1]
        params['get_url_param'] = uuid
        params['data']['title'] = repeat_title
        print(repeat_title)
        d = Request_method(params)
        response = d.send_request()
        # print(response)
        self.assertEqual(response.status_code,500,msg = '修改重复标题未正确判断')



if __name__ == '__main__':
    unittest.main()