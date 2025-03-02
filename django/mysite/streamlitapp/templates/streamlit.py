import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import datetime
import calendar

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
        height: 150px;
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

# หน้า Dashboard (แสดงทุกอย่างในหน้าเดียว)
st.title("KANGMOR CAFE DASHBOARD")

# === KPI Cards (4 คอลัมน์) ===
col1, col2, col3, col4 = st.columns(4)

# ยอดขายรวม (Total Sales)
with col1:
    total_sales_data = fetch_data("total_sales/")
    if total_sales_data:
        total_sales_value = total_sales_data.get("total_sales", 0)
        st.markdown(
            f"""
            <div class="kpi-card">
              <div class="kpi-title">ยอดขายรวม</div>
              <div class="kpi-number">{total_sales_value:,.2f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ช่อง col2 (เว้นว่างไว้หรือเพิ่ม KPI อื่นๆ ถ้ามี)

with col3:
    new_members_data = fetch_data("new_members/")
    if new_members_data:
        new_members_value = new_members_data.get("new_members_past_7_days", 0)
        st.markdown(
            f"""
            <div class="kpi-card">
              <div class="kpi-title">สมาชิกใหม่</div>
              <div class="kpi-number">{new_members_value:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

with col4:
    today = datetime.date.today().strftime("%Y-%m-%d")
    orders_today_data = fetch_data(f"order_by_date/?start_date={today}&end_date={today}")
    orders_today_count = len(orders_today_data) if orders_today_data is not None else 0
    st.markdown(
        f"""
        <div class="kpi-card">
          <div class="kpi-title">คำสั่งซื้อวันนี้</div>
          <div class="kpi-number">{orders_today_count:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================
# กราฟแนวโน้มการขายรายวัน (Daily Sales Trend)
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.subheader("แนวโน้มการขายรายวัน")
trend_filter = st.selectbox("เลือกวิธีดูแนวโน้ม", ["ดูทั้งหมด", "เลือกวัน", "เลือกเดือน"], key="trend_filter")

if trend_filter == "ดูทั้งหมด":
    trend_start_date = datetime.date.today() - datetime.timedelta(days=30)
    trend_end_date = datetime.date.today()
elif trend_filter == "เลือกวัน":
    trend_day = st.date_input("เลือกวัน", value=datetime.date.today(), key="trend_day_select")
    trend_start_date = trend_day
    trend_end_date = trend_day
elif trend_filter == "เลือกเดือน":
    orders_all = fetch_data("order_list/")
    if orders_all:
        df_all = pd.DataFrame(orders_all)
        df_all['order_date'] = pd.to_datetime(df_all['order_date'], errors='coerce')
        df_all['month'] = df_all['order_date'].dt.strftime("%Y-%m")
        months_available = sorted(df_all['month'].dropna().unique().tolist())
        selected_month_trend = st.selectbox("เลือกเดือน", months_available, key="trend_month_select")
        year, month = map(int, selected_month_trend.split("-"))
        trend_start_date = datetime.date(year, month, 1)
        last_day = calendar.monthrange(year, month)[1]
        trend_end_date = datetime.date(year, month, last_day)
    else:
        trend_start_date = datetime.date.today() - datetime.timedelta(days=30)
        trend_end_date = datetime.date.today()
else:
    trend_start_date = datetime.date.today() - datetime.timedelta(days=30)
    trend_end_date = datetime.date.today()

trend_start_str = trend_start_date.strftime("%Y-%m-%d")
trend_end_str = trend_end_date.strftime("%Y-%m-%d")
orders_by_date_data = fetch_data(f"order_by_date/?start_date={trend_start_str}&end_date={trend_end_str}")
if orders_by_date_data:
    df_orders_trend = pd.DataFrame(orders_by_date_data)
    if not df_orders_trend.empty:
        df_orders_trend['order_date'] = pd.to_datetime(df_orders_trend['order_date'], errors='coerce')
        daily_sales = df_orders_trend.groupby(df_orders_trend['order_date'].dt.date)['total_price'].sum().reset_index(name='sales')
        daily_sales.columns = ['order_date', 'sales']
        fig_daily = px.line(daily_sales, x="order_date", y="sales",
                            title="แนวโน้มการขายรายวัน", height=400)
        st.plotly_chart(fig_daily, use_container_width=True)
    else:
        st.info("ไม่มีข้อมูลการขายในช่วงที่เลือก")
else:
    st.info("ไม่พบข้อมูลการขาย")
st.markdown('</div>', unsafe_allow_html=True)

# ============================
# กราฟเมนูขายดี (Best Selling Menus by Sales) แบบ Bar Chart
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.subheader("เมนูขายดี (ดูจากยอดขาย)")
orders_data = fetch_data("order_list/")
if orders_data:
    df_orders = pd.DataFrame(orders_data)
    df_orders['total_price'] = pd.to_numeric(df_orders['total_price'], errors='coerce')
    df_orders['order_date'] = pd.to_datetime(df_orders['order_date'], errors='coerce')
    # ใช้ข้อมูลทั้งหมดโดยไม่ต้องกรองเพิ่มเติม
    df_filtered = df_orders.copy()
    if not df_filtered.empty:
        best_selling = df_filtered.groupby("menu__name")["total_price"].sum().reset_index()
        best_selling = best_selling.sort_values(by="total_price", ascending=False)
        category_order = best_selling["menu__name"].tolist()
        fig_best = px.bar(
            best_selling, 
            x="total_price", 
            y="menu__name", 
            orientation='h',
            category_orders={"menu__name": category_order},
            title="เมนูขายดี (ตามยอดขาย)", 
            labels={"menu__name": "ชื่อเมนู", "total_price": "ยอดขาย (บาท)"},
            height=400
        )
        st.plotly_chart(fig_best, use_container_width=True)
    else:
        st.info("ไม่มีข้อมูลคำสั่งซื้อ")
else:
    st.info("ไม่พบข้อมูลคำสั่งซื้อ")
st.markdown('</div>', unsafe_allow_html=True)

# ============================
# กราฟยอดขายรายเดือน (Monthly Sales) แสดงทั้งหมด
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.subheader("ยอดขายรายเดือน (ทั้งหมด)")
monthly_sales_data = fetch_data("monthly_sales/")
if monthly_sales_data:
    df_monthly_sales = pd.DataFrame(monthly_sales_data)
    fig_monthly = px.bar(df_monthly_sales, x="month", y="sales", title="ยอดขายรายเดือนทั้งหมด", height=400)
    st.plotly_chart(fig_monthly, use_container_width=True)
else:
    st.info("ไม่พบข้อมูลยอดขายรายเดือน")
st.markdown('</div>', unsafe_allow_html=True)

# ============================
# กราฟใหม่ที่ 1: ยอดขายตามวันในสัปดาห์ (Sales by Weekday)
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.subheader("ยอดขายตามวันในสัปดาห์")
if orders_data:
    df_orders = pd.DataFrame(orders_data)
    df_orders['order_date'] = pd.to_datetime(df_orders['order_date'], errors='coerce')
    # เพิ่มคอลัมน์ weekday โดยใช้ชื่อวันภาษาไทย
    weekday_mapping = {0: 'จันทร์', 1: 'อังคาร', 2: 'พุธ', 3: 'พฤหัสบดี', 4: 'ศุกร์', 5: 'เสาร์', 6: 'อาทิตย์'}
    df_orders['weekday'] = df_orders['order_date'].dt.dayofweek.map(weekday_mapping)
    weekday_sales = df_orders.groupby("weekday")["total_price"].sum().reset_index()
    # เพื่อให้แสดงตามลำดับที่ถูกต้อง
    weekday_order = ['จันทร์', 'อังคาร', 'พุธ', 'พฤหัสบดี', 'ศุกร์', 'เสาร์', 'อาทิตย์']
    weekday_sales['weekday'] = pd.Categorical(weekday_sales['weekday'], categories=weekday_order, ordered=True)
    weekday_sales = weekday_sales.sort_values("weekday")
    fig_weekday = px.bar(weekday_sales, x="weekday", y="total_price",
                         title="ยอดขายตามวันในสัปดาห์",
                         labels={"weekday": "วัน", "total_price": "ยอดขาย (บาท)"},
                         height=400)
    st.plotly_chart(fig_weekday, use_container_width=True)
else:
    st.info("ไม่พบข้อมูลคำสั่งซื้อ")
st.markdown('</div>', unsafe_allow_html=True)

# ============================
# กราฟใหม่ที่ 2: จำนวนคำสั่งซื้อตามเมนู (Order Count by Menu)
