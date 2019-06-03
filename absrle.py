#!/usr/bin/env python3
import os
import sys
import numpy as np
import argparse
import time

from lib.pyutils import byte2uint
from lib.pyutils import bd_info
import toolz as z


s1 = ''
s2 = 'B'
s3 = 'BWWWWBWWWW'
s4 = 'WWWWBWWWWB'
s5 = 'WWWWWWWWWWWWWBBWWWWWWWWWWWWBBBBB'
s6 = [0, 0, 0, 1, 1, 3, 7, 6, 2, 1, 1, 1, 1]
s7 = [0, 0, 0, 1, 1, 1, 3, 7, 6, 2, 3, 3 ,3, 5, 3, 2 ,1]
s7 = [5,3,2,1,0,0,0,0,0,0,0,0,3]
s8 = []
str_list = [s1, s2, s3, s4, s5]


def encode(s: str) -> str:
    encoded = []
    str_len = len(s)
    if str_len == 0:
        return encoded
    character = s[0]
    
    diff_len, diff_ini = 0, None
    _len = 1
    for i in range(1, str_len):
        #print(s[i])
        if character != s[i]:
            if _len == 1:
                diff_len += 1
                if diff_ini == None:
                    diff_ini = i-1
                character = s[i]
            else:
                encoded.append(_len) 
                encoded.append(character)
                _len = 1
                character = s[i]
            
        else:
            if diff_len > 0:
                encoded.append(0)
                encoded.append(diff_len)
                for j in range(diff_ini, diff_ini+diff_len):
                    encoded.append(s[j])
                character = s[i]
                diff_len = 0
                diff_ini = None
            _len += 1
    
    if diff_len > 0:
        encoded.extend([0,diff_len+1])
        for j in range(diff_ini, diff_ini+diff_len+1):
            encoded.append(s[j])
    elif _len > 1:
        encoded.extend([_len, character])
    else:
        now = time.time()
        encoded.extend([0,1,character])

        print(time.time()-now)

    return encoded

def decode(s: str) -> str:
    decoded = []
    str_len = len(s)
    if str_len == 0:
        return decoded

    i=0
    while(i<str_len):
        if s[i] == 0:
            N = i+2
            for j in range(N, N+s[i+1]):
                decoded.append(s[j])
            i=N+s[i+1]
            
        else:
            for j in range(s[i]):
                decoded.append(s[i+1])
            i+=2

    return decoded


    #import pdb;pdb.set_trace()

def main():
    parser = argparse.ArgumentParser(
        description="Run Length Encoding option")
    parser.add_argument('--out', '-o', default='result', help='Output directory')

    args = parser.parse_args()
    
    _, bytesize, dtype = bd_info(8)

    yuv_file = '0259.yuv'
    yuv_file = 'st_absrle.yuv'
    with open(yuv_file, 'rb') as f:
        yuv_data = np.frombuffer(f.read(), dtype=dtype)
    _list = yuv_data.tolist()

    encoded = encode(yuv_data)
    decoded = decode(encoded)

    #for a, b in zip(['比較'], [yuv_data == decoded]):
    #    print('{}: {}'. format(a, b))
    #print(len(yuv_data))
    #print(len(encoded))
    print(yuv_data == decoded)
    import pdb;pdb.set_trace()
    
    suffix = '.rle'
    suffix2 = '.drle'
    path = os.path.join(args.out, str(yuv_file.split('.')[0]))

    a = np.array(encoded)
    with open(path+suffix, 'wb') as f:
        f.write(np.array(encoded))
    with open(path+suffix2, 'wb') as f:
        f.write(np.array(decoded))
    np.savez_compressed(path, encoded)
    print()


def main2():
    _s = s7
    print(_s)
    encoded = encode(_s)
    print(encoded)
    decoded = decode(encoded)
    print(decoded)
    print(_s == decoded)

if __name__ == '__main__':
    main()
