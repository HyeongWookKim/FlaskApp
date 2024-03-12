import os
import logging
from flask import Flask, render_template, url_for, request, redirect, flash, make_response, session
from email_validator import validate_email, EmailNotValidError
# flask-debugtoolbar: HTTP 요청 정보나 flask routes 결과, DB가 발행하는 SQL을 브라우저에서 확인 가능
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message


# flask 클래스 인스턴스화
app = Flask(__name__)

app.config['SECRET_KEY'] = '2AZSMss3p5QPbsY2hBs'
app.logger.setLevel(logging.DEBUG) # 로그 레벨 설정
### 로그 출력 희망 시, 로그 레벨에 따라 아래와 같이 지정 ###
# app.logger.critical('fatal error')
# app.logger.error('error')
# app.logger.warning('warning')
# app.logger.info('info')
# app.logger.debug('debug')

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False # 리다이렉트를 중단하지 않도록 설정
toolbar = DebugToolbarExtension(app) # 애플리케이션에 debug toolbar 설정

# Mail 클래스의 config 추가
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
mail = Mail(app) # flask-mail 확장을 등록

##################################################################################################

def send_email(to, subject, template, **kwargs):
    '''
        이메일 송신 함수
    '''
    msg = Message(subject, recipients = [to])
    msg.body = render_template(template + '.txt', **kwargs) # HTML 메일을 수신할 수 없는 경우, 텍스트 이메일 송신
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

##################################################################################################

# URL과 실행할 함수 매핑
# <참고> flask2부터는 @app.get('/') 또는 @app.post('/')라고 사용 가능
@app.route('/')
def index():
    return 'Hello, FlaskApp!'

@app.route('/hello/<name>', methods = ['GET', 'POST'], endpoint = 'hello-endpoint')
def hello(name):
    return f'Hello, {name}!'

@app.route('/name/<name>')
def show_name(name):
    return render_template('index.html', name = name) # name 변수를 템플릿 엔진에 전달

# 현재의 루트 정보를 url_for 함수로 출력
with app.test_request_context('/users?updated=true'):
    print(request.args.get('updated')) # true가 출력됨
    # '/'
    print(url_for('index'))
    # '/hello/world'
    print(url_for('hello-endpoint', name = 'world'))
    # '/name/BK?page=1'
    print(url_for('show_name', name = 'BK', page = '1'))

@app.route('/contact')
def contact():
    # 응답 객체 취득
    response = make_response(render_template('contact.html'))

    # 쿠키 설정
    response.set_cookie('FlaskApp key', 'FlaskApp value')

    # 세션 설정
    session['username'] = 'BK'

    # 문의 폼 화면 표시(GET)
    return response

@app.route('/contact/complete', methods = ['GET', 'POST'])
def contact_complete():
    if request.method == 'POST':
        # form 속성을 사용해서 값 취득
        username = request.form['username']
        email = request.form['email']
        description = request.form['description']

        is_valid = True # 입력 체크

        if not username:
            flash('사용자 명 입력은 필수입니다.')
            is_valid = False
        
        if not email:
            flash('이메일 주소 입력은 필수입니다.')
            is_valid = False
        
        # 입력된 이메일 주소가 유효한 형태인지 확인
        try:
            validate_email(email)
        except EmailNotValidError:
            flash('이메일 주소의 형식으로 입력해 주세요.')
            is_valid = False

        if not description:
            flash('문의 내용 입력은 필수입니다.')
            is_valid = False

        # 입력이 유효하지 않은 경우, contact 엔드포인트로 리다이렉트
        if not is_valid:
            return redirect(url_for('contact'))

        # 이메일로 문의 내용 송신(POST)
        send_email(
            email, '문의 감사합니다.', 'contact_mail', 
            username = username, description = description
        )


        # 문의 완료 화면(contact 엔드포인트)으로 리다이렉트
        flash('문의해 주셔서 감사합니다.')
        return redirect(url_for('contact_complete'))
    
    # 문의 완료 화면 표시(GET)
    return render_template('contact_complete.html')