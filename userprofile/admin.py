from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from userprofile.models import Profile


# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'UserProfile'

# 将 Profile 关联到 User 中
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.register(Profile)
# 重新注册 User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)