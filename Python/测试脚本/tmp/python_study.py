import time

str1 = "9/5/2022 -- 08:58:24 - <Info> - All AFP capture threads are running."

time_str1 = "9/5/2022 08:58:24"
time_str2 = "02/28/2022-10:43:32"

print(str1.split(" "))

#  时间戳、格式化时间 *********************************
timeStamp = time.time()  # 1644741268.9751265
timeArray = time.localtime(timeStamp)  # time.struct_time(tm_year=2022, tm_mon=2, tm_mday=13, tm_hour=16, tm_min=35, tm_sec=14, tm_wday=6, tm_yday=44, tm_isdst=0)
otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)  # 2022-02-13 16:37:20
otherStyleTime1 = time.strftime("%d-%m-%Y %H:%M:%S", timeArray)  # 2022-02-13 16:37:20

print(otherStyleTime)
print(otherStyleTime1)

timeArray1 = time.strptime(time_str1, "%d/%m/%Y %H:%M:%S") # time.struct_time(tm_year=2022, tm_mon=5, tm_mday=9, tm_hour=8, tm_min=58, tm_sec=24, tm_wday=0, tm_yday=129, tm_isdst=-1)
timeStamp1 = time.mktime(timeArray1)
print(timeArray1)
print(timeStamp1)

timeArray2 = time.strptime(time_str2, "%m/%d/%Y-%H:%M:%S") # time.struct_time(tm_year=2022, tm_mon=5, tm_mday=9, tm_hour=8, tm_min=58, tm_sec=24, tm_wday=0, tm_yday=129, tm_isdst=-1)
timeStamp2 = time.mktime(timeArray2)
print(timeArray2)
print(timeStamp2)

