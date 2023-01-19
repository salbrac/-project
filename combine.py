# python 音频文件处理
# 多个 wav 格式语音文件合成
import librosa
import random
import numpy as np
import os
from pydub import AudioSegment

out_path = "combine"
file_path = "cut"
ff = 0
out = os.path.join(out_path , 'combine.wav')
filelist = os.listdir(file_path)
for file in filelist:  
    path = os.path.join(file_path ,file)
    print(path)
    sound = AudioSegment.from_file(path)
    ff = ff+sound
ff.export(out,format='wav')
