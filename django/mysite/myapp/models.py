from django.db import models
from django.contrib.auth.models import AbstractUser

# หากต้องการให้ Member มีฟิลด์เพิ่มเติม เช่น คะแนน และบทบาท สามารถปรับปรุง Member model ได้
class Member(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    # เพิ่มคะแนนสะสม (Reward Points)
    points = models.PositiveIntegerField(default=0)
    # เพิ่มบทบาท: 'customer' หรือ 'owner'

    def __str__(self):
        return self.username


class Menu(models.Model):
    CATEGORY_CHOICES = [
        ('coffee', 'เมนูกาแฟ'),
        ('tea', 'เมนูชา'),
        ('cocoa_milk', 'เมนูโกโก้ และ นม'),
        ('snack', 'เมนูขนม'),
        ('bakery', 'เบเกอรี่'),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='menu_images/')
    # review field ที่มีอยู่แล้วอาจไม่จำเป็น หากมี Review model แยกต่างหาก
    review = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Model สำหรับให้สมาชิกรีวิวเมนู
class Review(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='reviews')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(default=5)  # เช่น 1-5 ดาว
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.member.username} on {self.menu.name}"


# Model สำหรับโปรโมชั่น
class Promotion(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    discount_percentage = models.PositiveIntegerField()  # เช่น 10% ลด
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='promotions/', blank=True, null=True)

    def __str__(self):
        return self.title


# Model สำหรับกิจกรรมทางร้าน
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    # ผู้เข้าร่วมกิจกรรม
    participants = models.ManyToManyField(Member, blank=True, related_name='events')

    def __str__(self):
        return self.title


# Model สำหรับคูปอง
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=5, decimal_places=2)  # เช่น ส่วนลดเป็นตัวเลขหรือเปอร์เซ็นต์
    valid_from = models.DateField()
    valid_until = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

# Model สำหรับเมนู

class MenuItem(models.Model):
    name = models.CharField(max_length=255, verbose_name="ชื่อเมนู")
    description = models.TextField(blank=True, verbose_name="รายละเอียด")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="ราคา")
    image = models.ImageField(upload_to="menu_images/", blank=True, null=True, verbose_name="รูปภาพ")
    rating = models.FloatField(default=5.0, verbose_name="เรตติ้ง")

    def __str__(self):
        return self.name
