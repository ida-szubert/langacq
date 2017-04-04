class syn_sem:
    """
    A Dirichlet process of a (syntax,semantics) pair mapping to a distribution over words.
    """
    one_word = True
    syn_sem_top = None
    @staticmethod
    def set_one_word(oneWord):
        one_word = oneWord
        
    def __init__(self,syn_cat,sem_key):
        self.last_used = 0
        self.syn_cat = syn_cat
        self.sem_key = sem_key
        self.key = self.syn_cat+":"+self.sem_key
        self.words = {}
        #self.syn_sem_top = syn_sem_top
        self.alpha_tot = 0
        self.bleurgh_alpha_tot = 0
        self.bottom_term = 0
    def removelex(self,word):
        if not self.words.has_key(word):
            print self.words
        del self.words[word]
    def check(self,word,lex_item):
        if not self.words.has_key(word):
            self.words[word] = lex_item


    #################################################################
    def map_log_word_prob(self, word,alpha_tot,sentence_count,verbose):
        error()
        if sentence_count != 0:
            scale = Lexicon.extrascale*sentence_count
        else:
            scale = 1.0
        scale = 1.0
        verbose = True
        verbose = False
        
        log_prior = syn_sem.log_word_prior(word) + scale*syn_sem.syn_sem_top \
            - (scale*self.alpha_tot + scale*syn_sem.syn_sem_top)
        
        if word.find(" ")!=-1 and self.one_word: log_prior = -inf
        seen_log_prob = -inf
        if self.words.has_key(word) and self.words[word].alpha > 0:
            #seen_log_prob = psi(self.words[word].bleurgh_alpha)-psi(self.bleurgh_alpha_tot+self.syn_sem_top)
#            seen_log_prob = psi(self.words[word].alpha)-psi(self.alpha_tot+self.syn_sem_top)
            seen_log_prob = scale*self.words[word].alpha - (scale*alpha_tot + scale*syn_sem.syn_sem_top)
            if seen_log_prob > 0:
                print "too much seen log prob for syn-> sem ",self.key,"->",word
                print self.words[word].toString()
                print "alpha is ",self.words[word].alpha
                print "alpha tot is ",alpha_tot
                print "alpha o is ",syn_sem.syn_sem_top
                print "scale is ",scale
                print "l last seen at ",self.words[word].last_used
                print "ss last seen at ",self.last_used
                error()
        log_prob = log_sum(log_prior,seen_log_prob)
       
        if verbose:
            print "\nfor ",self.key," -> ",word
            print "alpha = ",self.words[word].alpha,"  alphatot = ",self.alpha_tot,"  synsemtop = ",syn_sem.syn_sem_top
            print "seen log prob = ",seen_log_prob
            print "log prior = ",log_prior
            print "log prob = ",log_prob
        
        # print "log prob = ",log_prob
        return log_prob

    #############################################################
            
    def log_word_prob(self,word,alpha_tot,sentence_count,verbose):
#       print "getting prob for ",self.key," -> ",word
#       if not self.words.has_key(word): return -inf
               
        if sentence_count != 0:
            scale = Lexicon.extrascale*sentence_count
        else:
            scale = 1.0
        scale = 1.0
        verbose = True
        verbose = False
        
        log_prior = syn_sem.log_word_prior(word) + psi(scale*syn_sem.syn_sem_top)-psi(scale*self.alpha_tot + scale*syn_sem.syn_sem_top)
        
        if word.find(" ")!=-1 and self.one_word: log_prior = -inf
        seen_log_prob = -inf
        if self.words.has_key(word) and self.words[word].alpha > 0:
            #seen_log_prob = psi(self.words[word].bleurgh_alpha)-psi(self.bleurgh_alpha_tot+self.syn_sem_top)
#            seen_log_prob = psi(self.words[word].alpha)-psi(self.alpha_tot+self.syn_sem_top)
            seen_log_prob = psi(scale*self.words[word].alpha)-psi(scale*alpha_tot + scale*syn_sem.syn_sem_top)
            if seen_log_prob > 0:
                print "too much seen log prob for syn-> sem ",self.key,"->",word
                print self.words[word].toString()
                print "alpha is ",self.words[word].alpha
                print "alpha tot is ",alpha_tot
                print "alpha o is ",syn_sem.syn_sem_top
                print "scale is ",scale
                print "l last seen at ",self.words[word].last_used
                print "ss last seen at ",self.last_used
                error()
        log_prob = log_sum(log_prior,seen_log_prob)
       
        if verbose:
            print "\nfor ",self.key," -> ",word
            print "alpha = ",self.words[word].alpha,"  alphatot = ",self.alpha_tot,"  synsemtop = ",syn_sem.syn_sem_top
            print "seen log prob = ",seen_log_prob
            print "log prior = ",log_prior
            print "log prob = ",log_prob
        
