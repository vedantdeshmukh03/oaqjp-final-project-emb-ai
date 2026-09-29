import os
import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import emotion_detector


class EmotionDetectorTests(unittest.TestCase):
    def setUp(self):
        os.environ["WATSON_API_KEY"] = "test-api-key"
        os.environ["WATSON_URL"] = "https://us-south.ml.cloud.ibm.com/ml/v1/text/emotion?version=2022-02-01"

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_dominant_anger(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "emotion": {
                "document": {
                    "emotion": {
                        "anger": 0.8,
                        "disgust": 0.1,
                        "fear": 0.12,
                        "joy": 0.3,
                        "sadness": 0.2,
                    }
                }
            }
        }
        mock_post.return_value = mock_response

        result = emotion_detector("I am furious and angry.")

        self.assertEqual(result["dominant_emotion"], "anger")
        self.assertAlmostEqual(result["anger"], 0.8)

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_dominant_disgust(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "emotion": {
                "document": {
                    "emotion": {
                        "anger": 0.2,
                        "disgust": 0.9,
                        "fear": 0.1,
                        "joy": 0.06,
                        "sadness": 0.15,
                    }
                }
            }
        }
        mock_post.return_value = mock_response

        result = emotion_detector("This is disgusting and revolting.")

        self.assertEqual(result["dominant_emotion"], "disgust")
        self.assertAlmostEqual(result["disgust"], 0.9)

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_dominant_fear(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "emotion": {
                "document": {
                    "emotion": {
                        "anger": 0.12,
                        "disgust": 0.08,
                        "fear": 0.84,
                        "joy": 0.05,
                        "sadness": 0.17,
                    }
                }
            }
        }
        mock_post.return_value = mock_response

        result = emotion_detector("I am terrified and afraid of what happens next.")

        self.assertEqual(result["dominant_emotion"], "fear")
        self.assertAlmostEqual(result["fear"], 0.84)

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_dominant_joy(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "emotion": {
                "document": {
                    "emotion": {
                        "anger": 0.04,
                        "disgust": 0.02,
                        "fear": 0.01,
                        "joy": 0.88,
                        "sadness": 0.09,
                    }
                }
            }
        }
        mock_post.return_value = mock_response

        result = emotion_detector("I feel happy and excited today.")

        self.assertEqual(result["dominant_emotion"], "joy")
        self.assertAlmostEqual(result["joy"], 0.88)

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_dominant_sadness(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "emotion": {
                "document": {
                    "emotion": {
                        "anger": 0.14,
                        "disgust": 0.07,
                        "fear": 0.16,
                        "joy": 0.05,
                        "sadness": 0.82,
                    }
                }
            }
        }
        mock_post.return_value = mock_response

        result = emotion_detector("I feel lonely and heartbroken after losing my friend.")

        self.assertEqual(result["dominant_emotion"], "sadness")
        self.assertAlmostEqual(result["sadness"], 0.82)

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_bad_request_returns_none_values(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        result = emotion_detector("I am very happy.")

        self.assertIsNone(result["anger"])
        self.assertIsNone(result["disgust"])
        self.assertIsNone(result["fear"])
        self.assertIsNone(result["joy"])
        self.assertIsNone(result["sadness"])
        self.assertIsNone(result["dominant_emotion"])


if __name__ == "__main__":
    unittest.main()
