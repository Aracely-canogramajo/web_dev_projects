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
from .models import get_user_email, get_user_name, get_user, get_username

from py4web.utils.url_signer import URLSigner
from .models import get_user_email
from py4web.utils.form import Form, FormStyleBulma
from .common import Field
from operator import itemgetter



url_signer = URLSigner(session)
#---------------------------

# @unauthenticated("index", "index.html")
@action('index/<username>')
@action('index/')
@action.uses(db, auth, auth.user, 'index.html')
def index(username=get_username()):
    current_user = auth.get_user()
    message = T("Hello, {first_name}!".format(**current_user) if current_user else "Hello")

    print(username)
    if username is None:
        username=get_username()
    assert username is not None
    query = db(db.auth_user.username == username).select() #query auth_user
    query3 = db((db.follow.followee == get_user())).select() #query followers

    if not len(query3) > 0:
        print("user not in database")
        if username == get_username():
            db.profile.insert(user=get_user())
            query3 = db((db.follow.followee == get_user())).select()
    try:
        current_user = {'username': query[0]['username'], 'first_name': query[0]['first_name'],
                    'last_name': query[0]['last_name'], 'id': query[0]['id'], 'bio': query3[0]['bio'],
                    'private_acc': query3[0]['private_acc'], 'featured_playlist': query3[0]['featured_playlist'],
                    'featured_song': query3[0]['featured_song'], 'dark_mode': query3[0]['dark_mode']}
    except:
        current_user = {'username': query[0]['username'], 'first_name': query[0]['first_name'],
                        'last_name': query[0]['last_name'], 'id': query[0]['id'], 'bio': "This account has not yet been set up",
                        'private_acc': 'true', 'featured_playlist': -1,
                        'featured_song': -1, 'dark_mode': 'false'}

    #check following status
    following = "false"
    following_query = db((db.follow.followee == current_user['id']) &
                   (db.follow.follower == get_user())).select().as_list()
    if len(following_query) > 0:
        print("in index: user is following")
        following = "true"
    
    # portion is for liked song section of profile
    songs = db(db.song.user == get_user()).select()
    print(songs)
    for s in songs:
        print(s.id)


    return dict(current_user=current_user,
                get_feed_url = URL('get_feed'),
                follower_feed_url = URL('follower_feed'), ## new
                add_post_url = URL('add_post', signer=url_signer),
                delete_post_url = URL('delete_post', signer=url_signer),
                like_post_url=URL('like_post', signer=url_signer),

                get_replies_url=URL('get_replies', signer=url_signer),
                delete_repost_url = URL('delete_post', signer=url_signer),
                get_liked_url=URL('get_song', signer=url_signer),
                follow_url = URL('follow', signer=url_signer),
                unfollow_url = URL('unfollow', signer=url_signer),
                
                username=username, 
                following_string=following,
                logged_in_user=get_username(), message=message)    
# def index(username=get_username()):
#     print("in index: ", username)
    
#     current_user = auth.get_user()
#     message = T("Hello, {first_name}!".format(**current_user) if current_user else "Hello")
    
    
#     print(username)
#     if username is None:
#         username=get_username()
#     assert username is not None
#     query = db(db.auth_user.username == username).select() #query auth_user
#     query2 = db(db.profile.user == query[0]['id']).select() #query profile

#     #checks if user is in profile table else ads it
#     if not len(query2) > 0:
#         print("user not in database")
#         if username == get_username():
#             db.profile.insert(user=get_user())
#             query2 = db(db.profile.user == query[0]['id']).select()

#     try :
#         current_user = {'username': query[0]['username'], 'first_name': query[0]['first_name'],
#                     'last_name': query[0]['last_name'], 'id': query[0]['id'], 'bio': query2[0]['bio'],
#                     'private_acc': query2[0]['private_acc'], 'featured_playlist': query2[0]['featured_playlist'],
#                     'featured_song': query2[0]['featured_song'], 'dark_mode': query2[0]['dark_mode']}
#     except:
#         current_user = {'username': query[0]['username'], 'first_name': query[0]['first_name'],
#                         'last_name': query[0]['last_name'], 'id': query[0]['id'], 'bio': "This account has not yet been set up",
#                         'private_acc': 'true', 'featured_playlist': -1,
#                         'featured_song': -1, 'dark_mode': 'false'}

