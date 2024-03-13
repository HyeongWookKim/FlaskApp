from flask import Flask


def create_app():
    '''
        Blueprint란 앱을 분할하기 위한 Flask의 기능으로, 
        앱의 규모가 커져도 간결한 상태를 유지할 수 있어서 보수성이 향상됨
        
        Blueprint를 사용하려면 Blueprint 객체를 생성하고, 
        Flask 앱인 app 인스턴스의 register_blueprint 메서드에 전달해서 등록해야 함
    '''

    # Flask 인스턴스 생성
    app = Flask(__name__)

    # CRUD 패키지로부터 views import
    from apps.crud import views as crud_views

    # register_blueprint를 사용해서 views의 crud를 앱에 등록
    app.register_blueprint(crud_views.crud, url_prefix = '/crud') # views의 엔드포인트 모든 URL이 crud로부터 시작되도록 설정

    return app