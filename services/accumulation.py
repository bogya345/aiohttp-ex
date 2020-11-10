import time
import requests as req

# own import
import savingData as saving

timing = time.time()

while True:
    # if time.time() - timing > 3.0:
    if time.time() - timing > 1800.0:
        res = req.get('http://localhost:8080/accumulation/weather')
        # saving.saveWeather('test1', 'test2')
        timing = time.time()
        print(timing)
