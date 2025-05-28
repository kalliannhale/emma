import chainlit as cl
from dotenv import load_dotenv
import os

from llm_agent_demo import DeepSeekAgent

# load our secrets like silk slips 🖤
load_dotenv()

# summon her
deep_agent = DeepSeekAgent(config={"name": "velvet-whisperer"})

# precious user data
user_cache = {}

# questions to woo a soul into bloom 🌸
dreamy_qs = [
    "what kinds of problems make you want to roll your sleeves up and solve them, even when no one’s watching? 🌙",
    "what’s a tech tool, platform, or concept that makes your brain light up like a disco ball? 💿✨",
    "describe your dream collab. who's on the team, what's the mission, and what role do *you* play? 💞",
    "what do you want people to feel when they see your portfolio? respected? inspired? curious? seen? 👀🌷",
    "what soft/personal skills do you feel most proud of, even if they don’t always show up on a résumé? 🧚‍♀️",
    "if you had to write a love letter to your future boss, what would it say about who you are? 💌",
    "what’s a social good initiative, org, or cause you’d be proud to support with your technical powers? 🌍"
]

# cleanse her response of reasoning fluff 🛁
def clean_response(response: str) -> str:
    parts = response.split("<think>", 1)
    if len(parts) > 1:
        response = parts[0] + parts[1].split("</think>")[-1]
    return response.strip()

# summon deepseek with extra grace 🌹
async def call_deepseek(prompt: str) -> str:
    mission = {
        "prompt": prompt,
        "temperature": 0.75,
        "max_tokens": 1024
    }

    result = await deep_agent.run_mission(mission)
    if "result" in result and isinstance(result["result"], dict):
        raw = result["result"].get("choices", [{}])[0].get("message", {}).get("content", "she stayed silent... 🥀")
        return clean_response(raw)
    else:
        return result.get("error", "something mysterious interrupted her flow 💔")

# when the user whispers something sweet 🌙
@cl.on_message
async def main(message: cl.Message):
    user_id = message.author

    if user_id not in user_cache:
        user_cache[user_id] = {
            "stage": "collecting_responses",
            "data": {"answers": []},
            "q_index": 0,
        }

        await cl.Message(content="hey, honey 🍯 proud of you for starting 💖 let’s ease in gently... \n\n" + dreamy_qs[0]).send()
    else:
        stage = user_cache[user_id]["stage"]
        q_index = user_cache[user_id]["q_index"]
        user_data = user_cache[user_id]["data"]

        if stage == "collecting_responses":
            user_data["answers"].append(message.content)
            q_index += 1
            user_cache[user_id]["q_index"] = q_index

            if q_index < len(dreamy_qs):
                await cl.Message(content=dreamy_qs[q_index]).send()
            else:
                user_cache[user_id]["stage"] = "summarizing"
                await cl.Message(content="Wonderful, thank you... 💖 You’ve given me so much beauty to work with. 💌\nLet me distill your essence...").send()

                joined_answers = "\n".join(user_data["answers"])
                summary_prompt = f"""
you are a soulful brand copywriter channeling energy into voice.

given these reflections from a user:

{joined_answers}

write a 2–3 sentence brand statement that captures their essence, values, soft power, and technical intrigue. make it luscious, confident, and true. 💖
"""

                summary = await call_deepseek(summary_prompt)
                user_data["brand_draft"] = summary
                user_cache[user_id]["stage"] = "refining_brand"

                await cl.Message(content=f""" This is just the first shimmer of your essence... ✨:

{summary}

Does it feel right? what should we shift — tone, language, boldness, softness? let’s co-create from here... 🧵""").send()

        elif stage == "refining_brand":
            refinement_prompt = f"""
the user just gave feedback on their brand statement:

original draft:
{user_cache[user_id]["data"]["brand_draft"]}

user said:
{message.content}

please rewrite the brand statement with this new direction in mind. keep it rich, confident, and warm.
"""

            refined = await call_deepseek(refinement_prompt)
            user_cache[user_id]["data"]["brand_draft"] = refined

            await cl.Message(content=f"""🪞 here’s the updated version:

{refined}

would you like to keep refining, or are we ready to move forward into your brand guide? 🌷""").send()

# welcome the darling with a warm whisper 🌸
@cl.on_chat_start
async def welcome():
    await cl.Message(
        content=(
            "hello, beautiful soul. 🌙\n\n"
            "i’m emma — your dream journal, co-creator, and brand whisperer... "
            "you don’t need to know exactly where you’re going just yet. 💖 "
            "we’ll find your essence together. :) \n\n"
            "when you're ready to start, just say hi... 💌"
        )
    ).send()