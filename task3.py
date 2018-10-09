import heapq
import random
import math
import sys
import matplotlib.pyplot as plt

def getExp(mean, random_number):
	return round(-mean * math.log(1 - random_number), 4)

def getArray(mean_arr_time, mean_orbit_time, service_time, max_buffer_size, MCL_stop, array):
	MCL = 0
	CLA = 2
	buffer_num = 0
	buffer_idx = []
	CLS = [0, -1] # -1 is the default index of request
	CLR = [] #using min heap
	idx = 0
	CLS_idx = 0

	while MCL <= MCL_stop:
		dic = {}
		#decide event
		event = ''
		#order is CLR, CLA, CLS
		if CLR != []:
			dic['CLR'] = CLR[0][0]
		else:
			dic['CLR'] = float("Inf")

		dic['CLA'] = CLA

		if CLS[0] != 0:
			dic['CLS'] = CLS[0]
		else:
			dic['CLS'] = float("Inf")

		#print(dic)

		event = min(dic, key=dic.get)
		#update MCL
		MCL = dic[event]
		#print(event)

		#if event is CLR
		#if buffer_num == 0 and CLS == 0,buffer += 1, CLS = item + service_time
		#if buffer_num == max_buffer_size, then heappush
		#else go into the buffer
		if event == 'CLR':
			item, item_idx = CLR[0]#pick the smallest one
			heapq.heappop(CLR)

			if CLR == []:#if the CLR is empty, remove the key
				dic.pop('CLR', None)

			if buffer_num == 0 and CLS[0] == 0:

				buffer_num += 1
				buffer_idx.append(item_idx)
				#if there is value in array[i][2], then update array[i][3], otherwise dont update
				if array[item_idx][2] != 0:
					array[item_idx][3] = item

				CLS[0] = item + service_time
				CLS[1] = item_idx
			elif buffer_num == max_buffer_size:
				random_number = random.random()
				orbit_time = getExp(mean_orbit_time, random_number)
				heapq.heappush(CLR, (round(item + orbit_time, 4), item_idx))
				#print("orbit_time:", round(orbit_time, 4))
			else:
				buffer_num += 1
				buffer_idx.append(item_idx)

				#if there is value in array[i][2], then update array[i][3], otherwise dont update
				if array[item_idx][2] != 0:
					array[item_idx][3] = item


		#if event is CLA, 
		#if buffer == 0 and CLS == 0, then buffer += 1 and CLS = CLA + service_time, 
		#if buffer == max_buffer_size, then heapq.heappush(CLR,CLA + orbit_time)
		#else:buffer += 1
		#then update CLA
		elif event == 'CLA':
			temp = [idx, MCL, 0, 0, 0]
			array.append(temp)
			
			if buffer_num == 0 and CLS[0] == 0:

				buffer_num += 1
				buffer_idx.append(idx)

				CLS[0] = CLA + service_time
				CLS[1] = idx
			elif buffer_num == max_buffer_size:
				random_number = random.random()
				orbit_time = getExp(mean_orbit_time, random_number)
				heapq.heappush(CLR, (round(CLA + orbit_time, 4), idx))
				#print("orbit_time:", round(orbit_time, 4))

				#update the array
				array[idx][2] = MCL 

			else:
				buffer_num += 1
				buffer_idx.append(idx)

			random_number = random.random()
			arr_time = getExp(mean_arr_time, random_number)
			CLA += arr_time

			#new request, idx += 1, put into the array, arrive time is the MCL
			idx += 1

			#print("arr_time:", round(arr_time, 4))



		#if event is CLS, 
		#if buffer_num > 0 then CLS += service_time, and buffer_num -= 1
		#if buffer_num == 0, CLS = 0   
		elif event == 'CLS':
			last_idx = buffer_idx.pop(0)
			
			terminated_time = CLS[0] #terminate time is equal to next go in to the queue
			terminated_idx = CLS[1]

			#update the array
			array[last_idx][4] = CLS[0]		

			if buffer_idx != []:
				buf_idx = buffer_idx[0]
			if buffer_num > 1:
				CLS[0] += service_time
				CLS[1] = buf_idx
				buffer_num -= 1


				
			elif buffer_num == 1:
				buffer_num -= 1
				CLS[0] = 0
				CLS[1] = -1




		#output
		#print(round(MCL, 4),"  ",round(CLA, 4),"  ",buffer_num, buffer_idx,"   ",CLS,"       ",CLR[:8])

	# for item in array:
	# 	print(item)
	# print(len(array))
	# print(array[-1])
	return array

