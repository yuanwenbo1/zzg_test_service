from flask import request

from app.api import api
from app.services.LoginLogDBS import LoginLogDBS
from app.thirdservices.zzg import OpenApi
from app.utils.response_service import response, Code

login_config = {
    "mobileBrand": None,
    "code": None,
    "osVersion": None,
    "mobileModel": None,
    "latitude": None,
    "ip": None,
    "mobile": None,
    "osType": None,
    "device": None,
    "version": None,
    "deviceId": None,
    "longitude": None,
    "img_captcha_default": None
}


@api.route("/testservice/login", methods=["POST"])
def index():
    try:
        login_config["mobileBrand"] = request.json.get("mobileBrand", "HONOR")
        login_config["osVersion"] = request.json.get("osVersion", "10")
        login_config["mobileModel"] = request.json.get("mobileModel", "EBG-AN10")
        login_config["latitude"] = request.json.get("latitude", 22.548807)
        login_config["ip"] = request.json.get("ip", "10.20.65.251")
        login_config["mobile"] = request.json.get("mobile")
        login_config["osType"] = request.json.get("osType", "android")
        login_config["device"] = request.json.get("device", "29d9108f-d147-495e-b632-c710a2279e32")
        login_config["version"] = request.json.get("version", 150005)
        login_config["deviceId"] = request.json.get("deviceId", "29d9108f-d147-495e-b632-c710a2279e32")
        login_config["longitude"] = request.json.get("longitude", 113.943248)
        login_config["img_captcha_default"] = request.json.get("img_captcha", "1234")
        if not login_config.get("mobile"):
            raise Exception("mobile为null")

    except Exception as e:
        return response(dict(code=400, message="参数异常:{}".format(e), data=None), status=400)

    try:
        res_info = {}
        mobile = str(login_config["mobile"])
        data = LoginLogDBS.query_token(mobile)
        if data:
            t_token = data.token
            if OpenApi.tokenCheck(t_token):
                return response(dict(code=Code.OK, message="成功,token未失效直接返回!", data=t_token), status=200)
        res = OpenApi.login_by_phone_num(login_config)
        if res.json().get("code") == 1:
            res_info["token"] = res.json().get("msg")
            LoginLogDBS.update_token(mobile, res_info["token"])
            return response(dict(code=Code.OK, message="成功,token失效重新生成!", data=res_info), status=200)
        else:
            return response(dict(code=403, message="失败,{}!".format(res.json().get("msg")), data=None), status=403)
    except Exception as e:
        return response(dict(code=500, message="服务异常:{}".format(e), data=None), status=500)
