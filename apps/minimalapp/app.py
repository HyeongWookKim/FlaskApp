from flask import Flask

# flask 클래스 인스턴스화
app = Flask(__name__)

# URL과 실행할 함수 매핑
@app.route('/')
def index():
    return 'Hello, FlaskApp!'