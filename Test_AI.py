from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

completion = client.chat.completions.create(
  extra_body={},
  model="deepseek/deepseek-chat-v3.1:free",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)
print(completion.choices[0].message.content)