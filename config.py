import logging
import os


class config:
    def __init__(self, **kwargs):
        # mystina.exe
        self.game_path = self.isfile_check(kwargs['gamePath'])
        # login.exe
        self.login_path = self.isfile_check(kwargs['loginPath'])

        self.save_captcha = kwargs['saveCaptcha']
        self.account_path = self.isfile_check(kwargs['accountPath'])

    def isfile_check(self, path: str):
        if os.path.isfile(path):
            return path
        logging.debug("{path} Not Found.".format(path=path))
        return None
