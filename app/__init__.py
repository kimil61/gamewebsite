from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from .models import db
from flask_wtf.csrf import CSRFProtect


load_dotenv()

# db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object('config.Config')
    # CSRF 보호 비활성화 (테스트용)  
    app.config['WTF_CSRF_ENABLED'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # 블루프린트 등록
    from .routes import bp
    app.register_blueprint(bp)

    # 보안 헤더 적용
    @app.after_request
    def apply_security_headers(response):
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'  # 클릭재킹 방지
        response.headers['X-Content-Type-Options'] = 'nosniff'  # MIME 타입 스니핑 방지
        response.headers['Content-Security-Policy'] = "default-src 'self'"  # 컨텐츠 보안 정책 설정
        return response

    return app
