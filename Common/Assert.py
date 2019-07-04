# -*- coding: utf-8 -*-

from Common import Log

class Assertions:
    def __init__(self):
        self.log = Log.Log()

    def assert_code(self, code, expect_code):
        """
        验证状态码
        :param code:
        :param expect_code:
        :return:
        """
        try:
            assert code == expect_code
            return True
        except Exception:
            self.log.error("statusCode error: expect_code is %s, statusCode is %s " % (expect_code, code))
            raise

    def assert_body(self, body, body_msg, expected_msg):
        '''
        验证response中任意属性的值
        :param body:
        :param body_msg:
        :param expected_msg:
        :return:
        '''
        try:
            msg = body[body_msg]
            assert msg == expected_msg
            return True
        except Exception:
            self.log.error('Response body msg =! %s expect_msg: %s ' % (body, expected_msg))
            raise

    def assert_in_text(self,rowkey,response):
        """
        验证rowkey在response中
        :param rowkey:
        :param response:
        :return:
        """
        try:
            if rowkey in response:
                return True
        except:
            raise

