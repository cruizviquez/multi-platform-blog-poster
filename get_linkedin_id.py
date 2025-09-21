import requests

# Paste your access token here
access_token = "AQWnhjFgsjCQ5FfnfvCbATxx6S8tPx4hAcm61b9GsIi6kdXmr_N3d8s-cadsCbGwD2aym8IIrr6nfkxDmxADdkW2DmBFHroCuogb74o_VkcJK50GK0cj2-u9SvywxkiSUTZ-trGyR4xfOE1Ebv4FIlYoqhSAvs105_VVGEOiOSm-jOfL3yjB9G1h2ioeU2mBi3KVlSWK0SJmcUQSXnFTlvL2UJ_RFVMUw1OP4gmoCcrrquX4YKWPYEy0mUMD9wYWwu2_yZdLn5BoGk68t6wrALLTI-uIlnPUA9IseGuOZwkr3KggBU3U3Ktu4Ydx84prfzJTpnBhKpIEsa3pON8kiESNCyISJA"

headers = {
    'Authorization': f'Bearer {access_token}',
    'X-Restli-Protocol-Version': '2.0.0'
}

# Get user info
response = requests.get('https://api.linkedin.com/v2/userinfo', headers=headers)
if response.status_code == 200:
    data = response.json()
    print(f"✅ Your LinkedIn User ID: {data['sub']}")
    print(f"Name: {data.get('name', 'N/A')}")
    print(f"Email: {data.get('email', 'N/A')}")
else:
    print(f"❌ Error: {response.status_code} - {response.text}")