# Final Project

This repository contains the IBM Skills Network Final Project: Emotion Detector.

The application analyzes text and identifies the dominant emotion using the IBM Watson EmotionPredict API through a Python requests-based HTTP call.

## Technologies

- Python
- Flask
- Requests
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

4. Configure the required IBM Watson environment variables:

   ```bash
   set WATSON_API_KEY=your_api_key
   set WATSON_URL=https://us-south.ml.cloud.ibm.com/ml/v1/text/emotion?version=2022-02-01
   ```

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
python -m unittest discover -v
```

## Run pylint

```bash
python -m pylint server.py EmotionDetection/emotion_detection.py
```
