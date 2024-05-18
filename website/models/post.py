from website.db_config.firebase import db, bucket
from google.cloud import firestore
import time as Time

post_ref = db.collection('posts')

def create_post(post, thumbnail, user_id):
    try:
        if thumbnail is not None:
            thumbnail_saved = save_image(thumbnail)
            if thumbnail_saved is not None:
                post['thumbnail'] = thumbnail_saved

        post['posted_by'] = db.collection('users').document(user_id)
                
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
    
def get_sorted_posts(post_id_start, limit : int = 10, user_id: str = None, owner_id: str = None):
    try:
        # Fetch all posts after the post_id_start and decending order by timestamp
        all_posts = []
        if (owner_id != None):
            post_ref = db.collection('posts').where('posted_by', '==', db.collection('users').document(owner_id)).order_by('created_at', direction=firestore.Query.DESCENDING).limit(limit)
        else:
            post_ref = db.collection('posts').order_by('created_at', direction=firestore.Query.DESCENDING).limit(limit)
        for post in post_ref.stream():
            if 'liked_by' not in post.to_dict():
                post.to_dict()['liked_by'] = []
                print(post.to_dict())
            if 'posted_by' not in post.to_dict():
                continue
            post_data = post.to_dict()
            post_data['id'] = post.id
            post_data['posted_by'] = post.to_dict()['posted_by'].get().to_dict()
            all_posts.append(post_data)

        for post in all_posts:
            if user_id != None and user_id in post['liked_by']:
                post['liked_by_me'] = True
            else:
                post['liked_by_me'] = False

        return all_posts
    except Exception as e:
        return str(e)
    
def get_post(post_id, user_id):
    try:
        post = post_ref.document(post_id).get().to_dict()
        post['id'] = post_id
        post['posted_by'] = post_ref.document(post_id).get().to_dict()['posted_by'].get().to_dict()
        if user_id != None and user_id in post['liked_by']:
            post['liked_by_me'] = True
        else:
            post['liked_by_me'] = False
        return post
    except Exception as e:
        return str(e)

def like_post(post_id, user_id):
    try:
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