# app/routes.py
from crypt import methods
from datetime import datetime

from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from .models import db, User, Post, Comment, Category, Tag, PostTag
from .utils import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from urllib.parse import urlparse, urljoin

bp = Blueprint('web', __name__)


# api_bp = Blueprint('api', __name__)
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


##################################################################################################
## admin


@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, is_admin=True).first()
        if user is None or not check_password_hash(user.password, password):
            error = 'Invalid username or password'
        else:
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or not is_safe_url(next_page):
                next_page = url_for('web.admin_index')
            return redirect(next_page)
    return render_template('admin_login.html', error=error)


@bp.route('/admin/index')
@login_required
def admin_index():
    return render_template('admin_index.html')


@bp.route('/admin/settings')
@login_required
def admin_settings():
    return render_template('admin_settings.html')


@bp.route('/admin/users')
@login_required
def admin_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)


@bp.route('/admin/users/create', methods=['POST'])
@login_required
def admin_create_user():
    try:
        # 폼 데이터 가져오기
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        email = request.form.get('email')
        is_admin = request.form.get('is_admin', 'off')

        # 필수 입력값 검증
        if not all([username, password, repassword, email]):
            return jsonify({
                'success': False,
                'message': '모든 필수 항목을 입력해주세요.'
            }), 400

        # 비밀번호 일치 여부 확인
        if password != repassword:
            return jsonify({
                'success': False,
                'message': '비밀번호가 일치하지 않습니다.'
            }), 400

        # 사용자 이름 중복 체크
        if User.query.filter_by(username=username).first():
            return jsonify({
                'success': False,
                'message': '이미 존재하는 사용자 이름입니다.'
            }), 400

        # 이메일 중복 체크
        if User.query.filter_by(email=email).first():
            return jsonify({
                'success': False,
                'message': '이미 존재하는 이메일입니다.'
            }), 400

        # checkbox 값을 boolean으로 변환 (on => 1, off => 0)
        is_admin_bool = 1 if is_admin == 'on' else 0

        # 새 사용자 생성
        new_user = User(
            username=username,
            password=generate_password_hash(password),  # 비밀번호 해시화
            email=email,
            is_admin=is_admin_bool,
            created_at=datetime.utcnow()
        )

        # DB에 저장
        db.session.add(new_user)
        db.session.commit()

        # 성공 응답 반환
        return jsonify({
            'success': True,
            'message': '사용자가 성공적으로 생성되었습니다.',
            'user': {
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email,
                'is_admin': new_user.is_admin,
                'created_at': new_user.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'사용자 생성 중 오류가 발생했습니다: {str(e)}'
        }), 500


@bp.route('/admin/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'message': '사용자를 찾을 수 없습니다.'
            }), 404

        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_admin,
                'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'사용자 정보를 불러오는 중 오류가 발생했습니다: {str(e)}'
        }), 500


@bp.route('/admin/users/<int:user_id>/update', methods=['POST'])
@login_required
def update_user(user_id):
    try:
        print(user_id)
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'message': '사용자를 찾을 수 없습니다.'
            }), 404

        # 기본 정보 업데이트
        username = request.form.get('username')
        email = request.form.get('email')
        is_admin = request.form.get('is_admin', 'off')

        # 사용자 이름 중복 체크 (현재 사용자 제외)
        existing_user = User.query.filter(
            User.username == username,
            User.id != user_id
        ).first()
        if existing_user:
            return jsonify({
                'success': False,
                'message': '이미 존재하는 사용자 이름입니다.'
            }), 400

        # 이메일 중복 체크 (현재 사용자 제외)
        existing_email = User.query.filter(
            User.email == email,
            User.id != user_id
        ).first()
        if existing_email:
            return jsonify({
                'success': False,
                'message': '이미 존재하는 이메일입니다.'
            }), 400

        # 정보 업데이트
        user.username = username
        user.email = email
        user.is_admin = is_admin == 'on'

        # 비밀번호 변경이 요청된 경우
        new_password = request.form.get('new_password')
        if new_password:
            confirm_new_password = request.form.get('confirm_new_password')
            if new_password != confirm_new_password:
                return jsonify({
                    'success': False,
                    'message': '새 비밀번호가 일치하지 않습니다.'
                }), 400
            user.password = generate_password_hash(new_password)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': '사용자 정보가 성공적으로 업데이트되었습니다.',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_admin,
                'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'사용자 정보 업데이트 중 오류가 발생했습니다: {str(e)}'
        }), 500


