# %% [markdown]
# بسم الله
# 
# **Troisième extraction**
# 
# Troisième notebook. Le but est d'essayer d'extraire tous les livres du site, en une fois, sans passer par des sous catégories comme on l'a fait dans la première étape.
# 
# On utilisera cependant la même démarche pour récupérer les urls que dans fiqhqmaliki-extract-1/2.

# %% [markdown]
# ## Etape 1 : Récupérer les urls

# %%
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from tqdm import tqdm

# %%
##Aller chercher les urls des livres
urls = []
new_urls = []
to_supp =[]
NB_MAX_PAGES = 100
print("Aller chercher les urls des livres\n")
for i in tqdm(range(2,NB_MAX_PAGES)):
    #if i%5 == 0:
    #  print('page ', i, '/', NB_MAX_PAGES, (i/NB_MAX_PAGES)*100, '%')
    i = str(i)
    r = requests.get('https://www.sifatusafwa.com/fr/accueil/?page=' + i)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('section', id = 'products')
    #s = s.find_all('div', class_ = 'products product_list row grid')
    #lines = s.find('h3', class_ = 's_title_block flex_child')
    #Affichage du contenu de la page
    #print(lines)

    #Extraire les liens
    
    for line in s.findAll('a'):
        urls.append(line.get('href'))#line.text.split(\'n') est une liste de chaine de caractères, donc [0] est 
        #seulement le str.
        #print(line.text.split('\n'))#line.text enlève les balises et les choses propres à html/css. Le .split split sur les \n
    #Tous les liens sont en double/ triple... on va les faire apparaitre qu'une seule fois.
    urls = list(np.unique(urls))
    #urls
    # On va supprimer les liens qui ne renvoient pas vers des livres : 
    #  - Ceux qui finissent pas '.asc' ou 'desc
    #  - Les liens de page ("?page=2", "?page=3"...) et le lien 'fiqh-maliki/'
    #  - les "javascript"
    
    #Suppression des liens ne renvoyant pas vers des livres.



# %%
len(urls)

# %%
for link in tqdm(urls):
    if (link.endswith('asc'))==False and \
        (link.endswith('.desc'))==False and \
        len(link.split('/'))>5 and \
        (link.split('/')[5].startswith('?page=')) == False and \
        (link.startswith('https://www.sifatusafwa.com/fr/accueil/?rewrite'))== False and\
        (link.split('/')[5] != ""):
        new_urls.append(link)            
    
for i in range(3):
    try:
        new_urls.remove('javascript:')
        new_urls.remove('javascript:;')
    except ValueError:
        continue
new_urls = pd.DataFrame(new_urls)
new_urls = new_urls.values.T.tolist()[0]
#on enlève tout ce qu'on a rajouté maintenant qu'on a pu faire la comparaison avec ce qu'il y avait
#a supprimer

# %%
len(new_urls)

# %% [markdown]
# ## Etape 2 : Boucle 1 (par ouvrage)

# %%
urls = new_urls

# %% [markdown]
# #### A régler

# %%
url = urls[0]
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
s = soup.find('section', class_='product-features')
L_string = []
for text in s.findAll(class_ ='data-sheet flex_container'):
    L_string.append(text.text.split('\n'))
L_string = np.array(L_string)
df = pd.DataFrame((L_string))
df = df.drop_duplicates()#des fois les volumes apparaissent deux fois
df.columns = ['supp', 'categories', str(url), 'supp2']# a cette étape on remplace ce qu'il faut pour voir les sites en colonnes
df.drop(['supp', 'supp2'], axis = 1, inplace=True)
df.set_index('categories', inplace = True)
urls.remove(urls[0]) #On enlève le lien qu'on a déjà mis dans le dataframe de base


# %% [markdown]
# #### Caractéristiques de base

# %%
print("Caractéristiques de base\n")
dfs = []
prices = []
auteurs = []
dates = []
domaines =[]
urls_obsolete = []
from tqdm import tqdm  
for url in tqdm(urls):
    # Ajout des caractéristiques du livre (de fiqhmaliki-extract-1)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('section', class_='product-features')
    L_string = []
    if s !=None:
        for text in s.findAll(class_ ='data-sheet flex_container'):
            L_string.append(text.text.split('\n'))
    else:
        urls_obsolete.append(url)
    L_string = np.array(L_string)
    df_other = pd.DataFrame((L_string))
    df_other = df_other.drop_duplicates()#des fois les volumes apparaissent deux fois
    if len(df_other.columns) == 4:
        df_other.columns = ['supp', 'categories',str(url), 'supp2']# a cette étape on remplace ce qu'il faut pour voir les sites en colonnes
        df_other.drop(['supp', 'supp2'], axis = 1, inplace=True)
        df_other.set_index('categories', inplace = True)
        dfs.append(df_other)

# %% [markdown]
# #### Ajout des auteurs/dates de décès/prix/domaines/descriptions 

