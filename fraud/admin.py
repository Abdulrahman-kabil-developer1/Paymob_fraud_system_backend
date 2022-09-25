from django.contrib import admin
from .models import *

admin.AdminSite.site_header = 'Paymob Fraud Detection'
admin.AdminSite.site_title = 'Paymob Fraud Detection'   
admin.AdminSite.index_title = 'Paymob Fraud Detection'  

class TransactionAdmin(admin.ModelAdmin):
    list_display=('amount','transaction_status','message','rule','name','merchant','email','phone','card_num')
    
class GlobalList(admin.ModelAdmin):
    list_display=('type','active','name','email','phone','card_num')
    list_editable=('active','type')
    list_display_links=('name','email','phone','card_num')

class ActionAdmin(admin.ModelAdmin):
    list_display=('name','active','description')
    list_editable=('active','description')
    list_display_links=('name',)

class List(GlobalList):
    fields=GlobalList.get_list_display(self=GlobalList,request=None)
    fields=list(fields)
    fields.insert(2,'merchant')
    fields.insert(3,'ip')
    list_display=fields

class RuleAdmin(admin.ModelAdmin):
    list_display=('name','active','priority','description')
    list_editable=('active','priority')
    filter_horizontal = ('condition','action')

class RviewAdmin(admin.ModelAdmin):
    list_display=('name','reviewed','review_action','reviewed_at','transaction_status','message','rule','merchant','email','phone','card_num')
    list_editable=('reviewed','review_action','reviewed_at')
    
class ConditionAdmin(admin.ModelAdmin):
    list_display=('name','active','type','compare_type','value','description')
    list_editable=('active',)

admin.site.register(Transaction,TransactionAdmin)
admin.site.register(Rule,RuleAdmin)
admin.site.register(Action,ActionAdmin)
admin.site.register(Review,RviewAdmin)
admin.site.register(GlobalBlacklist,GlobalList)
admin.site.register(Blacklist,List)
admin.site.register(Whitelist,List)
admin.site.register(GlobalWhitelist,GlobalList)
admin.site.register(Condition,ConditionAdmin)