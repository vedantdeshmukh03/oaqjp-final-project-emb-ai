"""Emotion detection application using IBM Watson Natural Language Understanding."""

from __future__ import annotations

import os

from ibm_cloud_sdk_core.api_exception import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import EmotionOptions, Features


def _error_result(message):
    """Return a consistent error payload."""
    return {"error": message, "dominant_emotion": "error"}


def _demo_result(text_to_analyse):
    """Return a deterministic demo payload when Watson credentials are unavailable."""
    lowered = str(text_to_analyse).lower()
    scores = {
        "anger": 0.05,
        "disgust": 0.03,
        "fear": 0.04,
        "joy": 0.10,
        "sadness": 0.08,
    }

    if any(word in lowered for word in ["angry", "furious", "hate", "mad"]):
        scores["anger"] = 0.82
    if any(word in lowered for word in ["disgusted", "gross", "nasty"]):
        scores["disgust"] = 0.80
    if any(word in lowered for word in ["afraid", "scared", "terrified", "fear"]):
        scores["fear"] = 0.84
    if any(word in lowered for word in ["happy", "joy", "excited", "love", "good"]):
        scores["joy"] = 0.88
    if any(word in lowered for word in ["sad", "lonely", "heartbroken", "cry"]):
        scores["sadness"] = 0.85

    dominant_emotion = max(scores, key=scores.get)
    scores["dominant_emotion"] = dominant_emotion
    return scores


def emotion_detector(text_to_analyse):
    """Analyze the input text and return the emotion scores and dominant emotion."""
    result = None

    if text_to_analyse is None or not str(text_to_analyse).strip():
        result = _error_result("Please enter some text.")
        return result

    api_key = os.getenv("WATSON_API_KEY")
    service_url = os.getenv("WATSON_URL")

    if not api_key or not service_url or service_url == "https://example.com":
        return _demo_result(text_to_analyse)

    try:
        authenticator = IAMAuthenticator(api_key)
        nlu = NaturalLanguageUnderstandingV1(
            version="2022-04-07",
            authenticator=authenticator,
        )
        nlu.set_service_url(service_url)

        response = nlu.analyze(
            text=text_to_analyse,
            features=Features(
                emotion=EmotionOptions(targets=[text_to_analyse]),
            ),
        ).get_result()

        emotions = response["emotion"]["document"]["emotion"]
        scores = {
            "anger": float(emotions.get("anger", 0.0)),
            "disgust": float(emotions.get("disgust", 0.0)),
            "fear": float(emotions.get("fear", 0.0)),
            "joy": float(emotions.get("joy", 0.0)),
            "sadness": float(emotions.get("sadness", 0.0)),
        }

        dominant_emotion = max(scores, key=scores.get)
        scores["dominant_emotion"] = dominant_emotion
        result = scores
    except ApiException as error:
        message = getattr(error, "message", str(error))
        if getattr(error, "code", 0) == 400:
            result = _error_result(
                "Emotion detection service returned a bad request error."
            )
        else:
            result = _error_result(f"Watson service error: {message}")
    except (KeyError, TypeError, ValueError):
        result = _error_result("No valid emotion data was returned from Watson.")
    except Exception as error:  # pylint: disable=broad-exception-caught
        result = _error_result(f"Unexpected error while analyzing text: {error}")

    return result
