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

st.set_page_config(page_title="AI Chat App", page_icon="🤖")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("AI Chat App 🤖")
user_input = st.text_input("Type your question:")

if st.button("Generate"):
    if not user_input.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=user_input
                )
                st.write(response.output_text)
            except Exception as e:
                st.error(f"OpenAI request failed: {e}")
                st.info("Check your OpenAI billing, usage limits, and API key.")

import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Social Media Automation",
    page_icon="📊",
    layout="wide"
)

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "billing_history" not in st.session_state:
    st.session_state.billing_history = [
        {
            "date": "2026-04-01",
            "plan": "Starter",
            "amount": "$9",
            "status": "Paid"
        },
        {
            "date": "2026-03-01",
            "plan": "Starter",
            "amount": "$9",
            "status": "Paid"
        },
        {
            "date": "2026-02-01",
            "plan": "Starter",
            "amount": "$9",
            "status": "Paid"
        }
    ]

# ---------- STYLING ----------
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
}

.sub-title {
    font-size: 1.1rem;
    color: #9aa0a6;
    margin-bottom: 1.5rem;
}

.feature-card {
    padding: 1.2rem;
    border-radius: 18px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 1rem;
}

.metric-card {
    padding: 1rem;
    border-radius: 16px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    text-align: center;
}

.pricing-card {
    padding: 1.4rem;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.04);
    min-height: 360px;
}

.highlight-card {
    padding: 1.4rem;
    border-radius: 20px;
    border: 1px solid #4f46e5;
    background: rgba(79, 70, 229, 0.14);
    min-height: 360px;
}

.small-muted {
    color: #9aa0a6;
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)

# ---------- TOP NAVIGATION ----------
nav1, nav2, nav3, nav4, nav5 = st.columns([2, 1, 1, 1, 1])

with nav1:
    st.markdown('<div class="main-title">Social Media Automation 🚀</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Create content, manage plans, and track your billing in one dashboard.</div>', unsafe_allow_html=True)

with nav2:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"

with nav3:
    if st.button("💳 Pricing", use_container_width=True):
        st.session_state.page = "Pricing"

with nav4:
    if st.button("🧾 Billing History", use_container_width=True):
        st.session_state.page = "Billing History"

with nav5:
    if st.button("⚙️ Account", use_container_width=True):
        st.session_state.page = "Account"

st.divider()