#        print "log prob = ",log_prob
        return log_prob

    def printout(self,alpha_tot):
        alphasum = 0.0
        print "\n",self.key
        #print "alphatot = ",self.alpha_tot
        print "alphatot = ",alpha_tot
        for w in self.words:
            print w, self.words[w].alpha 
            alphasum+=self.words[w].alpha
        print "alphasum = ",alphasum
        if alpha_tot == 0.0 and alphasum == 0.0: return
#        if abs((alpha_tot-alphasum)/alpha_tot)>0.1:
#            error()
#prob = prior*exp(psi(self.syn_sem_top))/exp(psi(self.alpha_tot+self.syn_sem_top))
            #pass
        #else:
            #prob = exp(psi(self.words[word].alpha))/exp(psi(self.alpha_tot+self.syn_sem_top)) + prior*exp(psi(self.syn_sem_top))/exp(psi(self.alpha_tot+self.syn_sem_top))
        #if prob > 1.0:
            #print 'word prob over 1'
        #print "word prob for ",self.key+"-->"+word," = ",prob
        #return prob
        #return 10000
    #def prob_word(self,word):
        #if word.find(' ')!=-1:
            #return 0
        #prior = self.words[word].set_word_prior()
    #prior = 0.01
     #   if self.words[word].alpha == 0:
      #      prob = prior*exp(psi(self.syn_sem_top))/exp(psi(self.alpha_tot+self.syn_sem_top))
       #     pass
       # else:
       #     prob = exp(psi(self.words[word].alpha))/exp(psi(self.alpha_tot+self.syn_sem_top)) + prior*exp(psi(self.syn_sem_top))/exp(psi(self.alpha_tot+self.syn_sem_top))
        #if prob > 1.0:
            #print 'word prob over 1'
        #print "word prob for ",self.key+"-->"+word," = ",prob
        #return prob
       # return 10000

#    def update_bleurgh_alpha(self,update):
#        self.bleurgh_alpha_tot = self.bleurgh_alpha_tot+update
    
    def update_alpha(self,update):
        #print "alpha was ",self.alpha_tot
        #print "alpha update ",update
        self.alpha_tot += update
        #print "alpha now ",self.alpha_tot
        if self.alpha_tot<-1E-5:
            print "negative alpha for ",self.key
            error()
        
    def set_bleurgh_alpha(self):
        self.bleurgh_alpha_tot = self.alpha_tot

    def update_bottom(self,prob):
        self.bottom_term += prob
    def set_last_used(self,sentence_count):
        self.last_used = sentence_count
    def clear_probs(self):
        self.bottom_term = 0
    @staticmethod 
    def getPrior(e):
        pass
        
