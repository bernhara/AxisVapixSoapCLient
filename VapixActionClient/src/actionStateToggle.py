
import sys
import os

if __name__ == '__main__':
    pass




from zeep import Client
from zeep import Settings
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

# Define the address, user name and password for the Axis product. <ip-address> is an IP address or host name.
# string address="<ip-address>";
# string username="<user name>";
# string password="<password>";
#  
# // Define the namespaces of the event and action services.
# string eventTargetNamespace = "http://www.axis.com/vapix/ws/event1";
# string actionTargetNamespace = "http://www.axis.com/vapix/ws/action1";
#  
# // Create an Entry Service client.
# EntryClient myEntryService = CreateEntryServiceClient(address, username, password);

# url="file:///C:/Users/bibi/EclipseWorkspaces/TMP/CamTest/etc/ActionServiceWithServiceDef.wsdl"

settings = Settings(strict=False, raw_response=False)

client = Client(url, transport=transport, settings=settings)

# client.set_ns_prefix('aa', "http://www.axis.com/vapix/ws/action1")
client.set_ns_prefix('wsnt', "http://docs.oasis-open.org/wsn/b-2")
client.set_ns_prefix('tns1', "http://www.onvif.org/ver10/topics")
# client.set_ns_prefix('tnsaxis', "http://www.axis.com/2009/event/topics")
# client.set_ns_prefix('aev', "http://www.axis.com/vapix/ws/event1")

# http://axis-mk2.home/wsdl/vapix/ActionService.wsdl?timestamp=1550949556124

service = client.create_service(
    '{http://www.axis.com/vapix/ws/action1}ActionBinding',
    'http://axis-mk2.home/vapix/services')


NewActionRule_type = client.get_type('ns0:NewActionRule')
TopicExpressionType_type = client.get_type('wsnt:TopicExpressionType') 

rules = service.GetActionRules()

ze_rule = rules[5]
#ze_rule = next (r for r in rules if r['Name'] == 'SendAutoTrack')

conditions = ze_rule['Conditions']
condition_FilterType=conditions['Condition']
value_1 = condition[0]

newActioRule = NewActionRule_type (Name=template_rule['Name']+'2',
                                   Enabled=template_rule['Enabled'],
                                   PrimaryAction=template_rule['PrimaryAction'],
                                   StartEvent=template_rule['StartEvent'],
                                   Conditions=template_rule['Conditions'],
#                                   ActivationTimeout=template_rule['ActivationTimeout'],
#                                   FailoverAction=template_rule['FailoverAction']
                                   )


add_result = service.AddActionRule (NewActionRule=newActioRule)





sys.ext(1)

AddActionRule_type = client.get_type('{http://www.axis.com/vapix/ws/action1}AddActionRule')
NewActionRule_type = client.get_type('{http://www.axis.com/vapix/ws/action1}NewActionRule')

#!! addActionRuleRequest_type = client.get_message('{http://www.axis.com/vapix/ws/action1}AddActionRuleRequest')


rules = service.GetActionRules()
# rr = service.RemoveActionRule ()
# cc = service.AddActionRule ()


tt = NewActionRule_type()
zz = AddActionRule_type(tt)


client.create_message(service, operation_name)
tt = new_rule_type()
node = client.create_message(service, 'AddActionRule', tt)

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

