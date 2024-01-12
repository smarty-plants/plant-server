import datetime

RED_ZONE_RATIO = 0.3
ORANGE_ZONE_RATIO = 0.4
YELLOW_ZONE_RATIO = 0.3

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


def generateRanges(min, max):
    ranges = []
    ranges.append(min * RED_ZONE_RATIO)
    ranges.append(min * ORANGE_ZONE_RATIO)
    ranges.append(min * YELLOW_ZONE_RATIO)
    ranges.append(max - min)
    space_left = 100 - max
    ranges.append(space_left * YELLOW_ZONE_RATIO)
    ranges.append(space_left * ORANGE_ZONE_RATIO)
    ranges.append(space_left * RED_ZONE_RATIO)
    return ranges

        