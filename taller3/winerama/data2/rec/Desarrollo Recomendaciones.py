#!/usr/bin/env python
# coding: utf-8

# In[5]:


import numpy as np
import pandas as pd
pu = np.loadtxt('UserMat.csv', delimiter = ',')
qi = np.loadtxt('ItemMat.csv', delimiter = ',')
nombres_rest = pd.read_csv('nombre_rest.csv', delimiter = ',')
usuario_ciudad = pd.read_csv('UsuarioCiudad.csv', delimiter = ',')
#ID_usuarios = pd.read_csv('UserIDS.csv', delimiter = ',')


# In[8]:


user = 93

# después la variable de entrada será el nombre del usuario
userX= (pu[user]).dot((qi).T)# + bu[userX] + bi.T + mean
userX = userX.T
lista_usuario = pd.DataFrame(userX, columns = ['stars'])
negocios = pd.read_csv('BusinessIDS.csv', delimiter = ',')
lista_usuario['business_id'] = negocios['business_id']

lista_usuario.setindex = 'business_id'
lista_usuario = pd.merge(nombres_rest, lista_usuario, on = 'business_id', how = 'right').sort_values(by = 'stars', ascending = False)
lista1 = lista_usuario[['name', 'city']][lista_usuario['city'] == usuario_ciudad.iloc[user, 2]].head(10)
lista1.to_csv('lista1.csv')
lista1


# In[4]:


negocios.head()


# In[ ]:




