# app/__init__.py
from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager
from .models import db, User
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS

load_dotenv()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    # SQLALCHEMY_DATABASE_URI 와 SECRET_KEY는 여기서 로딩이 된다
    app.config.from_object('config.Config')

    # CSRF 보호 비활성화 (테스트용)  
    app.config['WTF_CSRF_ENABLED'] = True
    db.init_app(app)
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    login_manager.init_app(app)
    login_manager.login_view = 'web.admin_login'  # Endpoint name of your login view

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        # db.drop_all()
        db.create_all()

    # blueprint 등록
    from .routes import bp
    app.register_blueprint(bp)

    # 보안 헤더 적용
    @app.after_request
    def apply_security_headers(response):
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'  # 클릭재킹 방지
        response.headers['X-Content-Type-Options'] = 'nosniff'  # MIME 타입 스니핑 방지
        # 이거 추가하면 외부의 이미지가 나오지 않음 .
        # response.headers['Content-Security-Policy'] = "default-src 'self'"  # 컨텐츠 보안 정책 설정
        return response

    return app
