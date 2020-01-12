import subprocess as sp
import os 
#import pyfiglet as pf

def ip_input():
	ip1 = input()
	if sp.getstatusoutput("ping -c 2 {}".format(ip1))[0] == 0:
		return ip1
	else:
		print("IP is down. I repeat, IP is down!!")	

def dependency_check(ip):
	ssh_key = sp.getstatusoutput("ssh-copy-id {}".format(ip))
	if "WARNING: All keys were skipped" in ssh_key[1]:
		pass
	else:
		print("Key send to {}".format(ip))
	jdk_lookup = sp.getoutput("ssh root@{} java -version".format(ip)).lower()
	if 'hotspot' not in jdk_lookup:
		jdk_scp = sp.getstatusoutput("scp /root/Desktop/Software/jdk-8u171-linux-x64.rpm {}:/tmp/jdk-8u171-linux-x64.rpm".format(ip))
		if jdk_scp[0] == 0:
			print("\n------------JDK file sent successfully----------------\n")
			jdk_install = sp.getstatusoutput("ssh {} rpm -ivh /tmp/jdk-8u171-linux-x64.rpm".format(ip))
			#sp.getstatusoutput("ssh {} java -version".format(ip))
			sp.getstatusoutput("ssh {} rm -rf /tmp/jdk-8u171-linux-x64.rpm".format(ip))
			if jdk_install[0] == 0:
				print("\n-------------JDK installation done successfully----------------\n")
				sp.getstatusoutput("scp /root/code/bash.py {}:/tmp/".format(ip))
				bash = sp.getstatusoutput("ssh {} python36 /tmp/bash.py".format(ip))
				if bash[0] == 0:
					print("\n-------------.bashrc file modified------------------\n")
				else:
					print("\n-------------.bashrc file already preset----------------\n")
			else:
				print("\n--------------Error occured in jdk installation-----------------\n")
		else:
			print("\n------------------Error occured in sending jdk file---------------------\n")
	else:
		print("\nJdk already setup\n")	
				
	hadoop_lookup = sp.getoutput("ssh root@ {} hadoop version".format(ip))			
	if 'hadoop' not in hadoop_lookup.lower():
		hadoop_scp = sp.getstatusoutput("scp /root/Desktop/Software/hadoop-1.2.1-1.x86_64.rpm {}:/tmp/".format(ip))
		if hadoop_scp[0] == 0:
			print("\n------------------Hadoop file sent successfully-----------------------\n")
			hadoop_install = sp.getstatusoutput("ssh {} rpm -ivh /tmp/hadoop-1.2.1-1.x86_64.rpm --force".format(ip))
			print("\n")
			sp.getoutput("ssh {} hadoop version".format(ip))
			os.system("ssh {} rm -rf /tmp/hadoop-1.2.1-1.x86_64.rpm".format(ip))
			if hadoop_install[0] == 0:
				print("\n-------------Hadoop installation done successfully--------------\n")
			else:
				print("\n-------------Error occured in hadoop installation---------------\n")
		else:
			print("\n---------------Error occured in sending hadoop file-------------------\n")
	else:
		print("\nHadoop setup prebuilt\n")							

condition = True

