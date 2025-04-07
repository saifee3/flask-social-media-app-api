from flask import Blueprint, request, jsonify
from models import db, Comment, Post
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('comment', __name__, url_prefix='/comment')

@bp.route('/post/<id>', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    current_user_id = int(get_jwt_identity())
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'error': 'Content is required'}), 400
    new_comment = Comment(
        user_id=current_user_id,
        post_id=post_id,
        content=data['content']
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({ 'message': 'Comment added successfully', 'comment': {'id': new_comment.id, 'user_id': new_comment.user_id, 'post_id': new_comment.post_id, 'content': new_comment.content,'created_at': str(new_comment.created_at) }}), 201


@bp.route('/post/<id>', methods=['GET'])
@jwt_required()
def get_post_comments(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    comments = Comment.query.filter_by(post_id=post_id).all()
    return jsonify({'post_id': post_id,'comments_count': len(comments),'comments': [{'id': comment.id, 'user_id': comment.user_id,'content': comment.content, 'created_at': str(comment.created_at),'updated_at': str(comment.updated_at)} for comment in comments] }), 200


@bp.route('/update/<id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment(comment_id):
    current_user_id = int(get_jwt_identity())
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    if comment.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized to update this comment'}), 403
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input'}), 400
    if request.method == 'PUT' and 'content' not in data:
        return jsonify({'error': 'Content is required for PUT request'}), 400
    if 'content' in data:
        comment.content = data['content']
        comment.updated_at = datetime.utcnow()
        db.session.commit()
    return jsonify({ 'message': 'Comment updated successfully','comment': { 'id': comment.id,  'user_id': comment.user_id, 'post_id': comment.post_id, 'content': comment.content,  'created_at': str(comment.created_at), 'updated_at': str(comment.updated_at) } }), 200


@bp.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    current_user_id = int(get_jwt_identity())
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    if comment.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized to delete this comment'}), 403
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted successfully'}), 200
