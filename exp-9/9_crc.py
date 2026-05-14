import netpack as npk

data = '100100'
key = '1101'
error_flag=False

print("[=] Message string : {}".format(data))
print("[=] Generator polynomial : {}".format(key))

c = npk.CRC_Class()

rm,CW=c.encode_data(data, key)
print("[=] Remainder is : {}".format(rm))
print("[=] Sender coded word is : {}".format(CW))

if error_flag:
	# Introduce error:
	val=list(CW)
	if val[-1]=='0':
		val[-1]='1'
	else:
		val[-1]='0'
	CW=''.join(val)
	print("-"*50)
	print("Introducing error in sender data")
	print("-"*50)

print("[=] Code word to receiver : {}".format(CW))

rm, msg=c.decode_data(CW, key)
print("[=] Receiver side remainder : {}".format(rm))
print("[=] Received message has [{}]".format(msg))