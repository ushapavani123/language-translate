import speech_recognition as spr
from googletrans import Translator
from gtts import gTTS
import os
import platform


# Function to capture voice and recognize text
def recognize_speech(recog, source):
    try:
        recog.adjust_for_ambient_noise(source, duration=0.2)
        audio = recog.listen(source)
        recognized_text = recog.recognize_google(audio)
        return recognized_text
    except spr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
        return None
    except spr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None


# Main script
if __name__ == "__main__":
    # Initialize Recognizer and Microphone
    recog1 = spr.Recognizer()
    mc = spr.Microphone()

    # Get target language input
    target_language_input = input("Enter the target language (e.g., 'Hindi', 'Telugu', 'Tamil'): ").strip()

    # Mapping user input to language codes
    language_map = {
        'Hindi': 'hi',
        'Telugu': 'te',
        'Kannada': 'kn',
        'Tamil': 'ta',
        'Malayalam': 'ml',
        'Bengali': 'bn'
    }

    # Check if the target language is valid
    if target_language_input not in language_map:
        print(f"Invalid language: {target_language_input}. Exiting.")
    else:
        target_language_code = language_map[target_language_input]

        # Capture voice and translate
        with mc as source:
            print("Speak now for language detection and translation...")
            MyText = recognize_speech(recog1, source)

        # If valid speech is captured
        if MyText:
            print(f"Recognized Text: {MyText}")

            # Initialize Translator
            translator = Translator()

            try:
                # Detect the language of the recognized text
                detected_language = translator.detect(MyText).lang
                print(f"Detected Language: {detected_language}")

                # Translate the recognized sentence into the target language
                text_to_translate = translator.translate(MyText, src=detected_language, dest=target_language_code)
                translated_text = text_to_translate.text
                print(f"Translated Text in {target_language_input}: {translated_text}")

                # Ensure output folder exists
                if not os.path.exists('outputs'):
                    os.makedirs('outputs')

                # Generate audio for the translated text
                audio_file = f"outputs/captured_voice_{target_language_input}.mp3"
                speak = gTTS(text=translated_text, lang=target_language_code, slow=False)
                speak.save(audio_file)

                # Play the audio file based on the operating system
                if platform.system() == "Windows":
                    os.system(f"start {audio_file}")
                elif platform.system() == "Darwin":  # macOS
                    os.system(f"open {audio_file}")
                else:  # Linux or others
                    os.system(f"xdg-open {audio_file}")
            except Exception as e:
                print(f"An error occurred during translation: {e}")
        else:
            print("No speech input detected. Exiting.")
