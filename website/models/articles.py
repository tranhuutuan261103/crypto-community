from website.db_config.firebase import db
from google.cloud import firestore
import pytz
tz = pytz.timezone('Asia/Bangkok')

article_ref = db.collection('articles')

def do_something():
    pass

def get_articles():
    try:
        all_articles = []
        query = article_ref.order_by('created_at', direction="DESCENDING")
        for article in query.stream():
            article_data = article.to_dict()
            article_data['id'] = article.id
            article_data['created_at'] = article_data['created_at'].replace(tzinfo=pytz.utc).astimezone(tz)
            article_data['created_at'] = article_data['created_at'].strftime('%d %B %Y %H:%M:%S')
            all_articles.append(article_data)
        return all_articles
    except Exception as e:
        return str(e)

def get_articles_by_type(article_type, limit=None):
    try:
        all_articles = []
        query = article_ref.where('status', '==', True).where('type', '==', article_type).order_by('created_at', direction="DESCENDING")
        if (limit != None):
            query = query.limit(limit)
        for article in query.stream():
            article_data = article.to_dict()
            article_data['id'] = article.id
            article_data['created_at'] = article_data['created_at'].replace(tzinfo=pytz.utc).astimezone(tz)
            article_data['created_at'] = article_data['created_at'].strftime('%d %B %Y %H:%M:%S')
            all_articles.append(article_data)
        return all_articles
    except Exception as e:
        return str(e)

def get_articles_by_highlight():
    try:
        all_articles = []
        query = article_ref.where('status', '==', True).where('highlight', '==', True).order_by('created_at', direction="DESCENDING")
        for article in query.stream():
            article_data = article.to_dict()
            article_data['id'] = article.id
            article_data['created_at'] = article_data['created_at'].replace(tzinfo=pytz.utc).astimezone(tz)
            article_data['created_at'] = article_data['created_at'].strftime('%d %B %Y %H:%M:%S')
            all_articles.append(article_data)
        return all_articles
    except Exception as e:
        return str(e)
    
def get_article_by_id(article_id):
    try:
        article = article_ref.document(article_id).get()
        article_data = article.to_dict()
        article_data['id'] = article_id
        article_data['created_at'] = article_data['created_at'].replace(tzinfo=pytz.utc).astimezone(tz)
        article_data['created_at'] = article_data['created_at'].strftime('%d %B %Y %H:%M:%S')
        return article_data
    except Exception as e:
        return str(e)

def get_article_sorted_by_view():
    try:
        all_articles = []
        query = article_ref.where('status', '==', True).order_by('views', direction="DESCENDING").limit(10)
        for article in query.stream():
            article_data = article.to_dict()
            article_data['id'] = article.id
            article_data['created_at'] = article_data['created_at'].replace(tzinfo=pytz.utc).astimezone(tz)
            article_data['created_at'] = article_data['created_at'].strftime('%d %B %Y %H:%M:%S')
            all_articles.append(article_data)
        return all_articles
    except Exception as e:
        return str(e)

def get_article_sorted_by_view_type(article_type):
    try:
        all_articles = []
        query = article_ref.where('status', '==', True).where('type', '==', article_type).order_by('views', direction="DESCENDING").limit(10)
        for article in query.stream():
            article_data = article.to_dict()
            article_data['id'] = article.id
            article_data['created_at'] = article_data['created_at'].replace(tzinfo=pytz.utc).astimezone(tz)
            article_data['created_at'] = article_data['created_at'].strftime('%d %B %Y %H:%M:%S')
            all_articles.append(article_data)
        return all_articles
    except Exception as e:
        return str(e)
    
def update_views(article_id):
    try:
        article = article_ref.document(article_id)
        article.update({'views': firestore.Increment(1)})
        return True
    except Exception as e:
        return False

def get_num_articles():
    try:
        all_articles = []
        query = article_ref
        for article in query.stream():
            all_articles.append(article.to_dict())
        return len(all_articles)
    except Exception as e:
        return str(e)

def get_num_views():
    try:
        all_articles = []
        query = article_ref
        for article in query.stream():
            all_articles.append(article.to_dict())
        return sum([article['views'] for article in all_articles])
    except Exception as e:
        return str(e)
    
def update_status_article(article_id, status):
    try:
        article = article_ref.document(article_id)
        article.update({'status': status})
        return status
    except Exception as e:
        print(str(e))
        return False
    
def update_highlight_article(article_id, status):
    try:
        article = article_ref.document(article_id)
        article.update({'highlight': status})
        return status
    except Exception as e:
        print(str(e))
        return False

def check_article_exist(articles):
    unique_titles = []  # Danh sách để lưu trữ các tiêu đề duy nhất
    try:
        for article in articles:
            query = article_ref.where('title', '==', article['title']).stream()
            if not any(doc.exists for doc in query):  # Kiểm tra nếu không có bất kỳ document nào tồn tại với tiêu đề này
                unique_titles.append(article)  # Thêm bài viết vào danh sách nếu tiêu đề là duy nhất
        return unique_titles  # Trả về danh sách các bài viết không trùng lặp
    except Exception as e:
        return []  # Trả về danh sách rỗng nếu có lỗi

def create_post(article):
    try:
        article['created_at'] = firestore.SERVER_TIMESTAMP
        article['status'] = False
        article['highlight'] = False
        article['views'] = 0
        article_ref.add(article)
        return True
    except Exception as e:
        return str(e)
    
def get_num_articles_by_type(article_type):
    try:
        all_articles = []
        query = article_ref.where('type', '==', article_type)
        for article in query.stream():
            all_articles.append(article.to_dict())
        return len(all_articles)
    except Exception as e:
        return str(e)
    
def get_information_index(categories):
    try:
        num_articles = 0;
        num_views = 0;
        num_articles_by_category = {}
        query = article_ref.stream()
        for article in query:
            article_data = article.to_dict()
            num_articles += 1
            num_views += article_data['views'] 
            num_articles_by_category[article_data['type']] = num_articles_by_category.get(article_data['type'], 0) + 1
        return num_articles, num_views, num_articles_by_category
    except Exception as e:
        return str(e)