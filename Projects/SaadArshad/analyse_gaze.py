"""Reproduce descriptive summaries for Lorenzoni & Dalmaso (2026), Exp. 1.

Run beside Results_Exp1.csv to create the de-identified course data file.
Then run beside gaze_exp1_trials.csv to reproduce the same summaries.
Requires pandas. The presentation builder uses these exact JSON values for
its editable chart and table. This script does not fit the authors' GLMM.
"""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parent
raw_path = ROOT / 'Results_Exp1.csv'
data_path = ROOT / 'gaze_exp1_trials.csv'
if raw_path.exists():
    raw = pd.read_csv(raw_path, low_memory=False)
    trials = raw.loc[(raw['condizione'] == 'esperimento') &
                     ~raw['participant'].astype(str).isin(['872665','159319'])].copy()
    ids = {x: f'P{i+1:03d}' for i,x in enumerate(sorted(trials['participant'].unique()))}
    d = pd.DataFrame({
        'participant': trials['participant'].map(ids),
        'stimulus': trials['tipo_stimolo'].map({'freccia':'Arrows','sguardo':'Gaze'}),
        'fixation': trials['tipo_fissazione'].map({'croce':'Cross','oggetto':'Object'}),
        'congruency': trials['congruenza'].map({'c':'Congruent','i':'Incongruent'}),
        'correct': trials['target.corr'],
        'rt_ms': pd.to_numeric(trials['target.rt'],errors='coerce') * 1000,
    })
    d.to_csv(data_path,index=False)
else:
    d = pd.read_csv(data_path)

# Authors' experimental trials, correct responses, and strict RT cut-offs.
clean = d.loc[(d['correct'] == 1) & d['rt_ms'].between(200,1300,inclusive='neither')].copy()
# Average within each participant before computing group summaries.
p = clean.groupby(['participant','stimulus','fixation','congruency'],observed=True)['rt_ms'].mean()
g = p.groupby(['stimulus','fixation','congruency'],observed=True)
summary = g.agg(M='mean',SD='std',N='count').reset_index()
summary.to_csv(ROOT/'gaze_summary.csv',index=False)
p.rename('mean_rt_ms').reset_index().to_csv(ROOT/'gaze_participant_means.csv',index=False)

rows=[]
for stimulus in ['Arrows','Gaze']:
    for fixation in ['Cross','Object']:
        z=summary[(summary.stimulus==stimulus)&(summary.fixation==fixation)].set_index('congruency')
        c=z.loc['Congruent']; i=z.loc['Incongruent']
        rows.append(dict(stimulus=stimulus,fixation=fixation,n=int(c.N),
                         congruent=float(c.M),congruent_sd=float(c.SD),
                         incongruent=float(i.M),incongruent_sd=float(i.SD),
                         effect=float(i.M-c.M)))
pd.DataFrame(rows).to_csv(ROOT/'gaze_table.csv',index=False)
report={'participants':int(d.participant.nunique()),'experimental_trials':len(d),
        'retained_trials':len(clean),'rows':rows,
        'raw_rows':17732,'raw_columns':100,
        'participant_mean_cells':len(p)}
(ROOT/'summary.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))

# Reproducible standalone SVG figure (standard-library SVG, no extra packages).
# The presentation uses an editable chart with the same values and axis limits.
from xml.sax.saxutils import escape
W,H=1000,620
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       '<rect width="100%" height="100%" fill="white"/>']
def text(x,y,label,size=20,anchor='start'):
    parts.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Arial,sans-serif" font-size="{size}" fill="#111111">{escape(str(label))}</text>')
for tick in range(0,701,100):
    y=500-tick/700*390
    parts.append(f'<line x1="95" y1="{y}" x2="960" y2="{y}" stroke="#dddddd"/>')
    text(80,y+6,tick,18,'end')
text(95,40,'Experiment 1: mean reaction time (ms)',26)
for k,row in enumerate(rows):
    x=180+k*210
    for offset,key,color in [(-38,'congruent','#4c4c4c'),(18,'incongruent','#7c9fbf')]:
        height=row[key]/700*390
        parts.append(f'<rect x="{x+offset}" y="{500-height}" width="48" height="{height}" fill="{color}"/>')
        text(x+offset+24,490-height,f'{row[key]:.1f}',17,'middle')
    text(x+15,535,row['stimulus'],20,'middle')
    text(x+15,562,row['fixation'],18,'middle')
for x,label,color in [(300,'Congruent','#4c4c4c'),(550,'Incongruent','#7c9fbf')]:
    parts.append(f'<rect x="{x}" y="70" width="20" height="20" fill="{color}"/>')
    text(x+30,88,label,19)
text(95,603,'Each participant contributes one mean per condition (N = 60). Descriptive means only.',17)
parts.append('</svg>')
(ROOT/'gaze_figure.svg').write_text('\n'.join(parts),encoding='utf-8')
