import requests
from api_auto_test.read_excel import GetData
import json

# 通过接口名称返回响应体，用作unittest断言
class Request_method(object):
    def __init__(self,params):
        print('--->',params)
        self.url = params['url']
        self.data = params['data']
        self.host = params['host']
        self.get_param = params['get_url_param']
        self.method = params['method']

    def get(self,header):
        # 传参处理,json格式传参
        globals = {'nan': 0}
        data = eval(str(self.data), globals)

        # 部分请求参数需要加在url上
        if self.get_param:
            test_url = self.url+self.get_param
        else:
            test_url = self.url

        #判断是否超时
        try:
            return requests.get(url=test_url, params=data, headers=header, timeout=60)
        except TimeoutError:
            return print(self.url, '-->请求超时')


    def post(self,header):
        try:
            return requests.post(url = self.url,data = json.dumps(self.data),headers = header,timeout = 60)
        except TimeoutError:
            return print(self.url,'-->请求超时')

    def put(self,header):
        test_url = self.url+self.get_param
        try:
            return requests.put(url = test_url,data = json.dumps(self.data),headers = header,timeout =60)
        except TimeoutError:
            return print(self.url,'-->请求超时')

    def send_request(self):
        login_url = '/api/v1/auth/login'
        responce = requests.post(url=self.host + login_url,
                                 data=json.dumps({'username': 'admin', 'password': 'admin'}),
                                 headers={'Content-Type': 'application/json'}).content
        token = json.loads(responce)['token']
        header = {'X-Thunderstorm-Key': token, 'Content-Type': 'application/json'}

        response = {}
        if self.method == 'post':
            response = json.loads(self.post(header=header).content)
        elif self.method == 'get':
            response = json.loads(self.get(header=header).content)
        elif self.method =='put':
            response = self.put(header=header)
        return response

#
if __name__ == '__main__':
    api_name = 'updatePlaylist'
    params = GetData().get_excel(api_name)
    params['data']['title'] = '20190730-134752cZA6L'
    params['get_url_param'] = '81a68f4d-9b17-4842-9cf6-58e1bd54d8d2'
    d = Request_method(params)
    print(d.send_request())


# createPlaylist
# getPlaylist

