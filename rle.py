#!/usr/bin/env python3
import os
import sys
import time
import numpy as np
import argparse

import pickle
import toolz as z


def encode(s: str) -> str:
    encoded = []
    str_len = len(s)
    if str_len == 0:
        return encoded
    start = 0
    character = s[0]
    for i in range(1, str_len):
        if character != s[i]:
            diff = i - start  
            _str1 = str(diff)+str(character)
            encoded.append(diff)
            encoded.append(character)
            character = s[i]
            start = i

    diff_len = str_len - start
    encoded.append(diff_len)
    encoded.append(character)

    return encoded


def decode(s: str) -> str:
    str_len = len(s)
    if str_len == 0:
        return decoded

    decoded = [s[i+1] for i in range(0, len(s), 2) for j in range(s[i])]

    return decoded


def main():
    parser = argparse.ArgumentParser(
        description="Run Length Encoding option")
    parser.add_argument('--out', '-o', default='.', help='Output directory')
    parser.add_argument('--file', default='stream.pic', help='file to be encoded')

    args = parser.parse_args()

    with open(args.file, mode='rb') as f:
       yuv_data = pickle.load(f) 

    yuv_data = np.array(yuv_data).flatten().tolist()

    t0 = time.time()
    encoded = encode(np.array(yuv_data).flatten().tolist())
    decoded = decode(encoded)
    t1 = time.time()

    for a, b in zip(['比較'],
                    [yuv_data == decoded]):
        print('{} : {}'. format(a, b))

    #print(len(yuv_data))
    #print(len(encoded))
    #print(len(decoded))
    
    suffix = '.rle'
    suffix2 = '.drle'
    path = os.path.join(args.out, str(args.file.split('.')[0]))

    with open(path+suffix, 'wb') as f:
        f.write(np.array(encoded))
    with open(path+suffix2, 'wb') as f:
        f.write(np.array(decoded))

    np.save(path, encoded)
    print("encode time : {}". format(t1-t0))


if __name__ == '__main__':
    main()
