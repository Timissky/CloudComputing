import hashlib
import time
import boto3


# Difficulty
# D = 8
# The result of founding nonce
found = 0
block = "COMSM0010cloud"
sqs = boto3.client('sqs')
response = sqs.get_queue_url(QueueName='Task.fifo')
task_url = response['QueueUrl']
response = sqs.get_queue_url(QueueName='Log.fifo')
log_url = response['QueueUrl']
response = sqs.get_queue_url(QueueName='Result.fifo')
result_url = response['QueueUrl']


try:
    for receive in range(1, 1000, 1):
        if found == 1:
            break
        content = sqs.receive_message(
            QueueUrl=task_url,
            AttributeNames=[
                'All'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=43100,
            WaitTimeSeconds=0
        )
        message = content['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        # define which task the instance received
        taskUnit = int(message['Body'])
        N = int(message['MessageAttributes']['Total']['StringValue'])
        D = int(message['MessageAttributes']['Difficulty']['StringValue'])
        unitLength = int(67108864/ N)
        unitBegin = unitLength * (taskUnit - 1)
        #4294967296
        if taskUnit == N:
            unitStop = 67108864 + 1
        else:
            unitStop = unitLength * taskUnit
        checkstr = ""
        for j in range(0, D):
            checkstr = checkstr + "0"
#################################################################################################3
# record the time unit begin
        sqs.send_message(
            QueueUrl=log_url,
            DelaySeconds=0,
            MessageGroupId=str(taskUnit),
            MessageDeduplicationId=str(taskUnit),
            MessageAttributes={
            },
            MessageBody=(
                "Unit " + str(taskUnit) + " begin"
            )
        )

        for num in range(unitBegin, unitStop, 1):
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
                    QueueUrl=result_url,
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
            QueueUrl=task_url,
            ReceiptHandle=receipt_handle
        )
        print('processed and deleted message: %s' % taskUnit)
# record the time unit finish
        sqs.send_message(
                QueueUrl=log_url,
                DelaySeconds=0,
                MessageGroupId=str(taskUnit)+"end",
                MessageDeduplicationId=str(taskUnit)+"end",
                MessageAttributes={
                },
                MessageBody=(
                    "Unit " + str(taskUnit) + " end"
                )
            )
######################################################################################################
except:
    sqs.send_message(
        QueueUrl=log_url,
        DelaySeconds=0,
        MessageGroupId=str(taskUnit) + "free",
        MessageDeduplicationId=str(taskUnit) + "free",
        MessageAttributes={
        },
        MessageBody=(
                "No more task after unit " + str(taskUnit)
        )
    )








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

# nonce = k
# print >> "./out.txt", "nonce = ", nonce

# print("nonce = ", nonce,file=f)
# spend = toc - tic
# f = open("./out.txt","w")
# f.write("gold nonce = "+str(nonce)+"\n")
# f.write("cost time = "+str(spend)+"\n")
# f.close()
