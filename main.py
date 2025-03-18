from flask import Flask, request, redirect, render_template
import psycopg2
import random
import string
import os

# Load database URL from environment variables
DATABASE_URL = "postgresql://postgres:!Buster1326@db.ylhulmcjvfiebllptqlh.supabase.co:5432/postgres"


# Connect to Supabase (PostgreSQL)
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

app = Flask(__name__)

# Function to generate short codes
def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Shorten a URL
@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['long_url']
    short_code = generate_short_code()
    
    # Insert into PostgreSQL
    cursor.execute("INSERT INTO urls (short_code, long_url) VALUES (%s, %s)", (short_code, long_url))
    conn.commit()
    
    short_url = f"http://127.0.0.1:5000/{short_code}"
    return render_template('index.html', short_url=short_url)

# Redirect shortened URL to the original URL
@app.route('/<short_code>')
def redirect_url(short_code):
    cursor.execute("SELECT long_url FROM urls WHERE short_code = %s", (short_code,))
    result = cursor.fetchone()
    
    if result:
        return redirect(result[0])  # Redirect to original URL
    return "URL not found", 404

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
