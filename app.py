import json
import os

from flask import Flask, jsonify

from config import Config
from services.workflow import ReviewWorkflow
from utils.logger import get_logger

logger = get_logger(__name__)
app = Flask(__name__)


@app.route("/reviews", methods=["GET"])
def reviews():
    try:
        result = ReviewWorkflow().run()

        os.makedirs("logs", exist_ok=True)
        with open("logs/response.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        return jsonify(result)

    except LookupError as exc:
        return jsonify({"error": str(exc)}), 404

    except Exception as exc:
        logger.error("Workflow failed: %s", exc)
        return jsonify({"error": str(exc)}), 502


if __name__ == "__main__":
    app.run(host=Config.host, port=Config.port, debug=Config.debug)