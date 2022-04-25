#!/usr/bin/python3
#---------------what does this script do?----------------
#cleans up tmp folder, opens csv, generate hosts file, generate yaml files, open yaml files,
# and generates radius secret files
#--------------------------------------------------------

import yaml,csv
#pip3 install --user pyyaml pwgen
import random
import string
import os
import subprocess
import glob
#from ansible_vault import Vault
from pwgen import pwgen
import argparse
import socket

ansible_vault_pass = ""
hosts_list = ""
redhat_found = ""
redhat_hostnames = ""
personal_password = ""

##---parse command line arguments---#
parser = argparse.ArgumentParser(description='Tell the script what csv to load')
#parser.add_argument('--csv', default='vm_list.csv', help='name of file to read (default: vm_list.csv)')
parser.add_argument('-c', default='vm_list.csv', help='name of file to read (default: vm_list.csv)')
csvargument=parser.parse_args()
csvtoread=csvargument.c

##----generate random strings on request----##
def get_random_alphanumeric_string(length):
	letters_and_digits = string.ascii_letters + string.digits
	result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
	#print("Random alphanumeric String is:", result_str)
	return result_str

##----generate a random password and return it----##
def generate_password(characters):
	password = pwgen(characters, no_ambiguous=True)
	return password

##----get any files that we need from lastpass----#
def get_file_from_lastpass(filename):
	print(filename)
	try:
		f = open("tmp/"+filename)
		print(f)
	except FileNotFoundError:
		print(filename+" not found, downloading from lastpass")
		f = open("tmp/"+filename, "w")
		p2 = subprocess.Popen(["lpass", "show", "--notes", "Shared-infra-ansible-server-setup/"+filename], stdout=f)
		os.chmod("tmp/"+filename, 0o400)
	finally:
		f.close()
##----mk dirs exist if they don't already----#
if not os.path.isdir("tmp"):
	os.makedirs("tmp")

if not os.path.isdir("tmp/radius"):
	os.makedirs("tmp/radius")

##----cleanup before our run to make sure we don't have things that we don't want----#
a=0
print("cleaning up tmp")
for file in os.listdir("tmp"):
#	print(file)
	if file.endswith(".yml"):
		file_relpath="tmp/"+file
		print(file+" is a yml file")
		print("removing old file :"+file_relpath)
		os.remove(file_relpath)
	if file.endswith(".json"):
		file_relpath="tmp/"+file
		print(file+" is a json file")
		print("removing old file :"+file_relpath)
		os.remove(file_relpath)
#	if os.path.isfile("tmp/ansible-vault-file"):
	if "ssh_host_ed25519_key" in file:
		file_relpath="tmp/"+file
		print(file+" is a ssh host key file")
		print("removing old file :"+file_relpath)
		os.remove(file_relpath)

for file in os.listdir("tmp/radius"):
	print("removing old file :"+file)
	os.remove("tmp/radius/"+file)

##call the get_file_from_lastpass function to make sure we have needed files
get_file_from_lastpass("ansible-vault-file")
get_file_from_lastpass("ansible-deploy.key")
get_file_from_lastpass("ansible-deploy.key.pub")
get_file_from_lastpass("server_ca")
get_file_from_lastpass("server_ca.pub")

##read in the vault password
with open("tmp/ansible-vault-file") as f:
	ansible_vault_pass = f.read().rstrip("\n")

## generate a username and personal password just incase we find any redhat vm's
###only get's used if we find a redhat vm
aduser = os.getenv('USER')
osuser = aduser.split('@')
personal_password = generate_password(10)


##read in the csv
csvfile = open(csvtoread, 'r')
datareader = csv.DictReader(filter(lambda row: row[0]!='#', csvfile), delimiter=",", quotechar='"')
data_headings = []

#open a hosts file for writing hosts to
print("building hosts file...")
hosts_file = open("inventory/autogen-newservers", 'w')
#this will hold information for us to build an ansible inventory file
hosts_text = ""

#hosts_text += "[radius]\n"
#hosts_text += "gary.snap.net.nz ansible_ssh_private_key_file=~/.ssh/id_rsa\n\n"
hosts_text += "[newservers]\n"

