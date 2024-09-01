import json
import re
import textwrap

import pandas as pd
import seaborn as sns
import tabulate
from matplotlib import pyplot as plt

sns.set_theme()


def wrap_text(text, width=40):
    texts = text.split("\n")
    return "\n".join(["\n".join(textwrap.wrap(text, width=width)) for text in texts])


with open("angle_results.jsonl") as f:
    d = [json.loads(el) for el in f]

with open("human_angles.json") as f:
    human = json.load(f)
hx, hy = list(zip(*human))

d = pd.DataFrame(d)


def extract_angle(row):
    text = row.response["choices"][0]["message"]["content"]
    matches = re.findall(r"<angle>(\d+)</angle>", text)
    if matches:
        return int(matches[-1])
    try:
        text = [el.strip() for el in text.strip().split("\n") if "Angle:" in el]
        text = text[-1].replace("Angle", "").replace(":", "").strip()
        return float(text)
    except Exception:
        return None


def extract_angle_fallback(row):
    return extract_angle(row) or row.angle + 180


models = d.model.unique()


d["guessed_angle"] = d.apply(extract_angle_fallback, axis=1)
d["guessed_angle_nullable"] = d.apply(extract_angle, axis=1)
d["error"] = (d.angle - d.guessed_angle).abs()

avg_error_df = d.groupby(["model", "contexts", "temp"])["error"].mean().reset_index()
markdown_table = tabulate.tabulate(
    avg_error_df, headers="keys", tablefmt="pipe", floatfmt=".2f", showindex="never"
)

best_temps_and_contexts = {}
for m in models:
    md = avg_error_df[avg_error_df.model == m].reset_index()
    min_vals = md.iloc[md.error.idxmin()]
    best_temps_and_contexts[m] = (min_vals.temp, min_vals.contexts)

f, ax = plt.subplots(figsize=(11.69 / 1.5, 8.27 / 1.5), dpi=300)
ax.plot([0, 360], [0, 360])

markers = ["*", "P", "o", "p"]
for m, mark in zip(models, markers):
    md = d[d.model == m]
    best_result = md[
        (md.temp == best_temps_and_contexts[m][0])
        & (md.contexts == best_temps_and_contexts[m][1])
    ]
    ax.plot(
        best_result.angle, [el for el in best_result.guessed_angle_nullable if el], mark
    )
ax.scatter(hx, hy, marker="$\heartsuit$")

for c in [17, 293, 165, 350]:
    ax.plot([c, c], [0, 360], "--", color="black", alpha=0.3)

print(sum(abs(x - y) for x, y in human) / len(human))
ax.legend(["Correct"] + models.tolist() + ["Wifey"] + ["Context"])
f.tight_layout()
f.savefig("all_simple.png")

f, ax = plt.subplots(figsize=(11.69 / 1.5, 8.27 / 1.5), dpi=300)
for m, mark in zip(models, markers):
    md = d[d.model == m]
    ax.plot(md.angle, md.guessed_angle, mark)
ax.plot(range(360), range(360))
f.savefig("all_simple_no_best.png")
