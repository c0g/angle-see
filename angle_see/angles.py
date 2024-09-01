import itertools
import json

from dotenv import load_dotenv
from tqdm import tqdm

from angle_see.general import cached_completion, encode_image
from angle_see.generate_simple_angle import generate_line_intersection_image

load_dotenv()  # take environment variables from .env.


def turn(angle, answer=None, prompt_prefix=""):
    image = generate_line_intersection_image(angle)
    base64_image = encode_image(image)
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt_prefix + "What angle is this image showing?",
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
        "content": """Estimate the angle shown in the image
The blue angle arc indicates the angle to pay attention to.
Feel free to use as many tokens as you need to reason, but always give a final numerical answer in degrees inside <angle> tags, like this: 
        
Lots of careful reasoning that leads me to think the angle is 10 degrees.
<angle>10</angle>""",
    },
]

known = (
    turn(
        293,
        """The blue angle arc is on the outside of the angle formed by the lines.
One line is pointing horizontally right, and the other is pointing nearly vertically downward, and slightly to the right.
I estimate the angle at 293 degrees.
<angle>293</angle>""",
    )
    + turn(
        17,
        """The blue angle arc is on the inside of the angle formed by the lines.
One line is pointing horizontally right, and the other is angled slightly up, but less than half of the way to 90 degrees.
It looks just less than a quarter of the way, so we could say 17 degrees.
<angle>17</angle>""",
    )
    + turn(
        165,
        """The blue angle arc is on the inside side of the angle formed by the lines, but they are nearly in line with each other.
One line is pointing horizontally right, and the other is pointing almost horizontally left, but is angled slightly upward.
I estimate the angle at 165 degrees.
<angle>165</angle>""",
    )
    + turn(
        350,
        """The blue angle arc is on the obtuse side of the angle formed by the lines.
One line is pointing horizontally right, and the other is angled very slightly down from that line, clockwise.
Since the angle arc is on the outside, this must be around 350 degrees.
<angle>350</angle>""",
    )
)


args = list(
    itertools.product(
        [
            "claude-3-5-sonnet-20240620",
            "gpt-4o",
            "gemini/gemini-1.5-pro-latest",
            "gemini/gemini-1.5-flash-latest",
        ],
        [0, 1, 2],  # 3 reps for each model
        [13, 83, 102, 190, 203, 279, 325],  # angles
        [0.2, 0.4, 0.6, 0.8, 1.0],  # temperatures
        [
            0,
            2,
            8,
        ],  # each example is two (question and answer), so this is giving 0, 1 or 4 examples
    )
)


results = []
results = []
for model, rep, angle, temp, known_slice in tqdm(args):
    these_messages = prompt + known[:known_slice] + turn(angle, prompt_prefix="Okay! ")
    response = cached_completion(model, messages=these_messages, temp=temp, rep=rep)
    text = response["choices"][0]["message"]["content"]
    results.append(
        {
            "model": model,
            "angle": angle,
            "temp": temp,
            "rep": rep,
            "contexts": known_slice,
            "messages": these_messages,
            "response": response,
        }
    )
    with open("angle_results.jsonl", "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
