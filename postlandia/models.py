"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_user():
    return auth.current_user.get('id') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
db.define_table(
    'posts',
    Field('text'),
    Field('first_name'),
    Field('last_name'),
    Field('email'),
    Field('rating', 'integer', default=0)
)

db.define_table(
    'thumbs',
    Field('post', 'reference posts'), # posts
    Field('rating', 'integer', default=0),
    Field('rater', 'reference auth_user', default=get_user), # User doing the rating.
)

db.define_table(
    'likes',
    Field('post', 'reference posts'),
    Field('likers'),
    Field('dislikers')
)

db.commit()
