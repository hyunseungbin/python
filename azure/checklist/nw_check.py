
from lib import level_const as level

def vnet_check(vnet,nat_list):
    
    peering_list = []
    subnet_nat = []
    vnet_name = vnet['name']
    vnet_addressSpace = vnet['properties']['addressSpace']['addressPrefixes']
    vnet_location = vnet['location']
    
    if len(vnet['properties']['virtualNetworkPeerings']) >= 1:
        for peering in vnet['properties']['virtualNetworkPeerings']:
            if peering['properties']['peeringState']:
                peering_list.append(peering['name'])
    for subnet in vnet['properties']['subnets']:
        id_check = subnet['id']
        for nat in nat_list:
            if id_check in nat['nat_subnet']:
                subnet_nat.append(id_check)
        subnet_info = {
            'subnet_name' : subnet['name'],
            'subnet_id' : subnet['id'],
            'subnet_address' : subnet['properties']['addressPrefix'],
        }
    vnet_info = {
        'vnet_name' : vnet_name,
        'vnet_location' : vnet_location,
        'vnet_addressSpace' : vnet_addressSpace,
        'vnet_peerings' : peering_list,
        'subnet_list' : subnet_info,
        'subnet_nat' : subnet_nat
    }
    return vnet_info

def check_lb_outbound(session):
    lb_list = session.get_resource_list('lb')
    no_outrule_check = []
    ret = common.CheckResult()
    for lb in lb_list:
        if len(lb['properties']) == 8:
            no_outrule_check.append(lb['name'])
    if len(no_outrule_check) >= 1:
        ret.title = 'check outbound rules in LB'
        ret.level = level.warning
        ret.msg = 'No outbound rules in LB'
        ret.result_rows = [lb_name for lb_name in no_outrule_check]
    else:
        ret.title = 'check outbound rules in LB'
        ret.level = level.success
        ret.msg = ''
    return ret

def check_lb_https(session):
    lb_list = session.get_resource_list('lb')
    no_outrule_check = []
    ret = common.CheckResult()
    for lb in lb_list:
        if len(lb['properties']) == 8:
            no_outrule_check.append(lb['name'])
    if len(no_outrule_check) >= 1:
        ret.title = 'check outbound rules in LB'
        ret.level = level.warning
        ret.msg = 'No outbound rules in LB'
        ret.result_rows = [lb_name for lb_name in no_outrule_check]
    else:
        ret.title = 'check outbound rules in LB'
        ret.level = level.success
        ret.msg = ''
    return ret

def nat_check(nats):
    nat_list = []
    nat_subnet_list = []
    nat_pip_list = []
    for nat in nats:
        if nat['properties']['subnets']:
            for subnet in nat['properties']['subnets']:
                nat_subnet_list.append(subnet['id'])
        if nat['properties']['subnets']:
            for pip in nat['properties']['publicIpAddresses']:
                nat_pip_list.append(pip['id'])
        nat_info = {
            'nat_name' : nat['name'],
            'nat_pip' :  nat_pip_list,
            'nat_subnet' :  nat_subnet_list,
        }
        nat_list.append(nat_info)
    return nat_list

def nic_check(nic):
    nic_name = nic['name']
    nic_subnet = (nic['properties']['ipConfigurations'][0]['properties']['subnet']['id']).split('/')[-1]
    nic_pip = (nic['properties']['ipConfigurations'][0]['properties']['publicIPAddress']['id']).split('/')[-1]
    nic_vm = (nic['properties']['virtualMachine']['id']).split('/')[-1]
    if len(nic_pip) >= 1:
        nic_type = 'public'
    else:
        nic_type = 'private'
    nic_info = {
        'nic_name' : nic_name,
        'nic_subnet' : nic_subnet,
        'nic_pip' : nic_pip,
        'nic_type' : nic_type,
        'nic_vm' : nic_vm
    }
    return nic_info

# def routetable_check(vnet):
#     routetable_list = []
#     for vnet in vnets:
#         for subnet in vnet['properties']['subnets']:
#             for sub in subnet['properties']:
#                 if sub == 'routeTable':
#                     routetable_list.append((subnet['properties']['routeTable']['id']).split('/')[8])

