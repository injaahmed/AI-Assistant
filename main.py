import ollama

messages = []

print("AI Agent Started!")

while True:
    user = input("You: ")

    if user.lower() == "exit":
        break

    messages.append(
        {
            "role": "user",
            "content": user
        }
    )

    response = ollama.chat(
        model="phi3",
        messages=messages
    )

    ai_reply = response["message"]["content"]

    messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )

    print("AI:", ai_reply)