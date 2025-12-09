import streamlit as st

if st.session_state.get("authenticated", False):
    st.switch_page("pages/app.py")

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI PaperIQ – Research Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- GLOBAL STYLES ----------
st.markdown("""
<style>
/* Overall background with subtle gradient */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #020617 0%, #0a0e27 50%, #020617 100%);
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Navbar with glassmorphism */
.navbar {
    background: rgba(2, 6, 23, 0.8);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(59, 130, 246, 0.2);
    padding: 1rem 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 50;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.nav-left {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.nav-logo {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
}
.nav-title {
    font-size: 1.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.nav-links {
    display: flex;
    gap: 2rem;
    font-size: 1rem;
}
.nav-link {
    color: #94a3b8;
    text-decoration: none;
    transition: color 0.3s;
    font-weight: 500;
}
.nav-link:hover {
    color: #3b82f6;
}
.nav-right-btn {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    border-radius: 10px;
    padding: 0.7rem 1.6rem;
    font-size: 1rem;
    font-weight: 600;
    border: none;
    color: white;
    cursor: pointer;
    transition: all 0.3s;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    text-decoration: none;
    display: inline-block;
}
.nav-right-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
}

/* Hero with enhanced styling */
.hero {
    margin-top: 3rem;
    padding: 4rem 2.5rem;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(29, 78, 216, 0.15) 0%, rgba(2, 6, 23, 0.9) 60%);
    border: 1px solid rgba(59, 130, 246, 0.3);
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
    pointer-events: none;
}
.hero-kicker {
    font-size: 1rem;
    font-weight: 600;
    color: #60a5fa;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.75rem;
    text-align: center;
}
.hero-title {
    font-size: 3.5rem;
    line-height: 1.15;
    font-weight: 800;
    background: linear-gradient(135deg, #e0f2fe 0%, #bfdbfe 50%, #93c5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1.2rem;
    text-align: center;
}
.hero-subtitle {
    font-size: 1.15rem;
    color: #cbd5e1;
    max-width: 42rem;
    line-height: 1.7;
    text-align: center;
    margin: 0 auto;
}
.hero-meta {
    display: flex;
    gap: 1rem;
    margin-top: 1.75rem;
    justify-content: center;
}
.hero-pill {
    font-size: 0.95rem;
    padding: 0.5rem 1.2rem;
    border-radius: 999px;
    background: rgba(59, 130, 246, 0.15);
    border: 1px solid rgba(59, 130, 246, 0.3);
    color: #cbd5e1;
}

/* Section Title with gradient */
.section-title {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #e0f2fe 0%, #bfdbfe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1.5rem;
}

/* Feature Grid with hover effects */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1.5rem;
    margin-top: 1rem;
}
.feature-card {
    background: linear-gradient(145deg, rgba(15, 23, 42, 0.6), rgba(2, 6, 23, 0.8));
    border-radius: 16px;
    border: 1px solid rgba(59, 130, 246, 0.2);
    padding: 2rem 1.75rem;
    transition: all 0.3s;
    cursor: pointer;
}
.feature-card:hover {
    transform: translateY(-5px);
    border-color: rgba(59, 130, 246, 0.5);
    box-shadow: 0 12px 30px rgba(59, 130, 246, 0.2);
}
.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 0.75rem;
    filter: drop-shadow(0 0 10px rgba(59, 130, 246, 0.3));
}
.feature-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #e5e7eb;
    margin-bottom: 0.6rem;
}
.feature-text {
    font-size: 1rem;
    color: #94a3b8;
    line-height: 1.6;
}

/* Stats Section */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}
.stat-card {
    background: linear-gradient(145deg, rgba(15, 23, 42, 0.6), rgba(2, 6, 23, 0.8));
    border-radius: 16px;
    border: 1px solid rgba(59, 130, 246, 0.2);
    padding: 2rem 1.5rem;
    text-align: center;
    transition: all 0.3s;
}
.stat-card:hover {
    transform: translateY(-5px);
    border-color: rgba(59, 130, 246, 0.5);
    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.2);
}
.stat-number {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.stat-label {
    font-size: 1rem;
    color: #94a3b8;
    font-weight: 500;
}

/* About Section */
.about-container {
    margin-top: 2rem;
    padding: 3rem 2.5rem;
    border-radius: 24px;
    background: linear-gradient(145deg, rgba(15, 23, 42, 0.6), rgba(2, 6, 23, 0.8));
    border: 1px solid rgba(59, 130, 246, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}
.about-text {
    font-size: 1.05rem;
    color: #cbd5e1;
    line-height: 1.8;
    margin-bottom: 1.5rem;
}
.about-highlight {
    color: #60a5fa;
    font-weight: 600;
}

/* CTA Buttons */
.stButton>button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 0.75rem 1.5rem !important;
    font-size: 1.05rem !important;
    transition: all 0.3s !important;
}
.stButton>button:hover {
    transform: translateY(-2px) !important;
}

.small-muted {
    font-size: 0.95rem;
    color: #94a3b8;
    line-height: 1.6;
}

/* Step cards */
.step-number {
    display: inline-block;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
    color: white;
    text-align: center;
    line-height: 36px;
    font-weight: 700;
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
}
.step-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #e5e7eb;
    margin-bottom: 0.5rem;
}

@media (max-width: 900px) {
    .hero { flex-direction: column; padding: 2.5rem 1.5rem; }
    .hero-title { font-size: 2.2rem; }
    .feature-grid { grid-template-columns: 1fr; }
    .stats-grid { grid-template-columns: repeat(2, 1fr); }
    .nav-links { display: none; }
}
</style>

<script>
function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}
</script>
""", unsafe_allow_html=True)

