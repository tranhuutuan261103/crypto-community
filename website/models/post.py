from website.db_config.firebase import db, bucket
from google.cloud import firestore
import time as Time
from flask_uploads import UploadSet, IMAGES
# Khởi tạo Flask-Uploads
photos = UploadSet('photos', IMAGES)

post_ref = db.collection('posts')

def create_post(post, thumbnail):
    try:
        if thumbnail is not None:
            thumbnail_saved = save_image(thumbnail)
            if thumbnail_saved is not None:
                post['thumbnail'] = thumbnail_saved
                
        post_ref.add(post)
        return True
    except Exception as e:
        return str(e)
    
def save_image(thumbnail):
    try:
        # Upload image to Firebase Storage
        content_type = thumbnail.content_type

        image_url = f"thumbnails in post/{Time.time()}_{thumbnail.filename}"
        blob = bucket.blob(image_url)
        blob.upload_from_file(thumbnail, content_type=content_type)
        blob.make_public()

        return blob.public_url
    except Exception as e:
        print(e)
        return None
    
def get_posts():
    try:
        # Fetch all posts and include the document ID with each post's data
        all_posts = []
        for post in post_ref.stream():
            if 'liked_by' not in post.to_dict():
                post.to_dict()['liked_by'] = []
            if 'posted_by' not in post.to_dict():
                continue
            post_data = post.to_dict()
            post_data['id'] = post.id
            all_posts.append(post_data)
        for post in all_posts:
            if 'user_id' in post['liked_by']:
                post['liked_by_me'] = True
            else:
                post['liked_by_me'] = False

        return all_posts
    except Exception as e:
        return str(e)
    
def get_sorted_posts(post_id_start, limit):
    try:
        # Fetch all posts after the post_id_start and decending order by timestamp
        all_posts = []
        for post in post_ref.order_by('created_at', direction=firestore.Query.DESCENDING).limit(limit).stream():
            if 'liked_by' not in post.to_dict():
                post.to_dict()['liked_by'] = []
                print(post.to_dict())
            if 'posted_by' not in post.to_dict():
                continue
            post_data = post.to_dict()
            post_data['id'] = post.id
            all_posts.append(post_data)

        for post in all_posts:
            if 'user_id' in post['liked_by']:
                post['liked_by_me'] = True
            else:
                post['liked_by_me'] = False

        return all_posts
    except Exception as e:
        return str(e)
    
def get_post(post_id):
    try:
        post = post_ref.document(post_id).get().to_dict()
        post['id'] = post_id
        if 'user_id' in post['liked_by']:
            post['liked_by_me'] = True
        else:
            post['liked_by_me'] = False
        return post
    except Exception as e:
        return str(e)

def like_post(post_id):
    try:
        user_id = 'user_id'
        post = db.collection('posts').document(post_id)
        # Add user ID to the list of users who liked the post
        if user_id not in post.get().to_dict()['liked_by']:
            post.update({u'liked_by': firestore.ArrayUnion([user_id])})
        else:
            post.update({u'liked_by': firestore.ArrayRemove([user_id])})
        return True
    except Exception as e:
        print(e)
        return False