import pandas as pd
import json
import os


# 获取EXCEL每列的值
class GetData(object):
    def __init__(self):
        # 直接用相对路径，被其它函数调用时会提示找不到文件
        current_path = os.path.dirname(__file__)
        self.path = current_path+'/test_data.xlsx'

    # 通过接口的名称返回参数信息
    def get_excel(self,api_name):
        da = pd.read_excel(self.path)
        host = 'http://k8s-test-1.aamcn.com.cn'
        # 将接口名称，遍例取出存入list
        # 通过接口名称，查询接口是否存在
        # 存在通过行列索引取出(因为pandas不能按名字去取行标)
        d_list=[]
        for i in range(len(da)):
            d_list.append(da['Name'][i])

        # print(len(d_list),d_list)

        if d_list.count(api_name):
            row_index= d_list.index(api_name)
            name = da.loc[row_index, 'Name']
            method = da.loc[row_index, 'Method']
            url = (host + da.loc[row_index, 'Url']).format(port='32110')
            get_url_param = da.loc[row_index,'url_param']

            # print(type(da.loc[row_index, 'Data']))
            # 读入的是字符串，从swagger中复制过来的是带有格式的，将转成json字符串后再转成字符串，会去掉复制过来的格式
            # 判断data类型，有值为str 为空时，类型是float，只有有值的情况才需处理
            if isinstance(da.loc[row_index, 'Data'],str):
                data = json.loads(da.loc[row_index, 'Data'])  #返回Json格式
                # print(data)
            else:
                data = 0
                # print(type(data))
            status_code = da.loc[row_index, 'status_code']
            check_text = da.loc[row_index, 'check_text']
            return {'name':name,'method':method,'host':host,'url':url,'get_url_param':get_url_param,
                    'data':data,'status_code':status_code,'check_text':check_text}
        else:
            return f'{api_name}接口不存在'


    def write_response(self,response):
        da = pd.read_excel(self.path)
        da['response'] = response
        pd.DataFrame(da).to_excel(self.path, index=False)




if __name__ == '__main__':
    d= GetData()
    print(d.get_excel('createPlaylist')['data'])


# createPlaylist
# getPlaylist

