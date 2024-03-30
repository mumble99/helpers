import requests
import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_DEFAULT_PROXY_ = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}


def log(*args):
    print("[%s]" % datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"), *args)


def create_session(need_proxy: bool = False, headers: dict = {}, cookies: dict = {}) -> requests.Session:
    s = requests.Session()
    if need_proxy:
        s.proxies = _DEFAULT_PROXY_

    s.headers.update(headers)

    for k, v in cookies.items():
        s.cookies.set(k, v)
    return s


def get_request(s: requests.Session, url: str, params: dict = {}, timeout: int = 3) -> dict:
    try:
        args = {
            "url": url,
            "params": params,
            "verify": False,
            "allow_redirects": False,
            "timeout": timeout,
        }
        r = s.get(**args)
        log(url, "GET", r.status_code)
        return {
            "status": True,
            "code": r.status_code,
            "text": r.text,
            "response_time": r.elapsed.total_seconds(),
            "headers": r.headers
        }
    except requests.exceptions.RequestException as e:
        log(e)
        return {
            "status": False,
            "code": 0,
            "text": "",
            "response_time": 0,
            "headers": {}
        }


def post_request(s: requests.Session, url: str, body: any, json: bool = False, params: dict = {},
                 timeout: int = 3) -> dict:
    try:
        args = {
            "url": url,
            "params": params,
            "verify": False,
            "allow_redirects": False,
            "timeout": timeout,
        }
        if json:
            args["json"] = body
        else:
            args["data"] = body
        r = s.post(**args)
        log(url, "POST", r.status_code)
        return {
            "status": True,
            "code": r.status_code,
            "text": r.text,
            "response_time": r.elapsed.total_seconds(),
            "headers": r.headers
        }
    except requests.exceptions.RequestException as e:
        log(e)
        return {
            "status": False,
            "code": 0,
            "text": "",
            "response_time": 0,
            "headers": {}
        }


# s = create_session(need_proxy=True)
# print(get_request(s, url="https://google.com/"))
# print(post_request(s, url="https://ya.ru/", body={"test": "test"}, json=True))
