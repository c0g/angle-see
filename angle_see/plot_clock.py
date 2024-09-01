import json
import re

# from xhtml2pdf import pisa
# from PyPDF2 import PdfMerger
# import base64
import textwrap

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from angle_see.generate_clock import draw_clock

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
    d.groupby(["model", "contexts", "temp"])["time_error"].mean().reset_index()
)

md = avg_error_df.reset_index()
min_vals = md.iloc[md.time_error.idxmin()]
print(min_vals.temp, min_vals.contexts)

# only plot the best temperature
d = d[d.temp == min_vals.temp]
print(d.time_error.mean())
plt.figure(figsize=(11.69 / 2, 8.27 / 2), dpi=300)
plt.plot(d.absolute_time, d.absolute_guessed_time, ".")
plt.plot(d.absolute_time, d.absolute_time)
# convert ticks to h:m from absolute time
tick_time = np.linspace(d.absolute_time.min(), d.absolute_time.max(), 7)
plt.xticks(tick_time, [f"{int(x // 60)}:{int(x % 60):02d}" for x in tick_time])
plt.xlabel("Time")
plt.yticks(tick_time, [f"{int(x // 60)}:{int(x % 60):02d}" for x in tick_time])
plt.ylabel("Guessed time")
plt.tight_layout()
plt.savefig("time_results.png")

for _, row in d.iterrows():
    print(row.time)
    print(row.guessed_time)
    print(row.response["choices"][0]["message"]["content"])
    image = draw_clock(
        resolution=512,
        hour_hand_length=100,
        minute_hand_length=200,
        hour_color=(255, 0, 0),
        minute_color=(0, 0, 255),
        hour=row.time[0],
        minute=row.time[1],
    )
    f, ax = plt.subplots(figsize=(6, 6), dpi=300)
    response = "\n".join(
        row.response["choices"][0]["message"]["content"].split("\n")[:-2]
    )
    ax.imshow(image)
    f.text(0.5, 0.03, response, ha="center", va="center", wrap=True, fontsize=12)
    ax.axis("off")
    f.tight_layout()
    f.savefig(f"clock_{row.time[0]}_{row.time[1]}_{row.rep}.png")
