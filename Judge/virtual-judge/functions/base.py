import requests


class BaseClass(object):
    SETTING = None
    CONFIG = None
    STATUS = None
    FINISHED_STATUS = None

    oj_name = None

    session = requests.session()

    def get_url(self, url, *args):
        return self.SETTING['host'] + self.SETTING[url] % args

    def do_login(self):
        """
        执行登陆。
        :return:返回Boolean 
        """
        pass

    def do_submit(self, pid, lang, code):
        """
        提交代码。
        :param pid: 
        :param lang: 
        :param code: 
        :return:返回Boolean 
        """
        pass

    def get_submissions(self, **kwargs):
        """
        取得某一页提交。
        :param kwargs: 
        :return: 
        """
        pass

