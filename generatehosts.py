#!/usr/bin/python3
import yaml,csv
#pip3 install --user pyyaml pwgen
import random
import string
import os
import subprocess
#from ansible_vault import Vault
from pwgen import pwgen
import argparse

ansible_vault_pass = ""

parser = argparse.ArgumentParser(description='Tell the script what csv to load')
#parser.add_argument('--csv', default='vm_list.csv', help='name of file to read (default: vm_list.csv)')
parser.add_argument('-c', default='vm_list.csv', help='name of file to read (default: vm_list.csv)')

csvargument=parser.parse_args()
csvtoread=csvargument.c
#print(csvtoread)
#exit()
#---------------what does this script do?----------------
#cleans up tmp folder, opens csv, generate hosts file, generate yaml files, open yaml files, generate radius secret files
#--------------------------------------------------------
#generate random strings on request
def get_random_alphanumeric_string(length):
	letters_and_digits = string.ascii_letters + string.digits
	result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
	#print("Random alphanumeric String is:", result_str)
	return result_str

def generate_password(characters):
	password = pwgen(characters, no_ambiguous=True)
	return password

#cleanup before our run to make sure we don't have things that we don't want
for file in os.listdir("tmp"):
	if file.endswith(".md"):
		print(file+" is a markdown file")
	elif os.path.isdir("tmp/"+file):
		print(file+" is a folder")
	else:
		file_relpath=os.path.join("tmp",file)
		print("removing old file :"+file_relpath)
		os.remove(file_relpath)
for file in os.listdir("tmp/radius"):
	print("removing old file :"+file)
	os.remove("tmp/radius/"+file)

##read in the vault password
with open("ansible-vault-file") as f:
	ansible_vault_pass = f.read().rstrip("\n")
#	vault = Vault(ansible_vault_pass)
#	print(vault)
#	print(ansible_vault_pass)

##read in the csv
csvfile = open(csvtoread, 'r')
datareader = csv.reader(csvfile, delimiter=",", quotechar='"')
data_headings = []

print("building hosts file...")
#open a hosts file for writing hosts to
hosts_file = open("inventory/autogen-newservers", 'w')
hosts_text = ""

hosts_text += "[radius]\n"
hosts_text += "gary.snap.net.nz ansible_ssh_private_key_file=~/.ssh/id_ed25519\n\n"
hosts_text += "[newservers]\n"

# Loop through each row...
for row_index, row in enumerate(datareader):

	# If this is the first row, populate our data_headings variable.
	if row_index == 0:
		data_headings = row

	# Othrwise, create a YAML file from the data in this row...
	else:
		# Open a new file with filename based on index number of our current row.
		#filename = str(row_index) + '.yml'
		#get the shortname from the first column
		print(row[3])
		filename = row[3]
		ymlfilepath = "tmp/"+filename+".yml"
		print("building "+filename+".yml")
		vm_yaml_file = open("tmp/"+filename+".yml", 'w')

		# Empty string that we will fill with YAML formatted text based on data extracted from our CSV.
		yaml_text = ""
		lp_text = ""
		lpr_text = ""
		lpz_text = ""
		zeus_data = ""
		root_data = ""
		# Loop through each cell in this row...
		for cell_index, cell in enumerate(row):

			# Compile a line of YAML text from our headings list and the text of the current cell, followed by a linebreak.
			# Heading text is converted to lowercase. Spaces are converted to underscores and hyphens are removed.
			# In the cell text, line endings are replaced with commas.
			cell_heading = data_headings[cell_index].lower().replace(" ", "_").replace("-", "")
			#grab the shortname for lastpass files
			if cell_heading == "vm_shortname":
				lp_text += "Hostname: "+cell+"\n"
			#if we spot the fqdn then grab it so we can use it
			if cell_heading == "vm_fqdn":
				hosts_text += cell+"\n"
			if cell_heading == "ipv6":
				#if ipv6 is false 0 or empty quit the loop so we don't write empty variables to the yaml
				if cell == "" or cell == "0" or cell.lower() == "false":
					yaml_text += cell_heading + ": false\n"
					print("found false for ipv6")
					break
			#generate radius compatible ipv6 name
			if cell_heading == "vm_ipv6_address":
				ipv6_address_underscores=cell.replace(':','_')
				cell_text_underscores = cell_heading + "_underscores" + ": " + ipv6_address_underscores.replace("\n ", ", ") + "\n"
				yaml_text += cell_text_underscores

			cell_text = cell_heading + ": " + cell.replace("\n", ", ") + "\n"

			# Add this line of text to the current YAML string.
			yaml_text += cell_text

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
		vm_yaml_file.write(yaml_text)
		vm_yaml_file.close()
		print(vm_yaml_file)

	#ecrpyt the yml file as it contains passwords
	#if it is commented out we are jsut encrpyint at the very end of processing everything
