from website.db_config.firebase import db
from google.cloud import firestore
from datetime import datetime

comments_ref = db.collection('comments')

def get_comments(post_id):
    try:
        # Fetch all comments for the post_id
        all_comments = []
        for comment in comments_ref.where('post_id', '==', post_id).stream():
            comment_data = comment.to_dict()
            comment_data['id'] = comment.id

            if 'liked_by' not in comment.to_dict():
                comment_data['liked_by'] = []
            if 'user_id' in comment_data['liked_by']:
                comment_data['liked_by_me'] = True
            else:
                comment_data['liked_by_me'] = False

            all_comments.append(comment_data)
        return all_comments
    except Exception as e:
        print(str(e))
        return []
    
def add_comment(post_id, user_id, parent_id, content):
    try:
        # Add a new comment to the post_id
        comments_ref.add({
            'parent_comment_id': parent_id,
            'post_id': post_id,
            'commented_by': {
                'user_id': user_id,
                'name': 'User Name',
                'avatar': 'https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50?s=200'
            },
            'content': content,
            'liked_by': [],
            'created_at': datetime.now()
        })
        return True
    except Exception as e:
        print(str(e))
        return False
    
def like_comment(comment_id, user_id):
    try:
        user_id = 'user_id'
        comment = comments_ref.document(comment_id)
        # Add user ID to the list of users who liked the post
        if user_id not in comment.get().to_dict()['liked_by']:
            comment.update({u'liked_by': firestore.ArrayUnion([user_id])})
        else:
            comment.update({u'liked_by': firestore.ArrayRemove([user_id])})

        comment_data = comment.get().to_dict()
        if user_id in comment_data['liked_by']:
            comment_data['liked_by_me'] = True
        else:
            comment_data['liked_by_me'] = False
        return comment_data
    except Exception as e:
        return {'error': str(e)}