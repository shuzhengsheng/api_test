import unittest
import paramunittest
import readConfig as ReadConfig
from common.Log import MyLog
from common import common
from common import configHttp
from common import businessCommon
import json

localReadConfig = ReadConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
localunit_save_xls = common.get_xls("userCase.xlsx", "unit_save")


@paramunittest.parametrized(*localunit_save_xls)
class unit_save(unittest.TestCase):

    def setParameters(self, case_name, method, url, data, result, code, msg):
        """

        :param case_name:
        :param method:
        :param url:
        :param data:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.url = str(url)
        self.data = str(data)
        self.result = str(result)
        self.code = str(code)
        self.msg = str(msg)
        self.response = None
        self.info = None

    def description(self):
        """

        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        # # login
        # self.login_token = businessCommon.login()

    def testunit_save(self):
        """
        test body
        :return:
        """
        request_list = common.get_from_sheetname('unit_save')
        for req in request_list:
            # set data
            localConfigHttp.set_data(req['data'])
            # set url
            localConfigHttp.set_url(req['url'])
            # CRUD
            if req['method'] == 'GET':
                self.response = localConfigHttp.get()
            elif req['method'] == 'POST':
                self.response = localConfigHttp.postWithJson()
            elif req['method'] == 'PUT':
                self.response = localConfigHttp.putWithArray() if req['type'] == 'Array' else localConfigHttp.putWithJson()
            elif req['method'] == 'DELETE':
                self.response = localConfigHttp.deleteWithArray() if req['type'] == 'Array' else localConfigHttp.deleteWithJson()
            else:
                print('无此方法')
            # check result
            self.checkResult()


    def tearDown(self):
        """

        :return:
        """
        self.log.build_case_line(self.case_name, self.code, self.msg)

    def checkResult(self):
        """
        check test result
        :return:
        """
        if self.response is None:
            return
        self.info = self.response.json()
        common.show_return_msg(self.response)

        if self.result == '0':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
            self.assertEqual(self.info['info'], 1)
        if self.result == '1':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)


def main():
    print('111')
    pass


if __name__ == '__main__':
    main()
