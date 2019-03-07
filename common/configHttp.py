import requests
import readConfig as readConfig
from Log import MyLog as Log
import json

localReadConfig = readConfig.ReadConfig()


class ConfigHttp:

    def __init__(self):
        global scheme, host, port, timeout
        scheme = localReadConfig.get_http("scheme")
        host = localReadConfig.get_http("baseurl")
        port = localReadConfig.get_http("port")
        timeout = localReadConfig.get_http("timeout")
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.headers = {}
        self.params = {}
        self.data = None
        self.url = None
        self.files = {}
        self.state = 0

    def set_url(self, url):
        """
        set url
        :param: interface url
        :return:
        """
        self.url = scheme+'://'+host + ":" + port + url

    def set_headers(self, header):
        """
        set headers
        :param header:
        :return:
        """
        self.headers = header

    def set_params(self, param):
        """
        set params
        :param param:
        :return:
        """
        self.params = param

    def set_data(self, data):
        """
        set data
        :param data:
        :return:
        """
        self.data = data

    def set_files(self, filename):
        """
        set upload files
        :param filename:
        :return:
        """
        if filename != '':
            file_path = 'E:/python3.6/api_test04/testFile/img' + filename
            self.files = {'file': open(file_path, 'rb')}

        if filename == '' or filename is None:
            self.state = 1

    # 定义get请求
    def get(self):
        """
        defined get method
        :return:
        """
        try:
            response = requests.get(self.url, headers=self.headers, params=self.params, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # 定义post请求
    # include get params and post data
    # uninclude upload file
    def post(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, params=self.params, data=self.data, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include upload file
    def postWithFile(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # for json
    def postWithJson(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, json=self.data, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None


    def putWithJson(self):
        """
        defined put method
        :return:
        """
        try:
            response = requests.put(self.url, headers=self.headers, json=self.data, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    def putWithArray(self):
        """
        defined put method
        :return:
        """
        try:
            response = requests.request(url=self.url, headers=self.headers, json=self.data, method='PUT',timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None
        except Exception as e:
            self.logger.error(e)
            return None


    def deleteWithJson(self):
        """
        defined delete method
        :return:
        """
        try:
            response = requests.delete(self.url, headers=self.headers, json=self.data, method='DELETE',timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    def deleteWithArray(self):
        """
        defined delete method
        :return:
        """
        try:
            response = requests.delete(self.url, headers=self.headers, json=self.data, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None



    def postJson(self):
        """
        json格式post请求
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(self.data), timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return



if __name__ == "__main__":
    print("ConfigHTTP")
#
# # coding:utf-8   #强制使用utf-8编码格式
# import json
# import readConfig
# import requests
#
# #TODO 请求内是否需要传headers （zrh 2019年2月27日15:01:09）
#
# # 定义常用4种方法
# class RunMain():
#
#     # 定义一个方法，传入需要的的url和data
#     def send_post(self, url, data, headers):
#         # 参数必须按照url、data的顺序传入
#         result = requests.post(url=url,data=data, headers=headers).json()
#         res = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=4)
#         return res
#
#     def send_get(self, url, data):
#         result = requests.get(url=url, params=data).json()
#         res = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=4)
#         return res
#
#     def send_put(self, url, data, headers):
#         result = requests.put(url=url, data=data, headers=headers).json()
#         res = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=4)
#         return res
#
#     def send_delete(self, url,data, headers):
#         result = requests.delete(url=url, data=data, headers=headers).json()
#         res = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=4)
#         return res
#
#     # 定义一个run_main函数，通过传来的method进行不同的请求
#     def run_main(self, method, url=None, data=None):
#         result = None
#         headers = {'content-type': "application/json;charset=UTF-8"}
#         if method == 'post':
#             result = self.send_post(url, data, headers)
#         elif method == 'get':
#             result = self.send_get(url, data)
#         elif method == 'put':
#             result = self.send_put(url, data, headers)
#         elif method == 'delete':
#             result = self.send_delete(url, data, headers)
#         else:
#             print("method错误")
#         return result
#
# if __name__ == '__main__':
#     # 此处写死参数，验证请求是否正确
#     result = RunMain().run_main('post', 'http://10.20.10.3:8010/devUnit/save', '{"dwlx": 1,"dwmc": "测试001CS"}'.encode('utf-8'))
#     print(result)
#     #print("configHttp")
