import azure.cognitiveservices.speech as speechsdk

def text_to_speech(speech_key, service_region):
    """Takes user input text and converts it to speech using Microsoft Azure"""
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    text = input("Enter text to speak: ")  # Taking user input

    result = speech_synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesis successful.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("Speech synthesis canceled:", result.cancellation_details)

# Example usage:
SPEECH_KEY = "F9Gcgcr3uBODrscmhrMUEaorbV6WF9H6bqc4kghYsNqvcux9ZavxJQQJ99BCACYeBjFXJ3w3AAAYACOGYQHZ"
SERVICE_REGION = "eastus"

text_to_speech(SPEECH_KEY, SERVICE_REGION)
