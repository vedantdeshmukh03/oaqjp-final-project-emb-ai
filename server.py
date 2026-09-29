"""Flask application for the emotion detector web interface."""

from __future__ import annotations

from flask import Flask, render_template_string, request

from EmotionDetection.emotion_detection import emotion_detector

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
      <form method="GET" action="/emotionDetector">
        <textarea name="textToAnalyze" placeholder="Type a sentence to analyze...">{{ text or '' }}</textarea>
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


@app.route("/", methods=["GET"])
def index():
    """Render the form and show emotion analysis results."""
    text = request.args.get("textToAnalyze", "")
    result = None

    if text.strip():
        result = emotion_detector(text)

    return render_template_string(HTML_TEMPLATE, text=text, result=result)


@app.route("/emotionDetector", methods=["GET"])
def emotion_detector_route():
    """Return the dominant emotion and scores for the supplied text."""
    text_to_analyse = request.args.get("textToAnalyze", "")

    if text_to_analyse is None or not str(text_to_analyse).strip():
        return "Invalid input! Try again."

    result = emotion_detector(text_to_analyse)
    if result is None:
        return "Invalid input! Try again."

    return (
        f"anger: {result['anger']}\n"
        f"disgust: {result['disgust']}\n"
        f"fear: {result['fear']}\n"
        f"joy: {result['joy']}\n"
        f"sadness: {result['sadness']}\n"
        f"dominant_emotion: {result['dominant_emotion']}"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