try:
	while condition:
		os.system("clear")
		print("\n\n")
		print("\n\t\t\tWelcome to Menu", end = '')
		#_fig = pf.Figlet(font='graffiti')
		#print(_fig.renderText("Welcome to Virtual Reality!!"))
		print("\n\t=================================\n\n")

		print("""\t\tPress 1: to capture photo
		Press 2: live video stream( with some lag :P)
		Press 3: to create web server
		Press 4: to create hadoop setup
		Press 5: to install docker
		Press 6: to install docker image
		Press 7: to exit\n""")

		ch = input("Enter input: ")
	
		if int(ch) == 1:
			print("Enter ip: ", end='')
			ip = ip_input()
			
			sp.getoutput("scp /root/lol.py root@{}:/tmp".format(ip))
			sp.getoutput("ssh root@{} python36 /tmp/lol.py".format(ip))
			sp.getoutput("scp {}:/root/Desktop/abc.png /root/Desktop/".format(ip))
		
		elif int(ch) == 2:
			print("Enter ip: ", end='')
			ip = ip_input()
			
			sp.getoutput("scp /root/video.py root@{}:/tmp".format(ip))
			sp.getoutput("ssh -X root@{} python36 /tmp/video.py".format(ip))
		
		elif int(ch) == 3:
			print("Enter ip: ", end='')
			ip = ip_input()
			
			ssh_key = sp.getoutput("ssh-copy-id {}".format(ip))
			sp.getoutput("scp /root/server.py root@{}:/tmp".format(ip))
			sp.getoutput("ssh root@{} python36 /tmp/server.py".format(ip))
	
		elif int(ch) == 4:
			condition_inside = True
			while condition_inside:
				os.system("clear")
				print("\n\n----------------------Welcome to hadoop installion----------------------------\n\n\n")
				print("""\t\tPress 1: to create namenode
		Press 2: to create datanode
		Press 3: to create client
		Press 4: to create jobtracker
		Press 5: to create tasktracker
		Press 6: to exit\n""")
				ch1 = input("Enter input: ")
				if int(ch1) == 1:
					print("Enter namenode ip: ", end='')
					ip = ip_input()
					sp.getoutput("echo {} | tee /root/Desktop/ip.txt".format(ip))
					dependency_check(ip)
					nn_sendfile = sp.getstatusoutput("scp /root/code/nn_set.py {}:/tmp".format(ip))
					if nn_sendfile[0] == 0:
						nn_file = sp.getstatusoutput("ssh {} python36 /tmp/nn_set.py".format(ip))
						if nn_file[0] == 0:
							print("Namenode script executed successfully\n")
							sp.getoutput("ssh {} hadoop namenode -format".format(ip))
							sp.getoutput("ssh {} iptables -F".format(ip))
							sp.getoutput("ssh {} hadoop-daemon.sh start namenode".format(ip))
							os.system("sleep 1")
						else:
							print("Error occured")
						
						jps_nn = sp.getstatusoutput("ssh {} jps".format(ip))
						if 'namenode' in jps_nn[1].lower():
							print("\nNameNode is being setup and running successfully in {}\n".format(ip))
						else:
							print("\nError in hadoop setup occured.\n")
					else:
						print("\n error in sending namenode setupfile\n")
					
				if int(ch1) == 2:
					num = input("\nEnter the number of datanodes to be setup: ")
					datanode_list = []
					print("\nPlease enter the IP(s):")
					for i in range(0, int(num)):
						ip = str(ip_input())
						datanode_list.append(ip)
					for ip in datanode_list:
						dependency_check(ip)
						print("\n")
						sp.getstatusoutput("scp /root/Desktop/ip.txt {}:/tmp/".format(ip))
						dn_sendfile = sp.getstatusoutput("scp /root/code/dn_set.py {}:/tmp/".format(ip))		
						if dn_sendfile[0] == 0:
							dn_file = sp.getstatusoutput("ssh {} python36 /tmp/dn_set.py".format(ip))
							if dn_file[0] == 0:
								print("Datanode script executed successfully\n")								
								sp.getoutput("ssh {} iptables -F".format(ip))
								sp.getoutput("ssh {} hadoop-daemon.sh start datanode".format(ip))
								os.system("sleep 2")
							else:
								print("Error occured starting datanode")
						
							jps_dn = sp.getstatusoutput("ssh {} jps".format(ip))
							if 'datanode' in jps_dn[1].lower():
								print("\nDataNode is being setup and running successfully in {}\n".format(ip))
							else:
								print("\nError in datanode setup occured.\n")
						else:
							print("\n Error in sending datanode setupfile in {}\n".format(ip))
			
				if int(ch1) == 3:
					print("Enter client ip: ", end='')
					client_ip = str(ip_input())
					sp.getstatusoutput("scp /root/Desktop/ip.txt {}:/tmp/".format(client_ip))
					client_sendfile = sp.getstatusoutput("scp /root/code/client_set.py {}:/tmp/".format(client_ip))		
					if client_sendfile[0] == 0:
						client_file = sp.getstatusoutput("ssh {} python36 /tmp/client_set.py".format(client_ip))
						if client_file[0] == 0:
								print("Client script executed successfully\n")								
								sp.getoutput("ssh {} iptables -F".format(client_ip))
						else:
							print("Client script execution failed\n")
					else:
						print("Error occured in sending client exec file")
	
					
					
				if int(ch1) == 4:
					print("Enter jobtracker ip: ", end='')	
					ip = str(ip_input())
					sp.getoutput("echo {} | tee /root/Desktop/jip.txt".format(ip))
					dependency_check(ip)
					sp.getstatusoutput("scp /root/Desktop/ip.txt {}:/tmp/".format(ip))
					jt_sendfile = sp.getstatusoutput("scp /root/code/jt_set.py {}:/tmp/".format(ip))		
					if jt_sendfile[0] == 0:
						jt_file = sp.getstatusoutput("ssh {} python36 /tmp/jt_set.py".format(ip))
						if jt_file[0] == 0:
							print("Jobtracker script executed successfully\n")								
							sp.getoutput("ssh {} iptables -F".format(ip))
							sp.getoutput("ssh {} hadoop-daemon.sh start jobtracker".format(ip))
							os.system("sleep 2")
						else:
							print("Error occured starting jobtracker")
						
						jps_jt = sp.getstatusoutput("ssh {} jps".format(ip))
						if 'jobtracker' in jps_jt[1].lower():
							print("\nJobtracker is being setup and running successfully in {}\n".format(ip))
						else:
							print("\nError in jobtracker setup occured.\n")
					else:
						print("\n Error in sending jobtracker setupfile in {}\n".format(ip))
				
				
				if int(ch1) == 5:
					num = input("\nEnter the number of tasktrackers to be setup: ")
					tasktracker_list = []
					print("\nPlease enter the IP(s):")
					for i in range(0, int(num)):
						ip = str(ip_input())
						tasktracker_list.append(ip)
					for ip in tasktracker_list:				
						dependency_check(ip)
						sp.getstatusoutput("scp /root/Desktop/jip.txt {}:/tmp/".format(ip))
						tt_sendfile = sp.getstatusoutput("scp /root/code/tt_set.py {}:/tmp/".format(ip))		
						if tt_sendfile[0] == 0:
							tt_file = sp.getstatusoutput("ssh {} python36 /tmp/tt_set.py".format(ip))
							if tt_file[0] == 0:
								print("Tasktracker script executed successfully\n")								
								sp.getoutput("ssh {} iptables -F".format(ip))
								sp.getoutput("ssh {} hadoop-daemon.sh start tasktracker".format(ip))
								os.system("sleep 2")
							else:
								print("Error occured starting tasktracker")
						
							jps_tt = sp.getstatusoutput("ssh {} jps".format(ip))
							if 'tasktracker' in jps_tt[1].lower():
								print("\nTasktracker is being setup and running successfully in {}\n".format(ip))
							else:
								print("\nError in tasktracker setup occured.\n")
						else:
							print("\n Error in sending tasktracker setupfile in {}\n".format(ip))	
					
				if int(ch1) == 6:
					condition_inside = False
			
		elif int(ch) == 5:
			print("Enter ip for docker setup: ", end = '')
			ip = str(ip_input())
			
			docker_send = sp.getstatusoutput("scp /root/code/docker_automate.py {}:/tmp".format(ip))
			if docker_send[0] == 0:
				sp.getstatusoutput("ssh {} python36 /tmp/docker_automate.py".format(ip))
			else:
				print("Error occured while sending docker file")
			 
				
		elif int(ch) == 6:
			print("\nOkie Bbye\n")
			condition = False

except (ValueError, EOFError) as e:
	print("\n\n******************Please provide correct input next time!**********************\n")
except KeyboardInterrupt:
	print("\n\nprogram terminated by user\n")
	


