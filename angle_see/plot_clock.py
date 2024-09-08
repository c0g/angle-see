import base64
import io
from datetime import datetime
import json
import re
from PIL import Image
import numpy as np
# from PyPDF2 import PdfMerger
# import base64
import textwrap

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from angle_see.realistic_clocks.clock_generator import generate_clock_image

sns.set_theme()


def wrap_text(text, width=40):
    texts = text.split("\n")
    return "\n".join(["\n".join(textwrap.wrap(text, width=width)) for text in texts])


with open("time_results.jsonl") as f:
    d = [json.loads(el) for el in f]

d = pd.DataFrame(d)


def extract_time(row):
    text = row.response["choices"][0]["message"]["content"]
    matches = re.findall(r"<time>(\d+):(\d+)</time>", text)
    if matches:
        h, m = matches[-1]
        return float(h), float(m)


models = d.model.unique()

d["guessed_time"] = d.apply(extract_time, axis=1)
d["absolute_guessed_time"] = d["guessed_time"].apply(lambda x: x[0] * 60 + x[1])
d["absolute_time"] = d["time"].apply(lambda x: x[0] * 60 + x[1])
d["time_error"] = (d["absolute_time"] - d["absolute_guessed_time"]).abs()

avg_error_df = (
    d.groupby(["model", "contexts", "temp", "design"])["time_error"].mean().reset_index()
)

md = avg_error_df.reset_index()
min_vals = md.iloc[md.time_error.idxmin()]
print(min_vals.temp, min_vals.contexts, min_vals.design)

# exit()
# import pdb; pdb.set_trace()
# only plot the best temperature
plt.figure(figsize=(11.69, 8.27), dpi=300)
markers = ["o", "s", "D", "P", "*", "X", "d", "p", "h", "H", "v", "^", "<", ">"]
for marker, design in enumerate(d.design.unique()):
    dd = d[d.temp == min_vals.temp]
    dd = dd[dd.design == design]
    print(dd.time_error.mean())
    plt.scatter(dd.absolute_time, dd.absolute_guessed_time, marker=markers[marker], label=design)
plt.plot(dd.absolute_time, dd.absolute_time, label="Correct")
plt.legend()
# convert ticks to h:m from absolute time
tick_time = np.linspace(d.absolute_time.min(), d.absolute_time.max(), 7)
plt.xticks(tick_time, [f"{int(x // 60)}:{int(x % 60):02d}" for x in tick_time])
plt.xlabel("Time")
plt.yticks(tick_time, [f"{int(x // 60)}:{int(x % 60):02d}" for x in tick_time])
plt.ylabel("Guessed time")
plt.tight_layout()
plt.savefig("time_results.png")

# exit()

# for _, row in d.iterrows():

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

for _, row in d[d.temp == min_vals.temp].iterrows():
    # continue
    print(row.time)
    print(row.guessed_time)
    print(row.response["choices"][0]["message"]["content"])
    image_b64 = row['messages'][-1]['content'][-1]['image_url']['url'].replace('data:image/png;base64,', '')
    clock = Image.open(io.BytesIO(base64.b64decode(image_b64)))
    # image is 800x800, extend 200 pixels downwards
    image = Image.new("RGB", (800, 1000), (255, 255, 255))
    image.paste(clock, (0, 0))

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("SFCompactRounded.ttf",26)
    response = "\n".join(
        row.response["choices"][0]["message"]["content"].split("\n")[:-2]
    )
    wrapped_response = wrap_text(response, width=60)
    draw.text((400, 800), wrapped_response,(0,0,0),font=font, align="center", anchor="ma")
    image.save(f"clock_{row.time[0]}_{row.time[1]}_{row.rep}_{row.design}.png")

# render examples of the clocks
images = []
for design in d.design.unique():
    time = datetime.strptime("10:10", "%H:%M")
    image = generate_clock_image(
        time=time,
        design=design,
        face_color="#FFFFFF",
        hand_color="#000000",
    )
    images.append(image)
# plot the clocks on the same row
big_image = Image.new("RGB", (800 * 6, 900), (255, 255, 255))
draw = ImageDraw.Draw(big_image)
font = ImageFont.truetype("SFCompactRounded.ttf",70)
for i, (design, image) in enumerate(zip(d.design.unique(), images)):
    draw.text((i * 800 + 400, 810), design,(0,0,0), font=font, align="center", anchor="ma")
    big_image.paste(image, (i * 800, 0))
big_image.save("clocks.png")