import pynetbox


url = 'https://netbox.2degrees.nz/'
token = 'your netbox token goes here'


nb = pynetbox.api(
url=url,
token=token,
threading=True,
)


# Get a vrf with the name IP_Tools
vrf = nb.ipam.vrfs.get(name='IP_Tools')


# Get all prefixes associated with IP_Tools vrf
perfix_list = nb.ipam.prefixes.filter(vrf_id=vrf.id)
