import os

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)

def coppy(r,w):
    lignes = r.readlines()
    for i in range(len(lignes)):
        w.write(lignes[i]) #.encode('ascii','ignore')
    return()

def html_creation(res_json):

    touch('../results/page.html')
    begin = open('../results/begin.txt','r')
    end = open('../results/end.txt','r')
    f = open('../results/page.html', 'w')
    coppy(begin,f)
    f.write(res_json)
    coppy(end,f)
    f.close()
    begin.close()
    end.close()