#     #check following status
#     following = "false"
#     following_query = db((db.follow.followee == current_user['id']) &
#                    (db.follow.follower == get_user())).select().as_list()
#     if len(following_query) > 0:
#         print("user is following")
#         following = "true"
#     return dict(current_user=current_user,
#                 get_feed_url = URL('get_feed'),
#                 follower_feed_url = URL('follower_feed_url'), ## new
#                 add_post_url = URL('add_post', signer=url_signer),
#                 delete_post_url = URL('delete_post', signer=url_signer),
#                 like_post_url=URL('like_post', signer=url_signer),

#                 get_replies_url=URL('get_replies', signer=url_signer),
#                 delete_repost_url = URL('delete_post', signer=url_signer),
#                 get_liked_url=URL('get_song', signer=url_signer),
#                 follow_url = URL('follow', signer=url_signer),
#                 unfollow_url = URL('unfollow', signer=url_signer),
                
#                 username=username, 
#                 following_string=following,
#                 logged_in_user=get_username(), message=message)
#        return dict(message=message)



@action('songpage')
@action.uses(db, auth, auth.user, 'songpage.html')
def song_page():
    print("here")
    songs = db(db.song.user == get_user()).select()
    name = get_username()
    return dict(songs=songs, name=name,upload_song_pic_url = URL('song_pic', signer=url_signer))



@action('directory')
@action.uses(db, auth, auth.user, 'directory.html')
def directory():
    rows = db(db.auth_user).select()

    for user in rows:
        user["fullname"] = user.first_name + " " + user.last_name
    return dict(rows=rows,
                follow_url = URL('follow', signer=url_signer),
                unfollow_url = URL('unfollow', signer=url_signer),
                get_directory_url = URL('get_directory', signer=url_signer),
                )

@action('get_directory')
@action.uses(db, auth, auth.user, url_signer.verify())
def get_directory():
    users = db(db.auth_user).select()
    users_to_return = []

    for user in users:
        user['fullname'] = user.first_name + " " + user.last_name
        following = db((db.follow.followee == user.id) &
                       (db.follow.follower == get_user())).select()
        if len(following) > 0:
            user['following'] = True
        else:
            user['following'] = False
        user['profile_url'] = URL('profile', user.username)
        users_to_return.append({'username': user.username, 'fullname': user.fullname, 'following': user.following, 'profile_url': user.profile_url})
    return(dict(users=users_to_return))


@action('edit_song/<song_id:int>',method=["GET","POST"])
@action.uses(db, auth, auth.user, 'edit_song.html')
def edit_song(song_id=None):
    assert song_id is not None
    s = db.song[song_id]
    song_name = s.song_name

    if s is None or get_user() != s.user:
        redirect(URL('songpage'))

    form = Form(db.song, record=s, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('songpage'))

    return dict(form=form,song_name=song_name)


@action('profile/<username>')
@action('profile/')
@action.uses(db, auth, auth.user, 'profile.html')
def profile(username=get_username()):
    print(username)
    if username is None:
        username=get_username()
    assert username is not None
    query = db(db.auth_user.username == username).select() #query auth_user
    query2 = db(db.profile.user == query[0]['id']).select() #query profile

    #checks if user is in profile table else ads it
    if not len(query2) > 0:
        print("user not in database")
        if username == get_username():
            db.profile.insert(user=get_user())
            query2 = db(db.profile.user == query[0]['id']).select()

    try :
        current_user = {'username': query[0]['username'], 'first_name': query[0]['first_name'],
                    'last_name': query[0]['last_name'], 'id': query[0]['id'], 'bio': query2[0]['bio'],
                    'private_acc': query2[0]['private_acc'], 'featured_playlist': query2[0]['featured_playlist'],
                    'featured_song': query2[0]['featured_song'], 'dark_mode': query2[0]['dark_mode']}
    except:
        current_user = {'username': query[0]['username'], 'first_name': query[0]['first_name'],
                        'last_name': query[0]['last_name'], 'id': query[0]['id'], 'bio': "This account has not yet been set up",
                        'private_acc': 'true', 'featured_playlist': -1,
                        'featured_song': -1, 'dark_mode': 'false'}

    #check following status
    following = "false"
    following_query = db((db.follow.followee == current_user['id']) &
                   (db.follow.follower == get_user())).select().as_list()
    if len(following_query) > 0:
        print("user is following")
        following = "true"

    # --- portion is for liked_songs section of profile
    songs = db(db.song.user == get_user()).select()
    print(songs)


    #--- portion for profile picture ------
    person = db.profile[current_user['id']]
    print("this is the profile pic")
    #print(person.profile_pic)

    # --- this portion is for the playlist
    playlist = db(db.playlist.username == get_username()).select()
    song_list = db(db.songinplaylist.user == get_user()).select().as_list()





    #------------------------------------
    return dict(current_user=current_user, #user of the profile
                get_feed_url = URL('get_feed'),
                add_post_url = URL('add_post', signer=url_signer),
                delete_post_url = URL('delete_post', signer=url_signer),
                delete_repost_url = URL('delete_repost', signer=url_signer),
                like_post_url = URL('like_post', signer=url_signer),
                get_replies_url = URL('get_replies', signer=url_signer),
                update_bio_url=URL('update_bio', signer=url_signer),
                get_liked_url = URL('get_song'),
                follow_url = URL('follow', signer=url_signer),
                unfollow_url = URL('unfollow', signer=url_signer),
                upload_profile_pic_url =URL('upload_profile_pic',signer=url_signer),
                get_p_url = URL('profile_get_playlist',signer=url_signer),
                username=username, logged_in_user=get_username(),
                following_string=following,
                songs =songs,
                person = person,
                playlist=playlist,
                song_list=song_list,
                )

