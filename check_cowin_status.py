import datetime
import requests
import argparse
import simpleaudio as sa

def play_alarm():
    filename = 'TF004.wav'
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def file_write(sessions_match, file_name = "MyFile.txt"):
    to_print = ""
    for i in sessions_match:

        to_print = to_print + "name: {}\n address: {}\n block_name: {}\n# Slots: {}\nage_limit: {}\n\n"\
                                .format( 
                                    i["name"],
                                    i["address"],
                                    i["block_name"],
                                    i["available_capacity"],
                                    i["min_age_limit"]
                                )
    file = open(file_name, "a")

    header = "\n=================================\n"+\
            datetime.datetime.now().__str__()+\
            "\n=================================\n"
    file.write(header + to_print)
    file.close()


def check_slots( pincodes, days, age_to_check ):

    pres_time = datetime.datetime.now()
    days = [pres_time.date() + datetime.timedelta(days = i) for i in range(1, days+1)]
    days = [day_i.strftime("%d-%m-%Y") for day_i in days]

    pin_codes = pincodes

    user_agent = "random"

    response_dict = {}

    for day_i in days:
        for pin_i in pin_codes:
            url = "https://cdn-api.co-vin.in/api/"

            find_sess = "v2/appointment/sessions/public/findByPin?pincode={}&date={}".format(pin_i, day_i)

            h = {
                "User-Agent": user_agent,\
            }

            response = requests.get(
                url = url + find_sess,
                headers = h,
                )

            if response.status_code == 200:
                response_dict[(day_i, pin_i)] = response
    
    session_list = []
    for key_i in response_dict.keys():
        for j in response_dict[key_i].json()["sessions"]:
            session_list.append(j)

    sessions_match = []
    for session_i in session_list:
        if (session_i["min_age_limit"] < age_to_check) & (session_i["available_capacity"] > 0):
            sessions_match.append(session_i)

    file_write(sessions_match)
    if (len(sessions_match) > 0):
        play_alarm()
    


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--pin_codes', nargs="*", type=int, help="Specify pin codes for which vaccine slots are probed. Default=100000", default=[100000])
    parser.add_argument('-d','--days', type=int, default=4, help="Specify the number of days to probe. Default = 4 days" )
    parser.add_argument('-a','--age_to_check', type=int, default=25, help="Specify the age (in years) to check for. Default = 18 years")
    args = parser.parse_args()
    args = vars(args)
    check_slots( args["pin_codes"], args["days"], args["age_to_check"] )
