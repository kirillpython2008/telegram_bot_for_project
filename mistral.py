import logging
from asyncio import run
from os import getenv

from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

MISTRAL_TOKEN = getenv("MISTRAL_TOKEN")

async def ask_mistral(query: str) -> str:
    async with Mistral(api_key=MISTRAL_TOKEN) as mistral:
        res = await mistral.chat.complete_async(model="mistral-small-latest",
                                          messages=[
                                              {
                                                  "content": query,
                                                  "role": "user"
                                              }
                                          ])

        return res.choices[0].message.content


async def positive_or_negative(text_feedback: str) -> bool:
    prompt = (f"представь, что ты не можешь писать ничего кроме True или False,"
                f"напиши True если по твоему мнению этот отзыв является позитивным или False в противном случае:"
                f"{text_feedback}")

    result = await ask_mistral(query=prompt)
    return eval(result)
