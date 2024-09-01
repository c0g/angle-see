import itertools
import json
import io
from dotenv import load_dotenv
import base64

from tqdm import tqdm

from angle_see.general import encode_image, cached_completion
from angle_see.generate_clock import draw_clock

load_dotenv()  # take environment variables from .env.

def encode_image(image):
    f = io.BytesIO()
    image.save(f, format="PNG")
    f.flush()
    return base64.b64encode(f.getvalue())


def turn(hour, minute, answer=None, prompt_prefix=""):
    image = draw_clock(resolution=512,
                       hour_hand_length=100,
                       minute_hand_length=200,
                       hour_color=(255, 0, 0),
                       minute_color=(0, 0, 255),
                       hour=hour,
                       minute=minute)

    base64_image = encode_image(image)
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt_prefix + "What time is the clock in this image showing?",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image.decode('utf-8')}"
                    },
                },
            ],
        }
    ]

    if answer:
        messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )
    return messages


prompt = [
    {
        "role": "system",
        "content": """Tell the time on the clock in this image. The hour hand is short, fat and red, and the minute hand is longer, thinner, and blue.
You can use as many tokens as you need to reason, but always give a final numerical answer in hours and minutes inside <time> tags, like this: 
<time>12:34</time>""", 
    },
]

known = (
    turn(
        12, 00,
        """The hands are in line with each other and pointing straight up, so the time is 12:00.
<time>12:00</time>
"""
    )
    + turn(
        9, 30,
        """The hour hand is halfway between 9 and 10, and the minute hand is pointing straight down, so the time is 9:30.
<time>9:30</time>
"""
    )
    + turn(
        3, 20,
        """The hour hand is about a third of the way from 3 to 4, and the minute hand is slightly further than horizontal, so the time is 3:20.
<time>3:20</time>
"""
    )
    + turn(
        6, 43,
        """The hour hand is past halfway between 6 and 7, and the minute hand is pointing slightly past 43 minutes after 6, so the time is 6:43.
<time>6:43</time>
"""
    )
)


args = list(
    itertools.product(
        [
            # ("claude-3-5-sonnet-20240620", 0.8, 8),
            # ("gpt-4o", 0.2, 2),
            ("gemini/gemini-1.5-pro-latest", 8),
            # ("gemini/gemini-1.5-flash-latest", 0.4, 8)
        ],
        [0.2, 0.4, 0.6, 0.8, 1.0],
        [0, 1, 2], # 3 reps for each model
        [(3, 45), (10, 10), (12, 1), (6, 37)], # times
    )
)


results = []
results = []
for (model, known_slice), temp, rep, time in tqdm(args):
    these_messages = prompt + known[:known_slice] + turn(time[0], time[1], prompt_prefix="Okay! ")
    response = cached_completion(model, messages=these_messages, temp=temp, rep=rep)
    text = response["choices"][0]["message"]["content"]
    results.append(
        {
            "model": model,
            "time": time,
            "temp": temp,
            "rep": rep,
            "contexts": known_slice,
            "messages": these_messages,
            "response": response,
        }
    )
    with open("time_results.jsonl", "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
