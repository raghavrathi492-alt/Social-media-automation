import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Social Media Automation", layout="wide")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("social_media_posts.csv")

df = load_data()

# -----------------------------
# SESSION STATE (for history)
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Generate Post", "Analytics", "History"])

# -----------------------------
# HOME PAGE
# -----------------------------
if page == "Home":
    st.title("🚀 AI Social Media Automation")

    st.subheader("Generate, optimize and simulate social media posts using AI")

    st.markdown("""
    ### 🔹 How it works:
    1. Enter your post idea  
    2. Generate AI content  
    3. Simulate posting  
    4. View analytics  
    """)

# -----------------------------
# GENERATE POST PAGE
# -----------------------------
elif page == "Generate Post":

    st.title("✍️ Generate Social Media Post")

    topic = st.text_input("Enter Topic")
    platform = st.selectbox("Platform", ["Instagram", "LinkedIn", "Twitter"])
    tone = st.selectbox("Tone", ["Professional", "Casual", "Funny"])
    audience = st.text_input("Target Audience")
    hashtag_count = st.slider("Number of Hashtags", 3, 10, 5)

    # -----------------------------
    # GENERATE BUTTON
    # -----------------------------
    if st.button("Generate Post"):

        if topic == "":
            st.warning("Please enter a topic")
        else:
            # Simple AI logic (can upgrade later)
            post_text = f"{topic} 🚀"
            caption = f"This is a {tone.lower()} post for {audience}"
            hashtags = " ".join([f"#tag{i}" for i in range(1, hashtag_count + 1)])
            cta = "👉 Follow us for more updates!"

            st.session_state.generated = {
                "post": post_text,
                "caption": caption,
                "hashtags": hashtags,
                "cta": cta,
                "platform": platform
            }

    # -----------------------------
    # SHOW OUTPUT
    # -----------------------------
    if "generated" in st.session_state:

        st.subheader("📢 Generated Content")

        st.write("**Post Text:**", st.session_state.generated["post"])
        st.write("**Caption:**", st.session_state.generated["caption"])
        st.write("**Hashtags:**", st.session_state.generated["hashtags"])
        st.write("**CTA:**", st.session_state.generated["cta"])

        col1, col2 = st.columns(2)

        # -----------------------------
        # SIMULATE POST
        # -----------------------------
        with col1:
            if st.button("🚀 Simulate Post Now"):
                st.success(f"Posted successfully on {st.session_state.generated['platform']}")

                # Save to history
                st.session_state.history.append({
                    "time": datetime.datetime.now(),
                    "post": st.session_state.generated["post"],
                    "platform": st.session_state.generated["platform"]
                })

        # -----------------------------
        # SAVE DRAFT
        # -----------------------------
        with col2:
            if st.button("💾 Save Draft"):
                st.info("Post saved as draft!")

# -----------------------------
# ANALYTICS PAGE
# -----------------------------
elif page == "Analytics":

    st.title("📊 Analytics Dashboard")

    st.subheader("Dataset Preview")
    st.dataframe(df)

    # -----------------------------
    # Engagement by Platform
    # -----------------------------
    st.subheader("Engagement by Platform")

    df["engagement"] = df["likes"] + df["comments"] + df["shares"]
    platform_data = df.groupby("platform")["engagement"].sum()

    fig1, ax1 = plt.subplots()
    platform_data.plot(kind="bar", ax=ax1)
    st.pyplot(fig1)

    # -----------------------------
    # Engagement by Hour
    # -----------------------------
    st.subheader("Engagement by Hour")

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour

    hour_data = df.groupby("hour")["engagement"].mean()

    fig2, ax2 = plt.subplots()
    hour_data.plot(ax=ax2)
    st.pyplot(fig2)

    # -----------------------------
    # Keyword Chart
    # -----------------------------
    st.subheader("Keyword Frequency")

    text = " ".join(df["post_text"])
    words = text.split()

    word_freq = pd.Series(words).value_counts().head(10)

    fig3, ax3 = plt.subplots()
    word_freq.plot(kind="bar", ax=ax3)
    st.pyplot(fig3)

# -----------------------------
# HISTORY PAGE
# -----------------------------
elif page == "History":

    st.title("📜 Post History")

    if len(st.session_state.history) == 0:
        st.info("No posts yet")
    else:
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df)

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Instagram Caption Generator", page_icon="📸")

# Read OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📸 Instagram Caption Generator")
st.write("Generate Instagram captions using OpenAI.")

topic = st.text_input("What is the post about?", placeholder="Example: launching my handmade candle brand")
tone = st.selectbox(
    "Choose a tone",
    ["Casual", "Professional", "Funny", "Luxury", "Inspirational", "Trendy"]
)
audience = st.text_input("Target audience", placeholder="Example: young entrepreneurs")
include_hashtags = st.checkbox("Include hashtags", value=True)
emoji_level = st.selectbox("Emoji style", ["None", "Low", "Medium", "High"], index=2)
caption_length = st.selectbox("Caption length", ["Short", "Medium", "Long"], index=1)
call_to_action = st.text_input("Call to action (optional)", placeholder="Example: Follow for more tips")

if st.button("Generate captions"):
    if not topic.strip():
        st.warning("Please enter what the post is about.")
    else:
        prompt = f"""
You are an expert Instagram copywriter.

Write 3 different Instagram captions for this post.

Post topic: {topic}
Tone: {tone}
Target audience: {audience if audience.strip() else "general audience"}
Include hashtags: {"Yes" if include_hashtags else "No"}
Emoji style: {emoji_level}
Caption length: {caption_length}
Call to action: {call_to_action if call_to_action.strip() else "None"}

Requirements:
- Make the captions engaging and natural.
- Keep each caption distinct from the others.
- Format the output clearly as:
Caption 1:
...
Caption 2:
...
Caption 3:
...
"""

        with st.spinner("Generating captions..."):
            try:
                response = client.responses.create(
                    model="gpt-5.4",
                    input=prompt
                )

                st.subheader("Generated Captions")
                st.write(response.output_text)

            except Exception as e:
                st.error(f"Error: {e}")
