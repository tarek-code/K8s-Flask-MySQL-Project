from flask import Flask, request, render_template_string
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

@app.route('/healthz')
def healthz():
    return "OK", 200

@app.route('/')
def home():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT count FROM counter WHERE id=1;")
        result = cursor.fetchone()
        count = result['count'] if result else 0
        conn.close()

        html = f'''
            <h1>Counter: {count}</h1>
            <form method="POST" action="/increment">
                <button type="submit">Increment</button>
            </form>
        '''
        return html
    except Exception as e:
        return f"Error: {e}"

# ✅ حل المشكلة: إضافة مسار /flask
@app.route('/flask')
def flask_route():
    return home()

@app.route('/increment', methods=['POST'])
def increment():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE counter SET count = count + 1 WHERE id = 1;")
        conn.commit()
        conn.close()
        return '<script>window.location.href = "/";</script>'
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
