# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 10:19:24 2023

@author: Marcus
"""

import serial
import time
import sys
import os

port='COM9'
log = 1 # Set to 1 to log HEX data
convert = 0 # Set to 1 to convert HEX data to raw & physical. Note: If log is set to 1, it will never exit logging to convert the data.

# command = 'tdona,BD,\r\n'
command = 'stdona,4A,\r\n' # HEX of Temp. AD, DO AD, Blue Phase AD, Red Phase AD, Blue Amp. AD, Red Amp. AD & LED accumulated time

# def AD_to_Phys(values,DC):

#     T_AD=values[0]
#     DO_AD=values[1]
#     t=values[2]
#     N=DO_AD/10000

#     T=A+B*T_AD+C*T_AD**2+D*T_AD**3+E*T_AD**4+F*T_AD**5
#     DO=(((1+d0*T) / (d1 + d2*N + d3*t + d4*t*N) )**e0 -1) * (1 / (c0 + c1*T + c2*T**2))

def initiate(s):

    # Check if there is sensor output
    s.write('wu,E7,\r\n'.encode())
    time.sleep(0.2)
    wu = s.read(s.in_waiting).decode()
    if len(wu) == 0:
        print('Error: No output from the sensor')
        sys.exit()

    # Reset serial connection buffers just in case
    s.reset_input_buffer()
    s.reset_output_buffer()

    # Check serial number
    s.write('*serialnumber,A0,\r\n'.encode())
    time.sleep(0.5)
    SN = s.read(s.in_waiting).decode().replace(',\r', '')
    if (len(SN)== 0) | (len(SN)<=18) | (SN[:13] != '*serialnumber'):
        print('Error: Could not grab Serial Number from the sensor')
        sys.exit()

    # Check model number
    s.write('model,C2,\r\n'.encode())
    time.sleep(0.5)
    MN = s.read(s.in_waiting).decode().replace(',\r', '')
    if len(MN) == 0:
        print('Error: Could not grab Model Number from the sensor')
        sys.exit()

    # Check Firmware Version
    s.write('fwver,A9,\r\n'.encode())
    time.sleep(0.5)
    FV = s.read(s.in_waiting).decode().replace(',\r', '')
    if len(FV) == 0:
        print('Error: Could not grab Firmware Version from the sensor')
        sys.exit()


    # Check calibration parameters
    s.write('dc,0C,\r\n'.encode())
    time.sleep(0.5)
    DC = s.read(s.in_waiting).decode().replace(',\r', '')
    if len(DC) == 0:
        print('Error: Could not grab calibration data from the sensor')
        sys.exit()

    time.sleep(0.5)

    return '\n'.join([SN, MN, FV, DC,
    '#####################################################################\n\n'])

def main(port,baud=38400):

    try:
        s = serial.Serial(port, baud, timeout=0.5)
    except:
        s.close()
        print('Could not connect to port')
    else:
        with s:
            data=initiate(s)
            SN = data[14:18]
            suffix = SN + '_'
            filename='AROD-FT_' + suffix + time.strftime('%Y%m%d%H%M%S', time.gmtime()) + '.csv'
            with open(filename,'w') as f:
                f.write(data)
                while (True):


                    starttime = time.time()
                    # Check if incoming bytes are waiting to be read from the serial input
                    # buffer.
                    if (s.in_waiting > 0):
                        # read the bytes and convert from binary array to ASCII
                        data_str = s.read(s.in_waiting).decode().replace(',\r', '')

                        timestamp=time.strftime('%Y%m%d%H%M%S', time.gmtime())
                        f.write(timestamp + ',' + data_str)

                        print(data_str)
                        # print(time.strftime('%Y%m%d%H%M%S', time.gmtime()))

                    s.write(command.encode())
                    try:
                        time.sleep(1.0 - ((time.time() - starttime) % 60.0))
                    except:
                        time.sleep(1.0)

def parse_header(header):

    new_header = []

    C = {}

    # Cs = ['C0','C1','C2','d0','d1','d2','d3','d4','Cp','e0','A','B','C','D','E','F','G','H']

    for i, s in enumerate(header):

        cont=s.strip()

        if (cont=='') | ('###' in cont):
            new_header.append(cont)
        else:

            item = cont[:-3]

            split = item.split('=')

            if not checksum_checker(cont,0):
                print(split[0] + 'parameter checksum could not be verified')
                continue

            new_header.append(item)

            if len(split) == 2:
                try:
                    val = int(split[1])
                except:
                    try:
                        val = float(split[1])
                    except:
                        val = split[1]
                C[split[0]] = val

    out = '\n'.join(new_header) + '\n'

    return out, C

def checksum_checker(sentence,col):
    split=sentence.strip().split(',')
    query = ','.join(split[col:-1]) + ','
    checksum = split[-1]
    sep=[hex(ord(item)) for item in query]
    value = hex(sum([int(item,base=16) for item in sep]))
    complement = hex(int(value,base=16) ^ 0xFFFFFFF)
    result = complement[-2:].upper()

    valid=result==checksum

    return valid


def hex_to_dec(hex_sentence):

    items = hex_sentence.split(',')
    for i, s in enumerate(items):

        if (i > 1) & (i < len(items)-1):
            items[i] = str(int(s, 16))

    out = ','.join(items[:-1])
    return out

def raw_to_phys(raw_sentence,Cal):
    raw = raw_sentence.split(',')



    try:
        T_AD = int(raw[2])
        N=int(raw[3])/10000
        t=int(raw[8])

        T = Cal['A'] + Cal['B']*T_AD + Cal['C']*T_AD**2 + Cal['D']*T_AD**3 + Cal['E']*T_AD**4 + Cal['F']*T_AD**5
        DO = (((1+Cal['d0']*T) / (Cal['d1'] + Cal['d2']*N + Cal['d3']*t + Cal['d4']*t*N) )**Cal['e0'] -1) * (1 / (Cal['C0'] + Cal['C1']*T + Cal['C2']*T**2))

        items = [raw[0], str(T), str(DO)]
        phys = ','.join(items)

        return phys
    except:
        return None

def convert_hex(hex_raw_file,out='both'):
    with open(hex_raw_file,'r') as f:
        content = f.readlines()

    ind = [i for i, s in enumerate(content) if '####' in s][0] + 2
    header = content[:ind]

    header, C = parse_header(header)

    data = content[ind:]

    filtered = [item for item in data if checksum_checker(item,1)]

    raw = [hex_to_dec(item) for item in filtered]

    if (out=='raw') | (out=='both'):
        filesplit = os.path.splitext(hex_raw_file)
        filesplit = [item for item in filesplit]

        filesplit.insert(-1,'_raw')
        filename = ''.join(filesplit)
        output=raw



        with open(filename,'w') as f:
                f.write(header)
                f.write('\n'.join(output))
        print('Converted to raw')

    if (out=='phys') | (out=='both'):
        filesplit = os.path.splitext(hex_raw_file)
        filesplit = [item for item in filesplit]

        filesplit.insert(-1,'_phys')
        filename = ''.join(filesplit)

        phys = [raw_to_phys(item,C) for item in raw if raw_to_phys(item,C) is not None]

        output=phys

        with open(filename,'w') as f:
            f.write(header)
            f.write('\n'.join(output))
        print('Converted to phys')


if __name__ == '__main__':
    if log:
        if len(sys.argv)<2:
            main(port)
        else:
            main(sys.argv[1])

    if convert:
        for file  in os.listdir():
            # if "AROD-FT_0050_20230425091011.csv" in file:
            if file.endswith('_phys.csv') | file.endswith('_raw.csv'):
                continue
            elif file.endswith('.csv'):
                convert_hex(file,out='both')

