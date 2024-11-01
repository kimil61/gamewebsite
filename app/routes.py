# routes.py
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from .models import db,User,Post,Comment,Category,Tag,PostTag
from .utils import check_password_hash, generate_password_hash

bp = Blueprint('web', __name__)
# api_bp = Blueprint('api', __name__)
##################################################################################################
## login



@bp.route('/login', methods=['get','POST'])
def login():
    error = None
    if request.method   ==   'POST':
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


@bp.route('/register', methods=['get','POST'])
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

# 이사 생략
##################################################################################################
## posts

@bp.route('/')
def hello():
    return render_template('index.html')

@bp.route('/404')
def not_found():
    return render_template('404.html')



@bp.route('/api/posts')
def index():
    posts = Post.query.order_by(Post.id.desc()).all()
    return jsonify([post.to_dict() for post in posts])

@bp.route('/api/posts/<int:id>')
def show(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_dict())

@bp.route('/api/posts/create', methods=['POST'])
def create():
    title = request.form['title']
    contents = request.form['contents']
    user_id = session.get('user_id')
    category_id = request.form['category_id']
    post = Post(title=title, contents=contents, user_id=user_id, category_id=category_id)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict())

@bp.route('/api/posts/<int:id>/update', methods=['PUT'])
def update(id):
    post = Post.query.get_or_404(id)
    post.title = request.form['title']
    post.contents = request.form['contents']
    db.session.commit()
    return jsonify(post.to_dict())

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
