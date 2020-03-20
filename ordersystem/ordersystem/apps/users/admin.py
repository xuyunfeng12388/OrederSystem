from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User
# Register your models here.


class UserProfileAdmin(UserAdmin):
    pass
#     list_display = ('username')
#     add_fieldsets = (
#         (None, {
#             'classes': (),
#             'fields': ('username'),
#         }),
#     )


admin.site.register(User, UserProfileAdmin)

admin.site.site_header = '点餐后台管理系统'
admin.site.site_title = '深圳龙域通信科技有限公司'
admin.site.index_title = '欢迎使用点餐后台管理系统'
