import PureCloudPlatformClientV2
import json

def bytesToMbit(bytes):
	return str(round((((8*bytes)/1024)/1024),2)) 

def printBW(edgeID):
	bw = EdgeApi.get_telephony_providers_edge_metrics(edgeID).to_json()
	bw = json.loads(bw)
	for interface in bw['networks']:
        	if (interface['ifname'] == "eno1"):
                	print ("WAN: ")
                	print ("\tRec Mbits: " + bytesToMbit(interface['received_bytes_per_sec']))
                	print ("\tSent Mbits: " + bytesToMbit(interface['sent_bytes_per_sec']))
        	elif (interface['ifname'] == "eno2"):
                	print ("LAN: ")
                	print ("\tRec Mbits: " + bytesToMbit(interface['received_bytes_per_sec']))
                	print ("\tSent Mbits: " + bytesToMbit(interface['sent_bytes_per_sec']))

# Login to Purecloud, make sure region is correct.
region = PureCloudPlatformClientV2.PureCloudRegionHosts.eu_central_1
PureCloudPlatformClientV2.configuration.host = region.get_api_host()

apiclient = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(token, secret)
authApi = PureCloudPlatformClientV2.AuthorizationApi(apiclient)

EdgeApi = PureCloudPlatformClientV2.TelephonyProvidersEdgeApi(apiclient)

# Get all edges
apiResponse = EdgeApi.get_telephony_providers_edges().to_json()

apiResponse = json.loads(apiResponse)

# Iterate through the edges to get status, calls & bandwidth
for edge in apiResponse['entities']:
  inbound_calls = 0
  outbound_calls = 0
  print (edge['name'] + ": ")
  print (edge['online_status'])
  trunks = EdgeApi.get_telephony_providers_edge_trunks(edge['id']).to_json()
  trunks = json.loads(trunks)
  for trunk in trunks['entities']:
    if (trunk['connected_status']):
      trunkMetrics = EdgeApi.get_telephony_providers_edges_trunk_metrics(trunk['id']).to_json()
      trunkMetrics = json.loads(trunkMetrics)
      inbound_calls = inbound_calls + trunkMetrics['calls']['inbound_call_count']
      outbound_calls = outbound_calls + trunkMetrics['calls']['outbound_call_count']	
  print ("In calls: " + str(inbound_calls))
  print ("Out calls: " + str(outbound_calls))
  printBW (edge['id'])
