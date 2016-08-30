# Create your views here.
from django.shortcuts import render_to_response

from django.http import HttpResponse

from models import Host, HostGroup

try:
    import json
except ImportError,e:
    import simplejson as json

def collect(request):
    req = request
    if req.POST:
        vendor = req.POST.get('vendor')
        product = req.POST.get('product')
        cpu_model = req.POST.get('cpu_model')
        cpu_num = req.POST.get('cpu_num')
        memory = req.POST.get('memory')
        sn = req.POST.get('sn')
        osver = req.POST.get('osver')
        hostname = req.POST.get('hostname')
        identity = req.POST.get('identity')
        try:
            host = Host.objects.get(identity=identity)
        except:
            host = Host()
        host.identity = identity
        host.hostname=hostname
        host.product=product
        host.cpu_num=int(cpu_num)
        host.cpu_model=cpu_model
        host.memory = int(memory)
        host.sn = sn
        host.osver = osver
        host.vendor = vendor
        host.ipaddr = req.POST.get('ip')
        host.save()
        return HttpResponse("ok")
    else:
        return HttpResponse("no post data")

def collectjson(request):
    req = request
    if req.method == "POST":
        jsonobj = json.loads(req.body)
        try:
            host = Host.objects.get(identity=jsonobj['identity'])
        except:
            host = Host()
        try:
            host.identity = jsonobj['identity']
            host.hostname = jsonobj['hostname']
            host.product = jsonobj['product']
            host.cpu_num = jsonobj['cpu_num']
            host.cpu_model = jsonobj['cpu_model']
            host.memory = jsonobj['memory']
            host.sn = jsonobj['sn']
            host.osver = jsonobj['osver']
            host.vendor = jsonobj['vendor']
            host.ipaddr = jsonobj['ip']
            host.save()
            return HttpResponse(json.dumps({'status':0,'message':"ok"}))
        except Exception, e:
            return HttpResponse(json.dumps({'status':-1,'message':str(e)}))
    else:
        return HttpResponse(json.dumps({'status':-2,'message':"no post data"}))

def gethosts(req):
    d=[]
    hostgroups = HostGroup.objects.all()
    for hg in hostgroups:
        ret_hg = {'hostgroup':hg.name,'members':[]}
        members = hg.members.all()
        for h in members:
            ret_h = {'hostname':h.hostname,
                'ipaddr': h.ipaddr,
            }
            ret_hg['members'].append(ret_h)
        d.append(ret_hg)
    ret = {'status':0,'data':d,'message':'OK'}
    return HttpResponse(json.dumps(ret))
                
def gethoststxt(req):
    d=""
    hostgroups = HostGroup.objects.all()
    for hg in hostgroups:
        members = hg.members.all()
        for h in members:
            ips = ','.join([i.ipaddr for i in h.ipaddr_set.all()])
            d += "%s %s %s\n" % (hg.name, h.hostname, ips)
    return HttpResponse(d)


def getHostByIdentity(req):
    try:
        identity = req.GET['hostidentity']
    except:
        return HttpResponse(json.dumps({'status':-1,'message':'no option'}))
    try:
        host = Host.objects.get(identity=identity)
    except:
        return HttpResponse(json.dumps({'status':-2,'message':'no host'}))
    data = {'hostname':host.hostname,
            'hostgroups': [str(hg.name) for hg in host.hostgroup_set.all()]
}
    return HttpResponse(json.dumps({'status':0,'message':'ok','data':data}))
    
