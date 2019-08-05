from read_excel import GetData
from get_response import Request_method
from read_database import get_mysql
import unittest,json


api_name = 'getPlaylist'
# params这句放函数里会报警告
params = GetData().get_excel(api_name)


class getPlaylist(unittest.TestCase):
    def setUp(self):
        self.playlist_uuid_df = get_mysql(db='playlist', sql='select ppl_uuid from playlist_data limit 1')

    def test_01_getPlaylist_sucess(self):
        '''验证正确的playuuid是否正确返回数据'''
        params['get_url_param'] = self.playlist_uuid_df['ppl_uuid'][0]
        d = Request_method(params)
        response = d.send_request()
        self.assertEqual(response['data']['uuid'],params['get_url_param'],msg = '查询uuid与返回不一致')


    def test_02_getPlaylist_notexist(self):
        '''验证错误的playuuid是否正确返回'''
        print(params['get_url_param'])
        params['get_url_param'] = 'error_uuid' #赋值错误的uuid

        # 发送请求
        d = Request_method(params)
        response = d.send_request()

        self.assertIsNone(response['data'],msg = '错误的playlist_uuid，正确返回了数据')

        # print(responce)
if __name__ == '__main__':
    unittest.main()
