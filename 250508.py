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

tabs = st.tabs(["📘 Instructions", "🔍 Check My Score", "📊 Leaderboard", "🍎 Group Score"])

# --- Tab 1: Instructions ---
with tabs[0]:

    st.caption("📍 This page will be available only until May 13.")
    st.markdown("---")
    st.markdown("""
    ### 📘 Tab 1: Instructions  
    This page provides information about the midterm exam results. By entering the passcode you submitted, you can check your score and see where your performance stands among all students. Please click each tab to view the details.

    ### 🔍 Tab 2: Check My Score  
    Enter your passcode to view your score.

    
    ### 📊 Tab 3: Leaderboard  
    Shows all scores as gray dots. Your score will be shown in red if you provide your Passcode in a textbox.

    ### 🍎 Tab 4: Group Score  
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

    # Define a color palette (auto-adjusts to group count)
    unique_groups = df["Group"].unique()
    palette = sns.color_palette("Set2", len(unique_groups))

    # Plot setup
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x="Group", y="Score", ax=ax, palette=palette)

    # Compute median values
    medians = df.groupby("Group")["Score"].median()

    # Add median text BELOW each box
    ax.set_title("Boxplot of Scores by Group")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 220)
    ax.set_xlabel("Group")

    # Display text below x-axis for each group
    # ax.set_ylim(df["Score"].min() - 10, df["Score"].max() + 10)
    for i, group in enumerate(sorted(df["Group"].unique())):
        median_value = medians[group]
        ax.text(i, df["Score"].min() - 15, f"Median: {median_value:.1f}", 
                ha='center', va='center', fontsize=8, color='black')

    st.pyplot(fig)
