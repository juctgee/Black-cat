from django.db import models

class UploadedFile(models.Model):
    file_name = models.CharField(max_length=255)  # ชื่อไฟล์ที่อัปโหลด
    upload_date = models.DateTimeField(auto_now_add=True)  # วันที่อัปโหลด
    data = models.JSONField()  # เก็บข้อมูลทั้งหมดในรูปแบบ JSON

class UserData(models.Model):
    data = models.JSONField()  # เก็บข้อมูลในรูปแบบ JSON
    uploaded_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)  # เชื่อมกับไฟล์ที่อัปโหลด
    upload_date = models.DateTimeField(auto_now_add=True)  # วันที่อัปโหลด

    def __str__(self):
        return f"ข้อมูลที่อัปโหลดเมื่อ {self.upload_date}"