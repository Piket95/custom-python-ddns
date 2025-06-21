# Custom Python DynDNS Skript

Ein Custom selfhosted DynDns service written in python!

Update your public ip address you got from your isp with a custom domain address.
Works with fritzbox or a custom http/https call to this server.

## Request:
```
http(s)://<ip-to-this-server>/update?user=<username>&password=<pass>&host=<domain>&ip=<ipaddr>
```


<!-- Add Setup steps including setting up a NS Record on the common Nameserver to redirect to this service -->