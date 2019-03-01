
import sys
import os
from _ast import Name

if __name__ == '__main__':
    pass

from zeep import Client
from zeep.transports import Transport
from zeep.cache import SqliteCache 

from requests.auth import HTTPDigestAuth

import logging.config

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'zeep.transports': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        },
    }
})

# create zeep transport
transport = Transport()

# # configure proxies
# transport.session.proxies = {
#     'http': 'localhost:8888',
#     'https': 'localhost:8888',
# }

# configure authentication
user = os.environ["axis_soap_user"]
password = os.environ["axis_soap_password"]
auth = HTTPDigestAuth(user, password)
transport.session.auth = auth

# configure cache
cache = SqliteCache(timeout=3600)
transport.cache = cache

url= "http://axis-mk2.home/wsdl/vapix/ActionService.wsdl"
#url = "http://www.axis.com/vapix/ws/EntryService.wsdl"
# http://www.axis.com/vapix/ws/action1/ActionService.wsdl

# url="file:///C:/Users/bibi/EclipseWorkspaces/TMP/CamTest/etc/ActionServiceWithServiceDef.wsdl"


client = Client(url, transport=transport)

# http://axis-mk2.home/wsdl/vapix/ActionService.wsdl?timestamp=1550949556124

service = client.create_service(
    '{http://www.axis.com/vapix/ws/action1}ActionBinding',
    'http://axis-mk2.home/vapix/services')

new_rule_type = client.get_type('{http://www.axis.com/vapix/ws/action1}NewActionRule')

#!! addActionRuleRequest_type = client.get_message('{http://www.axis.com/vapix/ws/action1}AddActionRuleRequest')


rules = service.GetActionRules()
# rr = service.RemoveActionRule ()
# cc = service.AddActionRule ()

for rule in rules:
    name = rule['Name']
    
    if name == 'TTT':
        
        rule_id = rule['RuleID']
        
        # !! remove_result = service.RemoveActionRule (rule_id)
        
        
        
        new_rule = {}
        
        new_rule['Name'] = rule['Name']
        new_rule['Enabled'] = False
        new_rule['StartEvent'] = rule['StartEvent']
        new_rule['PrimaryAction'] = rule['PrimaryAction']
        new_rule['Conditions'] = rule['Conditions']
        new_rule['ActivationTimeout'] = rule['ActivationTimeout']
        new_rule['FailoverAction'] = rule['FailoverAction']
                
        tt = new_rule_type()
        
        r  = new_rule_type(Name=rule['Name'],
                           Enabled=False,
                           StartEvent=rule['StartEvent'],
                           PrimaryAction=rule['PrimaryAction'],
                           Conditions=rule['Conditions'],
                           ActivationTimeout=rule['ActivationTimeout'],
                           FailoverAction=rule['FailoverAction'],
                           )
        
        node = client.create_message(service, 'AddActionRule', r)
        
        add_result = service.AddActionRule (r)
        
        
        
    
        
    

x = 1

