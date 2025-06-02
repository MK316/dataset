import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from gtts import gTTS
from io import BytesIO

# Load your CSV
@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/MK316/dataset/refs/heads/main/S250603.csv")
    df.columns = df.columns.str.strip()  # Remove extra spaces
    df["Midterm2"] = pd.to_numeric(df["Midterm2"], errors="coerce")  # Ensure numeric
    df = df.dropna(subset=["Group", "Midterm2"])  # Drop rows with missing values
    return df

df = load_data()

tabs = st.tabs(["📘 Instructions", "🍰 Overall Result", "🔍 Check My Score", "📊 Leaderboard", "🍎 Group Score"])

# --- Tab 1: Instructions ---
with tabs[0]:
    st.caption("📍 This page will be available only until June 5.")
    st.markdown("---")
    st.markdown("""
    ### 📘 Tab 1: Instructions  
    This page provides information about the midterm exam results. By entering the passcode you submitted, you can check your score and see where your performance stands among all students. Please click each tab to view the details.

    ### 📘 Tab 2: Overall result  
    This tab displays a boxplot showing the distribution of all scores. The median is the middle score when all scores are arranged from lowest to highest.

    ### 🔍 Tab 3: Check My Score  
    Enter your passcode to view your score.

    ### 📊 Tab 4: Leaderboard  
    The scores of all test takers are displayed in order. You can enter your passcode to see your own position.

    ### 🍎 Tab 5: Group Score  
    Displays score distribution per group using a boxplot, with median scores highlighted.
    """)

# --- Tab 2: Overall score ---
# --- Tab 2: Overall score ---
# --- Tab 2: Overall score ---
with tabs[1]:
    st.markdown("### 📦 Score Comparison: Midterm 1 vs Midterm 2")
    st.caption("The score inside each box represents Median (the center score).")
    # Prepare data
    df_long = pd.melt(df, value_vars=["Midterm1", "Midterm2"],
                      var_name="Exam", value_name="Score")

    # Plot
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.boxplot(data=df_long, x="Exam", y="Score", palette=["lightgray", "skyblue"], ax=ax)

    # Annotate medians inside boxes
    for i, col in enumerate(["Midterm1", "Midterm2"]):
        median = df[col].median()
        ax.text(i, median - 5, f"{median:.1f}",  # Adjust -5 to control vertical offset
                ha='center', va='center', fontsize=10, color='black', weight='bold')

    ax.set_title("Boxplot Comparison of Midterm 1 and Midterm 2")
    ax.set_ylim(0, 220)
    ax.set_ylabel("Score")
    st.pyplot(fig)



# --- Tab 3: Check My Score ---
# --- Tab 3: Check My Score ---
with tabs[2]:
    st.markdown("### 🔍 Check Your Score")
    passcode_input = st.text_input("Enter your passcode: One alphabet + 4 digits (e.g., J0000)")

    if passcode_input:
        match = df[df['Passcode'].astype(str) == passcode_input.strip()]
        if not match.empty:
            row = match.iloc[0]
            name = row['Name']
            group = row['Group']
            mid1 = row['Midterm1']
            mid2 = row['Midterm2']
            diff = row['Diff']

            arrow = "✅" if diff > 0 else ("🔻" if diff < 0 else "➡️")

            st.success(f"""
            ✅ **Name:** {name}  
            ✅ **Group:** {group}  
            📝 **Midterm 1:** {mid1}  
            📝 **Midterm 2:** {mid2}  
            📊 **Change:** {diff:+} {arrow}
            """)
        else:
            st.error("❌ Passcode not found. Please try again.")


# --- Tab 4: Leaderboard ---
# --- Tab 4: Leaderboard ---
with tabs[3]:
    st.markdown("### 📊 Leaderboard: Midterm1 Reference with Midterm2 Comparison")

    passcode_input_lb = st.text_input("🔐 (Optional) Enter your passcode to highlight your score:")

    # Sort by Midterm1 descending
    df_sorted = df.sort_values(by="Midterm1", ascending=False).reset_index(drop=True)

    user_index = None
    user_sid = None

    if passcode_input_lb:
        match = df[df['Passcode'].astype(str) == passcode_input_lb.strip()]
        if not match.empty:
            user_sid = match.iloc[0]['SID']
            user_index = df_sorted[df_sorted['SID'] == user_sid].index[0]

    # Prepare reversed x-values to display higher scores on the left
    num_students = len(df_sorted)
    x_vals = list(range(num_students - 1, -1, -1))  # reversed index

    # Plot setup
    fig, ax = plt.subplots(figsize=(10, 5))

    for x, i in zip(x_vals, range(num_students)):
        mid1 = df_sorted.iloc[i]["Midterm1"]
        mid2 = df_sorted.iloc[i]["Midterm2"]
        ax.plot([x, x], [mid1, mid2], color='gray', alpha=0.4, linewidth=1)

    # Plot Midterm1 (gray)
    ax.scatter(x_vals, df_sorted["Midterm1"], color='gray', s=90, label="Midterm 1", alpha=0.6)

    # Plot Midterm2 (blue)
    ax.scatter(x_vals, df_sorted["Midterm2"], color='blue', s=90, label="Midterm 2", alpha=0.9)

    # Highlight user if found

    if user_index is not None:
        user_x = x_vals[user_index]  # Correct x-position
        ax.scatter(user_x, df_sorted.loc[user_index, "Midterm1"], color="orange", s=130, label="Your Midterm 1")
        ax.scatter(user_x, df_sorted.loc[user_index, "Midterm2"], color="red", s=130, label="Your Midterm 2")


    ax.set_xlabel("Rank Order (by Midterm 1)")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 220)
    ax.set_title("Leaderboard: Midterm1 vs Midterm2 (Sorted by Midterm1)")
    ax.legend(loc='lower right')

    st.pyplot(fig)


# --- Tab 5: Group Score ---
with tabs[4]:
    st.markdown("### 📦 Group Score Distribution")

    unique_groups = df["Group"].unique()
    palette = sns.color_palette("Set2", len(unique_groups))

    fig, ax = plt.subplots(figsize=(8, 5))
    box = sns.boxplot(data=df, x="Group", y="Midterm2", ax=ax, palette=palette)

    ax.set_title("Boxplot of Scores by Group")
    ax.set_ylabel("Midterm2")
    ax.set_ylim(0, 220)
    ax.set_xlabel("Group")

    # Get group plotting order
    group_order = [label.get_text() for label in ax.get_xticklabels()]

    # Loop through each group
    for i, group in enumerate(group_order):
        group_data = df[df["Group"] == group]["Midterm2"].dropna()

        q1 = group_data.quantile(0.25)
        q3 = group_data.quantile(0.75)
        median = group_data.median()



        center_plot_y = (ax.get_ylim()[0] + ax.get_ylim()[1]) / 2  # midpoint of y-axis
        ax.text(i, center_plot_y, f"Median: {median:.1f}",
                ha='center', va='center', fontsize=9, color='black')


    st.pyplot(fig)


