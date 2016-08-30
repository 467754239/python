from models import Host, HostGroup
from django.contrib import admin


class HostAdmin(admin.ModelAdmin):
    list_display = ['vendor',
        'hostname',
        'ipaddr',
        'product',
        'osver',
        'cpu_model',
        'cpu_num',
        'sn',
        'identity',
        ]

class HostGroupAdmin(admin.ModelAdmin):
    list_display = ['name',]

admin.site.register(Host, HostAdmin)
#admin.site.register(IPaddr, IPaddrAdmin)
admin.site.register(HostGroup, HostGroupAdmin)
