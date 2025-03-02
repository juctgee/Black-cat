from django import forms
from .models import Promotion, Menu

class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = [
            'title',
            'description',
            'discount_percentage',
            'start_date',
            'end_date',
            'image',
            'usage_limit',
            'applicable_menus',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        # ไม่รวมฟิลด์ review เพราะไม่ต้องการให้แก้ไขข้อมูลนี้
        fields = ['name', 'price', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }