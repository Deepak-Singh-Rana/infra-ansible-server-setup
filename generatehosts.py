#!/usr/bin/python3
import yaml,csv
#pip3 install --user pyyaml
import random
import string
import os

#---------------what does this script do?----------------
#cleans up tmp folder, opens csv, generate hosts file, generate yaml files, open yaml files, generate radius secret files
#--------------------------------------------------------
#generate random strings on request
def get_random_alphanumeric_string(length):
	letters_and_digits = string.ascii_letters + string.digits
	result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
	#print("Random alphanumeric String is:", result_str)
	return result_str


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

##read in the csv
csvfile = open('vm_list.csv', 'r')
datareader = csv.reader(csvfile, delimiter=",", quotechar='"')
data_headings = []

print("building hosts file...")
#open a hosts file for writing hosts to
hosts_file = open("inventory/hosts", 'w')
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
		filename = row[3]
		print("building "+filename+".yml")
		vm_yaml_file = open("tmp/"+filename+".yml", 'w')

		# Empty string that we will fill with YAML formatted text based on data extracted from our CSV.
		yaml_text = ""
		# Loop through each cell in this row...
		for cell_index, cell in enumerate(row):

			# Compile a line of YAML text from our headings list and the text of the current cell, followed by a linebreak.
			# Heading text is converted to lowercase. Spaces are converted to underscores and hyphens are removed.
			# In the cell text, line endings are replaced with commas.
			cell_heading = data_headings[cell_index].lower().replace(" ", "_").replace("-", "")
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

		# Write our YAML string to the new text file and close it.
		vm_yaml_file.write(yaml_text)
		vm_yaml_file.close()



hosts_text += "\n"
hosts_text += "[newservers:vars]\n"
hosts_text += "ansible_ssh_private_key_file='./files/ansible-deploy.key'\n"
hosts_text += "ansible_ssh_extra_args='-o StrictHostKeyChecking=no'\n"

#write our hosts string to the hosts_file and close it
hosts_file.write(hosts_text)
hosts_file.close()
# We're done! Close the CSV file.
csvfile.close()

print("building radius files...")
#open all yml files and generate radius secret files from them
for file in os.listdir("tmp"):
	if file.endswith(".yml"):
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
