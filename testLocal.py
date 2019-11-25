import hashlib
import time

D = 4
found = 0
block = "COMSM0010cloud"
nonce = 65536
i = -1

checkstr = ""
for j in range(0, D):
    checkstr = checkstr + "0"

tic = time.time();
for j in range (0,nonce,1):
    if found == 1:
        break
    for k in range(0,nonce,1):
        i = i+1

        x = hashlib.sha256()
        y = hashlib.sha256()
        code = block + str(i)
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
toc = time.time();
nonce = i
# print >> "./out.txt", "nonce = ", nonce

# print("nonce = ", nonce,file=f)
spend = toc - tic
f = open("./out.txt","w")
f.write("gold nonce = "+str(nonce)+"\n")
f.write("cost time = "+str(spend)+"\n")
f.close()