# %%
print("Ajout des auteurs/dates de décès/prix/domaines/descriptions\n")
dfs_2 = []
from tqdm import tqdm  
prices = []
auteurs = []
dates = []
domaines = []
i = 0
for url in tqdm(urls):
    i = i+1
    #print('url numero', i, '/', len(urls), (i/len(urls))*100, "%")
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('section', id ='main')
## Ajout des auteurs/dates de décès/prix/domaines/descriptions (de fiqhmaliki-extract-2)
    #On vérifie si l'auteur du livre est disponible:
    s_auteur = s.find("a", class_= 'pro_extra_info_brand') #Si on divise pas en s_auteur et s_prix le find deviendra une liste car ce sera un find d'un find...
    
    #Soit pas d'auteur, soit auteur avec date, soit auteur sans date, soit auteur avec date mais deux
    #fois la parenthèse.

    if  s_auteur != None:#Auteur existe
        s_auteur = s_auteur.text         
        #Le try c'est juste pour couvrir tous les cas de date de décès possible
        try:#Cas 1 : La date existe : on l'ajoute
            s_dateauteur = s_auteur.split('(')[1].split('H)')[0]#s_auteur.split('(') = ['al qadhi iyyadh ', '544H)']
            dates.append(int(s_dateauteur))            

           #Ibn Rushd (Al-Jadd) (520H)	: split('\n') = ['', 'ibn rushd (Al hafid)', '']
        except IndexError:#Cas 2: Pas de date de décès disponible
            dates.append('') #On ne met pas de date pour pas qu'il y ait de décalage: un auteur avec la date de décès de l'auteur 
            #suivant
        except ValueError:#Cas 3: deux fois la parenthèse, il ne peut pas convertir en entier: c'est une 
            #chaine de caractères
            dates.append('') #Avantageux de remplir les auteurs après avoir vérifié la date car ibn rushd (al hafid) est coupé

        auteur = (s_auteur.split('\n')[1].split('(')[0])#s_auteur.split('\n) = ['', 'ibn rushd (Al hafid)', '']
         # ou ['', 'al qadi iyadd','(544)]
        auteurs.append(auteur) #Pour pas qu'on ait un espace à la fin.
            
    else: #Pas d'auteur
        auteurs.append('Auteur non disponible')
        dates.append('') #pour pas qu'il y ait de décalage: un auteur avec la date de décès de l'auteur suivant
    
    #Ajour du prix    
    s_prix = s.find("span", class_ = 'price')
    try:
        price = s_prix.text
        prices.append(price)

    except AttributeError: #s.find eset une liste et .text n'existe pas pour une liste: normalement plus d'erreur
        print(url, type(s))
        prices.append('Non disponible')
    #Ajout du domaine:
    domaine = url.split('/')[4]
    domaines.append(domaine)

# %% [markdown]
# On va faire un DataFrame avec les informations des livres (titre arabe, auteur, édition, volumes... de fiqh-extract1) et un autre avec les auteurs, les domaines.... (de fiqhmaliki-extract-2)

# %%
dfs_1 = pd.concat((i for i in dfs), axis = 1)
dfs_2 = pd.DataFrame({"lien": urls, 'auteurs': auteurs, 'date': dates, 'domaine':domaines, 'prix': prices})

# %%
dfs_1 = dfs_1.T


# %%
dfs_1['lien'] = dfs_1.index
dfs_1.set_index(np.arange(len(dfs_1)), inplace = True)

# %%
dfs_2['lien'][0] ==  dfs_1['lien'][0]

# %%
if 'isbn' in dfs_1.columns and "ean13" in dfs_1.columns:
    dfs_1.drop(['isbn', 'ean13'], axis = 1, inplace=True)#Données propres à l'édition d'un livre. Elles ont du
#etre présentes sur un des liens.

# %% [markdown]
# On pourra donc faire une jointure si besoin car les deux dataframes ont les mêmes sites aux mêmes index
# 
# On va faire un troisième DataFrame avec les descriptions des livres.

# %% [markdown]
# #### Ajout des descriptions

# %%
print("Ajout des descriptions\n")
descriptions = []
for url in tqdm(urls):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('section', id ='main')
    s_description = s.find(class_ = 'product-information')

    try:
        s_description = s_description.text.split('\n')
        description = ""
        passage = False
        for char in range(len(s_description)):
            if s_description[char] != "":
                description = description + s_description[char] + '\n'
                passage = True
            else:
                if passage == True:
                    break
        
    except AttributeError as e :
        print('pas diponible', e)
        description = 'erreur'
    descriptions.append(description)

# %%
dfs_3 = pd.DataFrame({'description':descriptions, 'lien':urls})
dfs_3.sample(15)

# %% [markdown]
# #### Ajout des éditions

# %%
print("Ajout des descriptions des éditions\n")

descriptions_edition = []
for url in tqdm(urls):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('section', id ='main')
    s_editiondescription =  s.find(class_ = 'product-description')
    description = ""
    passage = False
    try:
        if s_editiondescription != None:
            s_editiondescription = s_editiondescription.text.split('\n')
            for char in range(len(s_editiondescription)):
                if s_editiondescription[char] != "":
                    description = description + s_editiondescription[char] + '\n'
                    passage = True
                    char = char + 1
                else:
                    if passage == True:
                        break
                    char = char + 1
    except AttributeError as e:
            description = "Erreur"
    if passage == False: # Pas description d'édition
        description = 'Non disponible'
    descriptions_edition.append(description)


# %% [markdown]
# On ajoute un dernier DataFrame avec les descriptions éditions (certains ouvrages ne possèdent qu'une seule édition donc beaucoup de valeurs nulles si on les met dans le même DataFrame)

# %%
dfs_edition = pd.DataFrame({"descriptions_edition":descriptions_edition, "urls":urls})
dfs_edition["urls"].values

# %%
dfs_3.head()

# %%
dfs_1.to_csv('books_1.csv')
dfs_2.to_csv('books_2.csv')
dfs_3.to_csv('books_3.csv')

# %% [markdown]
# #### الحمد لله; la construction du dataset est terminée.

# %%
url = "https://www.sifatusafwa.com/fr/explications-de-livres-de-aqida/charh-aqidah-salaf-wa-ashab-al-hadith-cheikh-abdallah-al-ghunayman.html"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
s = soup.find('section', id ='main')
s_description = s.find(class_ = 'product-information')
s_description


