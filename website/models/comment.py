from website.db_config.firebase import db
from google.cloud import firestore
from datetime import datetime

comments_ref = db.collection('comments')
users_ref = db.collection('users')

def get_comments(post_id, user_id):
    try:
        # Fetch all comments for the post_id
        all_comments = []
        for comment in comments_ref.where('post_id', '==', post_id).stream():
            comment_data = comment.to_dict()
            comment_data['id'] = comment.id
            comment_data['commented_by'] = comment_data['commented_by'].get().to_dict()
            if 'replying_to' in comment_data and comment_data['replying_to'] != None:
                comment_data['replying_to'] = comment_data['replying_to'].get().to_dict()
            else:
                comment_data['replying_to'] = None

            if 'liked_by' not in comment.to_dict():
                comment_data['liked_by'] = []
            if user_id != None and user_id in comment_data['liked_by']:
                comment_data['liked_by_me'] = True
            else:
                comment_data['liked_by_me'] = False

            all_comments.append(comment_data)
        return all_comments
    except Exception as e:
        print(str(e))
        return []
    
def get_comment_by_id(comment_id):
    try:
        # Fetch a single comment by its ID
        comment = comments_ref.document(comment_id)
        comment_data = comment.get().to_dict()
        comment_data['id'] = comment.id
        comment_data['commented_by'] = comments_ref.document(comment_id).get().to_dict()['commented_by'].get().to_dict()
        if 'replying_to' in comment_data and comment_data['replying_to'] != None:
            comment_data['replying_to'] = comments_ref.document(comment_id).get().to_dict()['replying_to'].get().to_dict()
        else:
            comment_data['replying_to'] = None

        if 'liked_by' not in comment_data:
            comment_data['liked_by'] = []
        if 'user_id' in comment_data['liked_by']:
            comment_data['liked_by_me'] = True
        else:
            comment_data['liked_by_me'] = False

        return comment_data
    except Exception as e:
        return {'error': str(e)}
    
def add_comment(post_id, user_id, parent_id, content):
    try:
        if parent_id:
            parent_comment = comments_ref.document(parent_id)
            parent_comment_data = parent_comment.get().to_dict()
            post_id = parent_comment_data['post_id'] if parent_id else post_id

        # Add a new comment to the post_id
        comments_ref.add({
            'parent_comment_id': parent_id,
            'post_id': post_id,
            'commented_by': users_ref.document(user_id) if user_id else None,
            'content': content,
            'liked_by': [],
            'created_at': datetime.now()
        })
        return True
    except Exception as e:
        print(str(e))
        return False
    
def reply_comment(post_id, user_id, reply_comment_id, parent_comment_id, content):
    try:
        # Add a new comment to the post_id
        comments_ref.add({
            'parent_comment_id': parent_comment_id,
            'replying_to': comments_ref.document(reply_comment_id).get().to_dict()['commented_by'],
            'post_id': post_id,
            'commented_by': users_ref.document(user_id) if user_id else None,
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

        comment_data['commented_by'] = comments_ref.document(comment_id).get().to_dict()['commented_by'].get().to_dict()
        if 'replying_to' in comment_data and comment_data['replying_to'] != None:
            comment_data['replying_to'] = comments_ref.document(comment_id).get().to_dict()['replying_to'].get().to_dict()
        else:
            comment_data['replying_to'] = None

        return comment_data
    except Exception as e:
        return {'error': str(e)}