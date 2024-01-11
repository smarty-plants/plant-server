import datetime

def getDailyLight(data_list):
    if(len(data_list) == 0):
        return 0
    elif (len(data_list) == 1):
        return data_list[0].light_level
    else:
        dailyLight = 0
        for x in range(len(data_list)-1):
            reading1 = data_list[x]
            reading2 = data_list[x+1]
            sumOfLight = reading1.light_level + reading2.light_level
            timeDelta = (reading1.read_time-reading2.read_time) / datetime.timedelta(days=1)
            dailyLight += (sumOfLight*timeDelta)/2
        return dailyLight/100
    

def getFirst(data_list):
    if(len(data_list) == 0):
        return (0,0,0,0)
    else:
        return (data_list[0].humidity,data_list[0].temperature,data_list[0].soil_moisture,data_list[0].light_level)


        