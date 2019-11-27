import hashlib
import time
import boto3


# def compute(k):
#     # i = i+1
#     x = hashlib.sha256()
#     y = hashlib.sha256()
#     code = block + str(k)
#     # code = block+"0000000000"
#     # print ("code= ",code)
#     x.update(code.encode("utf-8"))
#     temstr = x.hexdigest()
#     # print("temstr= ",temstr)
#
#     y.update(temstr.encode("utf-8"))
#     result = y.hexdigest()
#     return result


D = 8
found = 0
block = "COMSM0010cloud"
sqs = boto3.client('sqs')
URL = sqs.get_queue_url(QueueName='Task.fifo')
queue_url = URL['QueueUrl']
response = sqs.get_queue_url(QueueName='Result.fifo')
resultURL = response['QueueUrl']

checkstr = ""
for j in range(0, D):
    checkstr = checkstr + "0"


# record the begin time
sqs.send_message(
        QueueUrl=resultURL,
        DelaySeconds=0,
        MessageGroupId='begin',
        MessageDeduplicationId='begin',
        MessageAttributes={
        },
        MessageBody=(
            "begin"
        )
    )
for receive in range(1, 50, 1):
    if found == 1:
        break
    content = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'All'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=3000,
        WaitTimeSeconds=0
    )
    message = content['Messages'][0]
    receipt_handle = message['ReceiptHandle']
    taskUnit = int(message['Body'])

    for num in range(33554433*(taskUnit-1)+1, 33554433*taskUnit+1, 1):
        x = hashlib.sha256()
        y = hashlib.sha256()
        code = block + str(num)
        # code = block+"0000000000"
        # print ("code= ",code)
        x.update(code.encode("utf-8"))
        temstr = x.hexdigest()
        # print("temstr= ",temstr)

        y.update(temstr.encode("utf-8"))
        result = y.hexdigest()
        if result[0:D] == checkstr:
            found = 1
            print("nonce = %s" % num)
            sqs.send_message(
                QueueUrl=resultURL,
                DelaySeconds=0,
                MessageGroupId=str(num),
                MessageDeduplicationId=str(num),
                MessageAttributes={
                },
                MessageBody=(
                    str(num)
                )
            )
            # break
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    print('processed and deleted message: %s' % taskUnit)
sqs.send_message(
        QueueUrl=resultURL,
        DelaySeconds=0,
        MessageGroupId='end',
        MessageDeduplicationId='end',
        MessageAttributes={
        },
        MessageBody=(
            "end"
        )
    )










# nonce = k
# print >> "./out.txt", "nonce = ", nonce

# print("nonce = ", nonce,file=f)
# spend = toc - tic
# f = open("./out.txt","w")
# f.write("gold nonce = "+str(nonce)+"\n")
# f.write("cost time = "+str(spend)+"\n")
# f.close()
