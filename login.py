import requests
from lxml import etree
import os
from PIL import Image
import io

CAPTCHA_IMAGE_URL = 'https://mo.lager.com.tw/captcha.php'
LOGIN_URL = 'https://mo.lager.com.tw/sns/start'
START_GAME_URL = 'https://mo.lager.com.tw/sns/startgame'
TIMEOUT = 10


class LoginError(Exception):
    def __init__(self, error_type,  account, message):
        self.error_type = error_type
        self.message = message
        self.account = account

    def __str__(self):
        return "{message} : {account}".format(message=self.message,
                                              account=self.account)


def get_session():
    session = requests.session()
    session.headers.update({
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
        'Origin': 'https://mo.lager.com.tw',
        'Referer': 'https://mo.lager.com.tw/sns/start',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1'
    })
    return session


def get_captcha(session: requests.session):
    image_data = session.get(url=CAPTCHA_IMAGE_URL, timeout=TIMEOUT)
    io_file = io.BytesIO(image_data.content)
    image = Image.open(io_file)
    image.show()

    return io_file


def login(session: requests.session, account: str, password: str,
          captcha_code=None, save_captcha=False):
    """Login to Mo Online.

    Arguments:
        session {requests.session} -- requests session.
        account {str} -- game account.
        password {str} -- game password.
        captcha {str} -- captcha code.

    Raises:
        LoginError:
            description: error_type
            server_error: Server timeout or error
            account_error: User password or account error
            captcha_error:  captcha code error.
    Returns:
        [str] -- game login url. (moop)
    """
    page = session.get(url=LOGIN_URL, timeout=TIMEOUT)
    if not isinstance(captcha_code, str):
        get_captcha(session)
        captcha_code = input("input captcha code: ")
    csrf_parse(page.text)
    login_data = {'loginAccount': account,
                  'loginPassword': password,
                  'loginCode': captcha_code,
                  'contract1': 'on',
                  'contract2': 'on',
                  'contract3': 'on',
                  **csrf_parse(page.text)
                  }

    post_login = session.post(
        url=LOGIN_URL,
        timeout=TIMEOUT,
        data=login_data)

    if post_login.url == START_GAME_URL and post_login.status_code == 200:
        _base_index = post_login.text.find('window.location.href')+24
        return post_login.text[_base_index:post_login.text.find(
            '"', _base_index+1)]

    elif post_login.textfind("密碼錯誤") > -1:
        raise LoginError(error_type='account_error',
                         account=account, message="account or password wrong.")
    elif post_login.textfind("驗證碼輸入不正確") > -1:
        raise LoginError(error_type='captcha_error',
                         account=account, message="captcha code error.")

    raise BaseException("Something error :(")


def open_game(moop_data: str, path: str):
    # Only support Windows 10
    def _moop_url_parse(url: str):
        url = url[7:].split("/")
        account = []
        account.append(url[0].split("@")[0])
        account.append(url[0].split("@")[1])
        account.append(url[1])

        return " ".join(i for i in account)
    dir_path = os.path.dirname(path)

    command = 'start /b /d "{dir_path}" mystina.exe {account_arg}'.format(
        dir_path=dir_path,
        account_arg=_moop_url_parse(moop_data)
    )
    os.system(command)


def open_login(moop_data: str, path: str):
    command = "{login_path} {moop_url}".format(
        login_path=path,
        moop_url=moop_data
    )
    os.system(command)


def csrf_parse(html: str):
    root = etree.HTML(html)
    input_tag = root.xpath('//input')
    res = {}
    for i in input_tag:
        if i.attrib.get('name'):
            if i.attrib.get('name') in ['csrf_name', 'csrf_value']:
                res[i.attrib.get('name')] = i.attrib.get('value')
    return res
