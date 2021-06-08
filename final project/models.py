"""
This file defines the database models
"""

from .common import db, Field, auth
from pydal.validators import *
import datetime

def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_user():
    return auth.current_user.get('id') if auth.current_user else None

def get_username():
    return auth.current_user.get('username') if auth.current_user else None

def get_user_name():
    return auth.current_user.get('first_name') + " " + auth.current_user.get('last_name') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
#
# db.commit()
#

db.define_table(
    'playlist',
    Field('creator', 'reference auth_user', default=get_user),
    Field('username'),
    Field('playlist_name'),
    Field('bio'),
    Field('num_plays', 'integer'),
    Field('num_reposts', 'integer'),
    Field('num_likes', 'integer'),
    Field('time_created', default=get_time),
    Field('time_modified', default=get_time),
)

db.define_table(
    'song',
    Field('song_name'),
    Field('artist'),
    Field('album'),
    Field('time_uploaded', default=get_time),
    Field('num_plays', 'integer'),
    Field('num_reposts', 'integer'),
    Field('num_likes', 'integer'),
    Field('file_location'),
    Field('art_location'),
    Field('thumbnail'),
    Field('user','reference auth_user',default=get_user),
    Field('username'),
    Field('song_pic','text'),
)

db.song.time_uploaded.readable = db.song.time_uploaded.writable = False;
db.song.num_plays.readable = db.song.num_plays.writable = False;
db.song.num_reposts.readable = db.song.num_reposts.writable = False;
db.song.num_likes.readable = db.song.num_likes.writable = False;
db.song.file_location.readable = db.song.file_location.writable = False;
db.song.art_location.readable = db.song.art_location.writable = False;
db.song.user.readable = db.song.user.writable = False;
db.song.id.readable = db.song.id.writable = False;
db.song.song_pic.readable = db.song.song_pic.writable = False;

db.define_table(
    'songinplaylist',
    Field('song_name', 'reference song'),
    Field('playlist_in', 'reference playlist'),
    Field('user', 'reference auth_user', default=get_user),
    Field('name_song'),
    Field('song_play_id','integer',default=0)

)


db.define_table(
    'profile',
    Field('user', 'reference auth_user', default=get_user),
    Field('bio', default="This is my first bio"),
    Field('private_acc', 'boolean', default=False),
    Field('featured_playlist', 'reference playlist'),
    Field('featured_song', 'reference song'),
    Field('featured_media', 'integer', default=0), #chooses to display nothing (0), a song (1), or a playlist (2)
    Field('dark_mode', 'boolean', default=False),
    Field('profile_pic','text')

)

db.define_table(
    'post',
    Field('author', 'reference auth_user', default=get_user),
    Field('quoted_post', 'reference post'),
    Field('content'),
    Field('num_likes', 'integer', default=0),
    Field('num_reposts', 'integer', default=0),
    Field('num_replies', 'integer', default=0),
    Field('time', default=get_time),
    Field('embedded_file')
)

db.define_table(
    'postlikes',
    Field('post', 'reference post'),
    Field('user', 'reference auth_user'),
    Field('time', default=get_time),
)

db.define_table(
    'follow',
    Field('follower', 'reference auth_user'),
    Field('followee', 'reference auth_user'),
    Field('time', default=get_time),
)

db.commit()
