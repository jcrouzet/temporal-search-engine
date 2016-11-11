
import numpy as np
import math
#import matplotlib.pyplot as mp


def valeur_bruit(n,k=0.33): #Selection de 33 %
    n = np.array(n)
    S_bruit=[]
    S_prime=[]
    S_bruit_liss=[]
    for i in range(0,200):
        S_bruit.append( (n > ((i/200) * max(n)) ).sum() ) # Seuillage du
    S_bruit=np.array(S_bruit)
    l=len(S_bruit)
    S_bruit_liss=( S_bruit[0:l-5] + S_bruit[1:l-4] + S_bruit[2:l-3] + S_bruit[3:l-2] + S_bruit[4:l-1] + S_bruit[5:l-0] )/ 6 #Lissage du seuil de bruit
    S_bruit_liss=np.concatenate((np.array([S_bruit_liss[0], S_bruit_liss[0], S_bruit_liss[0]]), S_bruit_liss))
    seuil = np.argmin(
    abs( S_bruit_liss - k *
    np.max(S_bruit_liss) ) )
    return((seuil/200)*n.max())


def peekadpt(hist,k1=0.33,k2=0.33):
    #mp.plot(hist)
    #mp.show()
    bruit=valeur_bruit(hist,k1)
    Hist=np.array(hist)
    l=len(Hist)
    Hist_liss = ( Hist[0:l-5] + Hist[1:l-4] + Hist[2:l-3] + Hist[3:l-2] + Hist[4:l-1] + Hist[5:l-0] )/ 6
    Hist_liss = np.concatenate( ( np.array( [Hist_liss[0], Hist_liss[0], Hist_liss[0]] ), Hist_liss ) )

    taille=[]
    duree=[]
    for j in range(1,100):
        matflag=(Hist_liss>(((1+(j/10))*bruit)))
        flag=False
        duree.append([])
        num=-1;
        for i in range(len(matflag)):
            if (matflag[i]):
                if not(flag):
                    duree[j-1].append([i,0])
                    flag=True
                    num+=1
            else:
                if (flag):
                    duree[j-1][num][1]=i
                    flag=False
        taille.append(len(duree[j-1]))
    taille=np.array(taille)
    l=len(taille)
    seuil=np.argmin(abs(taille-k2*max(taille)))
    return(duree[seuil-1])
