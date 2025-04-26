from flask import Blueprint, jsonify, request
from config.database_config import get_db_connection
from utils.prioritization_helper import prioritize_notification

# Create a Blueprint for the main routes
main = Blueprint('main', __name__)

# --- CREATE: Add a new notification ---
@main.route('/notifications', methods=['POST'])
def add_notification():
    try:
        # Log the raw request data
        print("Raw request data:", request.data)

        # Parse the JSON payload
        data = request.json
        print("Parsed JSON data:", data)

        # Validate input data
        if not data:
            print("Error: No input data provided")
            return jsonify({"error": "No input data provided"}), 400
        if "content" not in data or "priority" not in data:
            print("Error: Missing required fields")
            return jsonify({"error": "Missing required fields: 'content' and 'priority'"}), 400

        # Log the database connection attempt
        print("Connecting to the database...")
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check for duplicate content
        print(f"Checking for duplicate content: {data['content']}")
        cursor.execute("SELECT * FROM notifications WHERE content = %s;", (data["content"],))
        duplicate = cursor.fetchone()
        if duplicate:
            print("Error: Duplicate notification content")
            cursor.close()
            connection.close()
            return jsonify({"error": "Duplicate notification content"}), 400

        # Insert new notification
        print(f"Inserting notification: {data}")
        cursor.execute(
            "INSERT INTO notifications (content, priority) VALUES (%s, %s);",
            (data["content"], data["priority"])
        )
        connection.commit()
        cursor.close()
        connection.close()
        print("Notification added successfully!")
        return jsonify({"message": "Notification added successfully!"}), 200
    except Exception as e:
        print("Error in POST /notifications:", e)
        return jsonify({"error": str(e)}), 500
    
# --- READ: Fetch all notifications ---
@main.route('/notifications', methods=['GET'])
def get_notifications():
    try:
        # Get query parameters
        priority = request.args.get("priority")
        search = request.args.get("search")
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        offset = (page - 1) * limit

        print(f"Query parameters: priority={priority}, search={search}, page={page}, limit={limit}")  # Debugging log

        # Build dynamic query
        query = "SELECT * FROM notifications"
        filters = []
        params = []

        if priority:
            filters.append("priority = %s")
            params.append(priority)

        if search:
            keywords = search.split()
            keyword_filters = ["content ILIKE %s" for _ in keywords]
            filters.append(f"({' OR '.join(keyword_filters)})")
            params.extend([f"%{keyword}%" for keyword in keywords])

        if filters:
            query += " WHERE " + " AND ".join(filters)

        query += " LIMIT %s OFFSET %s;"
        params.extend([limit, offset])

        print("Executing query:", query, "with params:", params)  # Debugging log

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple(params))
        notifications = cursor.fetchall()
        cursor.close()
        connection.close()

        # Format the response
        return jsonify([
            {
                "id": row[0],
                "content": row[1],
                "priority": row[2]
            } for row in notifications
        ])
    except Exception as e:
        print("Error in GET /notifications:", e)  # Debugging log
        return jsonify({"error": str(e)}), 500

# --- UPDATE: Modify a specific notification ---
@main.route('/notifications/<int:id>', methods=['PUT'])
def update_notification(id):
    try:
        print("Raw request data:", request.data)  # Debugging log
        data = request.get_json(force=True)  # Force JSON parsing
        print("Parsed JSON data:", data)  # Debugging log

        # Validate input data
        if not data or "content" not in data or "priority" not in data:
            return jsonify({"error": "Missing required fields: 'content' and 'priority'"}), 400

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE notifications SET content = %s, priority = %s WHERE id = %s;",
            (data["content"], data["priority"], id)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Notification updated successfully!"}), 200
    except Exception as e:
        print("Error in PUT /notifications/<id>:", e)  # Debugging log
        return jsonify({"error": str(e)}), 500

# --- DELETE: Remove a specific notification ---
@main.route('/notifications/<int:id>', methods=['DELETE'])
def delete_notification(id):
    try:
        print(f"Deleting notification with ID: {id}")  # Debugging log

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM notifications WHERE id = %s;", (id,))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Notification deleted successfully!"}), 200
    except Exception as e:
        print("Error in DELETE /notifications/<id>:", e)  # Debugging log
        return jsonify({"error": str(e)}), 500