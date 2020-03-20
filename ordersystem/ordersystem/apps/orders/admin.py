from django.contrib import admin
from .models import OrderInfo, OrderGoods, DinnerTable

# Register your models here.
# class ApkAdmin(admin.ModelAdmin):
#     list_per_page = 20
#     search_fields = ["name", "pack_name"]
#     list_filter = ['is_launched', 'third_party', "category__name"]
#
#     list_display = ['name', "pack_name", 'show_app_packages', 'show_app_filesize', 'show_app_softwareVersion', 'show_app_VersionCode', "show_all_notSupporttype", "show_all_category","sequence","score","download",'is_image_log','is_big_log' , "is_launched","third_party", "create_time", "update_time"]
#     # readonly_fields = ['name', "pack_name"]
#     fieldsets = (
#         ('基本', {'fields': [('name', "is_launched", "third_party"), "pack_name", "sequence", 'category', 'caption', "introduce",  "author", "age", "apk_log", ('default_image_url','is_image_log'),('apk_big_log','is_big_log') ,"operatingSystems"]}),
#         ('高级', {
#             'fields': ['download', 'score', 'notSupporttype'],
#             'classes': ('collapse',)  # 是否折叠显示
#         })
#     )
#     # 设置关联字段编辑
#     list_display_links = ("name", 'pack_name', "show_all_category")
#
#     # inlines = [ApkSourceStackInline, ApkImageStackInline]
#
#     filter_horizontal = ['notSupporttype', 'category']
#
#     def show_all_notSupporttype(self, obj):
#         return [a.equipment_name for a in obj.notSupporttype.all()]
#
#     show_all_notSupporttype.short_description = '不支持设备类型'

admin.site.register(DinnerTable)
admin.site.register(OrderInfo)
admin.site.register(OrderGoods)
