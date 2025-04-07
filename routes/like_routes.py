from flask import Blueprint, request, jsonify
from models import db, Like, Post
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('like', __name__, url_prefix='/like')

@bp.route('/post/<id>', methods=['POST'])
@jwt_required()
def like_post(post_id):
    current_user_id = int(get_jwt_identity())
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    existing_like = Like.query.filter_by(user_id=current_user_id, post_id=post_id ).first()
    if existing_like:
        return jsonify({'error': 'You have already liked this post'}), 409
    new_like = Like(
        user_id=current_user_id,
        post_id=post_id
    )
    db.session.add(new_like)
    db.session.commit()
    return jsonify({'message': 'Post liked successfully','like': { 'id': new_like.id, 'user_id': new_like.user_id,'post_id': new_like.post_id,'created_at': str(new_like.created_at) } }), 201


@bp.route('/post/<id>', methods=['GET'])
@jwt_required()
def get_post_likes(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    likes = Like.query.filter_by(post_id=post_id).all()
    return jsonify({ 'post_id': post_id, 'likes_count': len(likes),'likes': [{ 'id': like.id, 'user_id': like.user_id, 'created_at': str(like.created_at) } for like in likes]}), 200


@bp.route('/post/<id>', methods=['DELETE'])
@jwt_required()
def unlike_post(post_id):
    current_user_id = int(get_jwt_identity())
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    like = Like.query.filter_by(   user_id=current_user_id, post_id=post_id ).first()
    if not like:
        return jsonify({'error': 'You have not liked this post'}), 404
    db.session.delete(like)
    db.session.commit()
    return jsonify({'message': 'Post unliked successfully'}), 200

