from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import string
import random
import validators
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', ''.join(random.choices(string.ascii_letters + string.digits, k=32)))

# Use SQLite for both development and production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    clicks = db.Column(db.Integer, default=0)

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        short_code = ''.join(random.choices(chars, k=length))
        if not URL.query.filter_by(short_code=short_code).first():
            return short_code

with app.app_context():
    db.create_all()

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
        
        # Check if URL already exists
        existing_url = URL.query.filter_by(original_url=original_url).first()
        if existing_url:
            return render_template('index.html', 
                                short_url=f"https://vxv.kr/{existing_url.short_code}",
                                original_url=original_url)
        
        short_code = generate_short_code()
        new_url = URL(original_url=original_url, short_code=short_code)
        db.session.add(new_url)
        db.session.commit()
        
        return render_template('index.html', 
                            short_url=f"https://vxv.kr/{short_code}",
                            original_url=original_url)
    
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    url_data = URL.query.filter_by(short_code=short_code).first()
    if url_data:
        url_data.clicks += 1
        db.session.commit()
        return redirect(url_data.original_url)
    else:
        flash('잘못된 URL입니다.', 'error')
        return redirect(url_for('index'))

@app.route('/stats/<short_code>')
def stats(short_code):
    url_data = URL.query.filter_by(short_code=short_code).first()
    if url_data:
        return render_template('stats.html', url_data=url_data)
    flash('URL을 찾을 수 없습니다.', 'error')
    return redirect(url_for('index'))

# Vercel requires a module-level app variable
app.debug = False 