import itertools
import json

from dotenv import load_dotenv
from tqdm import tqdm
from datetime import datetime
from angle_see.general import cached_completion, encode_image
from angle_see.generate_clock import draw_clock
from angle_see.realistic_clocks.clock_generator import generate_clock_image

load_dotenv()  # take environment variables from .env.


def turn(design, hour, minute, answer=None, prompt_prefix="", ):
    # image = draw_clock(
    #     resolution=512,
    #     hour_hand_length=100,
    #     minute_hand_length=200,
    #     hour_color=(255, 0, 0),
    #     minute_color=(0, 0, 255),
    #     hour=hour,
    #     minute=minute,
    # )
    time = datetime.strptime(f"{hour}:{minute}", "%H:%M")
    image = generate_clock_image(
        time=time,
        design=design,
        face_color="#FFFFFF",
        hand_color="#000000",
    )

    base64_image = encode_image(image)
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt_prefix
                    + "What time is the clock in this image showing?",
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
        "content": """Tell the time on the clock in this image.
        
        You can use as many tokens as you need to reason, but always give a final numerical answer in hours and minutes inside <time> tags, like this: 
<time>12:34</time>""",
    },
]

def known_for_style(design):
    return (
        turn(
            design,
            12,
            00,
        """The hands are in line with each other and pointing straight up, so the time is 12:00.
<time>12:00</time>
""",
    )
    + turn(
        design,
        9,
        30,
        """The hour hand is halfway between 9 and 10, and the minute hand is pointing straight down, so the time is 9:30.
<time>9:30</time>
""",
    )
    + turn(
        design,
        3,
        20,
        """The hour hand is about a third of the way from 3 to 4, and the minute hand is slightly further than horizontal, so the time is 3:20.
<time>3:20</time>
""",
    )
    + turn(
        design,
        6,
        43,
        """The hour hand is past halfway between 6 and 7, and the minute hand is pointing slightly past 43 minutes after 6, so the time is 6:43.
<time>6:43</time>
""",
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
        # [0.2, 0.4, 0.6, 0.8, 1.0],
        [0.2, 0.6, 1.0],
        [0, 1, 2],  # 3 reps for each model
        [(3, 45), (10, 10), (12, 1), (6, 37)],  # times
        ["classic", "modern", "minimalist", "vintage", "numbered", "roman"],
    )
)


results = []
results = []
for (model, known_slice), temp, rep, time, design in tqdm(args):
    these_messages = (
        prompt + known_for_style(design)[:known_slice] + turn(design, time[0], time[1], prompt_prefix="Okay! ")
    )
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
            "design": design,
        }
    )
    with open("time_results.jsonl", "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