########################################
# lexicalised_syn is just used with    #
# lexicon to get p(sem|syn)               #
########################################
class lexicalised_syn:
    def __init__(self,syn_key,syn_top):
        self.alpha_o = syn_top
        self.alpha = 0.0
        self.alpha_top = 0.0
        self.syn_key = syn_key
        self.prob = 0
        self.extrascale = Lexicon.extrascale
        #self.semantics = {}

    """
    def check(self,sem_key,syn_sem):
        if not self.semantics.has_key(sem_key):
            self.semantics[sem_key] = syn_sem
        
    def log_prob_new_sem_given_syn(self,sem_store,sentence_count):
        Added by Omri 28/7.
        Returns the log probability of a new semantic key being generated from this 
        syntactic category, that is, without multiplying by the base distribution.
        if sentence_count != 0:
            scale = self.extrascale*sentence_count
        else:
            scale = 1.0
        scale = 1.0
        log_prob = psi(scale*self.alpha_o)-psi(scale*self.alpha_top+scale*self.alpha_o)
        return log_prob

    def update_bleurgh_alpha_top(self,alpha_top):
        self.bleurgh_alpha_top = self.bleurgh_alpha_top + alpha_top
        pass
    def set_bleurgh_alpha(self):
        self.bleurgh_alpha_top = self.alpha_top

    """

    def log_prob_sem_given_syn(self,sem_key,sem_store,sentence_count,verbose=False):
        log_prior = sem_store.get_log_prior(sem_key)
        #verbose = True
        if sentence_count != 0:
            scale = self.extrascale*sentence_count
        else:
            scale = 1.0
        scale = 1.0
        
        log_prob = log_prior + psi(scale*self.alpha_o)-psi(scale*self.alpha_top+scale*self.alpha_o)
        
        seen_log_prob = -inf
        if self.semantics.has_key(sem_key) and self.semantics[sem_key].alpha_tot > 0:
            seen_log_prob = psi(scale*self.semantics[sem_key].alpha_tot) - \
                psi(scale*self.alpha_top + scale*self.alpha_o)
        if seen_log_prob > 0:
            print "too much seen log prob for syn-> sem ",self.syn_key,"->",sem_key
            print "alpha is ",self.semantics[sem_key].alpha_tot
            print "alpha top is ",self.alpha_top
            print "alpha o is ",self.alpha_o
            print "scale is ",scale 
            seen_log_prob = 0.0
            #error()
            
        log_prob = log_sum(log_prob, seen_log_prob)
        return log_prob
      
        if verbose or log_prob>0:
            print "\nfor ",self.syn_key," - > ",sem_key
            print "alpha tot is ",self.semantics[sem_key].alpha_tot
            print "alpha top is ",self.alpha_top
            print "alpha o is ",self.alpha_o
          
            print "log prob is ",log_prob
            print "log prior is ",log_prior
            print "from base is ",log_prior + psi(self.alpha_o)-psi(self.alpha_top+self.alpha_o)
            print "from seen is ",seen_log_prob
            #if log_prob > 0.0: error()
            log_prob = 0
        
    
    def map_log_prob_sem_given_syn(self,sem_key,sem_store,sentence_count,verbose=False):
        log_prior = sem_store.get_log_prior(sem_key)
        #verbose = True
        if sentence_count != 0:
            scale = self.extrascale*sentence_count
        else:
            scale = 1.0
        scale = 1.0
        log_prob = log_prior + log(scale*self.alpha_o) - log(scale*self.alpha_top+scale*self.alpha_o)
        seen_log_prob = -inf
        if self.semantics.has_key(sem_key) and self.semantics[sem_key].alpha_tot > 0:
            seen_log_prob = log(scale*self.semantics[sem_key].alpha_tot) - log(scale*self.alpha_top + scale*self.alpha_o)
        if seen_log_prob > 0:
            print "too much seen log prob for syn-> sem ",self.syn_key,"->",sem_key
            print "alpha is ",self.semantics[sem_key].alpha_tot
            print "alpha top is ",self.alpha_top
            print "alpha o is ",self.alpha_o
            print "scale is ",scale 
            seen_log_prob = 0.0
        
        log_prob = log_sum(log_prob, seen_log_prob)
        
        if verbose or log_prob>0:
            print "\nfor ",self.syn_key," - > ",sem_key
            print "alpha tot is ",self.semantics[sem_key].alpha_tot
            print "alpha top is ",self.alpha_top
            print "alpha o is ",self.alpha_o
            
            print "log prob is ",log_prob
            print "log prior is ",log_prior
            print "from base is ",log_prior + log(self.alpha_o) - log(self.alpha_top+self.alpha_o)
            print "from seen is ",seen_log_prob
            #if log_prob > 0.0: error()
            log_prob = 0.0
        return log_prob
    
    def prob_sem_given_syn(self,sem_key,sem_store,verbose=False):
        return exp(self.log_prob_sem_given_syn(sem_key,sem_store,verbose))
    def map_prob_sem_given_syn(self,sem_key,sem_store,verbose=False):
        return exp(self.map_log_prob_sem_given_syn(sem_key,sem_store,verbose))  
        
        
    def update_p(self,prob):
        self.prob = self.prob + prob
        
        
    def update_alpha_top(self,alpha_top):
        verbose = False
        if verbose:
            print "alpha top is ",self.alpha_top
            print "updating by ",alpha_top
        self.alpha_top += alpha_top
        #print 
        if verbose:
            print "alpha top now is ",self.alpha_top
        if self.alpha_top<-1E-7:
            print "negative alpha for ",self.syn_key
            print self.alpha_top
            error()
        pass
    def clear_probs(self):
        self.prob = 0
        

        
    def get_sem_from_type_prob(self,sem_store,syn_key,lfType,posType,arity,varorder):
        typeDict = {}
        seensems = []
        for semKey in self.syntax[syn_key].semantics:
            if not sem_store.check(semKey):
                print "not got sem entry for ",semKey
            else:
                sem = sem_store.get(semKey)
                # print "sem is ",sem," from ",semKey
                # print "sem.type is ",sem.type(),sem.type().toString()
                # print "semtype is ",lfType
                if not sem.type().equals(lfType):
                    continue

                #print sem.getPosType()==posType
                #if not posType=="*" and not sem.getPosType()==posType: continue
                if not sem.getPosType()==posType: continue
                if not sem.arity() == arity: continue


                if not sem.hasVarOrder(varorder):
                    continue

                self.refresh_syn_sem_params(syn_key,semKey)        
                #print "sem is ",sem.toString(True)
                semProb = self.syntax[syn_key].map_prob_sem_given_syn(semKey,sem_store)
                vo = ""
                for v in varorder:
                    vo = vo+str(v)
                dictkey = (lfType,posType,arity,vo)
                if not typeDict.has_key(dictkey):
                    print "type dict not got ",sem.type().toString()
                    typeDict[dictkey] = 0.0
                #else:
                    #print "type dict got ",sem.type().toString()
                #print "adding semProb :",semProb," for ",syn_key," from ",sem.type().toString()," from ",sem.toString(True)
                typeDict[dictkey]+=semProb
                seensems.append((semKey,semProb))
                if typeDict[dictkey]>1:
