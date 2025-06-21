# Custom Python DynDNS Service

A custom selfhosted DynDns service written in python using bind9!

Update your public ip address you got from your isp with a custom domain address.
Works with fritzbox or a custom http/https call to this server.

## Requirements
- Own base Domain Address
- Access to your DNS settings of your base domain

## Request:
```
http(s)://<ip-to-this-server>/update?user=<username>&password=<pass>&host=<domain>&ip=<ipaddr>
```
This Update-URL can be set 1:1 in the fritzbox admin interface. The variables in <> dont have to be replaced EXCEPT <ip-to-this-server> in the beginning.
Fritzbox replace the placeholders/variables automatically with the values provided by you in the form in the admin interface.


## Todos and considerations
- Add Setup steps including setting up a NS Record on the common Nameserver to redirect to this service in the README.md
- Maybe add environment variables in the dockerfile to set the zone subdomain and the nameserver domain name, aswell as the ip of the server the container gets installed on (or maybe we can get it from a script/command???)