# Loop through each row of the csv
for row_index, row in enumerate(datareader):
	# Empty string that we will fill with YAML formatted text based on data extracted from our CSV.
	yaml_text = ""
	lp_text = ""
	lpr_text = ""
	lpz_text = ""
	zeus_data = ""
	root_data = ""
	dnscheck = ""

	fqdn = row['vm_shortname'].lower()+".2dl.nz"
#	fqdn = row['vm_shortname'].lower()+"."+row['vm_domain'].lower()
#	print(fqdn)
#	try:
#		socket.gethostbyname(fqdn)
#	except:
#		print("Can't resolve: "+fqdn+" Exiting")
#		exit()
#	ymlfilepath = "tmp/"+fqdn+".yml"
	ymlfilepath = "tmp/"+row['vm_ipv4_address']+".yml"
	print("building "+row['vm_ipv4_address']+".yml")
#	vm_yaml_file = open("tmp/"+fqdn+".yml", 'w')
	vm_yaml_file = open("tmp/"+row['vm_ipv4_address']+".yml", 'w')
	# add the shortname to the lastpass text
	#grab the shortname for lastpass files
	lp_text += "Hostname: " + row['vm_shortname'].lower() +"\n"
#	hosts_text += fqdn + "\n"
	#us ip instead of fqdn, so we don't need dns already existing as IPA will create it itself
	hosts_text += row['vm_ipv4_address'] + "\n"
	hosts_list += fqdn + "\n"
	yaml_text += "vm_shortname: " + row['vm_shortname'].lower() +'\n'
	yaml_text += "primary_securitygroup: " + row['primary_securitygroup'].lower() + '\n'
#	yaml_text += "vm_domain: " + row['vm_domain'] +'\n'
	yaml_text += "vcenter_template: " + row['vcenter_template'] +'\n'
	yaml_text += "vcenter_fqdn: " + row['vcenter_fqdn'].lower() +'\n'
	yaml_text += "vcenter_vlan: " + row['vcenter_vlan'] +'\n'
	yaml_text += "vcenter_datacenter: " + row['vcenter_datacenter'] +'\n'
	yaml_text += "vcenter_datastore: " + row['vcenter_datastore'] +'\n'
	yaml_text += "vcenter_cluster: " + row['vcenter_cluster'] +'\n'
	yaml_text += "vcenter_folder: " + row['vcenter_folder'] +'\n'
	yaml_text += "vm_ipv4_address: " + row['vm_ipv4_address'] +'\n'
	yaml_text += "vm_ipv4_netmask: " + row['vm_ipv4_netmask'] +'\n'
	yaml_text += "vm_ipv4_gateway: " + row['vm_ipv4_gateway'] +'\n'
	print("setting dns to ipa servers ips")
	yaml_text += "vm_ipv4_dns_a: " + '172.21.238.3\n'
	yaml_text += "vm_ipv4_dns_b: " + '172.23.238.3\n'
#	print("hi")
	print(row['vcenter_template'])
	if row['vcenter_template'].lower() == "rhel8-template":
		print(osuser[0])
		redhat_found = "true"
#		redhat_hostnames += "  - " + row['vm_shortname'].lower() + "." + row['vm_domain'].lower() +"\n"
		redhat_hostnames += "  - " + row['vm_shortname'].lower() + ".2dl.nz\n"
		yaml_text += "vm_guest_id: rhel8_64Guest\n"
		yaml_text += "localuser: "+osuser[0]+"\n"
		yaml_text += "localpassword: "+personal_password+"\n"
	elif row['vcenter_template'].lower() == "rhel7-template":
		print(osuser[0])
		redhat_found = "true"
#		redhat_hostnames += "  - " + row['vm_shortname'].lower() + "." + row['vm_domain'].lower() +"\n"
		redhat_hostnames += "  - " + row['vm_shortname'].lower() + ".2dl.nz\n"
		yaml_text += "vm_guest_id: rhel7_64Guest\n"
		yaml_text += "localuser: "+osuser[0]+"\n"
		yaml_text += "localpassword: "+personal_password+"\n"
	elif row['vcenter_template'].lower() == "suse15-template":
		print(osuser[0])
		redhat_found = "true"
