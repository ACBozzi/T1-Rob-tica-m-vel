# -*- coding: utf-8 -*-
"""T1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1S1VEF04MOuryDYkWx0W-ydHxi-jDc9eU
"""

from google.colab import drive
drive.mount('/content/drive', force_remount=False)

import matplotlib.pyplot as plt
import numpy as np

import sys
import os
from tqdm import tqdm
import requests
import tarfile
import pickle

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.decomposition import PCA

from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier

"""Definir variaveis estáticas"""

from google.colab import files

file_data = '/content/drive/My Drive/robotica/cifar-10-batches-py'
label_names = ['aviao', 'carro', 'passaro', 'gato', 'veado', 'cachorro', 'sapo', 'cavalo', 'navio', 'caminhao']
#extension_archivo = '.goku'

"""Analizando Dataset"""

def load_batch(file):
    with open(file_data + file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    #vetor pra identificar a imagem
    labels = dict[b'labels']
    #matriz rgb da imagem 3072
    data = dict[b'data']
    return labels, data

label1, data1 = load_batch('/data_batch_1')

data1.shape

def Obtener_Todos_Batch():
    total_data = []
    total_label = []
    for i in range(1,6):
        label_temp, data_temp = load_batch('/data_batch_' + str(i))
        total_data.extend(data_temp)
        total_label.extend(label_temp)
    return total_label, np.array(total_data)

total_label, total_data = Obtener_Todos_Batch()

total_data.shape

label_test, data_test = load_batch('/test_batch')

data_test.shape

"""Aplicar o PCA - método estatístico para diminuir dimensões"""

pca = PCA()
pca.fit_transform(total_data)

pca.explained_variance_

pca.explained_variance_.shape

pca_K = PCA()
pca_K.fit_transform(total_data)

def Calculate_Best_K_OPT():
    k = 0
    k_opt = 0
    total = sum(pca_K.explained_variance_)
    current_sum = 0
    k_values = []
    var_values = []
    while(k< 1000):
        if(current_sum / total < 0.99):
            k_opt = k
        current_sum += pca_K.explained_variance_[k]
        k_values.append(k)
        var_values.append(current_sum/total)
        k += 1
    return k, k_opt, k_values, var_values

k, k_opt, k_values, variance_values = Calculate_Best_K_OPT()

plt.figure(figsize=(10,6))
plt.plot(k_values,variance_values,color='red', linestyle='dashed', marker='o',
         markerfacecolor='orange', markersize=10)
plt.title('Varianza vs. K')
plt.xlabel('K')
plt.axvline(658, 0, 0.95,label='k= '+ str(k_opt) +' -> Var='+str(0.99),c='r')
plt.legend()
plt.ylabel('Varianza')

def Calculate_Best_K():
    k = 0
    total = sum(pca.explained_variance_)
    current_sum = 0

    while(current_sum / total < 0.99):
        current_sum += pca.explained_variance_[k]
        k += 1
    return k

Calculate_Best_K()

pca = PCA(n_components=Calculate_Best_K(), whiten=True)

x_train_pca = pca.fit_transform(total_data)
x_test_pca = pca.transform(data_test)

x_train_pca.shape

"""KNN"""