@action('profile_get_playlist')
@action.uses(db)
def get_playlist():
    print("in the playlist")
    playlist = db(db.playlist.creator == get_user()).select()
    song_list = db(db.songinplaylist.user == get_user()).select()

    print("HEEEEEEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRRRE")
    for s in song_list:
        print(s.name_song)
    return dict(playlist=playlist,song_list=song_list)

@action('follower_feed')
@action.uses(db)
def follower_feed():
    print("in follower_feed")
    all_posts = []
    username = request.params.get('username')
    print(username)
    assert username is not None 
    following = db((db.follow.follower == get_user())).select()
    ######################################################################
    users = db(db.auth_user.username == username).select() # 
    for user in users:
        id = user['id']
        name = user['first_name'] + " " + user['last_name']
        username = user['username']
    posts = db(db.post.author == id).select().as_list()
    feed = []
    for post in posts:
        post['is_repost'] = False
        #if repost, swap info with original post
        if post['content'] is None and post['quoted_post'] is not None:
            print("swapping post")
            post = db(db.post.id == post['quoted_post']).select().as_list()[0]
            post['is_repost'] = True
        author = db(db.auth_user.id == post['author']).select()[0]
        post['name'] = author['first_name'] + " " + author['last_name']
        post['username'] = author['username']
        post['liked'] = False
        post['reposted'] = False
        post['show_replies'] = False
        post['replies'] = []
        if get_user() is not None:
            if get_user() is post['author']:
                post['is_author'] = True
            liked = db((db.postlikes.user == get_user()) &
                        (db.postlikes.post == post['id'])).select()
            reposted = db((db.post.author == get_user()) &
                          (db.post.quoted_post == post['id']) &
                          (db.post.content == None)).select()
            if len(liked) is not 0:
                post['liked'] = True
            if len(reposted) is not 0:
                post['reposted'] = True
        post['quoted_name'] = ""
        if post['quoted_post'] is not None:
            quoted_post = db(db.post.id == post['quoted_post']).select()[0]
            quoted_user = db(db.auth_user.id == quoted_post['author']).select()[0]
            post['quoted_name'] = quoted_user['first_name'] + " " + quoted_user['last_name']
        all_posts.append(post)
    ######################################################################   

    print("this is following", db((db.follow.follower == get_user())).select())
    for user in following:
        id = user['followee']
        print("this is id", id)
        user_posts = db(db.post.author == id).select().as_list()
        print("this is user_posts")
        for post in user_posts:
            print(post)
            if post['content'] is None and post['quoted_post'] is not None: 
                post = db(db.post.id == post['quoted_post']).select().as_list()[0]
                post['is_repost'] =  True
            author = db(db.auth_user.id == post['author']).select()[0]
            post['name'] = author['first_name'] + " " + author['last_name']
            post['username'] = author['username']
            post['liked'] = False
            post['reposted'] = False
            post['show_replies'] = False
            post['replies'] = []
            if get_user() is not None:
                if get_user() is post['author']:
                    post['is_author'] = True
                liked  = db((db.postlikes.user==get_user()) &
                            (db.postlikes.post == post['id'])).select()
                reposted = db((db.post.author == get_user()) & 
                            (db.post.quoted_post==post['id']) & 
                            (db.post.content == None)).select()
                if len(liked) is not 0:
                    post['liked'] = True 
                if len(reposted) is not 0:
                    post['reposted'] = True 
            post['quoted_name'] = ""
            if post['quoted_post'] is not None:
                quoted_post = db(db.post.id == post['quoted_post']).select()[0]
                quoted_user = db(db.auth_user.id == quoted_post['author']).select()[0]
                post['quoted_name'] = quoted_user['first_name'] + " " + quoted_user['last_name']
            all_posts.append(post)
    
    all_posts_sorted = sorted(all_posts, key=itemgetter('time'))
    print("end of follower feed")
    print(all_posts_sorted)
    return dict(all_posts_sorted=all_posts_sorted, get_feed_url = URL('get_feed'),)


