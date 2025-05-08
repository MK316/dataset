import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from gtts import gTTS
from io import BytesIO

# Load your CSV
@st.cache_data
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/MK316/dataset/refs/heads/main/S250508.csv")  # Replace with your actual CSV path

df = load_data()

tabs = st.tabs(["📘 Instructions", "🔍 Check My Score", "📊 Leaderboard", "📦 Group Score"])

# --- Tab 1: Instructions ---
with tabs[0]:
    st.markdown("### 📘 Instructions")
    st.markdown("""
    **Tab 1: Instructions**  
    This page explains how to use this app.

    **Tab 2: Check My Score**  
    Enter your passcode to view your group, name, and score.

    **Tab 3: Leaderboard**  
    Shows all scores as gray dots. Your score is shown in red.

    **Tab 4: Group Score**  
    Displays score distribution per group using a boxplot, with median scores highlighted.
    """)

# --- Tab 2: Check My Score ---
with tabs[1]:
    st.markdown("### 🔍 Check Your Score")
    passcode_input = st.text_input("Enter your passcode:")

    if passcode_input:
        match = df[df['Passcode'].astype(str) == passcode_input.strip()]
        if not match.empty:
            row = match.iloc[0]
            st.success(f"✅ Name: {row['Name']}, Group: {row['Group']}, Score: {row['Score']}")
        else:
            st.error("❌ Passcode not found. Please try again.")

# --- Tab 3: Leaderboard ---
with tabs[2]:
    st.markdown("### 📊 Leaderboard")
    passcode_input_lb = st.text_input("🔐 (Optional) Enter your passcode to highlight your score:")

    # Sort by score descending
    df_sorted = df.sort_values(by="Score", ascending=True).reset_index(drop=True)
    user_index = None
    user_score = None

    if passcode_input_lb:
        match = df[df['Passcode'].astype(str) == passcode_input_lb.strip()]
        if not match.empty:
            user_score = match.iloc[0]['Score']
            user_index = df_sorted[df_sorted['Score'] == user_score].index[0]

    # Plot setup
    fig, ax = plt.subplots(figsize=(8, 5))
    x_vals = range(len(df_sorted))
    y_vals = df_sorted['Score']

    # Plot all points as gray
    ax.scatter(x_vals, y_vals, color='gray', s=100, label='Others')

    # Highlight user point
    if user_index is not None:
        ax.scatter(user_index, user_score, color='red', s=120, label='You')

    ax.set_xlabel("Rank Order (Highest to Lowest)")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 211)
    ax.set_title("Leaderboard: Score Distribution")
    ax.invert_xaxis()  # Optional: Highest score on the left
    ax.legend()
    st.pyplot(fig)


# --- Tab 4: Group Score ---
with tabs[3]:
    st.markdown("### 📦 Group Score Distribution")

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=df, x="Group", y="Score", ax=ax)

    medians = df.groupby("Group")["Score"].median()
    for i, (group, median_val) in enumerate(medians.items()):
        ax.text(i, median_val + 1, f"Median: {median_val}", ha='center', fontsize=10, color='blue')

    ax.set_title("Boxplot of Scores by Group")
    st.pyplot(fig)