@bp.route('/admin/posts')
@login_required
def admin_posts():
    return render_template('admin_posts.html')


@bp.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('web.admin_login'))


##################################################################################################
## login


@bp.route('/login', methods=['get', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password, password):
            error = 'Invalid username or password'
        else:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@bp.route('/register', methods=['get', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User.query.filter_by(username=username).first()
        if user:
            error = 'Username already exists'
        else:
            user = User(username=username, password=generate_password_hash(password), email=email)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html', error=error)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#
# ##################################################################################################
# ## posts
#
# @bp.route('/')
# def hello():
#     return render_template('index.html')
#
#
# @bp.route('/404')
# def not_found():
#     return render_template('404.html')
#
#
# @bp.route('/api/posts')
# def api_index():
#     posts = Post.query.order_by(Post.id.desc()).all()
#     return jsonify([post.to_dict() for post in posts])
#
#
# @bp.route('/api/posts/<int:id>')
# def show(id):
#     post = Post.query.get_or_404(id)
#     return jsonify(post.to_dict())
#
#
# @bp.route('/api/posts/create', methods=['POST'])
# def create():
#     title = request.form['title']
#     contents = request.form['contents']
#     user_id = session.get('user_id')
#     category_id = request.form['category_id']
#     post = Post(title=title, contents=contents, user_id=user_id, category_id=category_id)
#     db.session.add(post)
#     db.session.commit()
#     return jsonify(post.to_dict())
#
#
# @bp.route('/api/posts/<int:id>/update', methods=['PUT'])
# def update(id):
#     post = Post.query.get_or_404(id)
#     post.title = request.form['title']
#     post.contents = request.form['contents']
#     db.session.commit()
#     return jsonify(post.to_dict())

# @bp.route('/api/posts/<int:id>')
# def show(id):
#     post = Post.query.get_or_404(id)
#     return jsonify(post.to_dict()) 

# @bp.route('/api/posts/create', methods=['POST'])
# def create():
#     post = Post(title='test', contents='test', user_id=1, category_id=1)
#     db.session.add(post)
#     db.session.commit()
#     return jsonify(post.to_dict())

# @bp.route('/api/posts/<int:id>/update', methods=['PUT'])
# def update(id):
#     post = Post.query.get_or_404(id)
#     post.title = 'updated'
#     db.session.commit()
#     return jsonify(post.to_dict())

# @bp.route('/api/posts/<int:id>/delete', methods=['DELETE'])
# def delete(id):
#     post = Post.query.get_or_404(id)
#     db.session.delete(post)
#     db.session.commit()
#     return jsonify(post.to_dict())

# @bp.route('/api/posts/<int:id>/thumbs_up', methods=['PUT'])
# def thumbs_up(id):
#     post = Post.query.get_or_404(id)
#     post.thumbs_up += 1
#     db.session.commit()
#     return jsonify(post.to_dict())

# @bp.route('/api/posts/<int:id>/thumbs_down', methods=['PUT'])
# def thumbs_down(id):
#     post = Post.query.get_or_404(id)
#     post.thumbs_down += 1
#     db.session.commit()
#     return jsonify(post.to_dict())

# @bp.route('/api/posts/<int:id>/view', methods=['PUT'])
# def view(id):
#     post = Post.query.get_or_404(id)
#     post.view_cnt += 1
#     db.session.commit()
#     return jsonify(post.to_dict())


# ##################################################################################################
# ## users
# @bp.route('/api/users')
# def users():
#     users = User.query.all()
#     return jsonify([user.to_dict() for user in users])

# @bp.route('/api/users/<int:id>')
# def user(id):
#     user = User.query.get_or_404(id)
#     return jsonify(user.to_dict())

# @bp.route('/api/users/create', methods=['POST'])
# def create_user():
#     user = User(username='test', password='test')
#     db.session.add(user)
#     db.session.commit()
#     return jsonify(user.to_dict())

# @bp.route('/api/users/<int:id>/update', methods=['PUT'])
# def update_user(id):
#     user = User.query.get_or_404(id)
#     user.username = 'updated'
#     db.session.commit()
#     return jsonify(user.to_dict())

# @bp.route('/api/users/<int:id>/delete', methods=['DELETE'])
# def delete_user(id):
#     user = User.query.get_or_404(id)
#     db.session.delete(user)
#     db.session.commit()
#     return jsonify(user.to_dict())
