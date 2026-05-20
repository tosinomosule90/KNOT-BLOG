from flask import Blueprint, render_template, redirect, url_for, flash, session,request
from .model import RegistrationForm, LoginForm, contentForm, updateForm
from .table import Company,Post,Comment
from .extension import db
import os
from test import save_picture, save_media
from datetime import datetime
from dotenv import load_dotenv
from flask_login import login_user, logout_user, login_required,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_dance.contrib.google import make_google_blueprint, google
load_dotenv()
blueprint=make_google_blueprint(client_id=os.getenv("GOOGLE_CLIENT_ID"), 
                                client_secret=os.getenv('GOOGLE_CLIENT_SECRET'), 
                                redirect_url="/google_login")

company = Blueprint("company", __name__)
company.register_blueprint(blueprint, url_prefix="/google")

@company.route("/", methods=["GET", "POST"])
@company.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()

    if form.validate_on_submit():
        
        if form.picture.data:
            
            pic_file = save_picture(form.picture.data)
        else:
            pic_file = 'default.jpg'
        
        
        hashed_password = generate_password_hash(form.password.data)

        user = Company(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        

        if user.query.filter_by(email=form.email.data).first():
            flash('EMAIL ALREADY EXIST')
        else:

            db.session.add(user)
            db.session.commit()

        
            return redirect(url_for("company.dashboard"))
    image_file=url_for('static',filename='profile_pics/default.jpg')

    return render_template("home.html", form=form,error=form.errors,image_file=image_file)


@company.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Company.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            session['name']=user.username
            login_user(user)
            return redirect(url_for("company.welcome"))

        flash("Invalid email or password")

    return render_template("login.html", form=form, error=form.errors)

@company.route("/dashboard",methods=['GET','POST'])
@login_required
def dashboard():
    page=request.args.get('page', 1, type=int)
    posts=Post.query.order_by(Post.date.desc()).paginate(page=page,per_page=5)
    search_query=request.args.get('search')
    if search_query:
        posts=Post.query.filter(Post.content.ilike(f'%{search_query}%')).order_by(Post.date.desc()).paginate(page=page,per_page=5)
        if not posts.items:
            flash("No posts found matching your search.", "info")
    else:
        posts=Post.query.order_by(Post.date.desc()).paginate(page=page,per_page=5)
    form=contentForm()
    if form.validate_on_submit():
        # handle image upload
        img_fn = None
        if form.image.data:
            img_fn = save_media(form.image.data, 'post_images')
            
        # Handle Video Upload
        vid_fn = None
        if form.video.data:
            vid_fn = save_media(form.video.data, 'post_videos')
        new_post=Post(content=form.content.data
                          ,user_id=current_user.id
                          ,date=None,image_file=img_fn
                          ,video_file=vid_fn)
            
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('company.dashboard'))
    
    image_file=url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template("base.html",current_user=current_user,form=form,
                           display=posts,current_year=datetime.now().year,
                           image_file=image_file, search_query=search_query)

