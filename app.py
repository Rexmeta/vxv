from flask import Flask, render_template, request, redirect, url_for, flash
import string
import random
import validators
from datetime import datetime
import os
from threading import Lock

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', ''.join(random.choices(string.ascii_letters + string.digits, k=32)))

# In-memory storage
class URLStore:
    def __init__(self):
        self.urls = {}
        self.lock = Lock()

    def add_url(self, original_url):
        with self.lock:
            # Check if URL already exists
            for short_code, data in self.urls.items():
                if data['original_url'] == original_url:
                    return short_code
            
            # Generate new short code
            while True:
                short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                if short_code not in self.urls:
                    break
            
            self.urls[short_code] = {
                'original_url': original_url,
                'created_date': datetime.utcnow(),
                'clicks': 0
            }
            return short_code

    def get_url(self, short_code):
        return self.urls.get(short_code)

    def increment_clicks(self, short_code):
        if short_code in self.urls:
            with self.lock:
                self.urls[short_code]['clicks'] += 1

url_store = URLStore()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form.get('url')
        
        if not original_url:
            flash('URL을 입력해주세요.', 'error')
            return redirect(url_for('index'))
        
        if not validators.url(original_url):
            flash('유효한 URL을 입력해주세요.', 'error')
            return redirect(url_for('index'))
        
        short_code = url_store.add_url(original_url)
        return render_template('index.html', 
                            short_url=f"https://vxv.kr/{short_code}",
                            original_url=original_url)
    
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    url_data = url_store.get_url(short_code)
    if url_data:
        url_store.increment_clicks(short_code)
        return redirect(url_data['original_url'])
    else:
        flash('잘못된 URL입니다.', 'error')
        return redirect(url_for('index'))

@app.route('/stats/<short_code>')
def stats(short_code):
    url_data = url_store.get_url(short_code)
    if url_data:
        return render_template('stats.html', 
                             url_data={
                                 'short_code': short_code,
                                 'original_url': url_data['original_url'],
                                 'created_date': url_data['created_date'],
                                 'clicks': url_data['clicks']
                             })
    flash('URL을 찾을 수 없습니다.', 'error')
    return redirect(url_for('index'))

# Health check endpoint
@app.route('/health')
def health_check():
    return {'status': 'healthy'}, 200

app.debug = False 