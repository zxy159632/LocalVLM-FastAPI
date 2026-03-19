from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8001/v1",
    api_key="EMPTY"
)

MODEL_NAME = "qwen3.5-int4"


def chat_text(prompt: str, max_tokens: int = 256, temperature: float = 0.7, stream: bool = False):
    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        stream=stream
    )
    # 如果是流式请求，直接返回生成器对象；否则返回完整的字符串内容
    if stream:
        return resp
    return resp.choices[0].message.content


def chat_image(prompt: str, image_base64: str, max_tokens: int = 256, temperature: float = 0.7, stream: bool = False):
    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_base64}}
                ]
            }
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        stream=stream
    )
    if stream:
        return resp
    return resp.choices[0].message.content