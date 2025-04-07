from flask import Blueprint, request, jsonify
from models import db, Post
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('post', __name__, url_prefix='/post')

@bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input'}), 400
    title = data.get('title')
    content = data.get('content')
    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400
    new_post = Post( title=title, content=content, user_id=current_user_id )
    db.session.add(new_post)
    db.session.commit()
    return jsonify({ 'message': 'Post created successfully', 'post': { 'id': new_post.id, 'title': new_post.title, 'content': new_post.content, 'user_id': new_post.user_id, 'created_at': str(new_post.created_at), 'updated_at': str(new_post.updated_at) } }), 201


@bp.route('/', methods=['GET'])
@jwt_required()
def get_posts():
    posts = Post.query.all()
    return jsonify([{'id': post.id, 'title': post.title, 'content': post.content, 'user_id': post.user_id, 'created_at': str(post.created_at), 'updated_at': str(post.updated_at)} for post in posts]), 200


@bp.route('/my-posts', methods=['GET'])
@jwt_required()
def get_user_posts():
    current_user_id = int(get_jwt_identity())
    posts = Post.query.filter_by(user_id=current_user_id).all()
    return jsonify([{'id': post.id, 'title': post.title, 'content': post.content, 'user_id': post.user_id, 'created_at': str(post.created_at), 'updated_at': str(post.updated_at)} for post in posts]), 200


@bp.route('/<id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    return jsonify({'id': post.id, 'title': post.title, 'content': post.content, 'user_id': post.user_id, 'created_at': str(post.created_at), 'updated_at': str(post.updated_at)}), 200


@bp.route('/<id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    current_user_id = int(get_jwt_identity())
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    if post.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized to update this post'}), 403
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input'}), 400
    if 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Title and content are required'}), 400
    post.title = data['title']
    post.content = data['content']
    post.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Post updated successfully', 'post': {'id': post.id, 'title': post.title, 'content': post.content, 'user_id': post.user_id, 'created_at': str(post.created_at), 'updated_at': str(post.updated_at)}}), 200
 
 
@bp.route('/<id>', methods=['PATCH'])
@jwt_required()
def patch_post(post_id):
    current_user_id = int(get_jwt_identity())
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    if post.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized to update this post'}), 403
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input'}), 400
    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']
    post.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Post updated successfully', 'post': {'id': post.id, 'title': post.title, 'content': post.content, 'user_id': post.user_id, 'created_at': str(post.created_at), 'updated_at': str(post.updated_at)}}), 200


@bp.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    current_user_id = int(get_jwt_identity())
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    if post.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized to delete this post'}), 403
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'}), 200
