
import sys
import os

if __name__ == '__main__':
    pass




from zeep import Client
from zeep import Settings
from zeep.transports import Transport
from zeep.cache import SqliteCache
from zeep import xsd
from lxml import etree
from pretend import stub


import requests

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

# configure proxies
transport.session.proxies = {
    'http': 'localhost:8888',
    'https': 'localhost:8888',
}
os.environ["http_proxy"] = 'http://localhost:8888'
os.environ["https_proxy"] = 'http://localhost:8888'


# configure authentication
user = os.environ["axis_soap_user"]
password = os.environ["axis_soap_password"]
auth = requests.auth.HTTPDigestAuth(user, password)
transport.session.auth = auth

# configure cache
#!!cache = SqliteCache(timeout=3600)
#!!transport.cache = cache

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

service = client.create_service(
    '{http://www.axis.com/vapix/ws/action1}ActionBinding',
    'http://axis-mk2.home/vapix/services')


client.set_ns_prefix('aa', "http://www.axis.com/vapix/ws/action1")
client.set_ns_prefix('wsnt', "http://docs.oasis-open.org/wsn/b-2")
client.set_ns_prefix('tns1', "http://www.onvif.org/ver10/topics")
client.set_ns_prefix('tnsaxis', "http://www.axis.com/2009/event/topics")
# client.set_ns_prefix('aev', "http://www.axis.com/vapix/ws/event1")

# http://axis-mk2.home/wsdl/vapix/ActionService.wsdl?timestamp=1550949556124


body = """
        <?xml version="1.0" ?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:aa="http://www.axis.com/vapix/ws/action1"
    xmlns:wsnt="http://docs.oasis-open.org/wsn/b-2"
    xmlns:tns1="http://www.onvif.org/ver10/topics"
    xmlns:tnsaxis="http://www.axis.com/2009/event/topics"
    xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
<soap:Body>
   <aa:AddActionRule xmlns="http://www.axis.com/vapix/ws/action1">
      <NewActionRule>
         <Name>TTTzz</Name>
         <Enabled>false</Enabled>
         <StartEvent>
             <wsnt:TopicExpression Dialect="http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet">tnsaxis:Storage/Disruption</wsnt:TopicExpression>
             <wsnt:MessageContent Dialect="http://www.onvif.org/ver10/tev/messageContentFilter/ItemFilter">boolean(//SimpleItem[@Name="disruption" and @Value="1"]) and boolean(//SimpleItem[@Name="disk_id" and @Value="SD_DISK"])</wsnt:MessageContent>
          </StartEvent>
         <PrimaryAction>36</PrimaryAction>
      </NewActionRule>
      </aa:AddActionRule>
   </soap:Body>
</soap:Envelope>
    """.strip()

response = stub(status_code=200, headers={}, content=content)

operation = service._binding._operations["AddActionRule"]
result = service._binding.process_reply(client, operation, response)




NewActionRule_type = client.get_type('ns0:NewActionRule')
Conditions_type = client.get_type('aa:Conditions')
TopicExpressionType_type = client.get_type('wsnt:TopicExpressionType')
FilterType_type = client.get_type('wsnt:FilterType')
# MessageContent_type = client.get_type('wsnt:MessageContent')


#       <!--===============================-->
# 
#       <xs:complexType name="Conditions">
#         <xs:sequence>
#           <xs:element name="Condition"
#                       type="wsnt:FilterType"
#                       minOccurs="1"
#                       maxOccurs="unbounded" />
#         </xs:sequence>
#       </xs:complexType>

rules = service.GetActionRules()

for r in rules:
    print (r['Name'])


ze_rule_list = (r for r in rules if r['Name'] == 'SendAutoTrack_tmpl')

ze_rule = next(ze_rule_list)
assert ze_rule is not None, "Rule SendAutoTrack_tmpl not found!"

#ze_rule = next (r for r in rules if r['Name'] == 'SendAutoTrack')

Conditions = ze_rule['Conditions']
Condition_seq=Conditions['Condition']
Condition_0=Condition_seq[0]
filterType_0_0_seq=Condition_0['_value_1']
any_0=xsd.AnyObject(FilterType_type,  filterType_0_0_seq[0])
any_1=xsd.AnyObject(FilterType_type,  filterType_0_0_seq[1])

any_list_NEW=[any_0,any_1]
Condition_0_NEW=FilterType_type(any_list_NEW)

Condition_seq_NEW = [Condition_0_NEW]
Conditions_NEW = Conditions_type(Condition_seq_NEW)

source_rule_to_clone = ze_rule

newActioRule = NewActionRule_type (Name=source_rule_to_clone['Name']+'2',
                                                Enabled=source_rule_to_clone['Enabled'],
                                                PrimaryAction=source_rule_to_clone['PrimaryAction'],
                                                StartEvent=source_rule_to_clone['StartEvent'],
                                                Conditions=Conditions_NEW
#                                               ActivationTimeout=source_rule_to_clone['ActivationTimeout'],
#                                               FailoverAction=source_rule_to_clone['FailoverAction']
                                                )

node = etree.Element("document")

