# Emotion Detector

A Flask-based web application that analyzes written text and identifies the dominant emotion using IBM Watson Natural Language Understanding.

## Technologies

- Python
- Flask
- Watson NLP
- unittest
- pylint

## Installation

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Set environment variables for IBM Watson:

   ```bash
   set WATSON_API_KEY=your_api_key
   set WATSON_URL=https://your-service-url
   ```

   If the Watson credentials are not configured in the local environment, the application falls back to a demo response so the interface can still be tested visually.

## Run the application

```bash
python server.py
```

Then open the browser at:

```text
http://localhost:5000
```

## Run tests

```bash
python -m unittest -v
```

## Run pylint

```bash
python -m pylint emotion_detection.py server.py
```
