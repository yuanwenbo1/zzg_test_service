from datetime import datetime

from . import db


class BaseModel:
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


class LoginLog(db.Model, BaseModel):
    """
    用户资料
    """
    __tablename__ = 'login_log'
    id = db.Column(db.BigInteger, primary_key=True)  # id
    phone = db.Column(db.Text, nullable=False)  # 电话号码
    token = db.Column(db.Text, nullable=False)  # 用户名


