from django.db import models

class Host(models.Model):
    """store host information"""
    hostname = models.CharField(max_length=30)
    osver = models.CharField(max_length=30)
    vendor = models.CharField(max_length=30)
    product = models.CharField(max_length=30)
    cpu_model = models.CharField(max_length=30)
    cpu_num = models.IntegerField(max_length=2)
    memory = models.IntegerField(max_length=8)
    sn = models.CharField(max_length=30)
    ipaddr = models.IPAddressField(max_length=15)
    identity = models.CharField(max_length=32)

    def __unicode__(self):
        return self.hostname

class HostGroup(models.Model):
    name = models.CharField(max_length=30)
    members = models.ManyToManyField(Host)

    def __unicode__(self):
        return self.name


def handle_hostsave_signal(sender, **kwargs):
    new_host = kwargs['instance']
    old_host = Host.objects.get(identity=new_host.identity)
    if new_host.hostname != old_host.hostname:
        change_hostname(new_host.ipaddr, new_host.hostname)

#models.signals.pre_save.connect(handle_hostsave_signal, sender=Host)
