import os
from flask import Flask
try:
    import redis
except ImportError:
    redis = None
app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "redis")
cache = None

if redis:
    try:
        cache = redis.Redis(
            host=redis_host,
            port=6379,
            socket_connect_timeout=1
        )
    except Exception:
        cache = None
@app.route("/")
def hello():
    count = None

    if cache:
        try:
            count = cache.incr("hits")
        except Exception:
            count = None

    if count is not None:
        return f"Hello from inside a Docker container! (Python/Flask) - Visited {count} times."

    return "Hello from inside a Docker container! (Python/Flask)"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)