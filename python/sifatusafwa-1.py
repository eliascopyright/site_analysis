# %% [markdown]
#    # بسم الله الرحمن الرحيم
# La premiere partie dresse un tableau avec les titres des livres de fiqh malikite en français
# & en arabe.
# %%
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
r = requests.get('https://www.sifatusafwa.com/fr/fiqh-maliki/')

# %%
#Affichage de l'url
r.url

# %%
#Affichage du titre de la page
soup = BeautifulSoup(r.content, 'html.parser')
print(soup.title)

# %% [markdown]
# ## Page 1

# %%
#Préparation du contenu de la page
s = soup.find('section', id = 'products')
s = s.find('div', class_ = 'products product_list row grid')

# %%
#Affichage du contenu de la page
#print(s)

# %%
#Affichage des titres des livres en francais et en arabe
lines = s.find_all('a')
#for line in lines:
#    print(line.text.split('\n'))

# %% [markdown]
# **Création d'une liste avec des chaine de caractères**

# %%
L = []
for line in lines:
    L.append(line.text.split('\n'))

# %%
L_string = []
for l in L:
    L_string.append(l[0])

# %%
#Affichage de la liste chaine de caractères
#L_string

# %%
#Remplacement des termes peu importants par des ""
r_item =['Aperçu rapide', 'Ajouter à la liste de souhaits', 'Ajouter au panier', 'Afficher plus']
for r in r_item:
    L_string = list(filter((r).__ne__, L_string))
    
#Suppression des ""
#for i in range(len(L_string)):
 #   L_string.remove('')

# %%
#Affichage du résultat
#L_string

# %%
for i in range(len(L_string)):
    L_string.remove('')

# %%
#L_string

# %%
#Création des colonnes pour DataFrame
Y = []
X =[]
for i in L_string:
    if L_string.index(i)%2 == 1:
        X.append(i)
    elif L_string.index(i)%2==0:
        Y.append(i)

# %%
X = pd.Series(X)
Y = pd.Series(Y)

# %%
M1 = pd.concat((Y, X), axis = 1)

# %%
M1.columns = ['fr', 'ar']

# %%
M1.head()

# %% [markdown]
# ## Page 2

# %%
#Préparation du contenu de la page
r = requests.get("https://www.sifatusafwa.com/fr/fiqh-maliki/?page=2")
soup = BeautifulSoup(r.content, 'html.parser')
s = soup.find('section', id = 'products')
#s = s.find_all('div', class_ = 'products product_list row grid')
lines = s.find_all('h3', class_ = 's_title_block flex_child')
#Affichage du contenu de la page
#print(lines)

#Enlever les balises
L_string = []
for line in lines:
    L_string.append((line.text.split('\n')[0]))#line.text.split(\'n') est une liste de hcaine de caractères, donc [0] est 
    #seulement le str.
    #print(line.text.split('\n'))#line.text enlève les balises et les choses propres à html/css. Le .split split sur les \n

# %%
#Affichage de la liste
#print(L_string) 
#Dispatchement en colonne arabe/ colonne français
X = []
Y = []
for l in range(len(L_string)):
    if l%2 == 0:
        X.append(L_string[l])
    else:
        Y.append(L_string[l])
M2 = pd.DataFrame({'fr': X, 'ar': Y})
M2.head()

# %% [markdown]
# ## Tentative d'extension à page 3

# %% [markdown]
# On a réussi pour les pages 1 et 2 on va teneter un copier coller jusqu'à la page 3:

# %%
#Préparation du contenu de la page
r = requests.get("https://www.sifatusafwa.com/fr/fiqh-maliki/?page=3")
soup = BeautifulSoup(r.content, 'html.parser')
s = soup.find('section', id = 'products')
#s = s.find_all('div', class_ = 'products product_list row grid')
lines = s.find_all('h3', class_ = 's_title_block flex_child')
#Affichage du contenu de la page
#print(lines)

#Enlever les balises
L_string = []
for line in lines:
    L_string.append((line.text.split('\n')[0]))#line.text.split(\'n') est une liste de hcaine de caractères, donc [0] est 
    #seulement le str.
    #print(line.text.split('\n'))#line.text enlève les balises et les choses propres à html/css. Le .split split sur les \n

# %%
#Affichage de la liste
#print(L_string) 
#Dispatchement en colonne arabe/ colonne français
X = []
Y = []
for l in range(len(L_string)):
    if l%2 == 0:
        X.append(L_string[l])
    else:
        Y.append(L_string[l])
M3 = pd.DataFrame({'fr': X, 'ar': Y})
M3.tail(4)

# %% [markdown]
# Ca fonctionne الحمد لله. On va essayer de tout concaténer.

