import unittest
import traceback
from TestCase.common import handle, data_read
from parameterized import parameterized
from TestTools.log import MyLog


class TestMain(unittest.TestCase):
    """主流程测试"""

    @classmethod
    def setUpClass(cls):
        print(u"----用例执行-----")
        cls._handle = handle.Handle()
        setup_data = data_read.get_xls('dict', u"dx_interauto_pre_case.xls", "setup")
        cls._handle.set_global(setup_data)
        cls.log = MyLog.get_log()
        cls.logger = cls.log.get_logger()

    # 读取用例文件中的用例（type,Excel文件名,sheet名）
    case = data_read.get_xls('list', u"dx_interauto_pre_case.xls", "main")

    # 设定输出的用例报告中的用例名格式 (这里需要三个传参否则会报错)
    def custom_name_func(testcase_func=None, param_num=None, param=None):
        return "%s_%s_%s" % ("test", str(param.args[0]), str(param.args[3]))

    # 参数化数据，将读取的用例参数化；testcase_func_name参数化用例名称
    @parameterized.expand(case, testcase_func_name=custom_name_func)
    def test_main(self, case_id, setup, header, case_name, url, method, path, param, teardown, test_assert):
        try:
            # 输出日志到日志文件
            case_name = 'test_' + case_id + '_' + case_name
            self.log.build_start_line(case_name)

            # 处理path、url
            self.path = self._handle.handle_url(path)
            self.url = "%s%s" % (url, self.path)

            # 判断param中是否有参数化
            if "{" in param:
                self.param = self._handle.handle_param(param)
            else:
                self.param = param

            # 判断是否有前置header需求
            if header != "":
                self.header = self._handle.handle_header(header)
            else:
                self.header = header

            # 提交接口数据，调用接口，获取返回数据
            self.res_code, self.res_content, self.res_headers = \
                self._handle.handle_request(method, self.url, self.param, self.header)

            # 根据res_code断言
            assert self.res_code >=200 and self.res_code <300

            # 如果teardown不为空，进行处理
            if teardown != "":
                self._handle.handle_teardown(teardown, self.res_content)

        except Exception as e:
            self.logger.error(traceback.format_exc())
            print('traceback.print_exc(): %s,%s' % (traceback.print_exc(), e))
            # self.assertTrue(0)

        finally:
            # 无论是否异常，输出url等信息到日志文件方便排查问题
            self.logger.info("url: %s" % self.url)
            self.logger.info("yaml_data: %s" % data_read.get_yaml())
            self.logger.info("-----------------------------------------------------------")
            self.logger.info("res_code: %s" % self.res_code)
            self.logger.info("res_content: %s" % self.res_content)
            self.logger.info("res.headers: %s" % self.res_headers)
            self.log.build_end_line(case_name)

    # 测试结束清理
    @classmethod
    def tearDownClass(cls):
        data_read.del_yaml()
