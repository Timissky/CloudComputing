import hashlib
import time
import boto3

D = 5
found = 0
block = "COMSM0010cloud"
nonce = 65536
i = -1
sqs = boto3.client('sqs')
URL = sqs.get_queue_url(QueueName='Task.fifo')
queue_url = URL['QueueUrl']

checkstr = ""
for j in range(0, D):
    checkstr = checkstr + "0"

for receive in range(1, 10, 1):
    if found == 1:
        break
    content = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=300,
        WaitTimeSeconds=0
    )
    message = content['Messages'][0]
    receipt_handle = message['ReceiptHandle']
    taskUnit = int(message['Body'])

    for k in range(32768*(taskUnit-1)+1, 32768*taskUnit+1 ,1):
        # i = i+1

        x = hashlib.sha256()
        y = hashlib.sha256()
        code = block + str(k)
        # code = block+"0000000000"
        # print ("code= ",code)
        x.update(code.encode("utf-8"))
        temstr = x.hexdigest()
        # print("temstr= ",temstr)

        y.update(temstr.encode("utf-8"))
        result = y.hexdigest()
        # bin_result = hexstr2binstr(result)

        # print("result= ", result)
        # print("bin_reslut = ", bin_result)
        # print("result[d] = ", result[0:2])
        if result[0:D] == checkstr:
            found = 1
            break
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    print('processed and deleted message: %s' % taskUnit)
print("nonce = %s" % k)
response = sqs.get_queue_url(QueueName='Result.fifo')
resultURL = response['QueueUrl']
sqs.send_message(
        QueueUrl=resultURL,
        DelaySeconds=0,
        MessageGroupId=1,
        MessageDeduplicationId=1,
        MessageAttributes={
            'Title': {
                'DataType': 'Number',
                'StringValue': k
            }
        },
        MessageBody=(
            k
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