@action('get_feed')
@action.uses(db)
def get_feed():
    username = request.params.get('username')
    print(username)
    assert username is not None
    users = db(db.auth_user.username == username).select()
    for user in users:
        id = user['id']
        name = user['first_name'] + " " + user['last_name']
        username = user['username']
    posts = db(db.post.author == id).select().as_list()
    feed = []
    for post in posts:
        post['is_repost'] = False
        #if repost, swap info with original post
        if post['content'] is None and post['quoted_post'] is not None:
            print("swapping post")
            post = db(db.post.id == post['quoted_post']).select().as_list()[0]
            post['is_repost'] = True
        author = db(db.auth_user.id == post['author']).select()[0]
        post['name'] = author['first_name'] + " " + author['last_name']
        post['username'] = author['username']
        post['liked'] = False
        post['reposted'] = False
        post['show_replies'] = False
        post['replies'] = []
        if get_user() is not None:
            if get_user() is post['author']:
                post['is_author'] = True
            liked = db((db.postlikes.user == get_user()) &
                        (db.postlikes.post == post['id'])).select()
            reposted = db((db.post.author == get_user()) &
                          (db.post.quoted_post == post['id']) &
                          (db.post.content == None)).select()
            if len(liked) is not 0:
                post['liked'] = True
            if len(reposted) is not 0:
                post['reposted'] = True
        post['quoted_name'] = ""
        if post['quoted_post'] is not None:
            quoted_post = db(db.post.id == post['quoted_post']).select()[0]
            quoted_user = db(db.auth_user.id == quoted_post['author']).select()[0]
            post['quoted_name'] = quoted_user['first_name'] + " " + quoted_user['last_name']
        feed.append(post)
    return dict(feed=feed)

@action('add_post', method="POST")
@action.uses(url_signer.verify(), db)
def add_post():
    quoted_post = request.json.get('quoted_post')
    print(quoted_post)
    quoted_name=""
    if quoted_post is not None: #replies or reposts
        print("quoted post is not none")
        if request.json.get('content') is not None: #reply
            print("post is reply")
            post = db(db.post.id == quoted_post).select().as_list()
            db.post.update_or_insert((db.post.id == quoted_post), num_replies=post[0]['num_replies'] + 1)
        else:
            print("post is repost")
            #check that repost doesn't already exist
            repost = db( (db.post.quoted_post == quoted_post) &
                         (db.post.author == get_user() &
                         (db.post.content == None))).select().as_list()
            if len(repost) > 0:
                print(repost)
                print("already posted")
                return dict()
            post = db(db.post.id == quoted_post).select().as_list()
            db.post.update_or_insert((db.post.id == quoted_post), num_reposts=post[0]['num_reposts'] + 1)
        # get the name of the author of the quoted post
        quoted_author = db(db.auth_user.id == post[0]['author']).select().as_list()[0]
        quoted_name = quoted_author['first_name'] + " " + quoted_author['last_name']
    id = db.post.insert(
        content=request.json.get('content'), quoted_post=quoted_post,
    )
    post = db(db.post.id == id).select().as_list()
    time = post[0]['time']
    name = get_user_name()
    return dict(id=id, author=get_user(), quoted_name=quoted_name, name=get_user_name(), username=get_username(), time=time)

@action('like_post')
@action.uses(url_signer.verify(), db)
def like_post():
    id = request.params.get('id')
    liked = int(request.params.get('liked'))
    assert id is not None
    assert liked is not None
    if liked == 0:
        db((db.postlikes.post == id) & (db.postlikes.user == get_user())).delete()
        post = db(db.post.id == id).select().as_list()
        if len(post) > 0:
            db.post.update_or_insert((db.post.id == id), num_likes=post[0]['num_likes']-1)
    else:
        db.postlikes.update_or_insert((db.postlikes.post == id) & (db.postlikes.user == get_user()), post=id, user=get_user())
        post = db(db.post.id == id).select().as_list()
        if len(post) > 0:
            db.post.update_or_insert((db.post.id == id), num_likes=post[0]['num_likes']+1)
    return id

