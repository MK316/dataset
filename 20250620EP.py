import streamlit as st
import pandas as pd

# GitHub raw CSV URL
CSV_URL = "https://raw.githubusercontent.com/MK316/dataset/refs/heads/main/data/S25engprofinal.csv"

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL, dtype={"Student_ID": str, "Passcode": str})
    return df

df = load_data()

# --- App layout ---
st.title("🎓 Grade Checker")
st.write("Enter your unique **Passcode** to check your grade details.")

passcode = st.text_input("🔑 Passcode", type="password")

if passcode:
    student_row = df[df['Passcode'] == passcode]

    if not student_row.empty:
        st.success("✅ Passcode matched! Here is your grade breakdown:")

        row = student_row.iloc[0]

        st.markdown(f"""
        **🆔 Student ID:** {row['Student_ID']}  
        **👥 Group:** {row['Group']}  

        ---
        ### 📝 1. Midterm Exams (40 %)  
        - **First Midterm (Raw Score):** {row['Mid1st']} / 210  
        - **Second Midterm (Raw Score):** {row['Mid2nd']} / 210  
        - **Midterm (Scaled to 40 pts):** **{row['Miterm']}** / 40  

        ---
        ### 📚 2. Assignments (20%) 
        - **HW1:** {'✔️ Completed (4 pts)' if row['HW1'] == 4 else '❌ Incomplete (0 pts)'}  
        - **HW2:** {'✔️ Completed (4 pts)' if row['HW2'] == 4 else '❌ Incomplete (0 pts)'}  
        - **HW3:** {row['HW3']} / 4 pts  (One minute video recording)  
        - **HW4:** {row['HW4']} / 4 pts (Hey Jude practice)
        - **HW5:** {row['HW5']} / 4 pts (3 minute's video recording)
        ##### ❄️ **Assignments Total:** {row['HW1'] + row['HW2'] + row['HW3'] + row['HW4'] + row['HW5']} / 20 
        ---
        ### ⭐ 3. Final Presentation (30 %)  
        - **Final Presentation:** {row['Final_Presentation']} pts
        ---
        ### 👥 4. Attendance (10 %)    
        - **Attendance:** {row['Att']} / 10  
        ---
        ### 💖 5. Extra Credits (5 points maximum)  
        
        - **Extra Credit (EC):** {row['EC']} pts
        ---
        st.markdown(f"""
        ### 🌀 Total Grade Summary
        - **Total Score:** **{row['Total']}** / 105  
        - **Performance Rank:** **{row['Rank']}** / 26 Students  
        """)


        # Grade decision
        total = row['Total']
        if total >= 95:
            grade = "A+"
        elif total >= 90:
            grade = "A"
        elif total >= 85:
            grade = "B+"
        elif total >= 80:
            grade = "B"
        elif total >= 75:
            grade = "C+"
        elif total >= 70:
            grade = "C"
        else:
            grade = "F"

        st.markdown(f"##### ❄️ **Your Expected Final Grade: {grade}**")

    else:
        st.error("❌ No match found. Please check your Passcode and try again.")
