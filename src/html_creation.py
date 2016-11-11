import os

def touch(path):
    with open(path, 'w'):
        os.utime(path, None)

def coppy(r,w):
    lignes = r.readlines()
    for i in range(len(lignes)):
        w.write(lignes[i]) #.encode('ascii','ignore')
    return()

def html_creation(res_json):

    touch('./results/page.html')
    begin = open('./results/begin.txt','r')
    end = open('./results/end.txt','r')
    f = open('./results/temporal_search_results.html', 'w')
    coppy(begin,f)
    f.write(res_json)
    coppy(end,f)
    f.close()
    begin.close()
    end.close()
