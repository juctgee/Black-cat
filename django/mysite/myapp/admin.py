from django.contrib import admin
from .models import Member, Menu, Coupon, Promotion, Event, Review, Order

# ลงทะเบียน models อื่น ๆ ตามปกติ
admin.site.register(Menu)
admin.site.register(Coupon)
admin.site.register(Promotion)
admin.site.register(Event)
admin.site.register(Review)
admin.site.register(Order)

# ลงทะเบียน Member โดยใช้ ModelAdmin ที่กำหนดเอง
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('username', 'points', 'created_at')   # แสดงคอลัมน์ created_at ในหน้า list view
    list_filter = ('created_at',)                           # สามารถกรองข้อมูลตามวันที่สร้างสมาชิกได้
    readonly_fields = ('created_at',)                       # แสดงค่า created_at ในหน้า detail แต่ไม่แก้ไขได้
