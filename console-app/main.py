from openai import OpenAI

client = OpenAI(
    api_key="TODO"
)


def send_prompt(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ]
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit"]:
            break

        response = send_prompt(user_input)
        print(f"ChatGPT: {response}")
