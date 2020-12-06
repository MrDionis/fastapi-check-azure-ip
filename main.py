import ipaddress, sqlite3

from typing import Optional
from fastapi import FastAPI, Query

app = FastAPI(
    title="API for check Azure's IP",
    description='This is an API for getting information about a Microsoft\'s Azure IP. Dump IP\'s range 26.11.2020',
    version='0.1b',
    docs_url=None,
    redoc_url=None)

conn = sqlite3.connect('azure_rang.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("select * from networks")
azure_ip = [(ipaddress.ip_network(x[0]), x[1]) for x in cursor.fetchall()]

@app.get("/")
def hello(ip: Optional[str] = Query(None, regex="^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")):

    if not ip:
        return {"msg": "Hello! It is checker AzureIP"}

    ip = ipaddress.ip_address(ip)
    for network in azure_ip:
        if ip in network[0]:
            ranges = ', '.join(network[1].split())
            cursor.execute(f"select * from ranges where id in ({ranges})")
            return {
                "azure": True,
                "msg": f"{str(ip)} in {str(network[0])} Azure's network(-s)",
                "network": [{
                    "name": x[1],
                    "region": x[2],
                    "sys_service": x[3],
                    "features": x[4]
                } for x in cursor.fetchall()]
            }
    return {"azure": False, "msg": f"{str(ip)} not is Azure's IP"}