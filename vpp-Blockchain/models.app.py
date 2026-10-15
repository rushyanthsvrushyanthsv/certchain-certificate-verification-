from database import get_connection


def get_dashboard():

    connection = get_connection()
    cursor = connection.cursor()

    producers = cursor.execute(
        "SELECT COUNT(*) AS count FROM producers"
    ).fetchone()["count"]

    consumers = cursor.execute(
        "SELECT COUNT(*) AS count FROM consumers"
    ).fetchone()["count"]

    generated = cursor.execute(
        "SELECT COALESCE(SUM(generated_kwh), 0) AS total FROM producers"
    ).fetchone()["total"]

    available = cursor.execute(
        "SELECT COALESCE(SUM(available_kwh), 0) AS total FROM producers"
    ).fetchone()["total"]

    transactions = cursor.execute(
        "SELECT COUNT(*) AS count FROM transactions"
    ).fetchone()["count"]

    connection.close()

    return {
        "producers": producers,
        "consumers": consumers,
        "generated_kwh": generated,
        "available_kwh": available,
        "transactions": transactions
    }