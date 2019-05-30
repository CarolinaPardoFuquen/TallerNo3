
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import random
import os
np.seterr(divide='ignore', invalid='ignore')

base_path = os.path.dirname(os.path.realpath(__file__))
def online(user_id):
    # In[2]:


    #k_nn = np.loadtxt(open("10-NN.csv"), delimiter=",")
    #ratings = pd.read_csv('ratings_online.csv')

    #w = list(ratings.userId.value_counts().sort_index().index)

    #k_nn2 = k_nn[np.in1d(k_nn[:, 0], w), :]

    #np.savetxt('10-NN.csv', k_nn2, delimiter = ',') 


    # In[3]:


    ontlog = pd.read_csv(os.path.join(base_path,'movies2.csv'))

    k_nn = np.loadtxt(open(os.path.join(base_path,"10-NN.csv")), delimiter=",")
    ol_user = pd.read_csv(os.path.join(base_path,'ratings-online.csv')) ################ PRUEBA ONLINE ##############
    generos = pd.read_csv(os.path.join(base_path,'generos.csv'))
    pelis_gen = np.loadtxt(open(os.path.join(base_path,"peli-genero.csv")), delimiter=",")
    user_gen = np.loadtxt(open(os.path.join(base_path,"user-genres.csv")), delimiter=",")
    listaoff = pd.read_csv(os.path.join(base_path,'Listas-offline.csv'))

    generos = generos.drop(['Unnamed: 0'], axis = 1)
    ol_user = ol_user.drop(['Unnamed: 0'], axis = 1).sort_values(by = 'date') ################ PRUEBA ONLINE ##############
    w = np.array([[0.15], [0.15], [0.7]])
    consec = -1
    matrix2 = np.zeros(shape = (300,19))


    # In[4]:


    x =  np.array(np.sum(pelis_gen[:, 1:19], axis = 1))   # número de géneros que tiene la película
    x = x.reshape((58098,1))

    # se reemplazan los 1s que indican los géneros, por 1/n indicando el peso que tendrá cada género para el cálculo del rating.
    z = -1
    for num in x:
        z = z + 1
        if num <= 3:
            pelis_gen[z, 1:19] = (pelis_gen[z, 1:19] / x[z])*(0.84 + 0.04*x[z])
        else:
            pelis_gen[z, 1:19] = pelis_gen[z, 1:19] / x[z]


    # # Estos bloques se corren cada vez que llega un registro nuevo

    # In[5]:


    consec = consec + 1
    #print('hola consec ',consec)
    #current = ol_user.iloc[[consec],:] ################ PRUEBA ONLINE ##############
    

    new_dataframe = ol_user.loc[ol_user['userId'] == user_id]
    #print('user id ',user_id,type(user_id))
    #print('DataFrame',new_dataframe)
    current = new_dataframe.sample()
    #print('current',current)
    #new_dataframe_rows = new_dataframe.shape[0]
    #other_new = new_dataframe.ix[random.sample(new_dataframe.index,new_dataframe_rows)]
    #print(type(new_dataframe))
    #print(new_dataframe.sample())
    usuario = current.userId.values[0]
    #usuario = user_id
    #print('cacaaaa ',current.userId.values)
    #current.merge(ontlog[['movieId','genres']])    ############### PRUEBA ONLINE ##############
    flujo = current.merge(ontlog[['movieId','genres']])    ################ PRUEBA ONLINE ##############
    #print (flujo)

    # In[6]:



    key = generos.Cat1.value_counts()
    key = list(key.index)
    key.remove('(no genres listed)')
    key.remove('IMAX')
    values = list(range(18))
    genmap = dict(zip(key, values))

    current2 = current.merge(generos, on = 'movieId')

    current2['Cat1'] = current2['Cat1'].map(genmap)

    current2['Cat2'] = current2['Cat2'].map(genmap)
    current2['Cat3'] = current2['Cat3'].map(genmap)
    current2['Cat4'] = current2['Cat4'].map(genmap)

    matrix = current2[['userId', 'rating', 'Cat1', 'Cat2', 'Cat3', 'Cat4']] 

    # Se convierte la tabla en matriz
    matrix = np.asmatrix(matrix)


    matrix_new = matrix[0,2:6].astype(int)

    matrix2[consec,0] = matrix[0,0]

    for cat in range(4):
            rrr = matrix_new[0,cat]
            if rrr >= 0:
                matrix2[consec, (rrr + 1)] = round(matrix[0,1], 1)

    matrix2[matrix2 == 0] = 2.5



    # In[7]:


    user = user_gen[(user_gen[:,0] == usuario), 2:20]  # ------ trae el vector de ratings prom.. del usuario por género                                       

    if sum(user[:,0:1]) == 0:
        user = np.array([2.5] * 17)
        user = user.reshape((1, 17))
        group = np.array([2.5] * 17)
        group = group.reshape((1, 17))
    else:
        user = user.reshape((1, 17))
        group = user_gen[np.in1d(user_gen[:, 0], list(k_nn[k_nn[:,0]==usuario])), 2:20] #- busca los 15 comparables del usuario en la matriz K-NN
        group = group.sum(axis = 0) / np.count_nonzero(group, axis = 0)#- promedia ratings de los comparables por género
        group = group.reshape((1, 17))


    group = np.concatenate((user, group, matrix2[matrix2[:,0]==usuario, 1:18].mean(axis = 0).reshape((1,17))), axis = 0)
    group[np.isnan(group)] = 2.5
    u_rating = w.T.dot(group)                                     # promedia ratings de comparables con los propios del
                                                                          # usuario 50/50  
    ratings2 = np.dot(pelis_gen[:, 1:19], u_rating.T) # -----------------califica todas las películas parecido a SVD.                  


    matriz_cal = pd.DataFrame(ratings2, index = pelis_gen[:,0], columns=['User']).sort_values(by = 'User', ascending = False).head(6)
            
    matriz_cal.index = matriz_cal.index.astype(int)
    matriz_cal.index.name = 'movieId'
    matriz_cal = pd.merge(matriz_cal, ontlog[['movieId','title','genres']], on = 'movieId', how = 'left')
    Onlinelist = matriz_cal[['title', 'genres']]


    # In[369]:


    listaoff[['title', 'genres']][listaoff.user == usuario]
    #print(current)
    #print (Onlinelist)

    return current, Onlinelist

#if __name__ == '__main__':
#    current_row, online_list = online(240712)
#
#    print(current_row)
#    print(online_list)