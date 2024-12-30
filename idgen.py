import hashlib
import base64

def generate_id(seed,ip,salt1,salt2):
    seedid = generate_seedid(seed,salt1,salt2)
    ipid = generate_ipid(ip,salt1,salt2)
    return (seedid[:7]+"-"+ipid[:4]).replace("=","!").replace("/","?")
    
def generate_seedid(seed,salt1,salt2):
    seedid = salt1 + seed + salt2
    return base64.b64encode(hashlib.sha256(seedid.encode()).hexdigest().encode()).decode('ascii')

def generate_ipid(ip,salt1,salt2):
    ipid = salt2 + ip + salt1
    return base64.b64encode(hashlib.sha256(ipid.encode()).hexdigest().encode()).decode('ascii')