# ---------- HOME PAGE ----------
if st.session_state.page == "Home":
    left, right = st.columns([1.3, 1])

    with left:
        st.markdown("## Welcome back")
        st.write("Manage your social media workflow with a modern dashboard.")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="metric-card"><h3>124</h3><p>Posts Created</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="metric-card"><h3>18</h3><p>Scheduled</p></div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="metric-card"><h3>3</h3><p>Active Plans</p></div>', unsafe_allow_html=True)

        st.markdown("### Quick Actions")
        qa1, qa2, qa3 = st.columns(3)

        with qa1:
            if st.button("✍️ Generate Post", use_container_width=True):
                st.success("This can open your post generation section.")

        with qa2:
            if st.button("📅 Schedule Content", use_container_width=True):
                st.success("This can open your scheduling section.")

        with qa3:
            if st.button("📈 View Analytics", use_container_width=True):
                st.success("This can open your analytics section.")

    with right:
        st.markdown("""
        <div class="feature-card">
            <h3>Platform Highlights</h3>
            <p class="small-muted">Everything important at the top of your homepage.</p>
            <ul>
                <li>Simple top navigation</li>
                <li>Dedicated Pricing page</li>
                <li>Billing History page</li>
                <li>Modern dashboard layout</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.info("Use the top buttons to switch between Home, Pricing, Billing History, and Account.")

# ---------- PRICING PAGE ----------
elif st.session_state.page == "Pricing":
    st.markdown("## 💳 Pricing Plans")
    st.write("Choose the plan that fits your content workflow.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="pricing-card">
            <h3>Starter</h3>
            <h1>$9<span style="font-size:18px;">/month</span></h1>
            <p class="small-muted">Best for beginners</p>
            <hr>
            <p>✅ 20 AI content generations</p>
            <p>✅ Basic analytics</p>
            <p>✅ Single user</p>
            <p>✅ Email support</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Choose Starter", use_container_width=True):
            st.success("Starter plan selected.")

    with col2:
        st.markdown("""
        <div class="highlight-card">
            <h3>Pro</h3>
            <h1>$29<span style="font-size:18px;">/month</span></h1>
            <p class="small-muted">Most popular plan</p>
            <hr>
            <p>✅ 200 AI content generations</p>
            <p>✅ Advanced analytics</p>
            <p>✅ Multi-platform support</p>
            <p>✅ Priority support</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Choose Pro", use_container_width=True):
            st.success("Pro plan selected.")

    with col3:
        st.markdown("""
        <div class="pricing-card">
            <h3>Business</h3>
            <h1>$79<span style="font-size:18px;">/month</span></h1>
            <p class="small-muted">For teams and agencies</p>
            <hr>
            <p>✅ Unlimited AI generations</p>
            <p>✅ Team access</p>
            <p>✅ Premium analytics</p>
            <p>✅ Dedicated support</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Choose Business", use_container_width=True):
            st.success("Business plan selected.")

# ---------- BILLING HISTORY PAGE ----------
elif st.session_state.page == "Billing History":
    st.markdown("## 🧾 Billing History")
    st.write("View your previous payments and subscription records.")

    st.dataframe(
        st.session_state.billing_history,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Current Billing Summary")
    s1, s2, s3 = st.columns(3)
    with s1:
        st.metric("Current Plan", "Starter")
    with s2:
        st.metric("Next Billing Date", "2026-05-01")
    with s3:
        st.metric("Last Payment", "$9")

# ---------- ACCOUNT PAGE ----------
elif st.session_state.page == "Account":
    st.markdown("## ⚙️ Account Settings")
    st.write("Basic account summary section.")

    with st.container():
        st.text_input("Full Name", "Your Name")
        st.text_input("Email", "you@example.com")
        st.selectbox("Current Plan", ["Starter", "Pro", "Business"])
        if st.button("Save Settings"):
            st.success("Settings saved successfully.")

# ---------- FOOTER ----------
st.divider()
st.caption(f"Last updated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")

import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Social Media Automation",
    page_icon="📊",
    layout="wide"
)

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "billing_history" not in st.session_state:
    st.session_state.billing_history = [
        {"date": "2026-04-01", "plan": "Starter", "amount": "$9", "status": "Paid"},
        {"date": "2026-03-01", "plan": "Starter", "amount": "$9", "status": "Paid"},
        {"date": "2026-02-01", "plan": "Starter", "amount": "$9", "status": "Paid"},
    ]

# ---------- STYLING ----------
st.markdown("""
<style>
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
}

.sub-title {
    font-size: 1.05rem;
    color: #9aa0a6;
    margin-bottom: 1.4rem;
}

.metric-card {
    padding: 1rem;
    border-radius: 18px;
    background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.08);
    text-align: center;
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

.feature-card {
    padding: 1.3rem;
    border-radius: 22px;
    background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 8px 28px rgba(0,0,0,0.18);
    margin-bottom: 1rem;
}

.upload-card {
    padding: 1.4rem;
    border-radius: 24px;
    background: linear-gradient(145deg, rgba(80,70,229,0.18), rgba(255,255,255,0.03));
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 10px 30px rgba(0,0,0,0.20);
    margin-top: 1rem;
    margin-bottom: 1rem;
}

.pricing-card {
    padding: 1.4rem;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.04);
    min-height: 360px;
}

.highlight-card {
    padding: 1.4rem;
    border-radius: 20px;
    border: 1px solid #4f46e5;
    background: rgba(79, 70, 229, 0.14);
    min-height: 360px;
}

.small-muted {
    color: #9aa0a6;
    font-size: 0.95rem;
}

.upload-label {
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
}

