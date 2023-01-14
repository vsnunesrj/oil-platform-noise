# -*- coding: utf-8 -*-
"""
Esse programa faz a combinação de uma fatia aleatoria de um aúdio de ruído (wav) ao áudio de fala correspondente (wav).
As relações sinal-ruído resultantes, são: SNR10 e SNR30.

Autor: Vinicius Nunes
Data: 22/08/21

"""

#!pip install pydub

from pydub import AudioSegment
from random import seed
from random import random
import os
import csv

seed(1)

noise_filename = "noise_tmp.wav"

#Criação do CSV temporário que será utilizado pelo play.py
csv_header = ['wav_filename']
csv_data = [ noise_filename ]
csv_filename = "noise_tmp.csv"
with open( csv_filename, 'w', encoding='UTF8', newline='') as f:
	writer = csv.writer(f)
	writer.writerow(csv_header)
	writer.writerow(csv_data)
	print("Created csv: ", csv_filename)

#Relações sinal-ruído do áudio resultante
snrs = ["10","30"]

#Obtém o áudio de ruído
noise = AudioSegment.from_wav("proa.wav")
len_noise = len(noise)

#Realiza as operações para todos os arquivos .wav do diretório clips/	
directory = r'clips'
for filename in os.listdir(directory):
    if filename.endswith(".wav") and filename.startswith("common_voice_pt_"):
        print("***************   Slice noise ...  ****************")
        print("filename = ", filename)
        full_filename = os.path.join(directory, filename)
        print("full_filename = ", full_filename)
        
        #Obtém o áudio de fala
        sound = AudioSegment.from_wav(full_filename)
        
        len_sound = len(sound)
        
        #Verifica a diferença de duração entres os dois aúdios
        len_difference = len_noise - len_sound
        print("len_sound = ", len_sound)
        print("len_noise = ", len_noise)
        print("len_difference = ", len_difference)

	#Para o intervalo identificado acima é determinado aleatóriamente a posição de início no corte do ruído
        value = random()
        print("random = ", value)

        start = value*len_difference
        print("start = ", start)
        short_noise = noise[start:]
        
	#O áudio de ruído gerado é armazenado temporariamente
        short_noise.export(noise_filename, format="wav")
        print("Created wav: ", noise_filename)

        play_directory = "/home/vinicius/mestrado/DeepSpeech/bin/"

	#Para SNR10 e SNR30 e executado o play.py do DeepSpeech para a sobreposição dos áudios	
        for snr in snrs:
          snr_dir = "proa-snr"+snr
		
          if not (os.path.exists(snr_dir)):
            os.mkdir(snr_dir)
		
          resulted_audio= "overlay_snr" + snr + "_" + filename
	  
          command = "python " + play_directory + "play.py --number 1 --start 0 --quiet "\
          + full_filename + " --augment overlay[source='noise_tmp.csv',snr=" + snr + \
          "] --pipe >" + snr_dir + "/" + resulted_audio
          
          print(command)

          os.system(command)

          print("Created audio: " + snr_dir + "/" + resulted_audio)
        print("***************************************************")

    else:
        continue

