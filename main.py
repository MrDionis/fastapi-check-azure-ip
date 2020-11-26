import ipaddress, pickle

from typing import Optional
from fastapi import FastAPI, Query

app = FastAPI(
    title="API for check Azure's IP",
    description='This is an API for getting information about a Microsoft\'s Azure IP. Dump IP\'s range 26.11.2020',
    version='0.1b',
    docs_url=None,
    redoc_url=None)

@app.get("/")
def hello(ip: Optional[str] = Query(None, regex="^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")):

    if not ip:
        return {"message":"Hello! It is checker AzureIP"}

    ip = ipaddress.ip_address(ip)
    with open('list_ip_azure.pickle', 'rb') as f:
        azure_ip = pickle.load(f)

    azure_ip = [ipaddress.ip_network(x) for x in azure_ip]
    for network in azure_ip:
        if ip in network:
            return {"azure": True, "message": f"{str(ip)} in {str(network)} Azure's network"}
    return {"azure": False, "message": f"{str(ip)} not is Azure's IP"}