@action('delete_post')
@action.uses(url_signer.verify(), db)
def delete_post():
    id = request.params.get('id')
    quoted_post = db(db.post.id == id).select()[0]['quoted_post']
    if quoted_post is not None:
        post = db(db.post.id == quoted_post).select().as_list()
        db.post.update_or_insert((db.post.id == quoted_post), num_replies=post[0]['num_replies'] - 1)
    assert id is not None
    db((db.post.id == id) & (db.post.author == get_user())).delete()
    return "ok"

@action('delete_repost')
@action.uses(url_signer.verify(), db)
def delete_repost():
    #decrease num reposts of reposted post
    id = request.params.get('id')
    post = db(db.post.id == id).select().as_list()
    db.post.update_or_insert((db.post.id == id), num_reposts=post[0]['num_reposts'] - 1)

    #find the id of the repost
    repostid = db((db.post.author == get_user()) &
                          (db.post.quoted_post == id) &
                          (db.post.content == None)).select()[0]['id']
    print("repost = " + str(repostid))

    #delete the repost
    db((db.post.author == get_user()) &
       (db.post.quoted_post == id) &
       (db.post.content == None)).delete()

    return dict(repostid=repostid)

@action('get_replies')
@action.uses(url_signer.verify(), db)
def get_replies():
    id = request.params.get('id')
    replies = db((db.post.quoted_post == id) & (db.post.content != None)).select().as_list()
    for reply in replies:
        user = db(db.auth_user.id == reply['author']).select()
        reply['name'] = user[0]['first_name'] + " " + user[0]['last_name']
        reply['username'] = user[0]['username']
        reply['liked'] = False
        if get_user() is not None:
            if get_user() is reply['author']:
                reply['is_author'] = True
            liked = db((db.postlikes.user == get_user()) &
                        (db.postlikes.post == reply['id'])).select()
            if len(liked) is not 0:
                reply['liked'] = True

    return(dict(replies=replies))

@action('playlist_page/<username>')
@action('playlist_page/')
@action.uses(db, auth, auth.user, 'playlist_page.html')
def playlist_page():
    message = "playlist page"
    username=get_username()
    if username is None:
        username=get_username()
    assert username is not None
    
    return dict(message=message, username=username,
     add_playlist_url = URL('add_playlist', signer=url_signer),
     get_playlists_url = URL('get_playlists', signer=url_signer),
     get_all_songs_url = URL('get_all_songs', signer=url_signer),
     add_songinplaylist_url = URL('add_songinplaylist', signer=url_signer),
     get_songsinplay_url = URL('get_songsinplay', signer=url_signer),
     )

@action('upload_page/<username>') #for upload_page.html
@action('upload_page/')
@action.uses(db, auth, auth.user, 'upload_page.html')
def upload_page():
    message = "upload page"
    return dict(message=message,
                add_song_url = URL('add_song', signer=url_signer),)

@action('add_song', method="POST") # function to add songs in upload_page.html
@action.uses(url_signer.verify(), db)
def add_song():
    k = auth.get_user();
    username = k["username"];
    id = db.song.insert(
        song_name=request.json.get('song_name'),
        album=request.json.get('album'),
        artist=request.json.get('artist'),
        num_likes=0,
        num_plays=0,
        num_reposts=0,
        file_location="NaN",
        art_location="NaN",
        username=username,
    )
    return dict(id=id)

@action('add_songinplaylist', method="POST") #update the song db to include in a playlist
@action.uses(url_signer.verify(), db)
def add_songinplaylist():
    song_id = request.json.get('song_id')
    playlist_id = request.json.get('playlist')
    song = request.json.get('song_name')
    name = db(db.song.id == song_id).select().first()

    names = name.song_name
    id = db.songinplaylist.insert(
        song_name=song_id,
        playlist_in=playlist_id,
        user=get_user(),
        name_song=name.song_name,
        song_play_id=playlist_id

    )

    return dict(id=id)
    
@action('get_songsinplay', method="POST")
@action.uses(url_signer.verify(), db)
def get_songsinplay():
    playlist_id = request.json.get('playlist_id')
    songs = db(db.songinplaylist.playlist_in == playlist_id).select().as_list();
    x = "";
    slist = []
    for s in songs:
        ara = db(db.song.id == s['song_name']).select().as_list();
        song_name = ara[0]["song_name"];
        song_artist = ara[0]["artist"];
        song_album = ara[0]["album"];
        x = song_name + "    " + song_artist + "    " + song_album;
        slist.append(x)
    return dict(songs=slist)

