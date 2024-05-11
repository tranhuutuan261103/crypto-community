from website.db_config.firebase import db

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