import json
import os

from flask import Flask, jsonify, request

from config import Config
from services.workflow import ReviewWorkflow
from utils.logger import get_logger

logger = get_logger(__name__)
app = Flask(__name__)

_idempotency_cache: dict = {}


@app.route("/reviews", methods=["GET"])
def reviews():
    Config.reload()
    idempotency_id = request.headers.get("Idempotency-Id")
    if idempotency_id and idempotency_id in _idempotency_cache:
        return jsonify(_idempotency_cache[idempotency_id])

    try:
        result = ReviewWorkflow().run()

        os.makedirs("logs", exist_ok=True)
        with open("logs/response.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        if idempotency_id:
            _idempotency_cache[idempotency_id] = result

        return jsonify(result)

    except LookupError as exc:
        return jsonify({"error": str(exc)}), 404

    except Exception as exc:
        logger.error("Workflow failed: %s", exc)
        return jsonify({"error": str(exc)}), 502


if __name__ == "__main__":
    app.run(host=Config.host, port=Config.port, debug=Config.debug)