@action('add_playlist', method="POST") # function to add new playlist in playlist_page.html
@action.uses(url_signer.verify(), db)
def add_playlist():
    k = auth.get_user();
    username = k["username"];
    id = db.playlist.insert(
        playlist_name=request.json.get('playlist_name'),
        bio=request.json.get('bio'),
        num_likes=0,
        num_plays=0,
        num_reposts=0,
        username=username,
    )
    return dict(id=id, username=username,)

@action('get_playlists') # function to get all the playlists
@action.uses(url_signer.verify(), db)
def load_posts():
    """Returns the list of posts."""
    playlist = db(db.playlist.creator == get_user()).select().as_list()
    return dict(playlists=playlist)

@action('get_all_songs')
@action.uses(url_signer.verify(), db)
def load_songs(): # return the list of all the songs
    return dict(songs=db(db.song).select(orderby=~db.song.id).as_list())
    

@action('post/<postid:int>')
@action.uses(db, 'post.html')
def post(postid=0):
    return dict(postid=postid,
                get_post_url = URL('get_post', signer=url_signer),
                add_post_url = URL('add_post', signer=url_signer),
                delete_post_url=URL('delete_post', signer=url_signer),
                like_post_url=URL('like_post', signer=url_signer),
                get_replies_url=URL('get_replies', signer=url_signer),
                logged_in_user=get_username(),
                )

@action('get_post')
@action.uses(url_signer.verify(), db)
def get_post():
    postid = int(request.params.get('postid'))

    if postid > 0:
        post = db(db.post.id == postid).select().as_list()[0]
        user = db(db.auth_user.id == post['author']).select()[0]
        post['name'] = user['first_name'] + " " + user['last_name']
        post['username'] = user['username']
        post['liked'] = False
        post['show_replies'] = False
        post['replies'] = []
        if get_user() is not None:
            if get_user() is user['id']:
                post['is_author'] = True
            liked = db((db.postlikes.user == get_user()) &
                       (db.postlikes.post == post['id'])).select()
            if len(liked) is not 0:
                post['liked'] = True
        post['quoted_name'] = ""
        if post['quoted_post'] is not None:
            quoted_post = db(db.post.id == post['quoted_post']).select()[0]
            quoted_user = db(db.auth_user.id == quoted_post['author']).select()[0]
            post['quoted_name'] = quoted_user['first_name'] + " " + quoted_user['last_name']
    return(dict(post=post))

@action('get_song')
@action.uses(db)
def get_song():
    rows = ['bob','mary','june','barbara','kathy','jones']

    return dict( rows=rows )

@action('follow', method="POST")
@action.uses(url_signer.verify(), db)
def follow():
    username = request.json.get('username')
    print(username)
    user = db(db.auth_user.username == username).select().as_list()
    print(user)
    if len(user) > 0:
        followee = user[0]['id']
        db.follow.insert(follower=get_user(), followee=followee)
        return "ok"
    return "user not found"

@action('unfollow', method="POST")
@action.uses(url_signer.verify(), db)
def unfollow():
    username = request.json.get('username')
    user = db(db.auth_user.username == username).select().as_list()
    if len(user) > 0:
        followee = user[0]['id']
        db((db.follow.followee == followee) &
           (db.follow.follower == get_user())).delete()
        return "ok"
    return "user not found"

@action('update_bio', method="POST")
@action.uses(url_signer.verify(), db)
def update_bio():
    user = get_user()
    new_bio = request.json.get('new_bio')
    print("updating bio: " + str(user) + " " + new_bio)
    db.profile.update_or_insert((db.profile.user == user), bio=new_bio)
    return "ok"



@action('upload_profile_pic', method="POST")
@action.uses(url_signer.verify(), db)
def upload_thumbnail():
    print("in the upload")
    picture = request.json.get("profile_pic")
    user = get_user()
    db.profile.update_or_insert((db.profile.id == user), profile_pic = picture)
    pict = db.profile[get_user()]



    return "ok"


@action('song_pic', method="POST")
@action.uses(url_signer.verify(), db)
def song_pic():
    print("im here")
    song_id = request.json.get("song_id")
    thumbnail = request.json.get("thumbnail")
    db.profile.update_or_insert((db.song.id == song_id), song_pic=thumbnail)
    return "ok"