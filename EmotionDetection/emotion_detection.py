"""Emotion detection using the IBM Watson EmotionPredict API."""

from __future__ import annotations

import os

import requests


def _none_result():
    """Return a consistent None-valued response for empty or failed requests."""
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }


def emotion_detector(text_to_analyse):
    """Call the IBM Watson EmotionPredict API and return the emotion scores."""
    if text_to_analyse is None or not str(text_to_analyse).strip():
        return _none_result()

    api_key = os.getenv("WATSON_API_KEY", "").strip()
    url = os.getenv("WATSON_URL", "").strip()

    if not api_key or not url:
        return _none_result()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
    }
    payload = {"raw_document": {"text": text_to_analyse}}

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            auth=("apikey", api_key),
            timeout=30,
        )
        if response.status_code == 400:
            return _none_result()
        response.raise_for_status()

        data = response.json()
        emotions = data.get("emotion", {}).get("document", {}).get("emotion", {})
        scores = {
            "anger": (
                float(emotions.get("anger"))
                if emotions.get("anger") is not None
                else None
            ),
            "disgust": (
                float(emotions.get("disgust"))
                if emotions.get("disgust") is not None
                else None
            ),
            "fear": (
                float(emotions.get("fear"))
                if emotions.get("fear") is not None
                else None
            ),
            "joy": (
                float(emotions.get("joy"))
                if emotions.get("joy") is not None
                else None
            ),
            "sadness": (
                float(emotions.get("sadness"))
                if emotions.get("sadness") is not None
                else None
            ),
        }

        scored_values = [
            (name, value) for name, value in scores.items() if value is not None
        ]
        if not scored_values:
            return _none_result()

        dominant_emotion, _ = max(scored_values, key=lambda item: item[1])
        scores["dominant_emotion"] = dominant_emotion
        return scores
    except (requests.RequestException, KeyError, TypeError, ValueError):
        return _none_result()