# %%
M = pd.concat((M1, M2, M3), axis = 0)
M

# %% [markdown]
# On a bien trois fois 11 titres, tout va bien الحمد لله. On va refaire l'index et on essaye de généraliser.

# %%
M.set_index(np.arange(len(M)), inplace = True)

# %% [markdown]
# ## Généralisation à toutes les pages

# %% [markdown]
# Maintenant on va essayer de trouver le nombre de pages total qu'il y a. On va prendre un maximum (100) et voir ce qui se passe si on envoie pour tous les nombres entre 3 et 100.

# %%
#Préparation du contenu de la page
M_list = []
for i in range(4,15):
    i = str(i)
    r = requests.get("https://www.sifatusafwa.com/fr/fiqh-maliki/?page=" + i)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('section', id = 'products')
    #s = s.find_all('div', class_ = 'products product_list row grid')
    lines = s.find_all('h3', class_ = 's_title_block flex_child')
    #Affichage du contenu de la page
    #print(lines)

    #Enlever les balises
    L_string = []
    for line in lines:
        L_string.append((line.text.split('\n')[0]))#line.text.split(\'n') est une liste de hcaine de caractères, donc [0] 
        #est seulement le str.
        #print(line.text.split('\n'))#line.text enlève les balises et les choses propres à html/css. Le .split split sur
        #les \n
        
        
    #Création des colonnes pour DataFrame
    Y = []
    X =[]
    for i in L_string:
        if L_string.index(i)%2 == 1:
            X.append(i)
        elif L_string.index(i)%2==0:
            Y.append(i)

    X = pd.Series(X)
    Y = pd.Series(Y)

    M_temp = pd.DataFrame({'fr':Y, 'ar':X})

    M_list.append(M_temp)

# %% [markdown]
# الحمد لله on a bien toutes nos pages. Maintenant on va essayer de tout concaténer : on aura tous les livres des malikiya du site dans un DataFrame

# %%
for i in range(len(M_list)):
    M = pd.concat((M, M_list[i]), axis = 0)

# %%
M.tail()

# %% [markdown]
# الحمد لله !!!!

# %%
M.set_index(np.arange(len(M)), inplace = True)

# %%
M.tail(15)

# %% [markdown]
# On remarque que les dernieres lignes se répètent: on va essayer de mettre une condition pour que si on voit que ca se repète, la boucle ne se relance pas.

# %%
L= []
for i in range(5):
    try:
        M_list[-1] == M_list[-2]
        break
    except ValueError:
        print("le code continue")
    print(i)

# %% [markdown]
# On le rajoute au grand code: on prendra un nombre de pages max de 15

# %%
#Préparation du contenu de la page
M_list = []
NB_MAX_PAGES = 15
for i in range(4,NB_MAX_PAGES):
        i = str(i)
        r = requests.get("https://www.sifatusafwa.com/fr/fiqh-maliki/?page=" + i)
        soup = BeautifulSoup(r.content, 'html.parser')
        s = soup.find('section', id = 'products')
        #s = s.find_all('div', class_ = 'products product_list row grid')
        lines = s.find_all('h3', class_ = 's_title_block flex_child')
        #Affichage du contenu de la page
        #print(lines)

        #Enlever les balises
        L_string = []
        for line in lines:
            L_string.append((line.text.split('\n')[0]))#line.text.split(\'n') est une liste de hcaine de caractères, donc [0] 
            #est seulement le str.
            #print(line.text.split('\n'))#line.text enlève les balises et les choses propres à html/css. Le .split split sur
            #les \n


        #Création des colonnes pour DataFrame
        Y = []
        X =[]
        for i in L_string:
            if L_string.index(i)%2 == 1:
                X.append(i)
            elif L_string.index(i)%2==0:
                Y.append(i)

        X = pd.Series(X)
        Y = pd.Series(Y)

        M_temp = pd.DataFrame({'fr':Y, 'ar':X})
        try :
            if (M_list[-1] == M_temp).fr.sum()!=0:
                break
            else:
                M_list.append(M_temp)
        except ValueError:
            M_list.append(M_temp)
            pass
        except IndexError:
            M_list.append(M_temp)
            pass

# %% [markdown]
# On concatène tout:

# %%
for i in range(len(M_list)):
    M = pd.concat((M, M_list[i]), axis = 0)

# %%
M.tail(10)

# %% [markdown]
# C'est bon ألحمد لله 

# %%
M.set_index(np.arange(len(M)), inplace = True)

# %%
M.to_excel('fiqh_maliki.xlsx', encoding='utf-8')

# %% [markdown]
# ## Fin 


