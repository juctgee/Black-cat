import pandas as pd
import requests
import streamlit as st
import json

st.title("อัปโหลดไฟล์และบันทึกข้อมูล")

# อัปโหลดไฟล์
uploaded_file = st.file_uploader("อัปโหลดไฟล์", type=["csv", "json", "xlsx"])

if uploaded_file is not None:
    try:
        # ตรวจสอบประเภทของไฟล์
        if uploaded_file.type == "application/json":
            # ถ้าเป็นไฟล์ JSON
            file_data = json.load(uploaded_file)
            st.write("ข้อมูลในไฟล์ JSON:")
            st.write(file_data)
        
        elif uploaded_file.type == "text/csv":
            # ถ้าเป็นไฟล์ CSV
            data = pd.read_csv(uploaded_file)
            
            # แทนที่ NaN ด้วย None ก่อนแปลงเป็น JSON
            data = data.where(pd.notnull(data), None)
            
            file_data = data.to_dict(orient="records")  # แปลงเป็นรูปแบบ JSON
            st.write("ข้อมูลในไฟล์ CSV:")
            st.dataframe(data)
        
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            # ถ้าเป็นไฟล์ Excel
            data = pd.read_excel(uploaded_file)
            
            # แทนที่ NaN ด้วย None ก่อนแปลงเป็น JSON
            data = data.where(pd.notnull(data), None)
            
            file_data = data.to_dict(orient="records")  # แปลงเป็นรูปแบบ JSON
            st.write("ข้อมูลในไฟล์ Excel:")
            st.dataframe(data)

        # ส่งข้อมูลไปยัง Django API
        if st.button("บันทึกข้อมูลในฐานข้อมูล"):
            response = requests.post(
                "http://localhost:8000/upload_data/",  # URL ของ Django API
                json={
                    "file_name": uploaded_file.name,
                    "data": file_data,
                },
            )
            if response.status_code == 201:
                st.success("บันทึกข้อมูลสำเร็จ!")
            else:
                st.error(f"เกิดข้อผิดพลาด: {response.text}")

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการอัปโหลดไฟล์: {e}")
