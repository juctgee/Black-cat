import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import datetime

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
    /* กล่อง/การ์ดสำหรับ KPI แต่ละตัว - กำหนดความสูงคงที่ */
    .kpi-card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
        height: 150px;  /* กำหนดความสูงของการ์ด */
        display: flex;
        flex-direction: column;
        justify-content: center;
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
    /* กล่องหลัก (card-like) สำหรับแต่ละ section ด้านล่าง */
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

def fetch_data(endpoint):
    try:
        url = BASE_URL + endpoint
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching data from {endpoint}: {e}")
        return None

# Sidebar สำหรับเลือกหน้าที่ต้องการแสดง
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("เลือกหน้า", ["Dashboard", "Menu", "Member"])

if page == "Dashboard":
    st.title("KANGMOR CAFE DASHBOARD")

    # === KPI Cards (4 คอลัมน์) ===
    col1, col2, col3, col4 = st.columns(4)

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

    # Upcoming Events
    with col2:
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

    # New Members
    with col3:
        new_members_data = fetch_data("new_members/")
        if new_members_data:
            new_members_value = new_members_data.get("new_members_past_7_days", 0)
            st.markdown(
                f"""
                <div class="kpi-card">
                  <div class="kpi-title">New Members</div>
                  <div class="kpi-number">{new_members_value:,}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Orders Today (ใช้ API order_by_date/)
    with col4:
        today = datetime.date.today().strftime("%Y-%m-%d")
        orders_today_data = fetch_data(f"order_by_date/?start_date={today}&end_date={today}")
        orders_today_count = len(orders_today_data) if orders_today_data is not None else 0
        st.markdown(
            f"""
            <div class="kpi-card">
              <div class="kpi-title">Orders Today</div>
              <div class="kpi-number">{orders_today_count:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # === กราฟในหน้า Dashboard ===

    # Monthly Sales Chart
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("Monthly Sales")
    monthly_sales_data = fetch_data("monthly_sales/")
    if monthly_sales_data:
        df_monthly_sales = pd.DataFrame(monthly_sales_data)
        months = df_monthly_sales["month"].unique().tolist()
        selected_month = st.selectbox("เลือกเดือน", months)
        filtered_df = df_monthly_sales[df_monthly_sales["month"] == selected_month]
        fig = px.bar(filtered_df, x="month", y="sales", title=f"Monthly Sales: {selected_month}",
                     height=400)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Best Selling Menus (Horizontal Bar Chart)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("Best Selling Menus (Horizontal)")
    best_selling_data = fetch_data("best_selling_menus/")
    if best_selling_data:
        df_best = pd.DataFrame(best_selling_data)
        fig_best = px.bar(df_best, x="num_reviews", y="name", orientation='h',
                          title="Best Selling Menus (by Reviews)",
                          labels={"name": "Menu Name", "num_reviews": "Number of Reviews"},
                          height=400)
        st.plotly_chart(fig_best, use_container_width=True)
    else:
        st.info("ไม่พบข้อมูล Best Selling Menus")
    st.markdown('</div>', unsafe_allow_html=True)

    # Daily Orders Trend Graph
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("Daily Orders Trend")
    orders_by_date_data = fetch_data("orders_by_date/")
    if orders_by_date_data:
        df_orders = pd.DataFrame(orders_by_date_data)
        if not df_orders.empty:
            df_orders['date'] = pd.to_datetime(df_orders['date'], errors='coerce')
            fig_orders = px.line(df_orders, x="date", y="orders",
                                 title="Daily Orders Trend", height=400)
            st.plotly_chart(fig_orders, use_container_width=True)
        else:
            st.info("ไม่มีข้อมูลคำสั่งซื้อในแต่ละวัน")
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
        # Pie Chart for Menu Category Distribution
        if not df_menu.empty and 'category' in df_menu.columns:
            category_count = df_menu['category'].value_counts().reset_index()
            category_count.columns = ['category', 'count']
            fig_pie = px.pie(category_count, values='count', names='category', 
                             title="Menu Category Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)
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
        # Bar Chart for Member Registrations by Month
        if not df_member.empty and 'created_at' in df_member.columns:
            try:
                df_member['created_at'] = pd.to_datetime(df_member['created_at'], errors='coerce')
                df_member['month'] = df_member['created_at'].dt.strftime("%B %Y")
                monthly_registrations = df_member.groupby('month').size().reset_index(name='count')
                if not monthly_registrations.empty:
                    fig_reg = px.bar(monthly_registrations, x='month', y='count', 
                                     title="Member Registrations by Month", height=400)
                    st.plotly_chart(fig_reg, use_container_width=True)
                else:
                    st.info("ไม่มีข้อมูลการสมัครสมาชิกแบ่งตามเดือน")
            except Exception as e:
                st.error(f"Error processing dates: {e}")
        else:
            st.info("คอลัมน์ created_at ไม่พบในข้อมูล")
    else:
        st.info("ไม่พบข้อมูลสมาชิก")
    st.markdown('</div>', unsafe_allow_html=True)
