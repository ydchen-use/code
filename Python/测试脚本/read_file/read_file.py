import fileinput
import time

for line in [line for line in fileinput.input(files="asset_task.log", openhook=fileinput.hook_encoded("utf-8"))][::-1][:1]:
    print(line)
    print(line.split(" "))
    print(type(line))
    line_list = line.split(" ")
    tmp_time = line_list[0] + " " + line_list[1].split(",")[0]
    timeArray = time.strptime(tmp_time, "%Y-%m-%d %H:%M:%S")
    timeStamp = time.mktime(timeArray)
    print(tmp_time)
    print(timeArray)
    print(timeStamp)
    print(int(timeStamp))
 
