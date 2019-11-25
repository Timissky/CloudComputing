import sys
import boto3
from boto3.session import Session
import configparser

DEBUG=False

sqs = boto3.client('sqs')

# create queue
# response = sqs.create_queue(
#     QueueName='Task.fifo',
#     Attributes={
#         'DelaySeconds': '0',
#         'MessageRetentionPeriod': '86400',
#         'FifoQueue': 'true'
#     }
# )

response = sqs.get_queue_url(QueueName='Task.fifo')


queue_url = response['QueueUrl']

for n in range(1, 10, 1):
    sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=0,
        MessageGroupId=str(n),
        MessageDeduplicationId=str(n),
        MessageAttributes={
            'Title': {
                'DataType': 'Number',
                'StringValue': str(n)
            },

            'WeeksOn': {
                'DataType': 'Number',
                'StringValue': str(n)
            }
        },
        MessageBody=(
            str(n)
        )
    )
    print(n)
# for receive in range(1, 4, 1):
#     content = sqs.receive_message(
#         QueueUrl=queue_url,
#         AttributeNames=[
#             'SentTimestamp'
#         ],
#         MaxNumberOfMessages=1,
#         MessageAttributeNames=[
#             'All'
#         ],
#         VisibilityTimeout=100,
#         WaitTimeSeconds=0
#     )
#     message = content['Messages'][0]
#     receipt_handle = message['ReceiptHandle']
#
#     sqs.delete_message(
#         QueueUrl=queue_url,
#         ReceiptHandle=receipt_handle
#     )
#
#     print('Received and deleted message: %s' % message)


# print(response)
# queue_url = 'SQS_QUEUE_URL'











# system output

# if len(sys.argv) == 1:
#     print("Usage: {0} <instance-id>".format(sys.argv[0]))
#     sys.exit(1)
#
# instance_id = sys.argv[1]
#
# ec2 = boto3.resource('ec2')
# ec2_instance = ec2.Instance(instance_id)
# json_output = ec2_instance.console_output()
# output = json_output.get('Output', '')
# print(output)




# run instance

# ec2 = boto3.client('ec2')
# response = ec2.describe_instances()
# print(response)

# instances = ec2.create_instances(
#      ImageId='ami-04b9e92b5572fa0d1',
#      MinCount=1,
#      MaxCount=10,
#      InstanceType='t2.micro',
#      KeyName='ec2_coursework'
#  )

# def get_config_info(configFile):
#     cf = configparser.ConfigParser()
#     cf.read(configFile)
#
#     return cf['config']['aws_access_key_id'], \
#            cf['config']['aws_secret_access_key'], \
#            cf['config']['region']
#
#
# def get_instances_info(resource, id_list, state):
#     instances = resource.instances.filter(
#         Filters=[{'Name': 'instance-state-name', 'Values': [state]}])
#
#     if any(instances):
#         for instance in instances:
#             id_list.append(instance.id)
#             print(instance.id, instance.instance_type, instance.state)
#     else:
#         print('instances none in  ' + state)
#
#     return
#
# def main():
#     cmd = ['START', 'STOP', 'CHECK']
#     status = ['stopped', 'running']
#
#     ids = []
#     info = get_config_info(str(sys.argv[1]))
#
#     session = boto3.session.Session(aws_access_key_id=info[0],
#                                     aws_secret_access_key=info[1],
#                                     region_name=info[2])
#
#     ec2 = session.resource('ec2')
#
#     action = sys.argv[2].upper()
#
#     if cmd[2] == action:
#         for sta in status:
#             get_instances_info(ec2, ids, sta)
#
#     elif cmd[0] == action:
#         get_instances_info(ec2, ids, status[0])
#         ec2.instances.filter(InstanceIds=ids).start()
#
#     elif cmd[1] == action:
#         get_instances_info(ec2, ids, status[1])
#         ec2.instances.filter(InstanceIds=ids).stop()
#
#
# if __name__ == '__main__':
#     main()