.preview-box {
    padding: 0.8rem;
    border-radius: 20px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ---------- TOP NAVIGATION ----------
nav1, nav2, nav3, nav4, nav5 = st.columns([2, 1, 1, 1, 1])

with nav1:
    st.markdown('<div class="main-title">Social Media Automation 🚀</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Create content, upload images, manage plans, and track billing in one dashboard.</div>', unsafe_allow_html=True)

with nav2:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"

with nav3:
    if st.button("💳 Pricing", use_container_width=True):
        st.session_state.page = "Pricing"

with nav4:
    if st.button("🧾 Billing History", use_container_width=True):
        st.session_state.page = "Billing History"

with nav5:
    if st.button("⚙️ Account", use_container_width=True):
        st.session_state.page = "Account"

st.divider()

# ---------- HOME PAGE ----------
if st.session_state.page == "Home":
    left, right = st.columns([1.35, 1])

    with left:
        st.markdown("## Welcome back")
        st.write("Build beautiful social media posts with text, image upload, and smart workflow tools.")

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown('<div class="metric-card"><h3>124</h3><p>Posts Created</p></div>', unsafe_allow_html=True)
        with m2:
            st.markdown('<div class="metric-card"><h3>18</h3><p>Scheduled</p></div>', unsafe_allow_html=True)
        with m3:
            st.markdown('<div class="metric-card"><h3>3</h3><p>Active Plans</p></div>', unsafe_allow_html=True)

        st.markdown("### Quick Actions")
        q1, q2, q3 = st.columns(3)

        with q1:
            show_generator = st.button("✍️ Generate Post", use_container_width=True)

        with q2:
            if st.button("📅 Schedule Content", use_container_width=True):
                st.success("Scheduling section can be added here.")

        with q3:
            if st.button("📈 View Analytics", use_container_width=True):
                st.success("Analytics section can be added here.")

        if show_generator:
            st.markdown("""
            <div class="upload-card">
                <div class="upload-label">✨ Create a Post</div>
                <div class="small-muted">Upload an image from your laptop and add post details in a clean creator panel.</div>
            </div>
            """, unsafe_allow_html=True)

            post_title = st.text_input("Post title", placeholder="Example: My Google certificate achievement")
            post_caption = st.text_area("Post caption / idea", placeholder="Write your caption idea here...")
            uploaded_file = st.file_uploader(
                "Upload an image",
                type=["png", "jpg", "jpeg", "webp"]
            )

            if uploaded_file is not None:
                st.markdown('<div class="preview-box">', unsafe_allow_html=True)
                st.image(uploaded_file, caption="Uploaded image preview", use_container_width=True)
                st.success("Image uploaded successfully.")
                st.markdown('</div>', unsafe_allow_html=True)

            cta1, cta2 = st.columns(2)
            with cta1:
                if st.button("🚀 Save Draft", use_container_width=True):
                    st.success("Draft saved successfully.")
            with cta2:
                if st.button("🎉 Publish Preview", use_container_width=True):
                    st.success("Post preview generated.")

    with right:
        st.markdown("""
        <div class="feature-card">
            <h3>Creator Panel</h3>
            <p class="small-muted">Everything is designed to feel cleaner and more premium.</p>
            <ul>
                <li>Upload image from laptop</li>
                <li>Instant image preview</li>
                <li>Modern creator card layout</li>
                <li>Draft and preview actions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.info("Click Generate Post to open the fancy image upload and post creation area.")

# ---------- PRICING PAGE ----------
elif st.session_state.page == "Pricing":
    st.markdown("## 💳 Pricing Plans")
    st.write("Choose the plan that fits your content workflow.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="pricing-card">
            <h3>Starter</h3>
            <h1>$9<span style="font-size:18px;">/month</span></h1>
            <p class="small-muted">Best for beginners</p>
            <hr>
            <p>✅ 20 AI content generations</p>
            <p>✅ Basic analytics</p>
            <p>✅ Single user</p>
            <p>✅ Email support</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Choose Starter", key="starter", use_container_width=True)

    with col2:
        st.markdown("""
        <div class="highlight-card">
            <h3>Pro</h3>
            <h1>$29<span style="font-size:18px;">/month</span></h1>
            <p class="small-muted">Most popular plan</p>
            <hr>
            <p>✅ 200 AI content generations</p>
            <p>✅ Advanced analytics</p>
            <p>✅ Multi-platform support</p>
            <p>✅ Priority support</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Choose Pro", key="pro", use_container_width=True)

    with col3:
        st.markdown("""
        <div class="pricing-card">
            <h3>Business</h3>
            <h1>$79<span style="font-size:18px;">/month</span></h1>
            <p class="small-muted">For teams and agencies</p>
            <hr>
            <p>✅ Unlimited AI generations</p>
            <p>✅ Team access</p>
            <p>✅ Premium analytics</p>
            <p>✅ Dedicated support</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Choose Business", key="business", use_container_width=True)

# ---------- BILLING HISTORY PAGE ----------
elif st.session_state.page == "Billing History":
    st.markdown("## 🧾 Billing History")
    st.write("View your previous payments and subscription records.")
    st.dataframe(st.session_state.billing_history, use_container_width=True, hide_index=True)

    s1, s2, s3 = st.columns(3)
    with s1:
        st.metric("Current Plan", "Starter")
    with s2:
        st.metric("Next Billing Date", "2026-05-01")
    with s3:
        st.metric("Last Payment", "$9")

# ---------- ACCOUNT PAGE ----------
elif st.session_state.page == "Account":
    st.markdown("## ⚙️ Account Settings")
    st.text_input("Full Name", "Your Name")
    st.text_input("Email", "you@example.com")
    st.selectbox("Current Plan", ["Starter", "Pro", "Business"])
    if st.button("Save Settings"):
        st.success("Settings saved successfully.")

st.divider()
st.caption(f"Last updated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")

       
