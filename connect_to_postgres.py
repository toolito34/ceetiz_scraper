import psycopg2
from psycopg2.extras import RealDictCursor

# Configuration de la base de données
DB_CONFIG = {
    "dbname": "ceetiz_db",
    "user": "postgres",
    "password": "passpass",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("Connexion à la base de données réussie")
        return conn
    except Exception as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None

def create_table(conn):
    try:
        with conn.cursor() as cursor:
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS activities (
                id SERIAL PRIMARY KEY,
                title TEXT,
                price TEXT,
                location TEXT,
                image TEXT,
                url TEXT
            );
            '''
            cursor.execute(create_table_query)
            conn.commit()
            print("Table 'activities' créée avec succès")
    except Exception as e:
        print(f"Erreur lors de la création de la table: {e}")

def insert_activity(conn, activity):
    try:
        with conn.cursor() as cursor:
            insert_query = '''
            INSERT INTO activities (title, price, location, image, url)
            VALUES (%s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (activity['title'], activity['price'], activity['location'], activity['image'], activity['url']))
            conn.commit()
            print("Activité insérée avec succès")
    except Exception as e:
        print(f"Erreur lors de l'insertion de l'activité: {e}")

def get_activities(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM activities")
            activities = cursor.fetchall()
            for activity in activities:
                print(activity)
    except Exception as e:
        print(f"Erreur lors de la récupération des activités: {e}")

if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        create_table(conn)
        # Exemple d'insertion d'une activité
        sample_activity = {
            "title": "Sample Activity",
            "price": "100€",
            "location": "Paris",
            "image": "http://example.com/image.jpg",
            "url": "http://example.com/activity"
        }
        insert_activity(conn, sample_activity)
        # Récupérer et afficher toutes les activités
        get_activities(conn)
        conn.close()