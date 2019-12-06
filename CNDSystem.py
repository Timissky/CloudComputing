import logging
import boto3
from botocore.exceptions import ClientError
import time


def create_ec2_instance(image_id, instance_type, keypair_name, security_groups, user_data, Number):
    # Provision and launch the EC2 instance
    ec2_client = boto3.client('ec2')
    try:
        response = ec2_client.run_instances(ImageId=image_id,
                                            InstanceType=instance_type,
                                            KeyName=keypair_name,
                                            MinCount=Number,
                                            MaxCount=Number,
                                            SecurityGroups=security_groups,
                                            UserData= user_data,
                                            CreditSpecification={'CpuCredits': 'unlimited'}
            )


    except ClientError as e:
        logging.error(e)
        return None
    return response['Instances'][0]

def getTimeout():
    print("please enter the time of System Timeout")
    input_str = input()
    if float(input_str) < 0:
        print("please enter a positive number")
        return getTimeout()
    return float(input_str)



def defineProcessor():
    P = 0
    print("enter 1 for single core - single process.   enter 2 for double core - multiprocessing")
    input_str = input()
    if (float(input_str) != 1 and float(input_str) != 2 ):
        print("please enter the right number")
        return defineProcessor()
    else:
        P = int(float(input_str))
        return P

def setDifficulty():
    print("please enter the Difficulty for hexadecimal zeros (D=1 for hexadecimal zeros equals D=4 for binary zeros) ")
    input_str = input()
    if float(input_str) % 1 != 0:
        print("please enter an integer")
        return setDifficulty()
    if float(input_str) < 0:
        print("please enter a positive number")
        return setDifficulty()
    D = int(float(input_str))
    return int(D)


def getNumOfInstances(LargerMargin95, LargerMargin99):
    N = 0
    confLevel=0
    expeTime=0
    print("please enter the number of instances you want.(1--15,integer) \n "
          " OR \nenter the confidence level (only accept 95 and 99) and the expected time (s) split by spacebar (the minimum time is 529)")
    input_str = input()
    inputNum = input_str.split(' ')
    if len(inputNum) == 1:
            if int(float(inputNum[0])) < 1 or int(float(inputNum[0])) >30 or float(inputNum[0]) % 1 != 0:
                    return getNumOfInstances(LargerMargin95, LargerMargin99)
            else:
                    N = inputNum[0]

    elif len(inputNum) == 2:
            if float(inputNum[0]) != 95 and float(inputNum[0]) != 99 or float(inputNum[1]) < 529:
                print("plaease enter the right confidence level and expected time,\nwe only accept 95 and 99 for confidence le"
                      "vel,\nand the expected time has to be larger than 529 \n")
                return getNumOfInstances(LargerMargin95, LargerMargin99)
            else:
                if float(inputNum[0]) == 95:
                    confLevel = int(float(inputNum[0]))
                    expeTime  = float(inputNum[1])
                    for num in range(0,30):
                        if float(LargerMargin95[num]) < expeTime:
                            N = num + 1
                            break
                elif float(inputNum[0]) == 99:
                    confLevel = int(float(inputNum[0]))
                    expeTime = float(inputNum[1])
                    for num in range(0, 30):
                        if float(LargerMargin99[num]) < expeTime:
                            N = num + 1
                            break
                else:
                    return  getNumOfInstances(LargerMargin95, LargerMargin99)
    else:
            print("please enter the right quantity of parameters")
            return getNumOfInstances(LargerMargin95, LargerMargin99)
    return int(N)

def createQ(sqs):
    # create queue
    createTaskQ = sqs.create_queue(
        QueueName='Task.fifo',
        Attributes={
            'DelaySeconds': '0',
            'MessageRetentionPeriod': '86400',
            'FifoQueue': 'true'
        }
    )
    createLogQ = sqs.create_queue(
        QueueName='Log.fifo',
        Attributes={
            'DelaySeconds': '0',
            'MessageRetentionPeriod': '86400',
            'FifoQueue': 'true'
        }
    )
    createResultQ = sqs.create_queue(
        QueueName='Result.fifo',
        Attributes={
            'DelaySeconds': '0',
            'MessageRetentionPeriod': '86400',
            'FifoQueue': 'true'
        }
    )
    print("CND has created Task.fifo, Result.fifo, Log.fifo Queues")
def splitTaskInQueue(sqs, task_url, N, D):
    for n in range(1, N+1, 1):
        sqs.send_message(
            QueueUrl= task_url,
            DelaySeconds=0,
            MessageGroupId=str(n),
            MessageDeduplicationId=str(n),
            MessageAttributes={
                'Total': {
                    'DataType': 'Number',
                    'StringValue': str(N)
                },
                'Difficulty' : {
                    'DataType': 'Number',
                    'StringValue': str(D)
                }
            },
            MessageBody=(
                str(n)
            )
        )
        # print(n)
    print("CND has divided the whole task evenly for every instances")


def terminateAllInstances():
    ec2 = boto3.resource('ec2')
    ec2.instances.terminate()
    print("The CND has terminate all the instances")