def calT(array):
	T = []
	for item in array:
		T.append(round(item[4] - item[1], 4))
	
	#take only the 1000th to 51000th
	T = T[1000:51001]
	#print("total T_mean:", round(sum(T) / len(T), 4))

	batch_mean_list = []
	batch_per_lsit = []
	for i in range(50):
		batch = T[i * 1000 : i * 1000 + 1000]
		batch_mean = round(sum(batch) / len(batch), 4)
		batch_mean_list.append(batch_mean)

		batch.sort()
		batch_per_lsit.append(batch[int(len(batch)*0.95)])
		#print("batch_mean:", batch_mean)
	batch_mean_list_mean = round(sum(batch_mean_list) / len(batch_mean_list), 4)
	batch_per_lsit_mean = round(sum(batch_per_lsit) / len(batch_per_lsit), 4)

	temp = 0
	for item in batch_mean_list:
		temp += (item - batch_mean_list_mean) ** 2
	batch_mean_list_sd = round((temp / (len(batch_mean_list) - 1)) ** 0.5, 4)

	temp = 0
	for item in batch_per_lsit:
		temp += (item - batch_per_lsit_mean) ** 2
	batch_per_lsit_sd = round((temp / (len(batch_mean_list) - 1)) ** 0.5, 4)

	CI1_mean = round(batch_mean_list_mean - round(1.96 * batch_mean_list_sd / len(batch_mean_list), 4), 4)
	CI2_mean = round(batch_mean_list_mean + round(1.96 * batch_mean_list_sd / len(batch_mean_list), 4), 4)

	CI1_per = round(batch_per_lsit_mean - round(1.96 * batch_per_lsit_sd / len(batch_per_lsit), 4), 4)
	CI2_per = round(batch_per_lsit_mean + round(1.96 * batch_per_lsit_sd / len(batch_per_lsit), 4), 4)


	print("T_batch_mean_list_mean:", batch_mean_list_mean)
	print("T_batch_mean_list_sd:", batch_mean_list_sd)
	print("T_batch_mean_list_CI:", "[",CI1_mean, CI2_mean, "]")

	print("T_batch_per_list_mean", batch_per_lsit_mean)
	print("T_batch_per_list_sd", batch_per_lsit_sd)
	print("T_batch_per_list_CI:", "[", CI1_per, CI2_per, "]")
	print("--")

	return batch_mean_list_mean, batch_mean_list_sd, [CI1_mean, CI2_mean], batch_per_lsit_mean, batch_per_lsit_sd, [CI1_per, CI2_per]

