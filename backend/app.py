from flask import Flask, request, jsonify
from ariadne import graphql_sync
from ariadne.explorer import ExplorerPlayground
from graphql_resolvers import schema
from flask_cors import CORS
from config import Config
from flask_socketio import SocketIO
from database import engine, Base
from utils import get_user_from_token
from azure_blob import upload_file_stream

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize DB tables (dev only, replace with Alembic in prod)
Base.metadata.create_all(bind=engine)

# Redis-backed SocketIO (falls back to in-memory if REDIS_URL not set)
socketio = SocketIO(app, cors_allowed_origins="*", message_queue=Config.REDIS_URL)

# Playground setup
explorer_html = ExplorerPlayground().html('')

# -----------------------------
# GraphQL Routes
# -----------------------------


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return explorer_html, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    context = {"request": request}

    auth = request.headers.get("Authorization")
    if auth and auth.startswith("Bearer "):
        token = auth.split(" ", 1)[1]
        user = get_user_from_token(token)
        if user:
            context["user"] = {"id": user.id, "username": user.username}

    success, result = graphql_sync(
        schema,
        data,
        context_value=context,
        debug=True,
    )
    status = 200 if success else 400
    return jsonify(result), status


# -----------------------------
# File Upload Endpoint
# -----------------------------


@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if not f:
        return {"error": "no file"}, 400
    url = upload_file_stream(f.stream, f.filename, content_type=f.content_type)
    return {"url": url}


# -----------------------------
# Main Entry
# -----------------------------

if __name__ == "__main__":
    # Enable auto-reload on code changes
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True,  # enables Flask debug mode
        use_reloader=True,  # enables automatic reload on code changes
    )
