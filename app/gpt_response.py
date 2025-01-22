from g4f.client import Client



user_contexts = {}
def get_response(user_id: int, user_message: str) -> str:
    max_length = 15
    if user_id not in user_contexts:
        user_contexts[user_id] = [{"role": "user", "content": 'Теперь ты мой ассистент'}]

    user_contexts[user_id].append({"role": "user", "content": user_message})
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=user_contexts[user_id],
        web_search = False
    )
    gpt_response = response.choices[0].message.content
    user_contexts[user_id].append({"role": "assistant", "content": gpt_response})
    if len(user_contexts[user_id]) > max_length:
        user_contexts[user_id] = user_contexts[user_id][-max_length:]

    return gpt_response


def get_image(user_prompt: str):
    client = Client()
    response = client.images.generate(
        model="flux",
        prompt=user_prompt,
        response_format="url"
    )

    image_url = response.data[0].url
    return image_url