def calD(array):
	D = []
	for item in array:
		D.append(round(item[3] - item[2], 4))
	
	#take only the 1000th to 51000th
	D = D[1000:51001]
	#print("total D_mean:", round(sum(D) / len(D), 4))

	batch_mean_list = []
	batch_per_lsit = []
	for i in range(50):
		batch = D[i * 1000 : i * 1000 + 1001]
		batch_mean = round(sum(batch) / len(batch), 4)
		batch_mean_list.append(batch_mean)

		batch.sort()
		batch_per_lsit.append(batch[int(len(batch)*0.95)])

		#print("batch_mean:", batch_mean)
	batch_mean_list_mean = round(sum(batch_mean_list) / len(batch_mean_list), 4)
	batch_per_lsit_mean = round(sum(batch_per_lsit) / len(batch_per_lsit), 4)

	temp = 0
	for item in batch_mean_list:
		temp += (item - batch_mean_list_mean) ** 2
	batch_mean_list_sd = round((temp / (len(batch_mean_list) - 1)) ** 0.5, 4)

	temp = 0
	for item in batch_per_lsit:
		temp += (item - batch_per_lsit_mean) ** 2
	batch_per_lsit_sd = round((temp / (len(batch_mean_list) - 1)) ** 0.5, 4)

	CI1_mean = round(batch_mean_list_mean - round(1.96 * batch_mean_list_sd / len(batch_mean_list), 4), 4)
	CI2_mean = round(batch_mean_list_mean + round(1.96 * batch_mean_list_sd / len(batch_mean_list), 4), 4)

	CI1_per = round(batch_per_lsit_mean - round(1.96 * batch_per_lsit_sd / len(batch_per_lsit), 4), 4)
	CI2_per = round(batch_per_lsit_mean + round(1.96 * batch_per_lsit_sd / len(batch_per_lsit), 4), 4)


	print("D_batch_mean_list_mean:", batch_mean_list_mean)
	print("D_batch_mean_list_sd:", batch_mean_list_sd)
	print("D_batch_mean_list_CI:", "[", CI1_mean, CI2_mean, "]")

	print("D_batch_per_list_mean", batch_per_lsit_mean)
	print("D_batch_per_list_sd", batch_per_lsit_sd)
	print("D_batch_per_list_CI:", "[", CI1_per, CI2_per, "]")

	return batch_mean_list_mean, batch_mean_list_sd, [CI1_mean, CI2_mean], batch_per_lsit_mean, batch_per_lsit_sd, [CI1_per, CI2_per]

if __name__== "__main__":
	# The input values are
	# - the mean inter-arrival time,
	# - mean orbiting time,
	# - service time,
	# - buffer size, and
	# - value of the master clock at which time the simulation will be terminated.

	#default value
	mean_arr_time = 6
	mean_orbit_time = 5
	service_time = [1,2,3,4]#1~6
	max_buffer_size = 5
	MCL_stop = 500000


	#input from terminal
	# mean_arr_time = int(sys.argv[1])
	# mean_orbit_time = int(sys.argv[2])
	# service_time = int(sys.argv[3])
	# max_buffer_size = int(sys.argv[4])
	# MCL_stop = int(sys.argv[5])

	random.seed(2)
	#print("MCL,    CLA,       buffer,    CLS,             CLR")

	T_mean = []
	T_CI = []

	T_per_mean = []
	T_per_CI = []

	D_mean = []
	D_CI = []

	D_per_mean = []
	D_per_CI = []


	for s_time in service_time:
		array = []#idx, each request of arrive time, when the begin retransmission, when to get into queue(get service), when finish
		print("service_time:", s_time)
		array = getArray(mean_arr_time, mean_orbit_time, s_time, max_buffer_size, MCL_stop, array)
	
		batch_mean_list_mean, batch_mean_list_sd, [CI1_mean, CI2_mean], batch_per_lsit_mean, batch_per_lsit_sd, [CI1_per, CI2_per] = calT(array)#return batch_mean_list_mean, batch_mean_list_sd, [CI1_mean, CI2_mean], batch_per_lsit_mean, batch_per_lsit_sd, [CI1_per, CI2_per]
		
		T_mean.append(batch_mean_list_mean)
		T_CI.append([CI1_mean, CI2_mean])

		T_per_mean.append(batch_per_lsit_mean)
		T_per_CI.append([CI1_per, CI2_per])
		

		batch_mean_list_mean, batch_mean_list_sd, [CI1_mean, CI2_mean], batch_per_lsit_mean, batch_per_lsit_sd, [CI1_per, CI2_per] = calD(array)
		D_mean.append(batch_mean_list_mean)
		D_CI.append([CI1_mean, CI2_mean])

		D_per_mean.append(batch_per_lsit_mean)
		D_per_CI.append([CI1_per, CI2_per])
		print("=======")

	print(T_mean)
	print(T_CI)

	print(D_per_mean)
	print(D_per_CI)
		# x = [2, 4, 6]
		# y = [1, 3, 5]
		# plt.plot(x, y)
		# plt.show()