add_result = service.AddActionRule (NewActionRule=newActioRule)


newFilterType_1 = xsd.AnyObject(xsd.String(), '1234')
newFilterTypes = [ [ newFilterType_1 ] ]



class MyRendered (object):
    localname = 'my_local_name'
    
    tt = '''<wsnt:TopicExpression Dialect="http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet">
          tns1:RuleEngine/tnsaxis:DigitalAutotracking/tracking//.
          </wsnt:TopicExpression>
          <wsnt:MessageContent Dialect="http://www.onvif.org/ver10/tev/messageContentFilter/ItemFilter">
              boolean(//SimpleItem[@Name="active" and @Value="1"])
          </wsnt:MessageContent>
          </Condition>'''
    nb_iter = None
    def __init__(self):
        self.nb_iter = 0
    
    def __iter__(self):
        print ("++++ ITERATE")
        return self
        
    def __next__(self):
        print ("++++ next element")
        
        if (self.nb_iter >= 1):
            raise StopIteration
        
        self.nb_iter += 1
        return self.tt
    
zz = xsd.String()
my_string=xsd.SkipValue

value = [ xsd.AnyType(MyRendered) ]
newConditionsRebuilt = Conditions_type (value)

newConditions = MyRendered ()


import zeep.xsd.types.builtins
# class RawXmlString(zeep.xsd.types.builtins.BuiltinType,
#              zeep.xsd.types.builtins.AnySimpleType):
#     _default_qname = xsd_ns('string')
#     accepted_types = six.string_types
# 
#     @check_no_collection
#     def xmlvalue(self, value):
#         if isinstance(value, bytes):
#             return value.decode('utf-8')
#         return six.text_type(value if value is not None else '')
# 
#     def pythonvalue(self, value):
#         return value




template_rule = ze_rule
newActioRule = NewActionRule_type (Name=template_rule['Name']+'2',
                                   Enabled=template_rule['Enabled'],
                                   PrimaryAction=template_rule['PrimaryAction'],
                                   StartEvent=template_rule['StartEvent'],
                                   Conditions=newConditions
#                                   ActivationTimeout=template_rule['ActivationTimeout'],
#                                   FailoverAction=template_rule['FailoverAction']
                                   )
# service.create_message(NewActionRule=newActioRule)
# node = client.create_message(service, 'AddActionRule', NewActionRule=newActioRule)

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

service.create_message(service, operation_name)
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


def test_element_any_type():
    node = etree.fromstring(
        """
        <?xml version="1.0"?>
        <schema xmlns="http://www.w3.org/2001/XMLSchema"
                xmlns:tns="http://tests.python-zeep.org/"
                targetNamespace="http://tests.python-zeep.org/"
                elementFormDefault="qualified">
          <element name="container">
            <complexType>
              <sequence>
                <element name="something" type="anyType"/>
              </sequence>
            </complexType>
          </element>
        </schema>
    """.strip()
    )
    schema = xsd.Schema(node)

    container_elm = schema.get_element("{http://tests.python-zeep.org/}container")
    obj = container_elm(something=datetime.time(18, 29, 59))

    node = etree.Element("document")
    container_elm.render(node, obj)
    expected = """
        <document>
            <ns0:container xmlns:ns0="http://tests.python-zeep.org/">
                <ns0:something>18:29:59</ns0:something>
            </ns0:container>
        </document>
    """
    assert_nodes_equal(expected, node)
    item = container_elm.parse(list(node)[0], schema)
    assert item.something == "18:29:59"


def test_element_any_type_elements():
    node = etree.fromstring(
        """
        <?xml version="1.0"?>
        <schema xmlns="http://www.w3.org/2001/XMLSchema"
                xmlns:tns="http://tests.python-zeep.org/"
                targetNamespace="http://tests.python-zeep.org/"
                elementFormDefault="qualified">
          <element name="container">
            <complexType>
              <sequence>
                <element name="something" type="anyType"/>
              </sequence>
            </complexType>
          </element>
        </schema>
    """.strip()
    )
    schema = xsd.Schema(node)

    Child = xsd.ComplexType(
        xsd.Sequence(
            [
                xsd.Element("{http://tests.python-zeep.org/}item_1", xsd.String()),
                xsd.Element("{http://tests.python-zeep.org/}item_2", xsd.String()),
            ]
        )
    )
    child = Child(item_1="item-1", item_2="item-2")

    container_elm = schema.get_element("{http://tests.python-zeep.org/}container")
    obj = container_elm(something=child)

    node = etree.Element("document")
    container_elm.render(node, obj)
    expected = """
        <document>
            <ns0:container xmlns:ns0="http://tests.python-zeep.org/">
                <ns0:something>
                    <ns0:item_1>item-1</ns0:item_1>
                    <ns0:item_2>item-2</ns0:item_2>
                </ns0:something>
            </ns0:container>
        </document>
    """
    assert_nodes_equal(expected, node)
    item = container_elm.parse(list(node)[0], schema)
    assert len(item.something) == 2
    assert item.something[0].text == "item-1"
    assert item.something[1].text == "item-2"
