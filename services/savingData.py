import json
import datetime

def saveWeather(city, temperatureF):
    addition_dic = {
        "city": str(city),
        "temparatureF": str(temperatureF),
        "datetime": str(datetime.datetime.now())
    }

    with open("./dataStorage/weather/accumulation.json", "r+") as file:
        data = json.load(file) 
        # data = data['storage']
        print(data)
        # if(data == []):
        #     data.append(addition_dic)
        # else:
        #     data.append(addition_dic)
        data.append(addition_dic)
        file.seek(0)
        json.dump(data, file)


# saveWeather('inner_test', 'inner_test')
