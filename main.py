from app import create_app

if __name__ == '__main__':
    app = create_app("production")
    app.run("0.0.0.0", port=7890, debug=True)
    # celery开启的命令 gevent协成
    # celery -A app.tasks.task_sms worker -l info -P gevent
