import json
from matplotlib import pyplot as plt
import pandas as pd
import tabulate
import json
import textwrap
import re

import seaborn as sns
sns.set_theme()

def wrap_text(text, width=40):
    texts = text.split("\n")
    return "\n".join(["\n".join(textwrap.wrap(text, width=width)) for text in texts])

with open("angle_results.jsonl") as f:
    d = [json.loads(el) for el in f]

with open('human_angles.json') as f:
    human = json.load(f)
hx, hy = list(zip(*human))

d = pd.DataFrame(d)

def extract_angle(row):
    text = row.response["choices"][0]["message"]["content"]
    matches = re.findall(r'<angle>(\d+)</angle>', text)
    if matches:
        return int(matches[-1]) 
    try:
        text = [el.strip() for el in text.strip().split("\n") if 'Angle:' in el]
        text = text[-1].replace("Angle", "").replace(":", "").strip()
        return float(text)
    except:
        return None
    
def extract_angle_fallback(row):
    return extract_angle(row) or row.angle + 180

models = d.model.unique()


d["guessed_angle"] = d.apply(extract_angle_fallback, axis=1)
d["guessed_angle_nullable"] = d.apply(extract_angle, axis=1)
d["error"] = (d.angle - d.guessed_angle).abs()

avg_error_df = (
    d.groupby(["model", "contexts", "temp"])["error"].mean().reset_index()
)
markdown_table = tabulate.tabulate(
    avg_error_df, headers="keys", tablefmt="pipe", floatfmt=".2f", showindex="never"
)

best_temps_and_contexts = {}
for m in models:
    md = avg_error_df[avg_error_df.model == m].reset_index()
    min_vals = md.iloc[md.error.idxmin()]
    best_temps_and_contexts[m] = (min_vals.temp, min_vals.contexts)

f, ax = plt.subplots(figsize=(11.69/1.5, 8.27/1.5), dpi=300)
ax.plot([0, 360], [0, 360])

markers = ['*', 'P', 'o', 'p']
for m, mark in zip(models, markers):
    md = d[d.model == m]
    best_result = md[
        (md.temp == best_temps_and_contexts[m][0])
        & (md.contexts == best_temps_and_contexts[m][1])
    ]
    ax.plot(best_result.angle, [el for el in best_result.guessed_angle_nullable if el], mark)
ax.scatter(hx, hy, marker='$\heartsuit$')

for c in [17, 293, 165, 350]:
    ax.plot([c, c], [0, 360], "--", color="black", alpha=0.3)

print(sum(abs(x - y) for x, y in human) / len(human))
ax.legend(['Correct'] +  models.tolist() + ["Wifey"] + ['Context'])
f.tight_layout()
f.savefig('all_simple.png')

f, ax = plt.subplots(figsize=(11.69/1.5, 8.27/1.5), dpi=300)
for m, mark in zip(models, markers):
    md = d[d.model == m]
    ax.plot(md.angle, md.guessed_angle, mark)
ax.plot(range(360), range(360))
f.savefig('all_simple_no_best.png')

# complicated plots here
# for m in models:
#     md = d[d.model == m]
#     result = (
#         md.groupby(["model", "contexts", "temp", "angle"])
#         .agg({"guessed_angle": "mean"})
#         .reset_index()
#     )
#     best_result = result[
#         (result.temp == best_temps_and_contexts[m][0])
#         & (result.contexts == best_temps_and_contexts[m][1])
#     ]
#     # plt.clf()
#     # plt.figure(figsize=(11.69, 8.27), dpi=300)
#     ff, aax = plt.subplots(figsize=(11.69, 8.27), dpi=300)
#     aax.set_title(m)
#     aax.plot(result.angle, result.angle)
#     aax.plot(result.angle, result.guessed_angle, ".")
#     aax.plot(best_result.angle, best_result.guessed_angle, "o")
    
#     aax.set_xlabel("Angle")
#     aax.set_ylabel("Guess")
#     ff.tight_layout()
#     aax.legend(["Correct", "All runs", "Best config"])
#     ff.savefig(f'{m.replace("/", "-")}_simple.png')

# for m in models:
#     md = avg_error_df[avg_error_df.model == m]
#     fig, ax = plt.subplots(figsize=(11.69, 8.27), dpi=300)
#     CS = ax.contour(
#         md.contexts.values.reshape(3, 5) // 2,
#         md.temp.values.reshape(3, 5),
#         md.error.values.reshape(3, 5),
#     )
#     ax.clabel(CS, inline=True, fontsize=10)
#     ax.set_xlabel("Contextual examples")
#     ax.set_ylabel("Temperature")
#     ax.set_title(f"Accuracy vs. temperature and examples, {m}")
#     plt.savefig(f'{m.replace("/", "-")}_surface.png')

# print(avg_error_df)