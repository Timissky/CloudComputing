Overview:

	The CND system has 4 files in total,
	CNDSystem.py  ----------------- running on local machine
	calculate.py  ----------------- single-process running on the instances
	calculate-2Process.py  -------- dual-processes running on the instances
	README.md  -------------------- help users configure the client
	
	I have uploaded calculate.py and calculate-2Process.py to Github, the user_data in CNDSystem.py will automatically download them to the instances.

Configuration:
	
	Local Environment :
		1.Install the Python3, pip, Boto3, AWSCLI
		2.Configure the AWS secret key in ~/.aws/credentials
		3.change the keypair_name in line 166 in CNDSystem.py into yours
		4.change the security_groups in line 167 in CNDSystem.py into yours
		5.the Difficulty is defined as the number of hexadecimal zeros, so D=1 for  hexadecimal zeros equals D=4 for binary zeros
        	6. remember to purge or delete all the SQS queues before second time you test.
        	7. When test for the second time, please wait for a few seconds until the all the instances have terminated.
		


	instances Environment :
		1.update and upgrade the Advanced Packaging tools
		2.install pip for Python3
		3.install Boto3 package with pip3
		4.configure the AWS secret key (
I have deleted the key on Github. 
You need to configure the AWS secret key yourself and delete the lines 255-260 and lines 273-278 in CNDSystem.py, which are shell commands about configuring the key. 
By the way, I created 2 user_data in order to distinguish different codes I run on instances. 
user_data1 is for single process, user_data2 is for dual-processes
)
		5.codes on instances must be run by Python3

Running:
	$ python3 CNDSystem.py

