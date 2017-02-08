import requests
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
chan_list = [29,31,33,35]
GPIO.setup(chan_list, GPIO.OUT, initial=GPIO.HIGH)
facebook = False

GOOGLE_KEY = "AIzaSyDjymcGFExAFSfujMUhd8lgJ0AelCDuZJw"
YOUTUBE_USER_NAME = "MancaveNL"


def get_channel_id():
    r = requests.get("https://www.googleapis.com/youtube/v3/channels?key={0}&forUsername={1}&part=id".format(GOOGLE_KEY,
                                                                                                             YOUTUBE_USER_NAME))
    channel_id = r.json()['items'][0]['id']
    return channel_id


def get_youtube_subs():
    request = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + get_channel_id() + "&key=" + GOOGLE_KEY
    r = requests.get(request)
    subscribers = r.json()['items'][0]['statistics']['subscriberCount']
    return subscribers


def get_facebook_likes():
    pass

def convert_bin(value):
    print(value)
    bin_value = [[0,0,0,0]]*6

    value_sep = [int(d) for d in str(value)]
    #convert to list with binair
    for i,x in enumerate(reversed(value_sep)):
        bin_value[-i-1] = [int(d) for d in "{0:04b}".format(x)]
    print(bin_value)

    return bin_value

def update_clock(bin):
    print(bin[5])
    GPIO.output(chan_list,bin[5])

while True:
    if facebook:
        update_clock(convert_bin(get_facebook_likes()))
    else:
        update_clock(convert_bin(get_youtube_subs()))
    sleep(5.0)