# ---------- NAVBAR ----------
st.markdown("""
<div class="navbar">
    <div class="nav-left">
        <div class="nav-logo">🧠</div>
        <div class="nav-title">AI PaperIQ</div>
    </div>
    <div class="nav-links">
        <a class="nav-link" href="#features" onclick="scrollToSection('features')">Features</a>
        <a class="nav-link" href="#workflow" onclick="scrollToSection('workflow')">How it works</a>
        <a class="nav-link" href="#stats" onclick="scrollToSection('stats')">Stats</a>
        <a class="nav-link" href="#about" onclick="scrollToSection('about')">About</a>
    </div>
    <div>
        <a href="/login" target="_self" class="nav-right-btn">Get Started</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- HERO ----------
st.markdown("""
<div class="hero">
    <div style="position: relative; z-index: 1; width: 100%; max-width: 900px;">
        <div class="hero-kicker">RESEARCH INTELLIGENCE</div>
        <div class="hero-title">Summarize research papers<br>with clarity & precision</div>
        <div class="hero-subtitle">
            Upload PDFs or paste text — AI PaperIQ transforms dense academic writing 
            into clean, accurate summaries with detailed analytics powered by Gemini AI.
        </div>
        <div class="hero-meta">
            <div class="hero-pill">📄 PDF & text support</div>
            <div class="hero-pill">🧠 AI-powered analysis</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- FEATURES ----------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div id="features"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">✨ Key Features</div>', unsafe_allow_html=True)
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon">📄</div>
        <div class="feature-title">Multi-Format Input</div>
        <div class="feature-text">
            Import academic PDFs or paste raw text — the system handles both formats seamlessly.
        </div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🧠</div>
        <div class="feature-title">Smart AI Summaries</div>
        <div class="feature-text">
            Generate crisp summaries highlighting objectives, methodology, findings, and limitations with high accuracy.
        </div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Deep Analytics</div>
        <div class="feature-text">
            View similarity scores, compression ratios, readability metrics, and interactive visualizations.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- HOW IT WORKS ----------
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown('<div id="workflow"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">🧩 How It Works</div>', unsafe_allow_html=True)
step_cols = st.columns(3)

with step_cols[0]:
    st.markdown("<div class='step-number'>1</div>", unsafe_allow_html=True)
    st.markdown("<div class='step-title'>Input your document</div>", unsafe_allow_html=True)
    st.markdown("<span class='small-muted'>Upload a PDF or paste text from any academic paper.</span>", unsafe_allow_html=True)

with step_cols[1]:
    st.markdown("<div class='step-number'>2</div>", unsafe_allow_html=True)
    st.markdown("<div class='step-title'>Generate summary</div>", unsafe_allow_html=True)
    st.markdown("<span class='small-muted'>Choose AI model settings (Pro or Flash) and generate a structured summary.</span>", unsafe_allow_html=True)

with step_cols[2]:
    st.markdown("<div class='step-number'>3</div>", unsafe_allow_html=True)
    st.markdown("<div class='step-title'>Explore insights</div>", unsafe_allow_html=True)
    st.markdown("<span class='small-muted'>Review comprehensive analytics to validate quality, readability, and accuracy.</span>", unsafe_allow_html=True)

# ---------- STATS ----------
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown('<div id="stats"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">📈 Platform Statistics</div>', unsafe_allow_html=True)
st.markdown("""
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-number">10K+</div>
        <div class="stat-label">Papers Summarized</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">95%</div>
        <div class="stat-label">Accuracy Rate</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">5K+</div>
        <div class="stat-label">Active Users</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">85%</div>
        <div class="stat-label">Time Saved</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- ABOUT ----------
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown('<div id="about"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">💡 The Story Behind AI PaperIQ</div>', unsafe_allow_html=True)
st.markdown("""
<div class="about-container">
    <p class="about-text">
        Imagine spending hours decoding a 40-page research paper, only to realize you needed just the key insights. 
        <span class="about-highlight">That frustration sparked AI PaperIQ.</span>
    </p>
    <p class="about-text">
        We're not just another summarization tool — we're your <span class="about-highlight">research companion</span> that thinks like you do. 
        While others simply compress text, we understand context, extract methodology, identify limitations, and surface the insights 
        that actually matter. Powered by <span class="about-highlight">Gemini AI's advanced reasoning</span>, we don't just read papers; 
        we comprehend them.
    </p>
    <p class="about-text">
        Picture this: A PhD student drowning in 200 papers for their literature review. A clinician racing to understand the latest 
        medical research between patient visits. An entrepreneur validating cutting-edge tech before making million-dollar decisions. 
        <span class="about-highlight">AI PaperIQ turns weeks into hours, and confusion into clarity.</span>
    </p>
    <p class="about-text">
        But here's what makes us different — we don't hide the details. Every summary comes with <span class="about-highlight">
        deep analytics</span>: similarity scores that validate accuracy, compression ratios that show efficiency, readability metrics 
        that ensure clarity. You're not just getting a summary; you're getting <span class="about-highlight">transparent, 
        trustworthy intelligence</span> you can stake your research on.
    </p>
    <p class="about-text" style="font-style: italic; color: #60a5fa; margin-top: 1.5rem;">
        Because in the world of research, understanding isn't a luxury — it's everything. And we're here to make sure you never 
        miss what matters.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<p class='small-muted' style='text-align:center;'>© 2024 AI PaperIQ · Built with ❤️ using Streamlit & Gemini AI</p>", unsafe_allow_html=True)