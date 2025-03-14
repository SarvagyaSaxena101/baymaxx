import azure.cognitiveservices.speech as speechsdk

def speech_to_text(speech_key, service_region):
    """Converts spoken audio to text using Microsoft Azure Speech-to-Text"""
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Listening... Speak now!")

    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized Text: {result.text}")
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
        return None
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("Speech recognition canceled:", result.cancellation_details)
        return None

# Example usage:
SPEECH_KEY = "F9Gcgcr3uBODrscmhrMUEaorbV6WF9H6bqc4kghYsNqvcux9ZavxJQQJ99BCACYeBjFXJ3w3AAAYACOGYQHZ"
SERVICE_REGION = "eastus"

recognized_text = speech_to_text(SPEECH_KEY, SERVICE_REGION)
print(recognized_text)
