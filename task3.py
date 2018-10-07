import heapq
import random
import math
import sys

def getExp(mean, random_number):
	return round(-mean * math.log(1 - random_number), 4)

def main(mean_arr_time, mean_orbit_time, service_time, max_buffer_size, MCL_stop, array):
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
		print(round(MCL, 4),"  ",round(CLA, 4),"  ",buffer_num, buffer_idx,"   ",CLS,"       ",CLR[:8])

	for item in array:
		print(item)


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
	service_time = 3
	max_buffer_size = 2
	MCL_stop = 200
	array = []#idx, each request of arrive time, when the begin retransmission, when to get into queue(get service), when finish

	#input from terminal
	# mean_arr_time = int(sys.argv[1])
	# mean_orbit_time = int(sys.argv[2])
	# service_time = int(sys.argv[3])
	# max_buffer_size = int(sys.argv[4])
	# MCL_stop = int(sys.argv[5])

	random.seed(2)
	print("MCL,    CLA,       buffer,    CLS,             CLR")
	main(mean_arr_time, mean_orbit_time, service_time, max_buffer_size, MCL_stop, array)