#		redhat_hostnames += "  - " + row['vm_shortname'].lower() + "." + row['vm_domain'].lower() +"\n"
		redhat_hostnames += "  - " + row['vm_shortname'].lower() + ".2dl.nz\n"
		yaml_text += "vm_guest_id: sles15_64Guest\n"
		yaml_text += "localuser: "+osuser[0]+"\n"
		yaml_text += "localpassword: "+personal_password+"\n"
	elif row['vcenter_template'].lower() == "ubuntu18-template":
		yaml_text += "vm_guest_id: ubuntu64Guest\n"
	elif row['vcenter_template'].lower() == "ubuntu20-template":
		yaml_text += "vm_guest_id: ubuntu64Guest\n"
	elif row['vcenter_template'].lower() == "ubuntu22-template":
		yaml_text += "vm_guest_id: ubuntu64Guest\n"
	elif row['vcenter_template'].lower() == "ubuntu22-alpha":
		yaml_text += "vm_guest_id: ubuntu64Guest\n"
	else:
		print("not a redhat server")
	print("ho")
	if row['ipv6'].lower() == "true" or row['ipv6'].lower() == "yes":
		print("ipv6 found")
		#generate radius compatible ipv6 name
		yaml_text += "vm_ipv6_address_underscores: "+row["vm_ipv6_address"].replace(':','_') +'\n'
		#print everything else
		yaml_text += "ipv6: true\n"
		yaml_text += "vm_ipv6_address: "+row["vm_ipv6_address"] +'\n'
		yaml_text += "vm_ipv6_netmask: "+row["vm_ipv6_netmask"] +'\n'
		yaml_text += "vm_ipv6_gateway: "+row["vm_ipv6_gateway"] +'\n'
		yaml_text += "vm_ipv6_dns_a: "+row["vm_ipv6_dns_a"] +'\n'
		yaml_text += "vm_ipv6_dns_b: "+row["vm_ipv6_dns_b"] +'\n'
	else:
		print("ipve6 not found")
		yaml_text += "ipv6: false\n"
	yaml_text += "description: " + row['description'] +'\n'
	# generate a random radius secret
	yaml_text += "vm_radius_secret: "+get_random_alphanumeric_string(24)+"\n"

	# generate a random password for root
	root_passwd = generate_password(16)
	yaml_text += "vm_root_password: "+root_passwd+"\n"

	lpr_text += "NoteType: Server\n"
	lpr_text += "Username: root\n"
	lpr_text += "Password: "+root_passwd+"\n"


	# generate a random password for zeus
	zeus_passwd = generate_password(16)
	yaml_text += "vm_zeus_password: "+zeus_passwd+"\n"

	lpz_text += "NoteType: Server\n"
	lpz_text += "Username: zeus\n"
	lpz_text += "Password: "+zeus_passwd+"\n"


	# Write our YAML string to the new text file and close it.
#		print(yaml_text)
	vm_yaml_file.write(yaml_text)
	vm_yaml_file.close()
	print(vm_yaml_file)


	#create the lastpass files to upload
		#root user
	root_json = "tmp/"+fqdn+"_root.json"
	vm_root_passwd_file = open("tmp/"+fqdn+"_root.json", 'w')
	root_data += lp_text
	root_data += lpr_text
#		print('-rootdata--\n')
#		print(root_data)
	vm_root_passwd_file.write(root_data)
	vm_root_passwd_file.close()

		#zeus user
	zeus_json = "tmp/"+fqdn+"_zeus.json"
	vm_zeus_passwd_file = open("tmp/"+fqdn+"_zeus.json", 'w')
	zeus_data += lp_text
	zeus_data += lpz_text
