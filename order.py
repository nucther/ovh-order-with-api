import ovh
import json
from pprint import pprint

filter = input("Enter Dedicate Code [KS]: ")
if filter is None or filter == "":
    filter = "KS"

region = input("Please enter region [SG]: ")
if region is None or region == "":
    region = "SG"

# create a client using configuration
client = ovh.Client()

print("Welcome", client.get('/me')['firstname'])

# Get Server Lists 

reqServers = client.get("/order/catalog/public/eco?ovhSubsidiary="+ region)
for plan in reqServers['plans']:
    msg = None
    sparator = ","
    if plan['invoiceName'].find(filter) > -1:
        msg = True
        promoAvail = False
        code = plan['planCode']
        name = plan['invoiceName']
        for price in plan['pricings']:
            if 'installation' in price['capacities'] and price['mode'] == 'default':
                dprice = str(price['price']/100000000) + " " + reqServers['locale']['currencyCode']
                # if price['price'] == 0:
                #     msg = False
                if len(price['promotions']) > 0:
                    promoAvail = True
                    for promo in price['promotions']:
                        dprice = str(promo['total']['value']/100000000)
                else:
                    discount = ""

            # pprint(plan['addonFamilies'])
        status = client.get("/dedicated/server/datacenter/availabilities?planCode=" + code)
        for s in status:
            dcStatus = ""
            for dc in s['datacenters']:
                if dc['availability'] != "unavailable" and dc['availability'] != "unknown" and dc['availability'] != "comingSoon":
                    dcStatus = dcStatus + "  " + dc['datacenter']
            avail = s['memory'] + " " + s['storage'] + " " + dcStatus
            if msg:
                if promoAvail:
                    name = "Promo: " + plan['invoiceName']
                if dcStatus != "":
                    print("{:<20} {:<50} {:<10} {:>10}".format(code, name, dprice,  avail))

# planSelected = input("Enter plan name: ")
