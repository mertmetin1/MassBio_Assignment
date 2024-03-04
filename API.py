from flask import Flask, render_template, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def create_connection():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="mert",
            password="mert007metin",
            host="localhost"
        )
        return conn
    except psycopg2.Error as e:
        print("Veritabanı bağlantı hatası:", e)
        return None

# Web interface
@app.route('/')
def index():
    return render_template('index.html')


#API Endpoint
@app.route('/assignment/query', methods=['POST'])
def query_data():
    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Veritabanı bağlantısı kurulamadı.'}), 500

    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Gelen isteği al
    request_data = request.json

    # Filtreleri ve sıralama bilgilerini al
    filters = request_data.get('filters', {})
    ordering = request_data.get('ordering', [])
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))

    # SQL sorgusunu oluştur
    query = "SELECT * FROM report_output"

    if filters:
        conditions = []
        for key, value in filters.items():
            # Filtrelerin değerlerine göre farklı sorgular oluştur
            if isinstance(value, list):  # Eğer filtre değeri bir liste ise
                conditions.append(f"{key} IN ({','.join(map(str, value))})")
            elif isinstance(value, int) or isinstance(value, float):  # Eğer filtre değeri bir sayı ise
                conditions.append(f"{key} = {value}")
            else:  # Diğer durumlarda
                conditions.append(f"{key} = '{value}'")
        query += " WHERE " + " AND ".join(conditions)

    if ordering:
        order_conditions = []
        for order_item in ordering:
            column, direction = order_item.popitem()
            order_conditions.append(f"{column} {direction.upper()}")
        query += " ORDER BY " + ", ".join(order_conditions)

    # Sayfalama
    query += f" LIMIT {page_size} OFFSET {(page - 1) * page_size}"

    try:
        # SQL sorgusunu çalıştır
        cur.execute(query)

        # Sonuçları al
        rows = cur.fetchall()

        # Bağlantıyı kapat
        cur.close()
        conn.close()

        # Yanıtı hazırla
        response = {
            'page': page,
            'page_size': page_size,
            'count': len(rows),
            'results': rows
        }

        return jsonify(response), 200, {'Content-Type': 'application/json'}

    except psycopg2.Error as e:
        print("Veritabanı sorgu hatası:", e)
        return jsonify({'error': 'Veritabanı sorgusu sırasında bir hata oluştu.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
