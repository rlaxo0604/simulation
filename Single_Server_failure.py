import numpy as np

class single_server:
    def __init__(self):

        self.Q =0 ; self.M=0 ; self.Before =0; self.SumQ =0; self.MH=0

    def initialize_routine(self):
        self.Q=0
        self.M=1
        self.MH=0
        self.Before =0
        self.SumQ =0

        self.time = 0
        self.clk=0
        self.Sreward=0
        self.failure_count = 0
        self.PM_count =0

        self.events = np.array([])
        self.events = np.append(self.events, [1, np.random.exponential(5)])
        self.events = np.vstack((self.events, np.array([4, np.random.exponential(25)])))

        self.events_t = np.array([])
        self.empty = 0


    def event_routine(self, k, time): # 1 = arrival, 2 = load, 3 = unload 4 = Health, 5=Fail, 6=Repair
        if k == 1:
            self.SumQ += self.Q*(time-self.Before)
            self.Sreward += -self.Q*(time-self.Before)
            self.Before = time
            self.Q += 1

            # generate new event
            if self.empty == 1:
                self.events = np.array([1, time + np.random.exponential(5)]) # arrival
                if self.M == 1:
                    self.events = np.vstack((self.events, np.array([2, time])))  # load
                self.events = self.events[np.argsort(self.events[:, 1])]
            else:
                self.events = np.vstack((self.events, np.array([1, time + np.random.exponential(5)]))) # arrival
                if self.M == 1:
                    self.events = np.vstack((self.events, np.array([2, time]))) # load
                self.events = self.events[np.argsort(self.events[:, 1])]
            #
            # print("Arrive | Q=%s, M=%s, MH= %s" % (self.Q, self.M, self.MH))

        elif k == 2:
            self.SumQ += self.Q*(time-self.Before)
            self.Sreward -= self.Q * (time - self.Before)
            self.Before = time
            self.Q -= 1
            self.M = 0

            # generate new event
            if self.empty == 1:
                self.events = np.array([3, time + np.random.exponential(2)])
                self.events = self.events[np.argsort(self.events[:, 1])]
            else:
                self.events = np.vstack((self.events, np.array([3, time + np.random.exponential(2)])))
                self.events = self.events[np.argsort(self.events[:, 1])]
            #
            # print("Load | Q=%s, M=%s, MH= %s" % (self.Q, self.M, self.MH))

        elif k == 3:
            self.M = 1
            # generate new event
            if self.Q > 0:
                if self.empty == 1:
                    self.events = np.array([2, time])
                    self.events = self.events[np.argsort(self.events[:, 1])]
                else:
                    self.events = np.vstack((self.events, np.array([2, time])))
                    self.events = self.events[np.argsort(self.events[:, 1])]

            # print("Unload | Q=%s, M=%s, MH= %s" %(self.Q, self.M, self.MH))

        elif k == 4:

            self.MH += 1

            self.events = np.vstack((self.events, np.array([4, time + np.random.exponential(25)])))
            self.events = self.events[np.argsort(self.events[:, 1])]
            if self.empty == 1:
                if self.MH > 4:
                    self.events = np.array([5, time])
                    self.events = self.events[np.argsort(self.events[:, 1])]
            else:
                if self.MH > 4:
                    self.events = np.vstack((self.events, np.array([5, time])))
                    self.events = self.events[np.argsort(self.events[:, 1])]

            # print("MH | Q=%s, M=%s, MH= %s" % (self.Q, self.M, self.MH))

        elif k == 5: # fail
            self.failure_count+=1
            self.M = 2
            # print(self.events)

            indexM = np.where(self.events == 4)  # MH
            # print(indexM)
            if list(indexM[0])!=[]:
                self.events = np.delete(self.events, indexM[0][0], axis=0)
            # print(self.events)

            indexU = np.where(self.events == 3) # unload
            # print(indexU)
            if list(indexU[0]) != []:
                self.events = np.delete(self.events, indexU[0][0], axis=0)
            # print(self.events)

            # indexL = np.where(self.events == 2)  # load
            # print(indexL)
            # if list(indexL[0]) != []:
            #     self.events = np.delete(self.events, int(indexL[0]), axis=0)
            # print(self.events)

            if self.empty == 1:
                self.events = np.array([6, time + np.random.exponential(125)])
                self.events = self.events[np.argsort(self.events[:, 1])]
            else:
                self.events = np.vstack((self.events, np.array([6, time + np.random.exponential(125)]))) # repair
                self.events = self.events[np.argsort(self.events[:, 1])]
            # print("============================")
            # print("Fail | Q=%s, M=%s, MH= %s" % (self.Q, self.M, self.MH))



        elif k == 6: # repair
            self.M = 1
            self.MH = 0

            if self.empty == 1:
                if self.Q > 0:
                    self.events = np.array([2, time]) # load
                    self.events = np.vstack((self.events, np.array([4, time + np.random.exponential(25)]))) # MH
                    self.events = self.events[np.argsort(self.events[:, 1])]
            else:
                if self.Q > 0:
                    self.events = np.vstack((self.events, np.array([2, time])))
                    self.events = np.vstack((self.events, np.array([4, time + np.random.exponential(25)])))
                    self.events = self.events[np.argsort(self.events[:, 1])]

            # print("Repair | Q=%s, M=%s, MH= %s" % (self.Q, self.M, self.MH))
            # print("============================")

        elif k==7: # Preventive maintenance
            self.PM_count+=1
            self.M = 2

            indexM = np.where(self.events == 4)  # MH
            # print(indexM)
            if list(indexM[0])!=[]:
                self.events = np.delete(self.events, indexM[0][0], axis=0)

            indexU = np.where(self.events == 3)  # unload
            if list(indexU[0]) != []:
                self.events = np.delete(self.events, indexU[0][0], axis=0)

            indexL = np.where(self.events == 2)  # load
            # print(indexL)
            if list(indexL[0]) != []:
                self.events = np.delete(self.events, indexL[0][0], axis=0)
           # print(self.events)

            if self.empty == 1:
                self.events = np.array([6, time + np.random.exponential(60)])
                self.events = self.events[np.argsort(self.events[:, 1])]
            else:
                self.events = np.vstack((self.events, np.array([6, time + np.random.exponential(60)])))  # repair
                self.events = self.events[np.argsort(self.events[:, 1])]
            # print("============================")
            # print("PM | Q=%s, M=%s, MH= %s" % (self.Q, self.M, self.MH))

    def reset_Sreward(self):
        self.Sreward = 0

    def fail_count(self):
        return self.failure_count

    def PMcount(self):
        return self.PM_count

    def retrieve_event(self):
        if np.shape(self.events) == (2,):
            k = self.events[0]
            time = self.events[1]
            self.events = 0
            self.empty = 1
        else:
            k = self.events[0, 0]
            time = self.events[0, 1]
            self.events = np.delete(self.events, 0, axis= 0)
            self.empty = 0

        return k, time

    def retrive_time(self):
        if np.shape(self.events) == (2,):
            time = self.events[1]
        else:
            time = self.events[0, 1]

        return time

    def next_event(self, a):
        if a ==0:
            while 1:
                k, time = self.retrieve_event()
                clk = time
                self.event_routine(k, time)
                if k == 3:
                    break
        else:
            time = self.retrive_time()
            clk=time
            self.event_routine(7,time)
            while 1:
                k, time = self.retrieve_event()
                clk = time
                self.event_routine(k, time)
                if k == 3:
                    break

        return self.Q, self.MH, self.Sreward, time

    def statistics(self, time):
        self.SumQ += self.Q * (time - self.Before)
        AQL = self.SumQ / time

        return AQL


#### main code ####
n_test = 30
AQL = np.zeros(n_test)
f_count = np.zeros(n_test)
m = single_server()
for i in range(n_test):
    clk = 0

    m.initialize_routine()

    while clk < 5000:
        k, time = m.retrieve_event()
        clk = time

        m.event_routine(k, time)

    AQL[i] = m.statistics(clk)
    f_count[i]= m.fail_count()

print("=======================================================================")
print("Test_failure_AQL = %s fail_count= %s " % ((np.mean(AQL)), np.mean(f_count)))
print("=======================================================================")

