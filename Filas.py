import pandas as pd
import random as rdm
TIME_STEP = 0.01 # Variavel global que define a passagem do tempo
colunas = ["Tempo_Fila_1", # Nomes das métricas de interesse que queremos observar
                  "Tempo_Servidor_1",
                  "Tempo_Fila_2",
                  "Tempo_Servidor_2",
                  "Tempo_Fila_3",
                  "Tempo_Servidor_3",
                  "Tempo_Total_Fila",
                  "Tempo_Total_Servico",
                  "Tempo_Total_Sistema"]

n_jobs = [20000, 100000, 1000000] # Faremos um experimento para cada número de jobs e modo de serviço
modes = [0,1,2] # Controla em que modo de serviço cada servidor será criado. Tempo fixo, uniforme ou exponencial
mode_str = ["Fixo", "Uniforme", "Exponencial"] # Usado com o conjunto acima para nomear os arquivos de saída csv


# Definição de um Processo como Objeto
class Process:
    def __init__(self, init_time):
        self.tS1 = 0.0 # Tempo total de serviço no servidor de número correnpondente
        self.tS2 = 0.0
        self.tS3 = 0.0
        self.tQ1 = 0.0 # Tempo total na fila antes de cada servidor
        self.tQ2 = 0.0
        self.tQ3 = 0.0
        self.QsT = init_time # Tempo determinístico do momento que o processo foi inserido numa fila qualquer

    def addStats(self): # É chamada apenas no momento que o processo sai do sistema
        total_service_time = self.tS1 + self.tS2 + self.tS3
        total_queue_time = self.tQ1 = self.tQ2 + self.tQ3
        total_system_time = total_service_time + total_queue_time
        final_results = pd.DataFrame([[self.tQ1,
                                        self.tS1,
                                        self.tQ2,
                                        self.tS2,
                                        self.tQ3,
                                        self.tS3,
                                        total_queue_time,
                                        total_service_time,
                                        total_system_time]], columns=colunas)
        global tempos
        tempos = pd.concat([tempos, final_results]) # Insere os tempos do processo num dataframe


class ServerOne:
    def __init__(self, mode):
        self.mode = mode # Variavel que define o tipo do tempo de serviço: fixo, uniforme ou exponencial
        self.proc = None # Variável que vai guardar um processo proveniente de uma fila
        self.totalTimeRequested = 0.0 # Tempo de serviço requisitado para um processo
        self.totalTimeElapsed = 0.0 # Tempo acumulado de serviço para o processo corrente

    def serviceTime(self): # Sorteia o tempo de serviço pelas especificações do trabalho
        if (self.mode == 0):
            return 0.4
        elif (self.mode == 1):
            return rdm.uniform(0.1, 0.7)
        else:
            return rdm.expovariate(lambd=1/0.4)

    def iterate(self, currTime):
        if (self.proc is None and len(q1) == 0): # Se não tiver processo e a fila estiver vazia não faz nada
            return
        elif (not (self.proc is None)):
            self.totalTimeElapsed += TIME_STEP
            if (self.totalTimeElapsed >= self.totalTimeRequested):
                self.proc.tS1 += self.totalTimeRequested # Se o tempo de processamento for maior que o tempo requisitado
                sendTo = rdm.randint(2, 3) # Manda para o servidor 2 ou 3 com 50% de chance cada
                if (sendTo == 2):
                    self.proc.QsT = currTime
                    q2.append(self.proc)
                else:
                    self.proc.QsT = currTime
                    q3.append(self.proc)
                self.proc = None
                if (len(q1)):
                    self.proc = q1.pop(0)
                    self.proc.tQ1 = currTime - self.proc.QsT
                    self.totalTimeRequested = self.serviceTime()
                    self.totalTimeElapsed = 0.0
                    return
        elif (len(q1)):
            self.proc = q1.pop(0)
            self.totalTimeRequested = self.serviceTime()
            self.totalTimeElapsed = currTime - self.proc.QsT
            return


