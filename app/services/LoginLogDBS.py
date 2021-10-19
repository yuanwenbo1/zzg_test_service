from app import db, id_worker
from app.models import LoginLog
from flask import current_app


class LoginLogDBS:

    @staticmethod
    def query_token(phone) -> LoginLog:
        '''
        获取脚本数据详情
        :return:
        '''
        data = LoginLog.query.filter_by(phone=phone).first()
        return data

    @staticmethod
    def update_token(phone, token):
        try:
            data = LoginLog.query.filter_by(phone=phone).first()
            if data:
                # 存在就更新token
                print("存在就更新token")
                data.token = token
                db.session.commit()
                return data
            else:
                # 不存在就插入
                print("不存在就插入")
                new_data = LoginLog()
                new_data.id = id_worker.get_id()
                new_data.phone = phone
                new_data.token = token
                db.session.add(new_data)
                db.session.commit()
                return data
        except Exception as e:
            current_app.logger.error("LoginLogDBS:{}".format(e))
            db.session.rollback()
