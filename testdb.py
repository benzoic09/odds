@app.route('/test/db')
def test_db():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({"db_status": "✅ Connected", "result": result})
    except mysql.connector.Error as err:
        return jsonify({"db_status": "❌ Failed", "error": str(err)})
