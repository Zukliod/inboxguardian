from flask import Blueprint, jsonify, request
import psycopg2

# Define the Blueprint for analytics
analytics = Blueprint('analytics', __name__)

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="inboxguardian",
        user="harshit",
        password="Zukliod2.0"  # Replace with your actual password
    )
    return conn

# Priority Distribution Endpoint (Simplified)
@analytics.route('/priority-distribution', methods=['GET'])
def priority_distribution():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Simplified SQL query to group by priority without pagination
    cursor.execute("""
        SELECT priority, COUNT(*) AS count
        FROM notifications
        GROUP BY priority;
    """)
    results = cursor.fetchall()
    conn.close()

    output = [{"priority": row[0], "count": row[1]} for row in results]
    return jsonify(output)

# Notification Frequency Endpoint with Date Filtering
@analytics.route('/notification-frequency', methods=['GET'])
def notification_frequency():
    # Get date range filters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Query notifications grouped by date and filtered by range
    if start_date and end_date:
        cursor.execute("""
            SELECT DATE(created_at) AS day, COUNT(*) AS total_notifications
            FROM notifications
            WHERE created_at >= %s AND created_at <= %s
            GROUP BY day
            ORDER BY day DESC;
        """, (start_date, end_date))
    else:
        cursor.execute("""
            SELECT DATE(created_at) AS day, COUNT(*) AS total_notifications
            FROM notifications
            GROUP BY day
            ORDER BY day DESC;
        """)
    results = cursor.fetchall()
    conn.close()

    output = [{"date": str(row[0]), "total_notifications": row[1]} for row in results]
    return jsonify(output)

# Time-Based Patterns Endpoint
@analytics.route('/time-based-patterns', methods=['GET'])
def time_based_patterns():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT EXTRACT(HOUR FROM created_at) AS hour, COUNT(*) AS total
        FROM notifications
        GROUP BY hour
        ORDER BY hour;
    """)
    results = cursor.fetchall()
    conn.close()

    output = [{"hour": int(row[0]), "total_notifications": row[1]} for row in results]
    return jsonify(output)