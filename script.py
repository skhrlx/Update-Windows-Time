import socket
import struct
import sys
import time
import datetime
import win32api

server_list = ['pool.ntp.br', 'time.nist.gov', 'time.windows.com', 'pool.ntp.org']

def gettime_ntp(addr='pool.ntp.br'):
    TIME1970 = 2208988800 
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = bytes('\x1b' + 47 * '\0', 'utf-8')
    try:
        client.settimeout(5.0)
        client.sendto(data, (addr, 123))
        data, address = client.recvfrom(1024)
        if data:
            epoch_time = struct.unpack('!12I', data)[10]
            epoch_time -= TIME1970
            return epoch_time
    except socket.timeout:
        return None

if __name__ == "__main__":
    for server in server_list:
        epoch_time = gettime_ntp(server)
        if epoch_time is not None:
            utcTime = datetime.datetime.utcfromtimestamp(epoch_time)
            win32api.SetSystemTime(utcTime.year, utcTime.month, utcTime.day, utcTime.hour, utcTime.minute, utcTime.second, 0)
            localTime = datetime.datetime.fromtimestamp(epoch_time)
            print("Time updated to: " + localTime.strftime("%Y-%m-%d %H:%M") + " from " + server)
            break
        else:
            print("Could not find time from " + server)
