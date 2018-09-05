import unittest
import traceback
from TestCase.common import handle, data_read
from parameterized import parameterized


class TestMain(unittest.TestCase):
    """主流程测试"""

    @classmethod
    def setUpClass(cls):
        print(u"----用例执行-----")
        cls._handle = handle.Handle()
        setup_data = data_read.get_xls('dict', u"dx_interauto_pre_case.xls", "setup")
        cls._handle.set_global(setup_data)

    # 读取用例文件中的用例（type,Excel文件名,sheet名）
    case = data_read.get_xls('list', u"dx_interauto_pre_case.xls", "main")

    # 设定输出的用例报告中的用例名格式 (这里需要三个传参否则会报错)
    def custom_name_func(testcase_func=None, param_num=None, param=None):
        return "%s_%s_%s" % ("test", str(param.args[0]), str(param.args[3]))

    # 参数化数据，将读取的用例参数化；testcase_func_name参数化用例名称
    @parameterized.expand(case, testcase_func_name=custom_name_func)
    def test_main(self, case_id, setup, header, case_name, url, method, path, param, teardown, test_assert):
        try:
            # print的内容会输出到报告中
            print("case_%s" % case_id)
            print("yaml_data: %s" % data_read.get_yaml())
            self.path = self._handle.handle_url(path)
            self.url = "%s%s" % (url, self.path)
            print("url: %s" % self.url)
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
            print("---------------------------------------------------------------")

            # 提交接口数据，调用接口，获取返回数据
            res_code, res_content, res_headers = self._handle.handle_request(method, self.url, self.param, self.header)
            print("res_code: %s & type: %s" % (res_code, type(res_code)))
            print("res_content: %s" % res_content)
            print("res.headers: %s" % res_headers)

            assert res_code >=200 and res_code <300

            if teardown != "":
                self._handle.handle_teardown(teardown, res_content)

        except Exception as e:
            print('traceback.print_exc(): %s,%s' % (traceback.print_exc(), e))
            self.assertTrue(0)

    # 测试结束清理
    @classmethod
    def tearDownClass(cls):
        data_read.del_yaml()
