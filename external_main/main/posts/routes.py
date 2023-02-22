from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from main.models import Post, Comment
from datetime import datetime
from main.posts.forms import PostForm, PostComment
from main import db
from main.users.utils import save_picture

posts = Blueprint('posts', __name__)


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    user_image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    form = PostComment()
    if post.post_picture:
        image_file = url_for('static',
                             filename='posts_images/' + post.post_picture)
        return render_template("post.html",
                               title=post.title,
                               post=post,
                               picture=image_file,current_user_image_file=user_image_file,form=form)
    return render_template("post.html", title=post.title, post=post, current_user_image_file=user_image_file, form=form)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data,
                                        img_path='posts_images')
        else:
            picture_file = None
        post = Post(title=form.title.data,
        data_posted=datetime.utcnow(),
                    content=form.content.data,
                    author=current_user,
                    post_picture=picture_file)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been published", 'success')
        return redirect(url_for("main.home"))
    return render_template('create_new_post.html',
                           title="New Post",
                           legend="Create Post",
                           form=form)


@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data,
                                        img_path='posts_images')
            post.post_picture = picture_file
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated", 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.picture.data = post.post_picture
    return render_template('create_new_post.html',
                           title="Update Post",
                           form=form,
                           legend="Update Post")


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted", 'success')
    return redirect(url_for("main.home"))

@posts.route("/post/<int:post_id>/create-comment", methods=["POST"])
@login_required
def create_comment(post_id):
    form = PostComment()
    post = Post.query.get_or_404(post_id)
    if not form.content.data:
        flash('Comment cannot be empty.', 'warning')
        return redirect(url_for('posts.post', post_id=post.id))
    else:
        if post:
            print(form.content.data,datetime.utcnow(),current_user)
            comment = Comment(text=form.content.data,date_created=datetime.utcnow(),author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('posts.post', post_id=post.id))
        else:
            flash('Post does not exist.', 'warning')
    return redirect(url_for('main.home'))

@posts.route("/post/<int:comment_id>/delete-comment")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    if not comment:
        flash('Comment does not exist!', 'warning')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash("You don't have peermisson to delete this comment!", 'error')
    else:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('posts.post', post_id=comment.post_id))