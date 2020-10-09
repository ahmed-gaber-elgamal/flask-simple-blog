from flask import render_template,url_for,flash,redirect,request,Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_blog import db
from flask_blog.models import  BlogPost
from flask_blog.blog_posts.forms import BlogPostForm
from flask_blog.blog_posts.picture_handler import add_post_pic
import os

blog_posts = Blueprint('blog_posts', __name__)


@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = BlogPostForm()
    if form.validate_on_submit():
        if form.picture.data:
            title = form.title.data
            pic = add_post_pic(form.picture.data, title)
            # BlogPost.post_image = pic

            blog_post = BlogPost(title=form.title.data,
                             text=form.text.data,
                             user_id=current_user.id,
                             post_image=pic)
            db.session.add(blog_post)
            db.session.commit()
            flash('Blog Post Created')
            return redirect(url_for('core.index'))
    post_image = url_for('static', filename='post_pics/' + str(form.picture.label))

    return render_template('create_post.html', form=form, post_image=post_image)



@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', title=blog_post.title,
                           date=blog_post.date, post=blog_post)


@blog_posts.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        pic = add_post_pic(form.picture.data, blog_post.title)
        blog_post.post_image = pic
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Updated')
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
        form.picture.data = blog_post.post_image
    post_image = url_for('static', filename='post_pics/' + str(form.picture.label))
    return render_template('create_post.html', title='Updating', form=form, post_image=post_image)


@blog_posts.route('/<int:blog_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(blog_post_id):

    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)

    db.session.delete(blog_post)
    img = os.path.abspath(os.path.join('flask_blog/static/post_pics/', blog_post.post_image))
    os.remove(img)
    # os.path.join(basedir, 'data.sqlite')

    db.session.commit()
    flash('Blog Post Deleted')
    return redirect(url_for('core.index'))
