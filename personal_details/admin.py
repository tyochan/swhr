from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, SalaryTitleRecord, AcademicRecord, Spouse

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['staff_id', 'last_name', 'first_name',
                    'is_active', 'is_staff', 'is_superuser']


admin.site.register(User, CustomUserAdmin)
admin.site.register(SalaryTitleRecord)
admin.site.register(AcademicRecord)
admin.site.register(Spouse)
