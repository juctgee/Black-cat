import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# กำหนด Page Config
st.set_page_config(
    page_title="KANGMOR CAFE DASHBOARD",
    page_icon="☕",
    layout="wide"
)

# === Custom CSS สำหรับตกแต่งการ์ดและองค์ประกอบต่าง ๆ ===
st.markdown(
    """
    <style>
    /* สีพื้นหลังของหน้าทั้งหมด */
    body {
        background-color: #F5F5F5;
    }
    /* กล่อง/การ์ดสำหรับ KPI แต่ละตัว */
    .kpi-card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0px; /* เว้นระยะด้านบน-ล่างเล็กน้อย */
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .kpi-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #333;
    }
    .kpi-number {
        font-size: 2rem;
        color: #FF5733;
        margin-top: 5px;
    }
    /* กล่องหลัก (card-like) ของแต่ละ section ด้านล่าง */
    .main-container {
        background-color: #FFFFFF;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    /* ตาราง DataFrame ให้ดูสวยขึ้น */
    .streamlit-table {
        background-color: #FFF;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# กำหนด Base URL ของ Django API
BASE_URL = "http://127.0.0.1:8000/api/"

# ฟังก์ชันสำหรับเรียก API และดึงข้อมูล (return เป็น DataFrame หรือ list/dict ก็ได้)
def fetch_data(endpoint):
    try:
        url = BASE_URL + endpoint
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        st.error(f"Error fetching data from {endpoint}: {e}")
        return None

# Sidebar สำหรับเลือกหน้าที่ต้องการแสดง
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("เลือกหน้า", ["Dashboard", "Menu", "Member"])

# ส่วนหัวของหน้า Dashboard (สำหรับ Dashboard และอื่น ๆ ที่ต้องการแสดง KPI)
if page == "Dashboard":
    st.title("KANGMOR CAFE DASHBOARD")

    # === ส่วนของ KPI: Total Sales, New Members, Upcoming Events ===
    col1, col2, col3 = st.columns(3)

    # Total Sales
    with col1:
        total_sales_data = fetch_data("total_sales/")
        if total_sales_data:
            total_sales_value = total_sales_data.get("total_sales", 0)
            st.markdown(
                f"""
                <div class="kpi-card">
                  <div class="kpi-title">Total Sales</div>
                  <div class="kpi-number">{total_sales_value:,.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # New Members
    with col2:
        new_members_data = fetch_data("new_members/")
        if new_members_data:
            new_members_value = new_members_data.get("new_members", 0)
            st.markdown(
                f"""
                <div class="kpi-card">
                  <div class="kpi-title">New Members</div>
                  <div class="kpi-number">{new_members_value:,}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Upcoming Events
    with col3:
        upcoming_events_data = fetch_data("upcoming_events/")
        if upcoming_events_data:
            num_events = len(upcoming_events_data)
            st.markdown(
                f"""
                <div class="kpi-card">
                  <div class="kpi-title">Upcoming Events</div>
                  <div class="kpi-number">{num_events:,}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Monthly Sales Chart
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("Monthly Sales")
    monthly_sales_data = fetch_data("monthly_sales/")
    if monthly_sales_data:
        df_monthly_sales = pd.DataFrame(monthly_sales_data)
        fig = px.bar(df_monthly_sales, x="month", y="sales", title="Monthly Sales")
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Upcoming Events (รายละเอียด)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("Upcoming Events")
    if upcoming_events_data:
        df_events = pd.DataFrame(upcoming_events_data)
        st.dataframe(df_events.style.set_properties(**{'border': '1px solid #ddd'}))
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Menu":
    st.title("Menu List")
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    menu_list_data = fetch_data("menu_list/")
    if menu_list_data:
        df_menu = pd.DataFrame(menu_list_data)
        st.dataframe(df_menu.style.set_properties(**{'border': '1px solid #ddd'}))
    else:
        st.info("ไม่พบข้อมูลเมนู")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Member":
    st.title("Member List")
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    member_list_data = fetch_data("member_list/")
    if member_list_data:
        df_member = pd.DataFrame(member_list_data)
        st.dataframe(df_member.style.set_properties(**{'border': '1px solid #ddd'}))
    else:
        st.info("ไม่พบข้อมูลสมาชิก")
    st.markdown('</div>', unsafe_allow_html=True)

