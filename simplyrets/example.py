import simplyrets
import PropertiesApi

print "SimplyRETS Python SDK"

api_client = simplyrets.Connection('simplyrets', 'simplyrets')
properties_api = PropertiesApi.PropertiesApi(api_client)

bs = ["SR1234"]
minb = 2
props = properties_api.properties(minbeds=minb, brokers=bs)
for prop in props:
    print 'BrokerId: ' + prop.office.brokerid

prop = properties_api.property(47638976)
print prop.address.full
