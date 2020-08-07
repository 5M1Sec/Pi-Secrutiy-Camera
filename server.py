# Author: 5M!Sec @ github
# MIT Licence


import socket
from datetime import datetime, timedelta
import os
import threading
import time

PORT_NUMBER = 12345

# Video Duration in Second
VIDEO_DURATION = 30
# Buffer size in bytes
BUFF_SIZE = 1000000
# Clean Interval in days
CLEAN_INTERVAL = 1
# Sleep time in second
SLEEP_TIME = 86400

TIME_FORMAT = "%m-%d-%Y-%H-%M-%S.h264"
TIME_REMOVAL_FORMAT = "%m-%d-%Y-*.h264"


def delete_old_videos():
    while True:
        if (datetime.now() - file_stamp_date).days > CLEAN_INTERVAL:
            days_to_subtract = CLEAN_INTERVAL
            while days_to_subtract > 0:
                delete_date = datetime.now() - timedelta(days=days_to_subtract)
                removal_command = "rm -rf " + delete_date.strftime(TIME_REMOVAL_FORMAT)
                os.system(removal_command)
                days_to_subtract -= 1
        time.sleep(SLEEP_TIME)


if __name__ == '__main__':

    try:
        # Use UDP socket
        ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('{} \n'.format("socket open error ", err))

    server_binding = ('', PORT_NUMBER)
    ss.bind(server_binding)
    host = socket.gethostname()
    print("[S]: Server host name is: " + str(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is  " + str(localhost_ip))

    # First file init
    # Use TIME_FORMAT as filename
    # Writing file in binary since video stream is in binary
    file_stamp_date = datetime.now()
    file_auto_clean_starting_stamp = datetime.now()
    FILE_OUTPUT_NAME = file_stamp_date.strftime(TIME_FORMAT)
    FILE_OUTPUT = open(FILE_OUTPUT_NAME, "wb")

    delete_old_videos_thread = threading.Thread(target=delete_old_videos)
    delete_old_videos_thread.start()

    while True:
        data, _ = ss.recvfrom(1000000)
        FILE_OUTPUT.write(data)
        time_delta = datetime.now() - file_stamp_date
        if time_delta.seconds > VIDEO_DURATION:
            file_stamp_date = datetime.now()
            FILE_OUTPUT.close()
            FILE_OUTPUT_NAME = file_stamp_date.strftime(TIME_FORMAT)
            FILE_OUTPUT = open(FILE_OUTPUT_NAME, "wb")