#                    print "too much prob for ",sem.type().toString()," ",syn_key
#                    print dictkey
#                    print typeDict[dictkey]
#                    print seensems
#                    print "\n\n"
                    at = 0.0
                    for s in seensems:
#                        print "for ",s[0]," semprob is ",s[1]," alpha is ",self.syntax[syn_key].semantics[s[0]].alpha_tot
                        at+=self.syntax[syn_key].semantics[s[0]].alpha_tot
                        self.syntax[syn_key].map_prob_sem_given_syn(s[0],sem_store,True)
#                    print "at is ",at
#                    print "alpha top is ",self.syntax[syn_key].alpha_top
                if typeDict[dictkey]==0.0:
#                    print "\n\nzero prob for ",sem.type().toString()," ",syn_key
#                    print dictkey
#                    print typeDict[dictkey]
#                    print seensems
#                    print "\nseensems"
                    at = 0.0
                    for s in seensems:
#                        print "for ",s[0]," semprob is ",s[1]," alpha is ",self.syntax[syn_key].semantics[s[0]].alpha_tot
                        at+=self.syntax[syn_key].semantics[s[0]].alpha_tot
                        self.syntax[syn_key].map_prob_sem_given_syn(s[0],sem_store,True)
#                    print "at is ",at
#                    print "\nallsems"
                    at = 0.0
                    for s in self.syntax[syn_key].semantics:
#                        print "for ",s," semprob is ",s," alpha is ",self.syntax[syn_key].semantics[s].alpha_tot
                        at+=self.syntax[syn_key].semantics[s].alpha_tot
                        self.syntax[syn_key].map_prob_sem_given_syn(s,sem_store,True)
#                    print "at is ",at
#                    print "alpha top is ",self.syntax[syn_key].alpha_top
                    #error()
        totprob = 0.0

        for k in typeDict:
            totprob += typeDict[k]
        if totprob > 1.0:
            print "too much prob for ",syn_key
            print totprob
            print "\n\n"
            print typeDict
            #error()
        return typeDict


    def get_sem_type_probs(self,syn_key,sem_store):
        typeDict = {}
        at = 0.0
        for semKey in self.syntax[syn_key].semantics:
            if not sem_store.check(semKey):
                print "not got sem entry for ",semKey
            else:
                sem = sem_store.get(semKey)
                #print "sem is ",sem
                #print "sem is ",sem.toString(True)
                semType = sem_store.get(semKey).type().toString()
                semProb = self.syntax[syn_key].map_prob_sem_given_syn(semKey,sem_store)
                if not typeDict.has_key(semType):
                    #print "type dict not got ",semType
                    typeDict[semType] = 0.0
            #else:
                #print "type dict got ",semType
                typeDict[semType]+= self.syntax[syn_key].semantics[semKey].alpha_tot
                typeDict[semType]+= self.syntax[syn_key].semantics[semKey].alpha_tot
                at += self.syntax[syn_key].semantics[semKey].alpha_tot
        for t in typeDict:
            typeDict2 = {}  
            #typeDict2[t] = exp(psi(typeDict[t])-psi(at)) 
            typeDict2[t] = t/at
                #semProb
        return typeDict2
        
    def update_alphas(self):
        #for s in self.syn_sem:
            #prob = self.syn_sem[(syn_key,sem_key)].bottom_term/self.syntax[syn_key].prob_sem_given_syn
        for l in self.lex:
            word = l[0]
            syn_key = l[1]
            sem_key = l[2]
            # you need to check this to find out whether it's sensible
            # to go straight for p(w,sem,syn|inside_outside)
            if self.syntax[syn_key].prob > 0:
                prob = self.updateweight*self.lex[(word,syn_key,sem_key)].top_term/self.syntax[syn_key].prob #self.syn_sem[(syn_key,sem_key)].bottom_term
                self.lex[(word,syn_key,sem_key)].update_alpha(prob)
                self.syn_sem[(syn_key,sem_key)].update_alpha(prob)
                self.syntax[syn_key].update_alpha_top(prob)
