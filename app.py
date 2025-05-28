import requests
import mysql.connector
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'your_mysql_user',
    'password': 'your_mysql_password',
    'database': 'odds'
}

# RapidAPI headers
headers = {
    "X-RapidAPI-Key": "cb40092ed8msh2925f33bcd505a7p15c78bjsn00478675fff6",
    "X-RapidAPI-Host": "rapidapi.com"
}

# Pull EPL fixtures from RapidAPI
def fetch_and_store_fixtures():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {
        "league": "39",  # EPL
        "season": "2024",
        "next": "10"     # fetch next 10 fixtures
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    fixtures = data.get('response', [])

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    for item in fixtures:
        fixture = item['fixture']
        teams = item['teams']
        odds = item.get('odds', {}).get('1x2', {})

        date = fixture['date'][:10]
        time = fixture['date'][11:16]
        home = teams['home']['name']
        away = teams['away']['name']
        odds_1 = odds.get('1', 0)
        odds_x = odds.get('X', 0)
        odds_2 = odds.get('2', 0)

        cursor.execute("""
            INSERT INTO fixtures (date, time, home_team, away_team, odds_1, odds_x, odds_2)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                odds_1 = VALUES(odds_1),
                odds_x = VALUES(odds_x),
                odds_2 = VALUES(odds_2)
        """, (date, time, home, away, odds_1, odds_x, odds_2))

    conn.commit()
    cursor.close()
    conn.close()

    # 4. Routes
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/fixtures')
def fixtures_api():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT date, time, home_team, away_team, odds_1, odds_x, odds_2 FROM fixtures ORDER BY date, time")
    fixtures = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"fixtures": fixtures})

# 👇 5. Trigger fetch from RapidAPI via browser
@app.route('/api/fetch-fixtures')
def fetch_fixtures():
    fetch_and_store_fixtures()
    return jsonify({"message": "Fixtures fetched and stored."})

if __name__ == '__main__':
    app.run(debug=True)
