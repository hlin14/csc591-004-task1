import heapq 

def main(arr_time, orbit_time, service_time, max_buffer_size, MCL_stop):
	MCL = 0
	CLA = 2
	buffer_num = 0
	CLS = 0
	CLR = [] #using min heap
	#dic = {}
	# d = {"CLR":8, "CLS":8, "CLA":8}
	# print(min(d, key=d.get))
	while MCL <= MCL_stop:
		dic = {}
		#decide event
		event = ''
		#order is CLR, CLA, CLS
		if CLR != []:
			dic['CLR'] = CLR[0]
		dic['CLA'] = CLA
		if CLS != 0:
			dic['CLS'] = CLS

		#print(dic)

		event = min(dic, key=dic.get)
		#update MCL
		MCL = dic[event]
		print(event)

		#if event is CLR
		#if buffer_num == 0 and CLS == 0,buffer += 1, CLS = item + service_time
		#if buffer_num == max_buffer_size, then heappush
		#else go into the buffer
		if event == 'CLR':
			item = CLR[0]
			heapq.heappop(CLR)

			if CLR == []:#if the CLR is empty, remove the key
				dic.pop('CLR', None)

			if buffer_num == 0 and CLS == 0:
				buffer_num += 1
				CLS = item + service_time
			elif buffer_num == max_buffer_size:
				heapq.heappush(CLR, item + orbit_time)
			else:
				buffer_num += 1


		#if event is CLA, 
		#if buffer == 0 and CLS == 0, then buffer += 1 and CLS = CLA + service_time, 
		#if buffer == max_buffer_size, then heapq.heappush(CLR,CLA + orbit_time)
		#else:buffer += 1
		#then update CLA
		elif event == 'CLA':
			if buffer_num == 0 and CLS == 0:
				buffer_num += 1
				CLS = CLA + service_time
			elif buffer_num == max_buffer_size:
				heapq.heappush(CLR, CLA + orbit_time)
			else:
				buffer_num += 1

			CLA += arr_time



		#if event is CLS, 
		#if buffer_num > 0 then CLS += service_time, and buffer_num -= 1
		#if buffer_num == 0, CLS = 0   
		elif event == 'CLS':
			if buffer_num > 0:
				CLS += service_time
				buffer_num -= 1
			elif buffer_num == 0:
				CLS = 0



		#output
		print(MCL,"  ",CLA,"  ",buffer_num,"   ",CLS,"   ",CLR)




if __name__== "__main__":
	# The input values are
	# - the mean inter-arrival time,
	# - mean orbiting time,
	# - service time,
	# - buffer size, and
	# - value of the master clock at which time the simulation will be terminated.
	arr_time = 6
	orbit_time = 5
	service_time = 10
	max_buffer_size = 2
	MCL_stop = 98
	print("MCL, CLA, buffer, CLS, CLR")
	main(arr_time, orbit_time, service_time, max_buffer_size, MCL_stop)