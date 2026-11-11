import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq_service import generate_with_groq, GroqConfigurationError, GroqServiceError
from prompts import build_prompt, MESSAGE_TYPES, TONES

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024  # 32 KB request limit


@app.route("/", methods=["GET"])
def home():
    return render_template(
        "index.html",
        message_types=MESSAGE_TYPES,
        tones=TONES
    )


@app.route("/generate", methods=["POST"])
def generate():
    if not request.is_json:
        return jsonify(success=False, error="Please send the form as JSON."), 400

    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    message_type = data.get("message_type", "")
    tone = data.get("tone", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify(success=False, error="Please enter your message."), 400
    if len(message) > 12000:
        return jsonify(success=False, error="Your message is too long. Please keep it under 12,000 characters."), 400
    if message_type not in MESSAGE_TYPES:
        return jsonify(success=False, error="Please select a valid message type."), 400
    if tone not in TONES:
        return jsonify(success=False, error="Please select a valid writing tone."), 400

    prompt = build_prompt(message_type, tone, message.strip())

    try:
        generated_message = generate_with_groq(prompt)
        if not generated_message:
            raise GroqServiceError("The AI returned an empty response.")
        return jsonify(success=True, generated_message=generated_message)
    except GroqConfigurationError:
        return jsonify(success=False, error="API key is missing. Add GROQ_API_KEY to your .env file and restart the app."), 503
    except GroqServiceError as exc:
        return jsonify(success=False, error=str(exc)), 502
    except Exception:
        app.logger.exception("Unexpected error while generating a message")
        return jsonify(success=False, error="Something went wrong. Please try again."), 500


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify(success=False, error="The submitted request is too large."), 413


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5055, debug=False)
