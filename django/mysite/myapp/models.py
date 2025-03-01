from django.db import models
from django.contrib.auth.models import AbstractUser
import decimal

# Model สำหรับสมาชิก
class Member(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    points = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # เพิ่มบรรทัดนี้
    # สามารถเพิ่มฟิลด์สำหรับบทบาท เช่น 'customer' หรือ 'owner' ได้ตามต้องการ

    def __str__(self):
        return self.username


# Model สำหรับเมนูอาหารและเครื่องดื่ม
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
    # หากต้องการคำนวณราคาควรใช้ DecimalField แต่หากยังใช้ CharField ให้แปลงก่อนคำนวณ
    price = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='menu_images/')
    review = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Model สำหรับให้สมาชิกรีวิวเมนู
class Review(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='reviews')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(default=5)  # คะแนนเต็ม 1-5 ดาว
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.member.username} on {self.menu.name}"


# Model สำหรับโปรโมชั่น
class Promotion(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    discount_percentage = models.PositiveIntegerField()  # เช่น ลด 10%
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
    participants = models.ManyToManyField(Member, blank=True, related_name='events')

    def __str__(self):
        return self.title


# Model สำหรับคูปอง
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=5, decimal_places=2)  # ส่วนลดเป็นตัวเลขหรือเปอร์เซ็นต์
    valid_from = models.DateField()
    valid_until = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='orders')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        # เนื่องจาก price ใน Menu ถูกเก็บเป็น CharField เราจึงต้องแปลงเป็น Decimal ก่อนคำนวณ
        try:
            price = decimal.Decimal(self.menu.price)
        except Exception:
            price = decimal.Decimal("0.00")
        self.total_price = price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} by {self.member.username}"
