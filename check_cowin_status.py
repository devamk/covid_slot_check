import datetime
import requests
import pyaudio
import wave 

def play_alarm():
    chunk = 1024
    f = wave.open(r"TF004.wav","rb")
    p = pyaudio.PyAudio() 
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  

    data = f.readframes(chunk)  

    while data:  
        stream.write(data)  
        data = f.readframes(chunk)  

    stream.stop_stream()  
    stream.close()  

    p.terminate()    


def file_write(session_match, file_name = "MyFile.txt"):
    to_print = ""
    for i in sessions_match:
        to_print = to_print \
                  +"name: {}\n".format(i["name"])\
                  + "address: {}\n".format(i["address"])\
                  + "block_name: {}\n".format(i["block_name"])\
                  + "# slots: {}\n".format(i["available_capacity"])\
                  + "age_limit: {}\n\n".format(i["min_age_limit"])
    file = open(file_name, "a")

    header = "\n=================================\n"+\
            datetime.datetime.now().__str__()+\
            "\n=================================\n"
    file.write(header + to_print)
    file.close()


def check_slots():
    pres_time = datetime.datetime.now()
    days = [pres_time.date() + datetime.timedelta(days = i) for i in range(1, 5)]
    days = [day_i.strftime("%d-%m-%Y") for day_i in days]

    pin_codes = [800001, 800014]

    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)" + \
                "AppleWebKit/537.36 (KHTML, like Gecko) "+\
                "Chrome/83.0.4103.97 Safari/537.36"

    response_dict = {}

    for day_i in days:
        for pin_i in pin_codes:
            url = "https://cdn-api.co-vin.in/api/"

            find_sess = "v2/appointment/sessions/public/findByPin?pincode={}&date={}".format(pin_i, "10-05-2021")

            h = {\
                'Accept-Language': 'en_US',\
                "User-Agent": user_agent,\
                'Authorization':'Bearer ar33ff22aawqff2df',\
            }

            response = requests.get(
                url = url + find_sess,\
                headers = h,\
                )
            response_dict[(day_i, pin_i)] = response

    session_list = []
    for key_i in response_dict.keys():
        for j in response_dict[key_i].json()["sessions"]:
            session_list.append(j)

    sessions_match = []
    for session_i in session_list:
        if (session_i["min_age_limit"] < 45) & (session_i["available_capacity"] > 0):
            sessions_match.append(session_i)

    file_write(sessions_match)
    if (len(sessions_match) > 0):
        play_alarm()
    


if (__name__ == "__main__"):
    check_slots()
