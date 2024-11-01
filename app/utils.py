# utils.py
from flask_bcrypt import Bcrypt

# 비밀번호 해싱
def generate_password_hash(password):
    bcrypt = Bcrypt()
    return bcrypt.generate_password_hash(password).decode('utf-8')

# 비밀번호 해싱 확인
def check_password_hash(hashed_password, password):
    bcrypt = Bcrypt()
    return bcrypt.check_password_hash(hashed_password, password)
