from read_excel import GetData
from get_response import Request_method
from read_database import get_mysql
import unittest,json
import random, string
import time

api_name = 'createPlaylist'
# params这句放函数里会报警告
params = GetData().get_excel(api_name)


class createPlaylist(unittest.TestCase):
    def setUp(self):
        # 生成唯一title
        dt = time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))
        self.title = dt + ''.join(random.sample(string.digits + string.ascii_letters, 5))
        self.repeat_title_df = get_mysql(db = 'playlist',sql = 'select title from playlist_data limit 1')

    def test_01_create_static_playlist(self):
        '''使用title做校验条件，title唯一是否正确添加'''

        params['data']['title'] = self.title
        # print(params)
        d = Request_method(params)
        response = d.send_request()

        self.assertEqual(response['code'],int(params['status_code']),msg='响应状态断言失败')
        self.assertIsNotNone(response['data'],msg = '未正确返回playlist_uuid')

    def test_02_create_repeat_title(self):
        '''重复title时是否正确返回错误码'''

        # self.repeat_title_df 返回的是个pandas的对像，所以需要用下标取相应的值
        params['data']['title'] = self.repeat_title_df['title'][0]
        d = Request_method(params)
        responce = d.send_request()
        # print(responce)
        self.assertEqual(responce['code'], 555, msg='播放列表名称重复时，响应状态断言失败')


    def test_03_create_auto_playlist(self):
        '''创建自动播放列表'''
        params['data']['show_attribute_groups'][0]['attributes'] = ['2D']
        params['data']['show_attribute_groups'][0]['name'] = 'test1'
        # 添加一组属性
        # params['data']['show_attribute_groups'].append({'attributes': ['3D'], 'name': 'test2'})
        params['data']['automatically_apply'] = True
        params['data']['title'] = self.title
        # print(params['data'])

        d= Request_method(params)
        response = d.send_request()
        playlist_uuid = response['data']

        # 是否自动添加匹配正片的占位符
        exec_sql="select count(*) as 'count' from playlist_version_content_association d where d.playlist_uuid='{}' and d.title = 'Automatic Feature Selector'".format(playlist_uuid)
        db = get_mysql('playlist',exec_sql)
        segment_count = db['count'][0]

        self.assertEqual(response['code'], 200, msg='自动播放列表创建失败')
        self.assertEqual(segment_count, 1, msg='自动播放列表未自动添加匹配正片的Segment')  # 有且只能有一条

    def test_04_repeat_attribute(self):
        '''同个属性组只能存在一个播放列表中'''
        # 与03同组属性
        params['data']['show_attribute_groups'][0]['attributes'] = ['3D','2D']
        params['data']['show_attribute_groups'][0]['name'] = 'test'
        params['data']['automatically_apply'] = True
        params['data']['title'] = self.title
        # print(params['data'])

        d = Request_method(params)
        repeat_response = d.send_request()

        # print(response)
        self.assertEqual(repeat_response['code'], 554, msg='同个属性组正常只能存在一个播放列表中')

    def testDown(self):
        pass
if __name__ == '__main__':
    unittest.main()