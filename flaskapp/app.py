from flask import Flask
import pymysql
 
app = Flask(__name__)

def get_connection():
    return pymysql.connect(
        host="db-service",
        port=3306,
        user="flaskuser",
        password="yourpassword",
        database="flaskdb",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def home():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM users;")
        result = cursor.fetchone()
        conn.close()
        return f"Flask app is working! ✅ Users in DB: {result['count']}"
    except Exception as e:
        return f"❌ Failed to connect to DB: {e}"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)