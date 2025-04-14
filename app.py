from flask import Flask, request, jsonify
from datetime import datetime
import pytz

app = Flask(__name__)

VALID_TOKEN = "supersecrettoken123"

capital_timezones = {
    "London": "Europe/London",
    "Paris": "Europe/Paris",
    "Tokyo": "Asia/Tokyo",
    "Washington": "America/New_York",
    "Canberra": "Australia/Sydney",
    "Ottawa": "America/Toronto",
    "New Delhi": "Asia/Kolkata",
    "Brasilia": "America/Sao_Paulo",
    "Beijing": "Asia/Shanghai",
}


@app.route("/time", methods=["GET"])
def get_time():
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {VALID_TOKEN}":
        return jsonify({"error": "Unauthorized. Please provide a valid token."}), 401

    city = request.args.get("city")
    if not city:
        return jsonify(
            {"error": "Please provide a capital city via ?city=CapitalName"}
        ), 400

    timezone = capital_timezones.get(city)
    if not timezone:
        return jsonify({"error": f"Sorry, '{city}' is not in our database."}), 404

    tz = pytz.timezone(timezone)
    local_time = datetime.now(tz)
    utc_offset = local_time.strftime("%z")
    formatted_offset = f"UTC{utc_offset[:3]}:{utc_offset[3:]}"

    return jsonify(
        {
            "city": city,
            "local_time": local_time.strftime("%Y-%m-%d %H:%M:%S"),
            "utc_offset": formatted_offset,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
