from . import bp as blog
from flask import request, url_for, jsonify 
from app import db
from flask_login import login_required, current_user
from .forms import PostForm, CommentForm
from app.models import Post, Comment
from app.auth import token_auth

@blog.route('/posts', methods=['GET'])
def posts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])

# Added comments here - JG
@blog.route('/posts/<int:id>', methods=['GET', 'POST'])
@token_auth.login_required
def post(id):
    p = Post.query.get_or_404(id)
    # comments = Comment.query.filter_by(p.id)
    # both = [p.to_dict(), [c.to_dict() for c in comments]]
    return jsonify(p.to_dict())

@blog.route('/createpost', methods=['POST'])
@token_auth.login_required
def createpost():
    data = request.json
    user = token_auth.current_user()
    p = Post(data['title'], data['content'], user.id)
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict())

@blog.route('/posts/<int:id>/comment', methods=['GET', 'POST'])
@token_auth.login_required
def postComment(id):
    # p = Post.query.get_or_404(id)
    comments = Comment.query.filter_by(post_id=id).all()
    # both = [p.to_dict(), [c.to_dict() for c in comments]]
    return jsonify([c.to_dict() for c in comments])

@blog.route('/posts/<int:id>/create/comment', methods=['GET', 'POST'])
@token_auth.login_required
def postCreateComment(id):
    data = request.json
    user = token_auth.current_user().id
    p = Comment(data['content'], id, user)
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict())


@blog.route('/myposts', methods=['GET'])
@token_auth.login_required
def myposts():
    title = "EAT | My Posts"
    posts = current_user.posts
    return jsonify([p.to_dict() for p in posts])


@blog.route('/myposts/<int:post_id>')
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    title = f"EAT | {post.title.upper()}"
    return jsonify(post)

@blog.route('/myposts/delete/<int:post_id>', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.id != current_user.id:
        message = "No can do! You can only delete your posts."
        return jsonify({ "message": message }), 404 
    db.session.delete(post)
    db.session.commit()
    message = "Post deleted"
    return jsonify({ "message": message }), 201



# Questions
    # Does data on likes and favorites live in both the user and posts data tables? 
    # the user SQL table and the userPosts sql table, and display info from both on the 
        # home page?