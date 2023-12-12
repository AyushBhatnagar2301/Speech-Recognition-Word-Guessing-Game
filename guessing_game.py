import random
import time
import speech_recognition as sr

def recognize_speech(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio), None
    except sr.UnknownValueError:
        return None, "Unable to recognize speech"
    except sr.RequestError:
        return None, "API unavailable"

def get_user_guess(recognizer, microphone, prompt_limit=5):
    for _ in range(prompt_limit):
        print("Speak now:")
        guess, error = recognize_speech(recognizer, microphone)
        if guess:
            return guess.lower()
        print(f"I didn't catch that. {error or 'Please try again.'}")
    return None

def main():
    WORDS = ["apple", "banana", "grape", "orange", "mango", "lemon"]
    NUM_GUESSES = 3

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    word = random.choice(WORDS)

    instructions = (
        "I'm thinking of one of these words:\n"
        f"{', '.join(WORDS)}\n"
        f"You have {NUM_GUESSES} tries to guess which one.\n"
    )

    print(instructions)
    time.sleep(10)

    for i in range(NUM_GUESSES):
        print(f'Guess {i+1}. Speak!')
        user_guess = get_user_guess(recognizer, microphone)
        
        if user_guess is None:
            print("Exiting due to too many failed attempts.")
            break

        print(f"You said: {user_guess}")

        if user_guess == word.lower():
            print(f"Correct! You win! The word was {word}.")
            break
        else:
            print("Incorrect. Try again.\n")
    else:
        print(f"Sorry, you lose! The word was {word}.")

if __name__ == "__main__":
    main()
