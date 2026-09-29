"""Flask application for the emotion detector web interface."""

from __future__ import annotations

import os

from flask import Flask, render_template_string, request

from emotion_detection import emotion_detector

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Emotion Detector</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        background: #f4f6fb;
        margin: 0;
        padding: 40px;
      }
      .container {
        max-width: 700px;
        margin: auto;
        background: white;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        padding: 30px;
      }
      h1 { color: #243b53; }
      textarea {
        width: 100%;
        min-height: 120px;
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        padding: 12px;
        box-sizing: border-box;
      }
      button {
        margin-top: 12px;
        background: #2563eb;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 18px;
        cursor: pointer;
      }
      .result {
        margin-top: 20px;
        border-top: 1px solid #e2e8f0;
        padding-top: 20px;
      }
      .error {
        color: #b91c1c;
        font-weight: bold;
      }
      .emotion-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 12px;
        margin-top: 12px;
      }
      .box {
        background: #eef6ff;
        border: 1px solid #bfdbfe;
        border-radius: 8px;
        padding: 10px;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Emotion Detector</h1>
      <form method="POST">
        <textarea name="text" placeholder="Type a sentence to analyze...">{{ text or '' }}</textarea>
        <button type="submit">Analyze</button>
      </form>

      {% if result %}
      <div class="result">
        {% if result.error %}
          <p class="error">{{ result.error }}</p>
        {% else %}
          <h2>Emotion Scores</h2>
          <div class="emotion-grid">
            <div class="box"><strong>Anger:</strong> {{ result.anger }}</div>
            <div class="box"><strong>Disgust:</strong> {{ result.disgust }}</div>
            <div class="box"><strong>Fear:</strong> {{ result.fear }}</div>
            <div class="box"><strong>Joy:</strong> {{ result.joy }}</div>
            <div class="box"><strong>Sadness:</strong> {{ result.sadness }}</div>
          </div>
          <p><strong>Dominant Emotion:</strong> {{ result.dominant_emotion }}</p>
        {% endif %}
      </div>
      {% endif %}
    </div>
  </body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    """Render the form and show emotion analysis results."""
    result = None
    text = ""

    if request.method == "POST":
        text = request.form.get("text", "")
        if not text or not text.strip():
            result = {"error": "Please enter some text."}
        else:
            if not os.getenv("WATSON_API_KEY") or not os.getenv("WATSON_URL"):
                os.environ["WATSON_API_KEY"] = "demo-key"
                os.environ["WATSON_URL"] = "https://example.com"
            result = emotion_detector(text)

    return render_template_string(HTML_TEMPLATE, text=text, result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