#		print('-zeusdata--\n')
#		print(zeus_data)
	vm_zeus_passwd_file.write(zeus_data)
	vm_zeus_passwd_file.close()

	#upload the root passwords
	print("uploading to lastpass :"+root_json)
	p1 = subprocess.Popen(["cat", root_json], stdout=subprocess.PIPE)
	p2 = subprocess.Popen(["lpass", "edit", "--notes", "--non-interactive", "Shared-Techm/auto-bgs/[bg]"+fqdn+"root"], stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close()
	p2.communicate()[0]
	#remove the password file
####	os.remove(root_json)

	#upload the zeus passwords
	print("uploading to lastpass :"+zeus_json)
	p1 = subprocess.Popen(["cat", zeus_json], stdout=subprocess.PIPE)
	p2 = subprocess.Popen(["lpass", "edit", "--notes", "--non-interactive", "Shared-Techm/auto-bgs/[bg]"+fqdn+"zeus"], stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close()
	p2.communicate()[0]
	subprocess.run(["lpass", "sync"])
	#remove the password file
####	os.remove(zeus_json)

	print("hosts_text -- "+hosts_text)
	print("hosts_list -- "+hosts_list)
	print("lp_text -- "+lp_text)

#generate the variables for the hosts
hosts_text += "\n"
hosts_text += "[newservers:vars]\n"
hosts_text += "ansible_ssh_private_key_file='./tmp/ansible-deploy.key'\n"
hosts_text += "ansible_ssh_extra_args='-o StrictHostKeyChecking=no'\n"

#write our hosts string to the hosts_file and close it
hosts_file.write(hosts_text)
hosts_file.close()
# We're done! Close the CSV file.
csvfile.close()
#exit()
##----open all yml files and generate radius secret files from them----##
print("building radius files...")
for file in os.listdir("tmp"):
	if file.endswith(".yml"):
		ymlfilepath="tmp/"+file
		print("building radius file for "+file+"...")
		yaml_file = open("tmp/"+ file, "r")
		parsed_yaml_file = yaml.load(yaml_file, Loader=yaml.FullLoader)
		radius_secret=(parsed_yaml_file["vm_radius_secret"])
		shortname=(parsed_yaml_file["vm_shortname"])
		ipv4_address=(parsed_yaml_file["vm_ipv4_address"])

		#write the ipv4 hosts file
		ipv4_radius_file = open("tmp/radius/"+ipv4_address,"w+")
		ipv4_radius_file.write("client "+ipv4_address+" {\n\t\tsecret = "+radius_secret+"\n\t\tshortname = "+shortname+"."+ipv4_address+"\n}\n")
		ipv4_radius_file.close()

		#if we find ipv6 information create an ipv6 secrets file
		if "vm_ipv6_address_underscores" in parsed_yaml_file:
			ipv6_address_underscores=(parsed_yaml_file["vm_ipv6_address_underscores"])
		if "vm_ipv6_address" in parsed_yaml_file:
			ipv6_address=(parsed_yaml_file["vm_ipv6_address"])

			#write the ipv6 hosts file
			ipv6_radius_file = open("tmp/radius/"+ipv6_address_underscores,"w+")
			ipv6_radius_file.write("client "+ipv6_address+" {\n\t\tsecret = "+radius_secret+"\n\t\tshortname = "+shortname+"."+ipv6_address+"\n}\n")
			ipv6_radius_file.close()


		yaml_file.close()
		#encrypt the file
		print("encrypting :"+ymlfilepath)
		subprocess.run(["ansible-vault", "encrypt", ymlfilepath, "--vault-password-file=tmp/ansible-vault-file"])

#we need to get host information for below

##---generate username and password info we can use for initial non ad redhat logins----#
if redhat_found:
	print("redhat server found, generating local user information")

	pswdfile = open("personal.yml",'a')
	#print(osuser[0])
	personal_text = ""
	personal_text += "#new server range\n"
	personal_text += "hosts:\n"
	personal_text += redhat_hostnames
	personal_text += "username: "+ osuser[0]+"\n"
	personal_text += "password: "+personal_password
	personal_text += "\n"
	personal_text += "\n"

	#write our hosts string to the hosts_file and close it
	pswdfile.write(personal_text)
	pswdfile.close()
#exit(0)

print("")
print("---------------------------------------------------------------------------------------------------")
print("--------------====You can now deploy the servers using one of the below commands====---------------")
print("---------------------------------------------------------------------------------------------------")

print("---===---====---===---===---===---===---for IPA testing only---===---===---===---===---===---===---")
print("ansible-playbook playbooks/newservers-ipa-stag.yml --vault-password-file tmp/ansible-vault-file")
print("")
print("")
print("---===---====---===---===---===---===---===--Production--===---===---===---===---===---===---===---")
print("ansible-playbook playbooks/newservers-ipa.yml --vault-password-file tmp/ansible-vault-file")
print("")
print("")
