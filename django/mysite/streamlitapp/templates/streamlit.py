import streamlit as st
import pandas as pd
import requests

st.title("Event Management System Dashboard")

# สร้าง Sidebar สำหรับ Navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("เลือกหน้า", ["Overview", "Members", "Menu"])

# ลิงก์สำหรับกลับไปยังเว็บไซต์ Django
st.sidebar.markdown("[กลับไปยังเว็บไซต์ร้าน](http://127.0.0.1:8000/)")

if page == "Overview":
    st.header("Overview")
    st.write("ภาพรวมของระบบจัดการกิจกรรม")

    # ดึงข้อมูลยอดขายรวมจาก API
    try:
        response_sales = requests.get("http://127.0.0.1:8000/api/total_sales/")
        response_sales.raise_for_status()
        sales_data = response_sales.json()  # API ควรส่งข้อมูลในรูปแบบ { "total_sales": <value> }
        total_sales = sales_data.get("total_sales", 0)
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเรียก API total_sales: {e}")
        total_sales = None

    # ดึงข้อมูลสมาชิกใหม่ใน 7 วันจาก API
    try:
        response_new_members = requests.get("http://127.0.0.1:8000/api/new_members/")
        response_new_members.raise_for_status()
        members_data = response_new_members.json()  # API ควรส่ง { "new_members_past_7_days": <value> }
        new_members = members_data.get("new_members_past_7_days", 0)
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเรียก API new_members: {e}")
        new_members = None

    # แสดงข้อมูลยอดขายและสมาชิกใหม่ด้วย st.metric (แสดงเป็น card)
    if total_sales is not None:
        st.metric("Total Sales", f"{total_sales} บาท")
    if new_members is not None:
        st.metric("New Members (7 days)", new_members)

    # ดึงข้อมูลยอดขายรายเดือนจาก API
    try:
        response_monthly = requests.get("http://127.0.0.1:8000/api/monthly_sales/")
        response_monthly.raise_for_status()
        # สมมุติว่า API ส่งข้อมูลในรูปแบบ [{ "month": "January", "sales": 10000 }, ... ]
        monthly_data = response_monthly.json()
        df_monthly = pd.DataFrame(monthly_data)
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเรียก API monthly_sales: {e}")
        df_monthly = None

    if df_monthly is not None and not df_monthly.empty:
        st.subheader("Monthly Sales")
        # กำหนดให้คอลัมน์ "month" เป็น index เพื่อให้แสดงกราฟได้เหมาะสม
        df_chart = df_monthly.set_index("month")
        st.bar_chart(df_chart)
        
        st.subheader("Monthly Sales Trend")
        st.line_chart(df_chart)

    # ดึงข้อมูลกิจกรรมที่กำลังจะมาถึงจาก API
    try:
        response_events = requests.get("http://127.0.0.1:8000/api/upcoming_events/")
        response_events.raise_for_status()
        events_data = response_events.json()  # API ควรส่งรายการกิจกรรมในอนาคตในรูปแบบ list of dicts
        df_events = pd.DataFrame(events_data)
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเรียก API upcoming_events: {e}")
        df_events = None

    if df_events is not None and not df_events.empty:
        st.subheader("Upcoming Events")
        st.table(df_events)

elif page == "Members":
    st.header("Members")
    st.write("แสดงข้อมูลสมาชิกทั้งหมดของร้าน")
    try:
        response_members = requests.get("http://127.0.0.1:8000/api/member_list/")
        response_members.raise_for_status()
        members = response_members.json()
        df_members = pd.DataFrame(members)
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเรียก API member_list: {e}")
        df_members = pd.DataFrame()
    st.table(df_members)

elif page == "Menu":
    st.header("Menu")
    st.write("แสดงเมนูของร้าน")
    try:
        response_menu = requests.get("http://127.0.0.1:8000/api/menu_list/")
        response_menu.raise_for_status()
        menus = response_menu.json()
        df_menus = pd.DataFrame(menus)
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเรียก API menu_list: {e}")
        df_menus = pd.DataFrame()
    st.table(df_menus)
