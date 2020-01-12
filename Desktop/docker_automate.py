docker_status = sp.getstatusoutput("which docker")
if docker_status[0] == 0:
	print("Docker already installed")
	sp.getstatusoutput("systemctl start docker")
else:
	sp.getstatusoutput("scp /root/Desktop/rhel7_extra_new_rpm/kube/docker* {}:/tmp/".format(ip))
	sp.getstatusoutput("ssh {} rpm -ivh docker*".format(ip))
	sp.getstatusoutput("systemctl start docker")
	sp.getstatusoutput("systemctl enable docker")
	while condition:
		os.system("clear")
		image = input("which operating system or OS image do you want to load: ")
		print("""Press 1: to load centos:latest
		Press 2: to load ubuntu:14.04
		Press 3: to load ubuntu:latest
		""")
		ch = int(input("Enter input: "))
		if ch == 1:
			docker_load = sp.getstatusoutput("ssh {} docker load -i /root/Desktop/rhel7_5_software_extras/cent*")
			if docker_load[0] == 0:
				print("Image loaded successfully\n")
			else:
				print("Image loading failed\n")
		elif ch == 2:
			docker_load = sp.getstatusoutput("ssh {} docker load -i /root/Desktop/rhel7_5_software_extras/ubuntu:14*")
			if docker_load[0] == 0:
				print("Image loaded successfully\n")
			else:
				print("Image loading failed\n")
		elif ch == 3:
			docker_load = sp.getstatusoutput("ssh {} docker load -i /root/Desktop/rhel7_5_software_extras/ubuntu:la*")
			if docker_load[0] == 0:
				print("Image loaded successfully\n")
			else:
				print("Image loading failed\n")
		else:
			condition = False
