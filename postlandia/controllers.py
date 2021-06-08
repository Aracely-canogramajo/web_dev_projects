"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:
    http://127.0.0.1:8000/{app_name}/{path}
If app_name == '_default' then simply
    http://127.0.0.1:8000/{path}
If path == 'index' it can be omitted:
    http://127.0.0.1:8000/
The path follows the bottlepy syntax.
@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object
session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email
from .models import get_user

url_signer = URLSigner(session)

@action('index')
@action.uses(db, auth.user, 'index.html')
def index():
    return dict(
        # COMPLETE: return here any signed URLs you need.
        my_callback_url = URL('my_callback', signer=url_signer),
        load_posts_url = URL('load_posts', signer=url_signer),
        add_post_url = URL('add_post', signer=url_signer),
        delete_post_url = URL('delete_post', signer=url_signer),
        load_user_url = URL('load_user', signer=url_signer),
        get_rating_url = URL('get_rating', signer=url_signer),
        set_rating_url = URL('set_rating', signer=url_signer),
        get_likers_url = URL('get_likers', signer=url_signer),
        get_dislikers_url = URL('get_dislikers', signer=url_signer),
    )

@action('load_posts')
@action.uses(url_signer.verify(), db)
def load_posts():
    """Returns the list of posts."""
    return dict(posts=db(db.posts).select(orderby=~db.posts.id).as_list())

@action('add_post', method="POST")
@action.uses(url_signer.verify(), db)
def add_post():
    k = auth.get_user();
    first_name = k["first_name"];
    last_name = k["last_name"];
    email = k["email"];
    id = db.posts.insert(
        text=request.json.get('text'),
        first_name=first_name,
        last_name=last_name,
        email=email,
    )
    thumb = db.thumbs.insert(
        post = id,
        rating = 0,
    )
    return dict(id=id, first_name=first_name, last_name=last_name, email=email, rating=0)

@action('delete_post')
@action.uses(url_signer.verify(), db)
def delete_post():
    id = request.params.get('id')
    assert id is not None
    db(db.posts.id == id).delete()
    return "ok"

@action('load_user')
@action.uses(url_signer.verify(), db)
def load_user():
    """Returns the list of posts."""
    user = auth.get_user();
    email = user["email"]
    return dict(email=email)

@action('get_rating')
@action.uses(url_signer.verify(), db, auth.user)
def get_rating():
    post_id = int(request.params.get('post_id'))
    row = db((db.thumbs.post == post_id) & (db.thumbs.rater == get_user())).select().first()
    rating = row.rating if row is not None else 0
    return dict(rating = rating)

@action('set_rating', method="POST")
@action.uses(url_signer.verify(), db, auth.user)
def set_rating():
    post_id = request.json.get('post_id')
    rating = int(request.json.get('rating'))
    db.thumbs.update_or_insert(
        (db.thumbs.post == post_id) & (db.thumbs.rater==get_user()),
        post=post_id,
        rater=get_user(),
        rating=rating,
    )
    return dict(rating=rating)

@action('get_likers', method="POST")
@action.uses(url_signer.verify(), db, auth.user)
def set_rating():
    post_id = int(request.json.get('post_id'))
    row = db((db.thumbs.post == post_id) & (db.thumbs.rating == 1)).select().as_list();
    s = "Liked by ";
    for r in row: 
        temp = r['rater']
        y = db(db.thumbs.rater == temp).select().as_list();
        rater = y[0]['rater'];
        z = db(db.auth_user.id == rater).select().as_list();
        s = s + z[0]['first_name'] + " " + z[0]['last_name'] + " ";
    if s == "Liked by ":
        s = ""
    return dict(s=s)

@action('get_dislikers', method="POST")
@action.uses(url_signer.verify(), db, auth.user)
def set_rating():
    post_id = int(request.json.get('post_id'))
    row = db((db.thumbs.post == post_id) & (db.thumbs.rating == -1)).select().as_list();
    s = "Disliked by ";
    for r in row: 
        temp = r['rater']
        y = db(db.thumbs.rater == temp).select().as_list();
        rater = y[0]['rater'];
        z = db(db.auth_user.id == rater).select().as_list();
        s = s + z[0]['first_name'] + " " + z[0]['last_name'] + " ";
    if s == "Disliked by ":
        s = ""
    return dict(s=s)
