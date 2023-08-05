import requests
import json
import msal
from lib import azure_restapi_urilist

class CustomerResourceManager:

    def __init__(self,tenant_id,subscription_id,app_id,app_key):

        self.tenant_id = tenant_id

        self.subscription_id = subscription_id

        self.app_id = app_id

        self.app_key = app_key

        self.authority = f'https://login.microsoftonline.com/{tenant_id}'

        self.context = msal.ConfidentialClientApplication(app_id, app_key, self.authority)

        self.scope = f'https://management.azure.com/.default'

        self.token = self.context.acquire_token_for_client([self.scope])

        self.headers = {'Authorization': 'Bearer ' + self.token['access_token'], 'Content-Type': 'application/json'}

    def request(self,url,resourcegroup=None):
        try:
            if resourcegroup != None:
                self.url = f'https://management.azure.com/subscriptions/{self.subscription_id}/resourceGroups/{resourcegroup}{url}'
                request = requests.get(self.url, headers=self.headers)
                result = json.dumps(request.json(), indent=4, sort_keys=True, separators=(',', ': '))
                result_list = json.loads(result)
                return(result_list['value'])
            else:
                self.url = f'https://management.azure.com/subscriptions/{self.subscription_id}{url}'
                request = requests.get(self.url, headers=self.headers)
                result = json.dumps(request.json(), indent=4, sort_keys=True, separators=(',', ': '))
                result_list = json.loads(result)
                
                return(result_list['value'])

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
    
    def get_azure_health(self):
        self.health = f'https://management.azure.com/subscriptions/{self.subscription_id}/providers/Microsoft.ResourceHealth/availabilityStatuses?api-version=2022-10-01'
        request = requests.get(self.health, headers=self.headers)
        result = json.dumps(request.json(), indent=4, sort_keys=True, separators=(',', ': '))
        heath_list = json.loads(result)
        return heath_list

    ## 구독내에 모든 리소스그룹 반환
    def get_resource_group(self):
        
        resource_group_url = f'/resourcegroups?api-version=2021-04-01'
        self.resource_group_list = self.request(resource_group_url)
        
        if len(self.resource_group_list) == 0:
            return []
        else:
            return self.resource_group_list
        
    ## 리소스그룹을 전달받아 리소스그룹 내에 전달 받은 인자에 리소스 출력
    def get_resource_list(self,resource_type,resource_group=None):
        self.all_resource = []

        if resource_type == "sql_db" or resource_type == "sql_fw":
            
            if resource_group is None:
                resource_groups = self.resource_group_list
            else:
                resource_groups = [resource_group]
                
            for group in resource_groups:
                resource_group_name = group['name']

                sql_server_list_url = f'/resourceGroups/{resource_group_name}' + azure_restapi_urilist.url['sql_server']
                sql_server_list = self.request(sql_server_list_url)

                for sql_server in sql_server_list:
                    sql_server_name = sql_server['name']
                    if resource_type == "sql_db":
                        sql_db_list_url = f'/resourceGroups/{resource_group_name}/providers/Microsoft.Sql/servers/{sql_server_name}/databases?api-version=2022-05-01-preview'
                        sql_list = self.request(sql_db_list_url)

                    elif resource_type == "sql_fw":
                        sql_fw_list_url = f'/resourceGroups/{resource_group_name}/providers/Microsoft.Sql/servers/{sql_server_name}/firewallRules?api-version=2022-05-01-preview'
                        sql_list = self.request(sql_fw_list_url)
  
                    if len(sql_list) != 0:
                        self.all_resource.extend(sql_list)  # Add VMs from the current resource group to the all_vms list
            if len(self.all_resource) == 0:
                return []
            else:
                return self.all_resource
                
        else:
            
            if resource_group is None:
                resource_groups = self.resource_group_list
            else:
                resource_groups = [resource_group]
                
            for group in resource_groups:
                resource_group_name = group['name']

                resource_list_url = f'/resourceGroups/{resource_group_name}' + azure_restapi_urilist.url[resource_type]
                resource_list = self.request(resource_list_url)
                
                if len(resource_list) != 0:
                    self.all_resource.extend(resource_list)  # Add VMs from the current resource group to the all_vms list
            if len(self.all_resource) == 0:
                return []
            else:
                return self.all_resource