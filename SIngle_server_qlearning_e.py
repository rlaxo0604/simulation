import numpy as np
from Single_Server_failure import *
import matplotlib.pyplot as plt
import pandas as pd

m = single_server()



Q = np.zeros(shape=(1500,10,2))
Queue =0; M=0; MH=0

n_episode = 5000

alpha = 0.1
gamma = 0.9
epsilon = 1
clk_max = 5000
sum_reward = np.zeros(n_episode)



for episode in range(n_episode):

    m.initialize_routine()
    clk = 0

    while clk < clk_max:
        # print("iteration %s" % (iter))
        if np.random.rand() < epsilon:
            a=np.random.randint(2)
            # print("random : %s" %(a))
        else:
            mx=np.max(Q[Queue,MH])
            a=np.random.choice(np.where(Q[Queue,MH] ==mx)[0])
            # print(np.where(Q[Queue,M,MH] ==mx)[0])
            # print(np.random.choice(np.where(Q[Queue,M,MH] ==mx)[0]))
        Queue_n, MH_n, reward, time = m.next_event(a)
       # print("Reward : %s "%(reward))
        sum_reward[episode]+=reward #### 고쳐야됨
        Q[Queue,MH,a]= (1.-alpha)*Q[Queue,MH,a]+alpha*(reward+gamma*np.max(Q[Queue_n,MH_n]))
        Queue = Queue_n; MH=MH_n
        m.reset_Sreward()
        clk = time

    epsilon = 1/(episode+1)
    AQL = m.statistics(clk)
    failure_count = m.fail_count()
    PM_count = m.PMcount()

    if episode%100 == 0:

        print("=======================================================================")
        print("Epi %s | AQL = %s, f_count= %s PM_count = %s sum_reward = %s" % (episode, AQL, failure_count, PM_count, sum_reward[episode]))
        print("=======================================================================")

n_test = 30
AQL = np.zeros(n_test)
clk = 0
Queue =0; M=0; MH=0
f_count = np.zeros(n_test)
epsilon = 0
f_test_c = np.zeros(n_test)
pm_test_c= np.zeros(n_test)

for test in range(n_test):
    m.initialize_routine()
    clk = 0
    while clk < clk_max:
        # print("iteration %s" % (iter))

        mx = np.max(Q[Queue, MH])
        a = np.random.choice(np.where(Q[Queue,MH] == mx)[0])
        # print("max : %s" %(a))
        Queue_n, MH_n, reward, time = m.next_event(a)
        # print("Reward : %s "%(reward))
        sum_reward[test] += reward
        Queue = Queue_n
        MH = MH_n
        m.reset_Sreward()
        clk = time

        AQL[test]= m.statistics(clk)
        f_test_c[test] = m.fail_count()
        pm_test_c[test] = m.PMcount()

print("===========================================================================")
print("TEST | AQL = %s f_count= %s PM_count = %s " % (np.mean(AQL), np.mean(f_test_c), np.mean(pm_test_c)))
print("===========================================================================")

Graph = np.zeros((5,5000))


for q in range(5000):
    for mh in range(5):
        if Q[q, mh, 0] >  Q[q, mh, 1]:
            Graph[mh, q] = 0
        elif Q[q, mh, 0] == Q[q, mh, 1]:
            Graph[mh, q] = 0.5
        else:
            Graph[mh, q] = 1

df = pd.DataFrame(Graph)
filepath = 'Policy_5000_e.xlsx'
df.to_excel(filepath, index=False)
