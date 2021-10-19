import time

import pymysql
import requests
host = "https://t-fssaas.lepass.cn"
pymysql_config = {"host": "172.20.33.22",
                  "port": 3321,
                  "user": "test_dev",
                  "password": "HBmAlCS3",
                  "database": "sms"}
class OpenApi:

    @staticmethod
    def tokenCheck(token):
        url = "/business/merchant/outer/tokenCheck"
        r = requests.get(host + url, headers={'token': token})
        if r.json().get("code") == 0:
            return True
        else:
            return False

    @staticmethod
    def captcha():
        url = "/open-api/b/captcha"
        r = requests.get(host + url)
        return r

    @staticmethod
    def smsSend(captchaCode="1234", sess="", mobile=""):
        url = "/open-api/b/smsSend"
        r = requests.post(host + url, json={
            "captchaCode": captchaCode,
            "sess": sess,
            "mobile": mobile
        })
        return r

    @staticmethod
    def get_sms_captcha(F_mobile):
        conn = pymysql.connect(host=pymysql_config.get("host"),
                               port=pymysql_config.get("port"),
                               user=pymysql_config.get("user"),
                               password=pymysql_config.get("password"),
                               database=pymysql_config.get("database")
                               )
        m = time.strftime("%m")
        curr = conn.cursor()
        curr.execute(''' SELECT f_create_time,F_update_time,F_mobile,F_content 
        FROM `sms`.`t_sms_record_{}` 
        WHERE F_mobile = '{}' ORDER BY f_create_time DESC'''.format(m, F_mobile))
        res = curr.fetchall()[0]
        conn.close()
        return res[-1][-4:]

    @staticmethod
    def login_by_phone_num(login_config):
        captcha_info = OpenApi.captcha().json().get("data")
        img = captcha_info.get("img")
        sess = captcha_info.get("sess")
        requests.get(img)
        mobile = login_config.get("mobile")
        OpenApi.smsSend(login_config.get("img_captcha_default"), sess, mobile)
        sms_captcha = OpenApi.get_sms_captcha(mobile)
        url = "/open-api/b/login"
        login_config["code"] = sms_captcha
        r = requests.post(host + url, json=login_config)
        return r