#		subprocess.run(["ansible-vault", "encrypt", ymlfilepath, "--vault-password-file=ansible-vault-file"])

	#create the lastpass files to upload
		root_json = "tmp/"+filename+"_root.json"
		zeus_json = "tmp/"+filename+"_zeus.json"
		vm_root_passwd_file = open("tmp/"+filename+"_root.json", 'w')
		vm_zeus_passwd_file = open("tmp/"+filename+"_zeus.json", 'w')
		zeus_data += lp_text
		zeus_data += lpz_text
		root_data += lp_text
		root_data += lpr_text
#		print('-zeusdata--\n')
#		print(zeus_data)
#		print('-rootdata--\n')
#		print(root_data)
		vm_root_passwd_file.write(root_data)
		vm_zeus_passwd_file.write(zeus_data)
		vm_root_passwd_file.close()
		vm_zeus_passwd_file.close()
	#upload the root passwords
		print("uploading to lastpass :"+root_json)
		p1 = subprocess.Popen(["cat", root_json], stdout=subprocess.PIPE)
		p2 = subprocess.Popen(["lpass", "edit", "--notes", "--non-interactive", "Shared-Techm/auto-bgs/[bg]"+filename+"root"], stdin=p1.stdout, stdout=subprocess.PIPE)
		p1.stdout.close()
		p2.communicate()[0]
	#remove the password file
		os.remove(root_json)
	#upload the zeus passwords
		print("uploading to lastpass :"+zeus_json)
		p1 = subprocess.Popen(["cat", zeus_json], stdout=subprocess.PIPE)
		p2 = subprocess.Popen(["lpass", "edit", "--notes", "--non-interactive", "Shared-Techm/auto-bgs/[bg]"+filename+"zeus"], stdin=p1.stdout, stdout=subprocess.PIPE)
		p1.stdout.close()
		p2.communicate()[0]
		subprocess.run(["lpass", "sync"])
	#remove the password file
		os.remove(zeus_json)

#		print("------------------???????????FIX THE PYTHON TO DELETE THE JSON FILES WITH PASSWORDS IN WE DPONT NEED ANYMORE")


hosts_text += "\n"
hosts_text += "[newservers:vars]\n"
hosts_text += "ansible_ssh_private_key_file='./files/ansible-deploy.key'\n"
hosts_text += "ansible_ssh_extra_args='-o StrictHostKeyChecking=no'\n"

#write our hosts string to the hosts_file and close it
hosts_file.write(hosts_text)
hosts_file.close()
# We're done! Close the CSV file.
csvfile.close()

#exit()

print("building radius files...")
#open all yml files and generate radius secret files from them
for file in os.listdir("tmp"):
	if file.endswith(".yml"):
		ymlfilepath="tmp/"+file
		#decrypt the file
#		subprocess.run(["ansible-vault", "decrypt", ymlfilepath, "--vault-password-file=ansible-vault-file"])
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
		#encrpyt the file
		subprocess.run(["ansible-vault", "encrypt", ymlfilepath, "--vault-password-file=ansible-vault-file"])
