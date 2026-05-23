import pyttsx3
import ollama

# Voice engine
engine = pyttsx3.init()

print("Voice AI Started!")

while True:

    user = input("You: ")

    if user.lower() == "exit":
        break

    # AI response
    response = ollama.chat(
        model="phi3",
        messages=[
            {
                "role": "user",
                "content": user
            }
        ]
    )

    ai_reply = response["message"]["content"]

    print("AI:", ai_reply)

    # Speak response
    engine.say(ai_reply)
    engine.runAndWait()