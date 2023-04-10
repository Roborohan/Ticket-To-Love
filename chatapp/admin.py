from django.contrib import admin
from .models import Message,Report
 
# Register models here.
 
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'content','sent_at','delivered_at','read_at','status')
admin.site.register(Message, MessageAdmin)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'reported_user', 'message','reason','timestamp')
admin.site.register(Report, ReportAdmin)