@company.route("/google_login")
def google_login():
    if not google.authorized:
        return redirect(url_for("company.google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    if resp.ok:
        user_info = resp.json()
        email = user_info["email"]

        user = Company.query.filter_by(email=email).first()
        if not user:
            user = Company(username=email.split("@")[0], email=email, password="")
            db.session.add(user)
            db.session.commit()

        login_user(user)
        return redirect(url_for("company.dashboard"))

#-----------DELETE ALL POSTS ROUTE------------------ 
@company.route("/wipe-posts")
@login_required
def wipe_posts():
    all_posts = Post.query.all()
    for post in all_posts:
        db.session.delete(post)
    db.session.commit()
    flash('All posts and associated comments have been wiped.', 'warning')
    return redirect(url_for('company.dashboard'))
# --------------UPDATE POST ROUTE------------------
@company.route("/update-post/<int:post_id>", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post_to_update = Post.query.get_or_404(post_id)
    
    # SECURITY BUG FIX: Prevent users from editing posts they don't own
    if post_to_update.author != current_user:
        flash("You do not have permission to edit this post.", "danger")
        return redirect(url_for('company.dashboard'))

    form = contentForm()

    if form.validate_on_submit():
        # Update text
        post_to_update.content = form.content.data
        
        # MEDIA UPDATE LOGIC:
        # If the user uploads a NEW image, save it and update the database
        if form.image.data:
            img_fn = save_media(form.image.data, 'post_images')
            post_to_update.image_file = img_fn
            
        if form.video.data:
            vid_fn = save_media(form.video.data, 'post_videos')
            post_to_update.video_file = vid_fn

        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for('company.dashboard'))

    # Pre-populate the form with existing data
    elif request.method == 'GET':
        form.content.data = post_to_update.content

    return render_template("update.html", form=form, post=post_to_update)

# ------------------------DELETE POST ROUTE------------------#

@company.route("/delete-post/<int:post_id>")
@login_required
def delete_post(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    
    # Security: Ensure the user owns the post
    if post_to_delete.user_id != current_user.id:
        flash("You cannot delete someone else's post!")
        return redirect(url_for('company.dashboard'))
    
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Post deleted successfully.")
    except Exception as e:
        db.session.rollback()
        flash("There was an error deleting that post.")
        
    return redirect(url_for('company.dashboard'))


# ===============================
# LOGOUT ROUTE
# ===============================
@company.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("company.login"))

# ===============================
# profile account route
# ===============================
@company.route("/account")
@login_required
def account():
     
     image_file=url_for('static',filename='profile_pics/'+current_user.image_file)
     return render_template("profile.html",image_file=image_file,
                            current_user=current_user)

# ===============================
# UPDATE ACCOUNT ROUTE
# ===============================
@company.route("/update-account",methods=['GET','POST'])
@login_required
def update_account():
     form=updateForm()
     if form.validate_on_submit():
          if form.picture.data:
            # Call our helper function
            picture_file = save_picture(form.picture.data,old_picture=current_user.image_file)
            current_user.image_file = picture_file
          current_user.username=form.username.data
          current_user.email=form.email.data

          if form.change_password.data:
                 current_user.password=generate_password_hash(form.change_password.data)

          db.session.commit()
          flash('Your profile has been updated!', 'success')
          return redirect(url_for('company.account'))
     elif request.method == 'GET':
          form.username.data=current_user.username
          form.email.data=current_user.email

     image_file=url_for('static',filename='profile_pics/'+current_user.image_file)
     
     return render_template("updateProfile.html",form=form,
                            current_user=current_user,
                            error=form.errors,image_file=image_file)

@company.route('/like/<int:post_id>')
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user in post.likers:
        post.likers.remove(current_user) # Unlike if already liked
    else:
        post.likers.append(current_user)
    db.session.commit()
    return redirect(request.referrer)

@company.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    body = request.form.get('comment_body')
    if body:
        comment = Comment(body=body, user_id=current_user.id, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment posted!', 'success')
    return redirect(request.referrer)

@company.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')

@company.route('/community')
@login_required
def community():
    image_file=url_for('static',filename='profile_pics/'+current_user.image_file)
    companys = Company.query.all()
    return render_template('community.html', companys=companys, image_file=image_file,current_user=current_user)

@company.route('/profile/<string:username>')
@login_required
def profile(username):
    # Fetch the user whose profile is being viewed
    user = Company.query.filter_by(username=username).first_or_404()
    
    # Get their posts, ordered by newest first
    # This assumes your 'posts' relationship is defined in the Company model
    posts = Post.query.filter_by(author=user).order_by(Post.date.desc()).all()
    
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    
    return render_template('profile_view.html', 
                           user=user, 
                           posts=posts, 
                           image_file=image_file)


# ================================
# CREATE NEW POST ROUTE
#==================================
@company.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = contentForm()
    if form.validate_on_submit():
        img_fn = save_media(form.image.data, 'post_images') if form.image.data else None
        vid_fn = save_media(form.video.data, 'post_videos') if form.video.data else None
        
        post = Post(content=form.content.data, 
                    author=current_user, 
                    image_file=img_fn, 
                    video_file=vid_fn)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('company.dashboard'))
    return render_template('create_post.html', form=form)