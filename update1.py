import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

# Load fixed timetable data
timetable_df = pd.read_csv(r"C:\Users\mohite\Desktop\sem6\face-recognition-main\face-recognition-main\timetable.csv")

# Count how many times each subject occurs in a week
weekly_lecture_counts = timetable_df['Subject'].value_counts()
all_subjects = timetable_df['Subject'].unique()

def calculate_overall_attendance(attendance_df, weekly_lecture_counts, all_subjects):
    attendance_df['Date'] = pd.to_datetime(attendance_df['Date'])
    start_date = attendance_df['Date'].min()
    end_date = attendance_df['Date'].max()
    num_weeks = (end_date - start_date).days // 7 + 1
    total_scheduled = weekly_lecture_counts.sum() * num_weeks
    
    student_attendance = {}
    subject_attendance = attendance_df['Subject'].value_counts().reindex(all_subjects, fill_value=0)
    
    for student_id in attendance_df['Student_ID'].unique():
        student_data = attendance_df[attendance_df['Student_ID'] == student_id]
        total_attended = student_data['Subject'].value_counts().sum()
        overall_attendance_percentage = (total_attended / total_scheduled) * 100 if total_scheduled > 0 else 0
        student_attendance[student_id] = overall_attendance_percentage
    
    attendance_summary_df = pd.DataFrame(list(student_attendance.items()), 
                                         columns=['Student_ID', 'Overall_Attendance_Percentage'])
    
    defaulters_df = attendance_summary_df[attendance_summary_df['Overall_Attendance_Percentage'] < 75]
    return attendance_summary_df, start_date, end_date, subject_attendance, defaulters_df

def dashboard():
    st.set_page_config(layout="wide")
    st.title("📊 Attendance Dashboard")
    uploaded_file = st.file_uploader("📂 Upload Attendance CSV", type=["csv"])
    
    if uploaded_file:
        attendance_df = pd.read_csv(uploaded_file)
        if attendance_df.empty:
            st.warning("⚠️ The uploaded file is empty or could not be read. Please upload a valid dataset.")
            return
        
        attendance_summary_df, start_date, end_date, subject_attendance, defaulters_df = calculate_overall_attendance(attendance_df, weekly_lecture_counts, all_subjects)
        
        col_summary, col_defaulters = st.columns([3, 1])
        with col_summary:
            st.subheader("Overall Attendance Summary")
            st.dataframe(attendance_summary_df)
            st.write(f"📅 Attendance Period: {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}")
        
        with col_defaulters:
            st.subheader("📌 Defaulters List")
            st.dataframe(defaulters_df)
        
        col_download1, col_download2 = st.columns(2)
        with col_download1:
            csv_overall = attendance_summary_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Overall Attendance (CSV)", data=csv_overall, file_name="overall_attendance.csv", mime='text/csv')
        
        with col_download2:
            csv_defaulters = defaulters_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Defaulters List (CSV)", data=csv_defaulters, file_name="defaulters_list.csv", mime='text/csv')
        
        col1, col2, col3 = st.columns(3)
        with col1:
            fig, ax = plt.subplots(figsize=(5, 5))
            sns.barplot(x=subject_attendance.index, y=subject_attendance.values, palette='viridis', ax=ax)
            ax.set_ylabel("Total Attendance")
            ax.set_xlabel("Subjects")
            ax.set_title("Overall Attendance by Subject")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots(figsize=(5, 5))
            subject_attendance.plot.pie(autopct="%.1f%%", labels=subject_attendance.index, cmap='coolwarm', ax=ax, startangle=90)
            ax.set_ylabel("")
            ax.set_title("Overall Attendance Distribution by Subject")
            st.pyplot(fig)
        
        with col3:
            fig, ax = plt.subplots(figsize=(5, 5))
            attendance_df.groupby("Date").size().plot(ax=ax, marker='o', linestyle='-', color='b')
            ax.set_ylabel("Total Lectures Attended")
            ax.set_xlabel("Date")
            ax.set_title("Overall Attendance Trend Over Time")
            st.pyplot(fig)
        
        student_id = st.text_input("Enter Student ID for Detailed Analysis:")
        
        if student_id:
            if student_id not in attendance_df['Student_ID'].astype(str).values:
                st.warning("No records found for the entered Student ID.")
                return
            
            student_data = attendance_df[attendance_df['Student_ID'].astype(str) == student_id]
            attended_counts = student_data['Subject'].value_counts().reindex(all_subjects, fill_value=0)
            
            attendance_summary = pd.DataFrame({
                "Lectures Attended": attended_counts,
                "Total Lectures": weekly_lecture_counts * ((end_date - start_date).days // 7 + 1)
            }).fillna(0)
            
            attendance_summary["Attendance Percentage"] = (attendance_summary["Lectures Attended"] / 
                                                             attendance_summary["Total Lectures"]) * 100
            
            total_attended = attendance_summary["Lectures Attended"].sum()
            total_scheduled = attendance_summary["Total Lectures"].sum()
            overall_attendance_percentage = (total_attended / total_scheduled) * 100 if total_scheduled > 0 else 0
            
            st.subheader(f"Detailed Attendance for Student {student_id}")
            st.dataframe(attendance_summary)
            
            col4, col5, col6 = st.columns(3)
            with col4:
                fig, ax = plt.subplots(figsize=(5, 5))
                sns.barplot(x=attendance_summary.index, y=attendance_summary["Attendance Percentage"], palette='viridis', ax=ax)
                ax.set_ylabel("Attendance Percentage")
                ax.set_title(f"Attendance Report for Student {student_id}")
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
                st.pyplot(fig)
            
            with col5:
                fig, ax = plt.subplots(figsize=(5, 5))
                attendance_summary["Lectures Attended"].plot.pie(autopct="%.1f%%", labels=attendance_summary.index, cmap='coolwarm', ax=ax, startangle=90)
                ax.set_ylabel("")
                ax.set_title("Attendance Distribution by Subject")
                st.pyplot(fig)
            
            with col6:
                student_data_grouped = student_data.groupby("Date").size()
                fig, ax = plt.subplots(figsize=(5, 5))
                student_data_grouped.plot(ax=ax, marker='o', linestyle='-', color='b')
                ax.set_ylabel("Number of Lectures Attended")
                ax.set_xlabel("Date")
                ax.set_title("Attendance Trend Over Time")
                st.pyplot(fig)
            
            csv_student = attendance_summary.to_csv(index=False).encode('utf-8')
            st.download_button(f"📥 Download Report for Student {student_id} (CSV)", data=csv_student, file_name=f"attendance_{student_id}.csv", mime='text/csv')

dashboard()
