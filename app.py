import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Social Media Automation",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("social_media_posts.csv")
        return df
    except Exception:
        return pd.DataFrame({
            "platform": ["Instagram", "LinkedIn", "Twitter"],
            "likes": [120, 80, 60],
            "comments": [20, 15, 10],
            "shares": [10, 8, 5],
            "timestamp": ["2026-04-01 10:00:00", "2026-04-01 14:00:00", "2026-04-01 18:00:00"],
            "post_text": [
                "Launch your brand with confidence",
                "Professional growth matters",
                "Quick update for our followers"
            ]
        })

df = load_data()

# -----------------------------
# SESSION STATE
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "billing_history" not in st.session_state:
    st.session_state.billing_history = [
        {"date": "2026-04-01", "plan": "Starter", "amount": "$9", "status": "Paid"},
        {"date": "2026-03-01", "plan": "Starter", "amount": "$9", "status": "Paid"},
        {"date": "2026-02-01", "plan": "Starter", "amount": "$9", "status": "Paid"},
    ]

if "show_generator" not in st.session_state:
    st.session_state.show_generator = False

# -----------------------------
# STYLING
# -----------------------------
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

.section-space {
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
st.sidebar.title("Navigation")
sidebar_page = st.sidebar.radio(
    "Go to",
    ["Home", "Generate Post", "Analytics", "History"],
    key="sidebar_navigation"
)

st.session_state.page = sidebar_page

# -----------------------------
# HOME PAGE
# -----------------------------
if st.session_state.page == "Home":
    nav1, nav2, nav3, nav4 = st.columns([2.2, 1, 1, 1])

    with nav1:
        st.markdown('<div class="main-title">Social Media Automation 🚀</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sub-title">Create content, upload images, manage pricing, and track billing in one dashboard.</div>',
            unsafe_allow_html=True
        )

    with nav2:
        if st.button("💳 Pricing", use_container_width=True, key="top_pricing"):
            st.session_state.page = "Pricing"

    with nav3:
        if st.button("🧾 Billing History", use_container_width=True, key="top_billing"):
            st.session_state.page = "Billing History"

    with nav4:
        if st.button("⚙️ Account", use_container_width=True, key="top_account"):
            st.session_state.page = "Account"

    st.divider()

    left, right = st.columns([1.35, 1])

    with left:
        st.markdown("## Welcome back")
        st.write("Build beautiful social media posts with text, image upload, smart workflow tools, and analytics.")

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
            if st.button("✍️ Generate Post", use_container_width=True, key="home_generate_post"):
                st.session_state.page = "Generate Post"

        with q2:
            if st.button("📅 Schedule Content", use_container_width=True, key="home_schedule"):
                st.success("Scheduling section can be added next.")

        with q3:
            if st.button("📈 View Analytics", use_container_width=True, key="home_analytics"):
                st.session_state.page = "Analytics"

    with right:
        st.markdown("""
        <div class="feature-card">
            <h3>Platform Highlights</h3>
            <p class="small-muted">Everything is designed to feel cleaner and more premium.</p>
            <ul>
                <li>Dedicated pricing page</li>
                <li>Billing history page</li>
                <li>Fancy generate-post section</li>
                <li>Image upload and preview</li>
                <li>Analytics and history tracking</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.info("Use the sidebar or the top buttons to move around the app.")

# -----------------------------
# GENERATE POST PAGE
# -----------------------------
elif st.session_state.page == "Generate Post":
    st.title("✍️ Generate Social Media Post")
    st.write("Create a social media post and upload an image from your laptop.")

    st.markdown("""
    <div class="upload-card">
        <div class="upload-label">✨ Creator Panel</div>
        <div class="small-muted">Write your post idea, choose the style, upload an image, and preview the content beautifully.</div>
    </div>
    """, unsafe_allow_html=True)

    col_form, col_preview = st.columns([1.1, 1])

    with col_form:
        topic = st.text_input("Enter Topic", placeholder="Example: Certificate of Google completion")
        platform = st.selectbox("Platform", ["Instagram", "LinkedIn", "Twitter"], key="platform_select")
        tone = st.selectbox("Tone", ["Professional", "Casual", "Funny"], key="tone_select")
        audience = st.text_input("Target Audience", placeholder="Example: students, recruiters, followers")
        hashtag_count = st.slider("Number of Hashtags", 3, 10, 5, key="hashtag_slider")
        post_title = st.text_input("Post Title", placeholder="Example: Proud moment in my learning journey")
        post_caption = st.text_area("Caption Idea", placeholder="Write your post idea here...")
        uploaded_file = st.file_uploader(
            "Upload an image",
            type=["png", "jpg", "jpeg", "webp"],
            key="image_upload"
        )

        if st.button("🚀 Generate Post", use_container_width=True, key="generate_post_main"):
            if not topic.strip():
                st.warning("Please enter a topic.")
            else:
                post_text = f"{topic} 🚀"
                caption = post_caption if post_caption.strip() else f"This is a {tone.lower()} post for {audience if audience.strip() else 'your audience'}."
                hashtags = " ".join([f"#tag{i}" for i in range(1, hashtag_count + 1)])
                cta = "👉 Follow us for more updates!"

                st.session_state.generated = {
                    "title": post_title if post_title.strip() else topic,
                    "post": post_text,
                    "caption": caption,
                    "hashtags": hashtags,
                    "cta": cta,
                    "platform": platform,
                    "audience": audience,
                    "tone": tone
                }

                st.success("Post generated successfully.")

    with col_preview:
        st.markdown("### Preview")

        if uploaded_file is not None:
            st.markdown('<div class="preview-box">', unsafe_allow_html=True)
            st.image(uploaded_file, caption="Uploaded image preview", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if "generated" in st.session_state:
            st.markdown("#### 📢 Generated Content")
            st.write("**Title:**", st.session_state.generated["title"])
            st.write("**Post Text:**", st.session_state.generated["post"])
            st.write("**Caption:**", st.session_state.generated["caption"])
            st.write("**Hashtags:**", st.session_state.generated["hashtags"])
            st.write("**CTA:**", st.session_state.generated["cta"])

            c1, c2 = st.columns(2)

            with c1:
                if st.button("💾 Save Draft", use_container_width=True, key="save_draft_btn"):
                    st.info("Post saved as draft!")

            with c2:
                if st.button("🚀 Simulate Post Now", use_container_width=True, key="simulate_post_btn"):
                    st.success(f"Posted successfully on {st.session_state.generated['platform']}")
                    st.session_state.history.append({
                        "time": datetime.now(),
                        "post": st.session_state.generated["post"],
                        "platform": st.session_state.generated["platform"]
                    })

# -----------------------------
# ANALYTICS PAGE
# -----------------------------
elif st.session_state.page == "Analytics":
    st.title("📊 Analytics Dashboard")

    st.subheader("Dataset Preview")
    st.dataframe(df, use_container_width=True)

    if not df.empty:
        df["engagement"] = df["likes"] + df["comments"] + df["shares"]

        st.subheader("Engagement by Platform")
        platform_data = df.groupby("platform")["engagement"].sum()
        fig1, ax1 = plt.subplots()
        platform_data.plot(kind="bar", ax=ax1)
        st.pyplot(fig1)

        st.subheader("Engagement by Hour")
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["hour"] = df["timestamp"].dt.hour
        hour_data = df.groupby("hour")["engagement"].mean()
        fig2, ax2 = plt.subplots()
        hour_data.plot(ax=ax2)
        st.pyplot(fig2)

        st.subheader("Keyword Frequency")
        text = " ".join(df["post_text"].astype(str))
        words = text.split()

        if len(words) > 0:
            word_freq = pd.Series(words).value_counts().head(10)
            fig3, ax3 = plt.subplots()
            word_freq.plot(kind="bar", ax=ax3)
            st.pyplot(fig3)
        else:
            st.info("No keyword data available.")
    else:
        st.info("No analytics data available.")

# -----------------------------
# HISTORY PAGE
# -----------------------------
elif st.session_state.page == "History":
    st.title("📜 Post History")

    if len(st.session_state.history) == 0:
        st.info("No posts yet.")
    else:
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df, use_container_width=True)

# -----------------------------
# PRICING PAGE
# -----------------------------
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
        if st.button("Choose Starter", key="starter_plan", use_container_width=True):
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
        if st.button("Choose Pro", key="pro_plan", use_container_width=True):
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
        if st.button("Choose Business", key="business_plan", use_container_width=True):
            st.success("Business plan selected.")

# -----------------------------
# BILLING HISTORY PAGE
# -----------------------------
elif st.session_state.page == "Billing History":
    st.markdown("## 🧾 Billing History")
    st.write("View your previous payments and subscription records.")

    st.dataframe(
        st.session_state.billing_history,
        use_container_width=True,
        hide_index=True
    )

    s1, s2, s3 = st.columns(3)
    with s1:
        st.metric("Current Plan", "Starter")
    with s2:
        st.metric("Next Billing Date", "2026-05-01")
    with s3:
        st.metric("Last Payment", "$9")

# -----------------------------
# ACCOUNT PAGE
# -----------------------------
elif st.session_state.page == "Account":
    st.markdown("## ⚙️ Account Settings")
    st.text_input("Full Name", "Your Name", key="account_name")
    st.text_input("Email", "you@example.com", key="account_email")
    st.selectbox("Current Plan", ["Starter", "Pro", "Business"], key="account_plan")
    if st.button("Save Settings", key="save_settings_btn"):
        st.success("Settings saved successfully.")

# -----------------------------
# FOOTER
# -----------------------------
st.divider()
st.caption(f"Last updated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
