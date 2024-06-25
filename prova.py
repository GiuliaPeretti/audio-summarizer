import multiprocessing as mp

def bo(n,results):
    results[n]=(n*n)

if __name__=='__main__':

    p=[]
    manager = mp.Manager()
    results=manager.list()
    for i in range(0,3):
        p.append(mp.Process(target=bo, args=(i,results)))
        results.append("")
        p[i].start()

    for i in range(0,3):
        p[i].join()

    print(results)