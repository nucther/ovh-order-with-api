import ovh
from pprint import pprint

client = ovh.Client()

# Get Dedicate server
dedicates = client.get('/order/catalog/public/eco?SG')

pprint(dedicates['dedicated'])
