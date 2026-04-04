import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

# Abdullah Mikayılov tərəfindən yaradılan A-ZEKA-ULTRA
client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential("SENIN_GITHUB_TOKENIN"), # Bura xüsusi kod lazımdır
)

system_instruction = "Sən A-ZEKA-ULTRA-san. Abdullah Mikayılov tərəfindən yaradılmış dahi AI-san."

def chat_with_bot(user_input):
    response = client.complete(
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input},
        ],
        model="gpt-4o",
    )
    print(response.choices[0].message.content)

# Test üçün:
chat_with_bot("Salam, özünü təqdim et!")
