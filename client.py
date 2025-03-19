
from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

completion = client.chat.completions.create(
  model="deepseek/deepseek-r1:free",
  messages=[
    {
      "role": "user",
      "content": "what is coding?"
    }
  ]
)
print(completion.choices[0].message.content)

# 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