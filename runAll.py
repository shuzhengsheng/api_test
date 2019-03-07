import os
import unittest
from common.Log import MyLog as Log
import readConfig as readConfig
import HTMLTestRunner
# from common.configEmail import MyEmail
from configEmail import MyEmail

localReadConfig = readConfig.ReadConfig()


class AllTest:
    def __init__(self):
        global log, logger, resultPath, on_off
        log = Log.get_log()
        logger = log.get_logger()
        resultPath = log.get_report_path()
        on_off = localReadConfig.get_email("on_off")
        # 配置执行哪些测试文件的配置文件路径
        self.caseListFile = os.path.join(readConfig.proDir, "caselist.txt")
        # 真正的测试断言文件路径
        self.caseFile = os.path.join(readConfig.proDir, "testCase")
        print(self.caseFile)
        # self.caseFile = None
        self.caseList = []
        self.email = MyEmail.get_email()

    def set_case_list(self):
        """
        读取caselist.txt文件中的用例名称，并添加到caselist元素组
        :return:
        """
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            # 如果data非空且不以#开头
            if data != '' and not data.startswith("#"):
                # 读取每行数据会将换行转换为\n,去掉每行数据中的\n
                self.caseList.append(data.replace("\n", ""))
                #print(self.caseList)
        fb.close()

    def set_case_suite(self):
        """
        set case suite
        :return:
        """
        # 通过set_case_list()拿到caselist元素组
        self.set_case_list()
        test_suite = unittest.TestSuite()
        suite_module = []

        # 从casel元素组中循环取出case
        for case in self.caseList:
            # 通过spilt函数来将aaa/bbb分割字符串，-1取后面，0取前面
            case_name = case.split("/")[-1]
            # 打印取出来的名称
            #print(case_name+".py")
            # 批量加载用例，第一个参数为用例存放路径，第一个参数为路径文件名
            discover = unittest.defaultTestLoader.discover(self.caseFile+'\\user', pattern=case_name + '.py', top_level_dir=None)
            # 将discover存入suite_module元素组
            suite_module.append(discover)

        # 判断suite_module元素组是否存在元素
        if len(suite_module) > 0:
            # 如果存在，循环取出元素组内容，命名为suite
            for suite in suite_module:
                # 从discover中取出test_name，使用addTest添加到测试集
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None
        # 返回测试集
        return test_suite


    def run(self):
        """
        run test
        :return:
        """
        try:
            # 调用set_case_suite获取test_suite
            suit = self.set_case_suite()
            # 判断test_suite是否为空
            if suit is not None:
                logger.info("********TEST START********")
                # 打开result/xxxxxxxxxx/report.html测试报告文件，如果不存在
                fp = open(resultPath, 'wb')
                # 调用HTMLTestRunner
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Test Report', description='Test Description')

                runner.run(suit)
            else:
                logger.info("Have no case to test.")
        except Exception as ex:
            logger.error(str(ex))
        finally:
            logger.info("*********TEST END*********")
            fp.close()
            # 判断邮件发送的开关
            if on_off == 'on':
                self.email.send_email()
            elif on_off == 'off':
                logger.info("邮件发送开关配置关闭，请打开开关后可正常自动发送测试报告.")
            else:
                logger.info("Unknow state.")


if __name__ == '__main__':
    obj = AllTest()

    obj.run()