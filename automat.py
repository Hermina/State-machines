class DKA:
    ''' Deterministicki konacni automat'''
    def __init__(self, Q, sigma, funkcPrijelaza, pocetno, zavrsno):
        self.sigma = sigma
        self.Q = Q
        self.delta  = funkcPrijelaza # funkcija prijelaza iz stanja u stanje
        self.q0     = pocetno # pocetno stanje
        self.F      = zavrsno # skup zavrsnih stanja
        
    def ispitaj(self, stanje, rijec):
        # stanja su u obliku mapa(stanje:mapa(znak:stanje))
        # iz jednog stanja sa nekim znakom dobijemo drugo stanje
        for znak in rijec:
            try:
                stanje = self.delta[stanje][znak]
            except KeyError:
                pass
        return stanje

    def daLiJeUJeziku(self, rijec):
        return self.ispitaj(self.q0,rijec) in self.F

class NKA:
    def __init__(self, Q, sigma, funkcPrijelaza, pocetno, zavrsno):
        self.sigma = sigma
        self.Q = Q
        self.delta  = funkcPrijelaza
        self.q0     = pocetno
        self.F        =set(zavrsno)

    def ispitaj(self, stanje, rijec):
        #stanja = set([stanje])
        i = 0
        znak=rijec[0]
        skupStanja = set()
        try:
            for st in self.delta[stanje][znak]:
                if (len(rijec)>1):
                    skupStanja = skupStanja | self.ispitaj(st, rijec[1:])
                else:
                    skupStanja=skupStanja | set([st])
        except KeyError:
            pass
        return skupStanja
        
    def daLiJeUJeziku(self,rijec):
        return len(self.ispitaj(self.q0, rijec) & self.F) > 0

class eNKA:
    def __init__(self, Q, sigma, funkcPrijelaza, pocetno, zavrsno):
        self.sigma = sigma
        self.Q = Q
        self.delta = funkcPrijelaza
        self.q0 = pocetno
        self.F = set(zavrsno)

    def eOkruzenje (self, stanja):
        novaStanja=stanja
        for st in stanja:
            try:
                if (not (self.delta[st]['eps'] <= stanja)):
                    novaStanja=novaStanja | self.eOkruzenje(self.delta[st]['eps'])
            except KeyError:
                pass
        return novaStanja

    def ispitaj(self, stanje, rijec):
        skupStanja=set()
        znak=rijec[0]
        
        for sta in self.eOkruzenje(set([stanje])):
            try:
                for st in (self.delta[sta][znak]):
                    if (len(rijec)>1):
                        skupStanja = skupStanja | self.ispitaj(st, rijec[1:])
                    else:
                        skupStanja=skupStanja | self.eOkruzenje(set([st]))
                #skupStanja = skupStanja | set([sta])
            except KeyError:
                pass
        return skupStanja    
    
    def daLiJeUJeziku(self,rijec):
        return len(self.ispitaj(self.q0, rijec) & self.F) > 0

def eNKAuNKA(e):
    f=e.F
    delta={}
    if len(e.F & e.eOkruzenje(set([e.q0])))>0:
        f=f|set([e.q0])
    for q in e.Q:
        delta[q]={}
        for a in e.sigma:
            if len(e.ispitaj(q,a))>0:
                delta[q][a]=e.ispitaj(q,a)
    Nka=NKA(e.Q, e.sigma, delta, e.q0, f)
    return Nka

def NKAuDKA(n):
    q0=frozenset([n.q0])
    skupStanja=set()
    f=set()
    isprobana=set()
    delta={}
    #stog=[set(a) for a in n.Q] 
    stog=[set([n.q0])]
    while len(stog)>0:
        a=stog.pop()
        isprobana.add(frozenset(a))
        skupStanja.add(frozenset(a))
        pom=set()
        delta[frozenset(a)]={}
        for znak in n.sigma:
            pom = set()
            for k in a:
                stanja=n.ispitaj(k, znak)
                pom=pom | stanja
                if len(stanja & n.F)>0:
                    f.add(frozenset(stanja))
                    skupStanja.add(frozenset(stanja))

                if (stanja not in isprobana):
                    stog.append(stanja)
            delta[frozenset(a)][znak]=frozenset(pom)
    dka=DKA(skupStanja, n.sigma, delta, q0, f)
    return dka


delta = {'q0':{'eps':set(['q1']),'0':set(['q0'])}, 'q1':{'eps':set(['q2']),'1':set(['q1'])}, 'q2':{'2':set(['q2'])}}
N = eNKA(set(['q0','q1','q2']),set(['0','1','2']),delta, 'q0', ['q2'])
n2=eNKAuNKA(N)
n3=NKAuDKA(n2)
print "----------------------ISPIS DELTI------------------------------"
print " "
print "----------------------e NKA------------------------------------"
print N.delta
print "----------------------NKA------------------------------------"
print n2.delta
print "----------------------DKA------------------------------------"
print n3.delta
print " "
print "++++++++++++++++++++++Provjera ispravnosti++++++++++++++++++++++"
print " "
print "----------------------e NKA------------------------------------"
print [(x, N.daLiJeUJeziku(x)) for x in ['0001', '00012', '120101', '00010']]
print "----------------------NKA------------------------------------"
print [(x, n2.daLiJeUJeziku(x)) for x in ['0001', '00012', '120101', '00010']]
print "----------------------DKA------------------------------------"
print [(x, n3.daLiJeUJeziku(x)) for x in ['0001', '00012', '120101', '00010']]
