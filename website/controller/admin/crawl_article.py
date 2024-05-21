from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, WebDriverException

class ArticleCrawler:
    def __init__(self, driver_path):
        self.driver_path = driver_path

    def crawl_article(self, url, type):
        service = Service(self.driver_path)
        options = Options()
        options.add_argument('--headless')

        driver = webdriver.Chrome(service=service, options=options)

        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'post-item'))
            )

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            common = soup.find(class_='appMainContent')
            articles = common.find_all('a', class_='sc-f70bb44c-0 iQEJet cmc-link')

            new_articles = []
            for article in articles:
                try:
                    title = article.find('p', class_='title').text.strip()
                    description = article.find('p', class_='description').text.strip()
                    thumbnailUrl = article.find('img', class_='post-img')['src'].strip()
                    linkDetail = article['href'].strip()
                    
                    driver.get(linkDetail)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.TAG_NAME, 'article'))
                    )

                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    common = soup.find('article')
                    author = soup.find('p', class_='sc-4984dd93-0 fOOliX').find('a', class_='name').text.strip()
                    new_article = {
                        'title': title,
                        'subDescription': description,
                        'thumbnailUrl': thumbnailUrl,
                        'author': author,
                        'content': str(common),  # Convert the article content to string to avoid BeautifulSoup object issues
                        'type': type,
                    }
                    new_articles.append(new_article)
                    print(len(new_articles))
                except Exception as e:
                    print(f"Lỗi khi thu thập bài viết: {str(e)}")
                    continue
            return new_articles
        except (TimeoutException, WebDriverException) as e:
            print(f"Lỗi khi thực hiện web scraping: {str(e)}")
            return None
        finally:
            driver.quit()
