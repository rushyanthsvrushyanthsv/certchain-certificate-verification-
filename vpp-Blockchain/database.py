import sqlite3

DATABASE = "voltchain.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():

    connection = get_connection()
    cursor = connection.cursor()

    # Users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # Producers
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS producers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            energy_source TEXT,
            capacity_kw REAL DEFAULT 0,
            generated_kwh REAL DEFAULT 0,
            available_kwh REAL DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Consumers
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consumers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            demand_kwh REAL DEFAULT 0,
            consumed_kwh REAL DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Energy readings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS energy_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producer_id INTEGER,
            generation_kwh REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(producer_id) REFERENCES producers(id)
        )
    """)

    # Transactions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producer_id INTEGER,
            consumer_id INTEGER,
            energy_kwh REAL NOT NULL,
            price_per_kwh REAL NOT NULL,
            total_amount REAL NOT NULL,
            blockchain_hash TEXT,
            status TEXT DEFAULT 'COMPLETED',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(producer_id) REFERENCES producers(id),
            FOREIGN KEY(consumer_id) REFERENCES consumers(id)
        )
    """)

    connection.commit()
    connection.close()