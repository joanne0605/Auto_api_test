from HTMLTestRunner import HTMLTestRunner
import unittest


discover = unittest.defaultTestLoader.discover('./testCase',pattern='test*.py')

if __name__ == '__main__':

    filepath = './test_result/api_testreport.html'
    print (filepath)
    fp = open(filepath,'wb')
    runner = HTMLTestRunner(stream=fp,title='playlist接口测试',description='用例执行情况:')

    runner.run(discover)
    fp.close()