class ServerTwo:
    def __init__(self, mode):
        self.mode = mode
        self.proc = None
        self.totalTimeRequested = 0.0
        self.totalTimeElapsed = 0.0

    def serviceTime(self):
        if (self.mode == 0):
            return 0.6
        elif (self.mode == 1):
            return rdm.uniform(0.1, 1.1)
        else:
            return rdm.expovariate(lambd=1 / 0.6)

    def iterate(self, currTime):
        if (self.proc is None and len(q2) == 0):
            return
        elif (not (self.proc is None)):
            self.totalTimeElapsed += TIME_STEP
            if (self.totalTimeElapsed >= self.totalTimeRequested):
                self.proc.tS2 += self.totalTimeRequested
                sendTo = rdm.choices([2, 4], weights=[0.2, 0.8], k=1)
                if (sendTo == 2):
                    self.proc.QsT = currTime
                    q2.append(self.proc)
                else:
                    self.proc.addStats()
                self.proc = None
                if (len(q2)):
                    self.proc = q2.pop(0)
                    self.proc.tQ2 = currTime - self.proc.QsT
                    self.totalTimeRequested = self.serviceTime()
                    self.totalTimeElapsed = 0.0
                    return
        elif (len(q2)):
            self.proc = q2.pop(0)
            self.totalTimeRequested = self.serviceTime()
            self.totalTimeElapsed = currTime - self.proc.QsT
            return


class ServerThree:
    def __init__(self, mode):
        self.mode = mode
        self.proc = None
        self.totalTimeRequested = 0.0
        self.totalTimeElapsed = 0.0

    def serviceTime(self):
        if (self.mode == 0):
            return 0.95
        elif (self.mode == 1):
            return rdm.uniform(0.1, 1.8)
        else:
            return rdm.expovariate(lambd=1 / 0.95)

    def iterate(self, currTime):
        if (self.proc is None and len(q3) == 0):
            return
        elif (not (self.proc is None)):
            self.totalTimeElapsed += TIME_STEP
            if (self.totalTimeElapsed >= self.totalTimeRequested):
                self.proc.tS3 += self.totalTimeRequested
                self.proc.addStats()
                self.proc = None
                if (len(q3)):
                    self.proc = q3.pop(0)
                    self.proc.tQ3 = currTime - self.proc.QsT
                    self.totalTimeRequested = self.serviceTime()
                    self.totalTimeElapsed = 0.0
                    return
        elif (len(q3)):
            self.proc = q3.pop(0)
            self.totalTimeRequested = self.serviceTime()
            self.totalTimeElapsed = currTime - self.proc.QsT
            return


for n in range(len(n_jobs)):
    for m in range(len(modes)):

        Server1 = ServerOne(modes[m])
        Server2 = ServerTwo(modes[m])
        Server3 = ServerThree(modes[m])
        tempos_de_chegada = []
        for i in range (n_jobs[n] + 100):
            if(i == 0):
                tempos_de_chegada.append(rdm.expovariate(lambd = 2))
            else:
                tempos_de_chegada.append(rdm.expovariate(lambd = 2) + tempos_de_chegada[i-1])
        tempos = pd.DataFrame([[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]],columns=colunas)
        currTime = 0.0
        q1 = []
        q2 = []
        q3 = []

        # loop de iteração
        while (1):
            if (len(tempos_de_chegada) != 0):
                if (currTime >= tempos_de_chegada[0]):
                    q1.append(Process(tempos_de_chegada.pop(0)))

            Server1.iterate(currTime)
            Server2.iterate(currTime)
            Server3.iterate(currTime)

            if (len(tempos.index) >= n_jobs[n]+1):
                break
            print(len(tempos.index))
            currTime += TIME_STEP
        tempos.to_csv("Stats_Servidor" + mode_str[m] + "_" + str(n_jobs[n]) + "_jobs.csv")

