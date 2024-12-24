import subprocess
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UploadedFile, UserData
from django.shortcuts import render
import streamlit as st

@csrf_exempt
def upload_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # รับข้อมูลที่ส่งมาในรูปแบบ JSON
            file_name = data["file_name"]
            file_data = data["data"]

            # สร้างไฟล์ในฐานข้อมูล
            file, _ = UploadedFile.objects.get_or_create(file_name=file_name, data=file_data)

            # บันทึกข้อมูลในตาราง UserData
            for row in file_data:
                UserData.objects.create(
                    data=row,  # เก็บข้อมูลในรูปแบบ JSON
                    uploaded_file=file  # เชื่อมโยงกับไฟล์ที่อัปโหลด
                )

            return JsonResponse({"message": "บันทึกข้อมูลสำเร็จ"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "รองรับเฉพาะ POST เท่านั้น"}, status=405)

def streamlit(request):
    return render(request, "streamlitapp/streamlit.html") 
