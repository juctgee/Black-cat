import streamlit as st
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt

# ตั้งชื่อหน้าหลัก
st.title("Event Management System Dashboard")

# สร้าง Sidebar สำหรับ Navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("เลือกหน้า", ["Overview", "Events", "Reports"])

# เพิ่มลิงก์สำหรับกลับไปยังหน้า Django
st.sidebar.markdown("[กลับไปยังเว็บไซต์ร้าน](http://127.0.0.1:8000/)")

if page == "Overview":
    st.header("Overview")
    st.write("ภาพรวมของระบบจัดการกิจกรรม")
    # ตัวอย่างข้อมูลสถิติ
    st.metric("Upcoming Events", 5, delta="2")
    st.metric("Total Participants", 120, delta="15")
    
elif page == "Events":
    st.header("Events")
    st.write("รายละเอียดของกิจกรรม")
    
    # ตัวอย่างการเรียก API เพื่อดึงข้อมูลกิจกรรม
    try:
        response = requests.get("http://127.0.0.1:8000/api/events/")  # URL ของ API ที่ต้องการเรียก
        response.raise_for_status()  # ตรวจสอบ error หากมี
        events = response.json()
        # สมมุติว่า API ส่งข้อมูลในรูปแบบ list ของ dict
        df_events = pd.DataFrame(events)
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเรียก API: {e}")
        # หากเรียก API ไม่ได้ ก็ใช้ข้อมูลตัวอย่าง
        df_events = pd.DataFrame({
            "Event": ["Conference", "Meetup", "Workshop"],
            "Date": ["2025-04-01", "2025-04-15", "2025-05-01"],
            "Status": ["Scheduled", "Completed", "Scheduled"]
        })
    st.table(df_events)
    
elif page == "Reports":
    st.header("Reports")
    st.write("รายงานและสถิติการเข้าร่วมกิจกรรม")
    # ตัวอย่างการแสดง Histogram ด้วย Matplotlib
    data = np.random.randn(50)
    fig, ax = plt.subplots()
    ax.hist(data, bins=10, color='skyblue', edgecolor='black')
    ax.set_title("Distribution of Sample Data")
    st.pyplot(fig)
