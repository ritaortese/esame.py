#importo la funzione DATETIME per controllare la data
import datetime

#definisco la classe delle eccezioni che alzero'
class ExamException(Exception):
    pass

#definisco la classe genitore 
class CSVTimeSeriesFile():

    #istanzio classe con il nome del file 
    def __init__ (self,name):

        #faccio un eccezione con la quale controllo che il nome sia una stringa 
        if type(name) is not str:
            raise ExamException('ERRORE: il nome del file, "{}", non e- una stringa'.format(name))
        #inizializzo nome come oggetto
        self.name=name
        
    #controllo che l'elemento sia una data
    def validate(self, date):
        try:
            datetime.datetime.strptime(date, '%Y-%m')
            return True
        except ValueError:
            return False

    #definisco il metodo che torna una lista di liste con l'anno e il numero dei passeggeri
    def get_data (self):

        #creo la lista 
        my_list=[]

        #provo ad aprire il file, senno alzo un eccezione
        try:
            #provo a leggere e ad aprire il file,senno' alzo un'eccezione
            my_file=open(self.name,'r')
        except Exception :
            raise ExamException('ERRORE: impossibile aprire il file "{}"'.format(self.name))
        
        
        #se risco ad aprire il file inserisco i valori nella lista
        for line in my_file:

            #separo le stringhe con la virgola
            elements=(line.split(','))

            #schippo il primo elemento
            if elements[0]!='Date':

                #setto la data e il valore
                try:
                #setto la data
                    date=str(elements[0])

                    #controllo che il dato sia una data
                    if not self.validate(date):
                        continue

                except:
                    continue
                
                
                            
                try:    
                    #setto il valore dei passeggeri
                    value=int(elements[1])
                except ValueError:
                    continue
                    #controllo che il numero dei passeggeri sia positivo
                if value<0:
                        #se e' negativo, passo al prossimo
                    continue

                
                    
                  
            #controllo che la data non sia ripetuta e che le date siano in ordine crescente
            if len(my_list)>0:

                for item in my_list:
                    #creo una variabile temporanea
                    date_temp= item[0]
                    #controllo che la data non sia ripetuta, che timestamp non sia duplicato
                    if date==date_temp:
                        raise ExamException('ERRORE: la data "{}" viene ripetuta'.format(date))
                    #controllo che le date siano in ordine crescente, che timestamp sia in ordine crescente
                    if date<date_temp :
                        raise ExamException('ERRORE: le date all_interno del file non sono in ordine crescente') 

            #inserisco la data e il valore all'interno della mia lista
            my_list.append([date,value])
                
                    
        #chiudo il file
        my_file.close()

        #controllo che la lista non sia vuota
        if not my_list :
            raise ExamException('ERRORE: la lista "{}" e- vuota!'.format(my_list))
            
        #torno la lista
        return my_list

#definisco la funzione per la media dei valori
def compute_avg_monthly_difference(time_series, first_year,last_year):
    


    #controllo che i due anni inseriti dall'utente siano stringhe e siano presenti nel file
    #anno iniziale 
    if type(first_year)  is not str:
        raise ExamException('ERRORE: l_anno non e- una stringa ma e- "{}"'.format(type(first_year)))
    #anno finale
    if type(last_year)  is not str:
        raise ExamException('ERRORE: l_anno non e- una stringa ma e- "{}"'.format(type(last_year)))
    
    #controllo che i due anni siano presenti nel file
    if first_year<time_series[0][0][:4]:
        raise ExamException('ERRORE: l_anno "{}" inserito dall_utente non e- presente nella lista'.format(first_year))
    if last_year>time_series[-1][0][:4]:
        raise ExamException('ERRORE: l_anno "{}" inserito dall_utente non e- presente nella lista'.format(last_year))


    #controllo che i due anni non siano uguali
    if first_year==last_year:
        raise ExamException('ERRORE: gli anni inseriti dall_utente "{}", "{}" sono uguali'.format(first_year).format(last_year))

    #controllo che l'anno iniziale sia minore di quello finale
    if first_year>last_year:
        raise ExamException('ERRORE: il primo anno inserito dall_utente "{}" e- maggiore del secondo "{}"'.format(first_year).format(last_year))

    #controllo che la lista sia effettivamente una lista e non sia vuota
    if type(time_series) is not list:
        raise ExamException ('ERRORE: "{}" non e- una lista ma e- "{}"'.format(type(time_series)))
   

    #creo due liste, una per suddividere i valori degli anni richiesti dall'utente, l'altra per la lista finale
    
    lista_anni=[]
    lista_finale=[]
    
    #divido gli elementi all'interno della lista, cosi' da avere l'anno, il mese e il numero dei passeggeri separati
    for dati in time_series:
        data_raw=dati[0].split("-")
        year=data_raw[0]
        month=data_raw[1]
        value=dati[1]
        

        #se l'anno e' uguale a quello inserito dall'utente, non e' nullo e e' minore dell'anno massimo, creo una lista con i valori degli anni
        if(year>=first_year and year!=None and year<=last_year):                
            #itero il mese in un range di 12
            for i in range(12):
                
                #quando trovo lo stesso mese, aggiungo il numero dei passeggeri all'interno della lista
                #con la funzione zfill elimino lo zero del mese
                if (month==str(i+1) or month==str(i+1).zfill(2)):
                    
                    lista_anni.append(value)
                    
                #se il mese e' differente aggiungo 0 alla lista
                else:
                    if value==0 or value==None:
                        lista_anni.append(0)
            
     
        
    #divido la lunghezza della lista in 12 parti, sara' il numero degli anni e quindi il divisore della media 
    len_years=int(len(lista_anni)/12)
    
    
    for i in range(0,12):
        somma=0
        risultato=0
        #se ci sono solo due anni 
        if (len_years==2):
        #se un valore e' 0 la media in quel mese equivale a 0
            if lista_anni[i]==0 or lista_anni[i+12]==0:
                risultato=0
         
        else:   
            #cosi' faccio la sottrazione tra i valori dello stesso mese
            for b in range(1,len_years):
                #se l'intervallo degli anni e' maggiore di due, ma ci sono meno di due misurazioni per un mese, il risultato sara' Zero
                if (lista_anni[i+(12*b)]==0) or (lista_anni[i+12*(b-1)]==0):
                    risultato=0
                else:
                    #senno' faccio la media
                    somma1=(lista_anni[i+(12*b)]-lista_anni[i+12*(b-1)])
                    
                    somma+=somma1
                    risultato=somma/(len_years-1)
               
        lista_finale.append(risultato)

    #controllo che la lista finale non sia vuota
    if not lista_finale:
        raise ExamException('ERRORE: la lista finale"{} e- vuota'.format(lista_finale))
    
    return lista_finale