#######################################################################
def main():
    # Assign these values before running the program
    # N = 5
    image_id = 'ami-04b9e92b5572fa0d1'
    instance_type = 't2.medium'
    keypair_name = 'ec2_coursework'
    security_groups = ['default']

    P = defineProcessor()
    D = setDifficulty()
    N = getNumOfInstances(LargerMargin95, LargerMargin99)
    Timeout = getTimeout()
    sqs = boto3.client('sqs')
    createQ(sqs)
    response = sqs.get_queue_url(QueueName='Task.fifo')
    task_url = response['QueueUrl']
    response = sqs.get_queue_url(QueueName='Log.fifo')
    log_url = response['QueueUrl']
    response = sqs.get_queue_url(QueueName='Result.fifo')
    result_url = response['QueueUrl']
    splitTaskInQueue(sqs, task_url, N, D)
    # Set up logging
    # logging.basicConfig(level=logging.DEBUG,
    #                     format='%(levelname)s: %(asctime)s: %(message)s')
    # Provision and launch the EC2 instance
    if(P == 1):
        instance_info = create_ec2_instance(image_id, 't2.micro', keypair_name, security_groups, user_data1, N)
    elif(P == 2):
        instance_info = create_ec2_instance(image_id, 't2.medium', keypair_name, security_groups, user_data2, N)


    # if instance_info is not None:
    #     logging.info(f'Launched EC2 Instance {instance_info["InstanceId"]}')
    #     logging.info(f'    VPC ID: {instance_info["VpcId"]}')
    #     logging.info(f'    Private IP Address: {instance_info["PrivateIpAddress"]}')
    #     logging.info(f'    Current State: {instance_info["State"]["Name"]}')
    print("CND has run %s instances \n..........Begin to monitor the response of instances.........." % N)
    time.sleep(4)
    state = 0
    time1 = time.time()
    while state == 0:
        # time.sleep(1)
        try:
            content = sqs.receive_message(
                QueueUrl=result_url,
                AttributeNames=[
                    'All'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ],
                VisibilityTimeout=0,
                WaitTimeSeconds=0
            )
            goldNonce = int(content['Messages'][0]['Body'])
            state = 1
            terminateAllInstances()
            print("\n.\n.\n.\n.\nthe first golden nonce we found is %s \n.\n.\n.\n.\n." % goldNonce)

        except Exception as e:
            messagesNum = sqs.get_queue_attributes(
                QueueUrl=log_url,
                AttributeNames=[
                    'ApproximateNumberOfMessages'])['Attributes']['ApproximateNumberOfMessages']
            time2 = time.time()
            if int(messagesNum) == 3*N:
                state = 2
                terminateAllInstances()
                print("\n.\n.\n.\n.\nthere isn't any golden nonce under D = %s \n.\n.\n.\n.\n." % str(D))
            if (time1-time2) > Timeout:
                terminateAllInstances()
                print("System Timeout , all instances have been terminate")


# recording the larger margin of the confidence interval
LargerMargin95 = [12724.3, 6682.19, 5276.53, 3573.33, 2494.89, 2257.17,
                  2071.77, 1853.70, 1680.51, 1553.54, 1435.17, 1352.80,
                  1213.51, 1085.54, 937.30,  885.69,  861.04,  829.85,
                  809.58,  779.87,  756.68,  709.48,  651.39,  632.85,
                  625.80,  601.59,  558.25,  552.79,  538.98,  521.94
                ]
LargerMargin99 = [12725.68, 6683.93, 5277.99, 3575.14, 2496.51, 2259.74,
                  2073.76, 1855.66, 1682.80, 1556.26, 1437.74, 1355.22,
                  1215.80, 1088.26, 940.75,  889.73,  866.06,  835.20,
                  813.98,  784.39,  761.54,  714.68,  657.39,  638.20,
                  630.29,  607.24,  564.18,  559.36,  545.22,  528.57
                ]


user_data1 = """#!/bin/bash
touch /home/ubuntu/begin.txt
cd /home/ubuntu/
git clone https://github.com/Timissky/CloudComputing.git


cd /root
mkdir .aws
cp /home/ubuntu/CloudComputing/credentials /root/.aws/credentials
cp /home/ubuntu/CloudComputing/config /root/.aws/config

cd /home/ubuntu/
sudo apt-get -y  update
sudo apt-get -y upgrade
sudo apt-get -y install python3-pip
pip3 install boto3


sudo python3 /home/ubuntu/CloudComputing/calculate.py 
touch local.txt
"""
user_data2 = """#!/bin/bash
touch /home/ubuntu/begin.txt
cd /home/ubuntu/
git clone https://github.com/Timissky/CloudComputing.git


cd /root
mkdir .aws
cp /home/ubuntu/CloudComputing/credentials /root/.aws/credentials
cp /home/ubuntu/CloudComputing/config /root/.aws/config

cd /home/ubuntu/
sudo apt-get -y  update
sudo apt-get -y upgrade
sudo apt-get -y install python3-pip
pip3 install boto3


sudo python3 /home/ubuntu/CloudComputing/calculate-2Process.py 
touch local.txt
"""
if __name__ == '__main__':
    main()












# import boto3
#
# ec2 = boto3.client('ec2')

# print(response)

#     user_data = """#!/bin/bash
# touch /home/ubuntu/t1.txt
# cat>/home/ubuntu/localtest.py<<EOF
# 12312
# EOF
# """

#user_data2 = """#!/bin/bash
# cd /home/ubuntu/
# git clone https://github.com/Timissky/CloudComputing.git
# cd /home/ubuntu/CloudComputing/
#
# sudo apt-get -y  update
# sudo apt-get -y upgrade
# echo " update finish ------------------------------"
#
# sudo apt-get -y install python-pip
# echo "installed pip --------------------"
#
# sudo apt -y install awscli
# pip install boto3
# pip install awscli
# echo "installed boto3, awscli"
# python /home/ubuntu/CloudComputing/localtest.py
#
# """