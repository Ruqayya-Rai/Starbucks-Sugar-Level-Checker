import os
import streamlit as st
import pandas as pd
import joblib

# Page configuration
st.set_page_config(page_title="Starbucks Sugar Level Checker", page_icon="🍬", layout="centered")

# Load trained model
saved = joblib.load(os.path.join(os.path.dirname(__file__), "sugar_level_classifier.pkl"))
model = saved["model"]
features = saved["features"]
examples = saved["examples"]

LEVELS = {
    "Low": {"color": "#3bceac", "emoji": "😊", "range": "under 25 g",
            "text": "Within the ideal daily sugar limit. A smart pick!", "pos": 16},
    "Medium": {"color": "#ffd23f", "emoji": "😐", "range": "25 – 50 g",
               "text": "Half to a full day's sugar limit in one cup. Enjoy sometimes.", "pos": 50},
    "High": {"color": "#ff6b9d", "emoji": "😵", "range": "over 50 g",
             "text": "More than a FULL day's sugar limit in one cup! Try a smaller size or less syrup.", "pos": 84},
}

# ---------- Styles: Neo-brutalism ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Archivo+Black&display=swap');

html, body, [class*="css"], .stMarkdown, p, label, input, button { font-family: 'Space Grotesk', sans-serif !important; }
.stApp { background-color: #fff6e5;
  background-image: radial-gradient(#11111122 1.2px, transparent 1.2px); background-size: 22px 22px; }
[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 860px; padding-top: 2.2rem; padding-bottom: 3rem; }

.box { background: #fff; border: 3px solid #111; border-radius: 14px; box-shadow: 7px 7px 0 #111; }
.hero { background: #ffd23f; padding: 28px 28px 24px; position: relative; overflow: hidden; }
.hero .tag { display: inline-block; background: #111; color: #fff; font-weight: 700; font-size: 12px;
  letter-spacing: .14em; padding: 6px 12px; border-radius: 8px; transform: rotate(-2deg); }
.hero h1 { font-family: 'Archivo Black', sans-serif; font-size: clamp(36px, 8vw, 64px); line-height: .95;
  color: #111; margin: 16px 0 10px; text-transform: uppercase; }
.hero p { color: #111; font-size: 17px; font-weight: 500; max-width: 560px; margin: 0; }
.hero .candy { position: absolute; right: 18px; top: 14px; font-size: 64px; transform: rotate(14deg); }
.pills { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 20px; }
.pill { background: #fff; border: 3px solid #111; border-radius: 999px; padding: 6px 14px; font-weight: 700;
  box-shadow: 3px 3px 0 #111; color: #111; }

.title { font-family: 'Archivo Black', sans-serif; font-size: 22px; text-transform: uppercase; color: #111;
  margin: 30px 0 14px; }
.title span { background: #111; color: #fff; padding: 2px 10px; border-radius: 6px; margin-right: 8px; }

.stButton > button { border: 3px solid #111 !important; border-radius: 12px !important; color: #111 !important;
  font-weight: 700 !important; box-shadow: 4px 4px 0 #111 !important; transition: transform .12s ease, box-shadow .12s ease;
  padding: 12px 8px !important; }
.stButton > button p { font-weight: 700 !important; font-size: 16px !important; color: #111; }
.stButton > button:hover { transform: translate(-2px, -2px); box-shadow: 6px 6px 0 #111 !important; }
.stButton > button:active { transform: translate(4px, 4px); box-shadow: 0 0 0 #111 !important; }
.st-key-ex0 button { background: #3bceac !important; }
.st-key-ex1 button { background: #ffd23f !important; }
.st-key-ex2 button { background: #ff6b9d !important; }
.st-key-check button { background: #111 !important; color: #fff !important; font-size: 20px !important;
  font-family: 'Archivo Black', sans-serif !important; letter-spacing: .06em; padding: 16px !important;
  box-shadow: 6px 6px 0 #ff6b9d !important; }
.st-key-check button p { color: #fff !important; font-size: 20px !important; font-family: 'Archivo Black', sans-serif !important; }

.st-key-inputs { background: #fff; border: 3px solid #111; border-radius: 14px; box-shadow: 7px 7px 0 #111;
  padding: 22px 24px 10px; margin-bottom: 24px; }
[data-testid="stWidgetLabel"] p { color: #111 !important; font-weight: 700 !important; font-size: 15px !important; }
[data-testid="stNumberInputContainer"] { border: 3px solid #111 !important; border-radius: 10px !important;
  background: #fff6e5 !important; box-shadow: 3px 3px 0 #111 !important; }
[data-testid="stNumberInputField"] { background: transparent !important; color: #111 !important; font-weight: 700; font-size: 17px; }
[data-testid="stNumberInputStepDown"], [data-testid="stNumberInputStepUp"] { background: transparent !important; color: #111 !important; }

.result { margin-top: 26px; padding: 26px; }
.result .head { display: flex; align-items: center; gap: 18px; }
.result .emoji { font-size: 64px; line-height: 1; }
.result .lvl { font-family: 'Archivo Black', sans-serif; font-size: clamp(30px, 7vw, 46px); color: #111; line-height: 1; }
.result .rng { font-weight: 700; color: #111; margin-top: 6px; font-size: 16px; }
.result .txt { margin-top: 16px; font-size: 17px; font-weight: 500; color: #111; }
.meter { position: relative; display: grid; grid-template-columns: 1fr 1fr 1fr; border: 3px solid #111; border-radius: 10px;
  overflow: hidden; margin: 24px 0 8px; height: 30px; }
.meter div { border-right: 3px solid #111; }
.meter div:last-child { border-right: none; }
.marker { position: absolute; top: -14px; transform: translateX(-50%); font-size: 26px; }
.scale { display: grid; grid-template-columns: 1fr 1fr 1fr; font-weight: 700; font-size: 13px; color: #111; text-align: center; }
.actual { margin-top: 18px; background: #fff6e5; border: 3px dashed #111; border-radius: 10px; padding: 12px 14px;
  font-weight: 500; color: #111; }

.footer { margin-top: 34px; background: #111; color: #fff; border-radius: 14px; padding: 18px 22px;
  display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;
  box-shadow: 7px 7px 0 #ff6b9d; border: 3px solid #111; }
.footer .name { font-family: 'Archivo Black', sans-serif; font-size: 22px; text-transform: uppercase; }
.footer .roll { background: #ffd23f; color: #111; font-weight: 700; padding: 6px 14px; border-radius: 8px; border: 2px solid #fff; }
</style>
""", unsafe_allow_html=True)

# ---------- Hero ----------
st.markdown(f"""
<div class="box hero">
<div class="candy">🍬</div>
<div class="tag">DECISION TREE CLASSIFIER</div>
<h1>Sugar<br>Level Checker</h1>
<p>How much sugar is hiding in your Starbucks cup? Enter calories, fat and protein — the model tells you the sugar level.</p>
<div class="pills">
<div class="pill">🎯 {saved['accuracy'] * 100:.0f}% accuracy</div>
<div class="pill">☕ 242 drinks</div>
<div class="pill">📏 WHO limit: 50 g/day</div>
</div>
</div>
""", unsafe_allow_html=True)

# ---------- Session state ----------
defaults = {"cal": 200.0, "fat": 5.0, "protein": 8.0}
if "cal" not in st.session_state:
    for k, v in defaults.items():
        st.session_state[k] = v
    st.session_state.example = None
    st.session_state.show = False


def use_example(i):
    for k, v in zip(defaults, examples[i]["values"]):
        st.session_state[k] = v
    st.session_state.example = i
    st.session_state.show = True


def check_clicked():
    st.session_state.example = None
    st.session_state.show = True


def values_changed():
    st.session_state.example = None
    st.session_state.show = False


# ---------- Examples ----------
st.markdown('<div class="title"><span>01</span>Try a real drink</div>', unsafe_allow_html=True)
cols = st.columns(len(examples))
for i, (col, ex) in enumerate(zip(cols, examples)):
    with col:
        st.button(ex["label"], key=f"ex{i}", on_click=use_example, args=(i,), width="stretch")

# ---------- Inputs ----------
st.markdown('<div class="title"><span>02</span>Or enter your own</div>', unsafe_allow_html=True)
with st.container(key="inputs"):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.number_input("🔥 Calories (kcal)", 0.0, 520.0, step=10.0, key="cal", on_change=values_changed)
    with c2:
        st.number_input("🧈 Total Fat (g)", 0.0, 20.0, step=0.5, key="fat", on_change=values_changed)
    with c3:
        st.number_input("💪 Protein (g)", 0.0, 20.0, step=0.5, key="protein", on_change=values_changed)

st.button("CHECK SUGAR LEVEL →", key="check", on_click=check_clicked, width="stretch")

# ---------- Prediction ----------
if st.session_state.show:
    data = pd.DataFrame([[st.session_state.cal, st.session_state.fat, st.session_state.protein]], columns=features)
    level = model.predict(data)[0]
    info = LEVELS[level]

    actual = ""
    if st.session_state.example is not None:
        ex = examples[st.session_state.example]
        mark = "✅" if ex["actual"] == level else "❌"
        actual = (f'<div class="actual">{mark} Real drink: <b>{ex["drink"]}</b> has <b>{ex["sugar"]} g</b> sugar '
                  f'(<b>{ex["actual"]}</b>)</div>')

    st.markdown(f"""
<div class="box result" style="background:{info['color']}">
<div class="head">
<div class="emoji">{info['emoji']}</div>
<div><div class="lvl">{level.upper()} SUGAR</div><div class="rng">Estimated sugar: {info['range']}</div></div>
</div>
<div class="txt">{info['text']}</div>
<div class="meter">
<div style="background:#3bceac"></div><div style="background:#ffd23f"></div><div style="background:#ff6b9d"></div>
<span class="marker" style="left:{info['pos']}%">⬇️</span>
</div>
<div class="scale"><span>LOW &lt;25 g</span><span>MEDIUM 25–50 g</span><span>HIGH &gt;50 g</span></div>
{actual}
</div>
""", unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("""
<div class="footer">
<div class="name">Ruqayya Shareef</div>
<div class="roll">ROLL NO. 308</div>
</div>
""", unsafe_allow_html=True)
