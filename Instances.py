import logging
import boto3
from botocore.exceptions import ClientError


def create_ec2_instance(image_id, instance_type, keypair_name, security_groups, user_data):
    """Provision and launch an EC2 instance
    The method returns without waiting for the instance to reach
    a running state.
    :param image_id: ID of AMI to launch, such as 'ami-XXXX'
    :param instance_type: string, such as 't2.micro'
    :param keypair_name: string, name of the key pair
    :return Dictionary containing information about the instance. If error,
    returns None.
    """

    # Provision and launch the EC2 instance
    ec2_client = boto3.client('ec2')
    try:
        response = ec2_client.run_instances(ImageId=image_id,
                                            InstanceType=instance_type,
                                            KeyName=keypair_name,
                                            MinCount=1,
                                            MaxCount=1,
                                            SecurityGroups=security_groups,
                                            UserData= user_data
                                            )

    except ClientError as e:
        logging.error(e)
        return None
    return response['Instances'][0]

#######################################################################
def main():
    """Exercise create_ec2_instance()"""

    # Assign these values before running the program
    image_id = 'ami-04b9e92b5572fa0d1'
    instance_type = 't2.micro'
    keypair_name = 'ec2_coursework'
    security_groups = ['default']
    user_data = """#!/bin/bash
touch /home/ubuntu/t1.txt
cat>/home/ubuntu/localtest.py<<EOF
12312
EOF
"""


    user_data2 = """#!/bin/bash
cd /home/ubuntu/
git clone https://github.com/seekelvis/UoB_CloudComputing.git
cd /home/ubuntu/UoB_CloudComputing/

sudo apt-get -y  update
sudo apt-get -y upgrade
echo " update finish ------------------------------"

sudo apt-get -y install python-pip
echo "installed pip --------------------"

sudo apt -y install awscli 
pip install boto3
pip install awscli
echo "installed boto3, awscli"
python /home/ubuntu/UoB_CloudComputing/localtest.py 

mkdir .aws
cp /home/ubuntu/UoB_CloudComputing/credentials /home/ubuntu/.aws/credentials
"""
    user_data3 = """#!/bin/bash
touch /home/ubuntu/t1.txt
cd /home/ubuntu/
git clone https://github.com/seekelvis/UoB_CloudComputing.git

sudo apt-get -y  update
sudo apt-get -y upgrade
sudo apt-get -y install python-pip
sudo apt -y install awscli 
pip install boto3
pip install awscli
pip  install hashlib

mkdir .aws
cp /home/ubuntu/UoB_CloudComputing/credentials /home/ubuntu/.aws/credentials
cp /home/ubuntu/UoB_CloudComputing/config /home/ubuntu/.aws/config
cd /home/ubuntu/

echo " installed hashlib"
python /home/ubuntu/UoB_CloudComputing/localtest.py 
python /home/ubuntu/UoB_CloudComputing/SQS_receive.py
"""
    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # Provision and launch the EC2 instance
    instance_info = create_ec2_instance(image_id, instance_type,
                                        keypair_name,security_groups,user_data3)
    if instance_info is not None:
        logging.info(f'Launched EC2 Instance {instance_info["InstanceId"]}')
        logging.info(f'    VPC ID: {instance_info["VpcId"]}')
        logging.info(f'    Private IP Address: {instance_info["PrivateIpAddress"]}')
        logging.info(f'    Current State: {instance_info["State"]["Name"]}')


if __name__ == '__main__':
    main()


# import boto3
#
# ec2 = boto3.client('ec2')
# response = ec2.describe_key_pairs()
# print(response)

