from website.db_config.firebase import db
from google.cloud import firestore

categories_ref = db.collection('categories')

def do_something():
    pass

def get_categories():
    try:
        all_categories = []
        query = categories_ref.where('status', '==', True)
        for category in query.stream():
            category_data = category.to_dict()
            category_data['id'] = category.id
            all_categories.append(category_data)
        return all_categories
    except Exception as e:
        return str(e)

def get_all_categories():
    try:
        all_categories = []
        query = categories_ref
        for category in query.stream():
            category_data = category.to_dict()
            category_data['id'] = category.id
            all_categories.append(category_data)
        return all_categories
    except Exception as e:
        return str(e)

def get_num_categories():
    try:
        all_categories = []
        query = categories_ref
        for category in query.stream():
            all_categories.append(category)
        return len(all_categories)
    except Exception as e:
        return str(e)

def update_status_category(category_id, status):
    try:
        category_ref = categories_ref.document(category_id)
        category_ref.update({'status': status})
        return status
    except Exception as e:
        print(str(e))
        return False
