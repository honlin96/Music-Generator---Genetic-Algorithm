# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 12:01:17 2018

@author: honlin
"""
import xlrd 
import random
import pyglet 
import time
import matplotlib.pyplot as plt
import math
import pickle
data = xlrd.open_workbook("Music database.xlsx").sheet_by_index(0)
note_database = []
rhythm_database = []

##############################################################################
#Define a new class individual. Individual contains the information about the
#fitness of the chromosome
class Individual:
    global score_list
    bestChromosome = None
    bestFitness = 0
    def __init__(self, chromosome):
        self.chromosome = chromosome
    #compute fitness based on different fitness functions
        #f5 = chromatic_circle_fitness(chromosome)
        # f3 = similarity_fitness(chromosome)
        #f2 = octave_fitness(chromosome)
        f3 = fractal_fitness(chromosome)
        #f4 = circle_progression_fitness(chromosome)
        fitness = f3
        self.fitness = fitness
        #find the best fitness and best chromosome
        if fitness > Individual.bestFitness:
           Individual.bestChromosome = chromosome
           Individual.bestFitness = fitness
    def getFitness (self):
        return self.fitness
    def getChromosome (self):
        return self.chromosome
    def setChromosome(self, newChrom):
        self.chromosome = newChrom
        
class RIndividual:
    #if the chromosome is a rhythm chromosome:
    global r_score_list  
    bestChromosome = None
    bestFitness = 0
    def __init__(self, chromosome):
        self.chromosome = chromosome     
        # fitness = rhythm_beat_fitness(chromosome)
        #f3 = fractal_fitness(chromosome)
        #f1 = rhythm_beat_fitness(chromosome)
        #f2 = rhythm_complex_fitness(chromosome)
        # fitness = rhythm_simple_fitness(chromosome)
        fitness = fractal_fitness(chromosome)
        self.fitness = fitness
        #find the best fitness and best chromosome
        if fitness > RIndividual.bestFitness:
           RIndividual.bestChromosome = chromosome
           RIndividual.bestFitness = fitness
    def getFitness (self):
        return self.fitness
    def getChromosome (self):
        return self.chromosome
    def setChromosome(self, newChrom):
        self.chromosome = newChrom

#--------------------create data base-----------------------#   
def createNoteDatabase(startDatabase, endDatabase,sampleSize):
     #open the database file
    data = xlrd.open_workbook("Music database.xlsx").sheet_by_index(0)
    #create empty note_database
    note_database = []
    for i in range (0, sampleSize):
        note_database.append([])
    #notes
    counter = 0
    for column in range (startDatabase, endDatabase, 3):
        #find number of rows in each column
        rowSize = 0
        i = 0
        while (i < data.nrows and data.cell(i, column).value != ''):
            rowSize = rowSize + 1
            i = i + 1
        for row in range (2, rowSize):
           #save note_data
            note_database[counter].append(notes_numbs(row,column))   
        counter = counter + 1
    return note_database

def notes_numbs(row, column):
    global data
    switcher = {
        "0": 0,
        "A3": 1,
        "A3#": 2,
        "B3": 3,
        "C3": 4,
        "C3#": 5,
        "D3": 6,
        "D3#": 7,
        "E3": 8,
        "F3": 9,
        "F3#": 10,
        "G3": 11,
        "G3#": 12,
        "A4": 13,
        "A4#": 14,
        "B4": 15,
        "C4": 16,
        "C4#": 17,
        "D4": 18,
        "D4#": 19,
        "E4": 20,
        "F4": 21,
        "F4#": 22,
        "G4": 23,
        "G4#": 24,
        
    }
    return switcher.get(str(data.cell(row, column).value), 0)

def switcherRhythm(beat):
    #convert the integer to the respective time duration
    switcher = {
        0: 0.75,
        1: 0.25,
        2: 0.5,
        3: 1,
        4: 1.5,
        5: 2,
        6: 3,
        7: 4
    }
    return switcher[beat]

def modifysize(note_list,length):
    #this function change the length of the note_list to the desire length
    list_length = len(note_list)
    modified_list = note_list
    if list_length < length:
    #if the list is too short, append
        while len(note_list) < length:
            #append the list until the length of the list is longer or equal to the 
            #desired length
            note_list.extend(modified_list)
        note_list = note_list[:length]
        return note_list
    elif list_length > length:
        #if the list is too long, trim it to match the desire length
        note_list = note_list[:length]
        return note_list
    else:
        #if equal length, do nothing
        return note_list

def createRhythmDatabase(startDatabase, endDatabase,sampleSize):
    data = xlrd.open_workbook("Music database.xlsx").sheet_by_index(0)
    #rhythm
    rhythm_database = []
    for i in range(0,sampleSize):
        rhythm_database.append([])
    counter = 0
    for column in range (startDatabase + 1, endDatabase, 3):
        #find number of rows in each column
        rowSize = 0
        i = 0
        while (i < data.nrows and data.cell(i, column).value != ''):                
            rowSize = rowSize + 1
            i = i + 1
                
        for row in range (2, rowSize):
           #save rhythm_data
            rhythm = int(data.cell(row, column).value)
            rhythm_database[counter].append(rhythm)
            

        counter = counter + 1
    return rhythm_database

#--------------------Create score list for fitness ------------------#       
def note_score_list(note_database):
    #This function takes note_database as input, compute the occurence of the
    #notes in each position, and output the score list. 
    global score_list
    score_list = [] 
    counter = 0
    notes_numbs = len(note_database[0])
    for i in range(0,notes_numbs):
        #create a list which will store the score for the 13 notes
        mini_score = []
        for element in range(0,25):
            mini_score.append(0)
        #loop through the song lists
        for j in note_database: 
            for k in range(0, 25):
                #register each note to the right entry in miniscore.
                if j[counter] == k:
                    mini_score[k] = mini_score[k] + 1
        # normalise the score
        mini_score[:] = [x/25 for x in mini_score]
        score_list.append(mini_score)
        counter = counter + 1

def rhythm_score_list(rhythm_database):
    global r_score_list
    r_score_list = []
    counter = 0
    rhythm_numbs = len(rhythm_database[0])
    for i in range(0,rhythm_numbs):
        #create a list which will store the score for the 8 rhythm
        mini_score = []
        for element in range(0,8):
            mini_score.append(0)
        #loop through the song list
        for j in rhythm_database: 
            for k in range(0, 8):
                #register each rhythm to the right entry in miniscore.
                if j[counter] == k:
                    mini_score[k] = mini_score[k] + 1
        # normalise the score
        mini_score[:] = [x/8 for x in mini_score]
        r_score_list.append(mini_score)
        counter = counter + 1

#--------------------fitness function------------------------#
def similarity_fitness(chromosome):
    #similarity_fitness compares each note with the notes occurence in the 
    #database, the more frequenct the note appears in the database, the higher
    #the score
    fitness = 0
    for i in range(0, len(chromosome)):
        #compare each value to the modified_database
        fitness = chromosome[i]* score_list[i][chromosome[i]] + fitness            
        # normalise the fitness score
    fitness = fitness/ len(chromosome)
    return fitness

def chromatic_circle_fitness(chromosome):
    #chromatic_circle_fitness assign scores to the repeated patterns, if next tone
    # is just a tone higher or lower than the previous note, it will be given more points
    fitness = 0
    previous_note = chromosome[0]
    score = 0
    for i in range(1, len(chromosome)):
        difference = abs(chromosome[i] - previous_note)
        if  difference < 4:
           score = score + 1
        elif difference > 4 and difference < 8:
            score = score + 0.5
        previous_note = chromosome[i]
    #normalise the score to return fitness
    fitness = score/(len(chromosome)-1)
    return fitness

def octave_fitness(chromosome):
    #octave fitness gives point if the notes are within the octave
    fitness = 0
    score = 0
    for i in range(1,len(chromosome)):
        difference = abs(chromosome[i] - chromosome[0])
        if difference < 12:
           if  difference < 6:
               score = score + 1
        elif difference > 6 and difference < 12:
             score = score + 0.5
        else :
            score = score + 0.2
    #normalise the score
    fitness = score/(len(chromosome)-1)
    return fitness

def circle_progression_fitness(chromosome):
    #circle progression fitness gives higher score if the notes follow the
    #circle progression (6-2-5-1)
    fitness = 0
    score = 0
    for i in range(4,len(chromosome)):
        note0 = chromosome[i-4]
        note1 = chromosome[i-3]
        note2 = chromosome[i-2]
        note3 = chromosome[i-1]
        difference0 = note1 - note0
        difference1 = note2 - note1
        difference3 = note3 - note2
        difference4 = chromosome[i] - note3
        if difference0 == 6 and difference1 == 2 and difference3 == 5 and difference4 ==1:
           score = score + 1
        elif difference0 == -6 and difference1 == -2 and difference3 == -5 and difference4 ==-1:
           score = score + 1
    return fitness

def rhythm_simple_fitness(chromosome):
    #calculate the beat, if the beat is not a simple triple
    #fitness should be lower
    time = 0
    time_score = 0
    counter = 0
    similarity_score = 0
    for i in range(0,len(chromosome)):
        similarity_score= chromosome[i]*r_score_list[i][chromosome[i]] + similarity_score
        time = time + switcherRhythm(chromosome[i])
        if time > 4:
           time = switcherRhythm(chromosome[i])
           time_score = time_score - 1
           counter = counter + 1
        elif time == 4:
           time_score = 1 + time_score
           time = 0
           counter = counter + 1
    if time_score < 0:
       time_score = 0
        #normalise 
    similarity_score = similarity_score/len(chromosome)
    fitness = 0.5*similarity_score + 0.5*(time_score/counter) 
    return fitness

def rhythm_beat_fitness(chromosome):
    # repeating beat should be given higher score
    # time_signature : 4/4:4 , 3/4:3 , 2/4:2, 1/4:1
    time_signature = 4;
    beat_list = []
    beat = []
    time = 0
    total_score = 0
    beat_score = 0
    counter = 0
    for i in range(0,len(chromosome)):
        time = time + switcherRhythm(chromosome[i])
        if time < time_signature:
           beat.append(chromosome[i]) 
        elif time > time_signature:
            beat = []
            time = 0
            counter = counter + 1
        elif time == time_signature:
            beat.append(chromosome[i])
            time = 0 
            total_score = total_score + 0.5
            counter = counter + 1
            #check if the beat has been repeated, if yes, then score +1
            for j in beat_list:
                if len(beat) == len(j):
                    for k in range(len(beat)):
                        #stop checking if there is difference
                        if beat[k] != j[k]:
                           beat_score = 0
                           break
                        else:
                            beat_score = beat_score + 1
                    #normalise beat score
                beat_score = beat_score/len(beat)
                #stop checking if we have found a similar beat
                if beat_score == 1:
                   break
            if beat_score == 1:
               total_score = 0.5*beat_score + total_score
            else:
                beat_list.append(beat)
            beat_score = 0
    fitness = total_score/counter
    return  fitness

def rhythm_complex_fitness(chromosome):
    # repeating beat should be given higher score, a bar should contain more than 1 note
    # time_signature : 4/4:4 , 3/4:3 , 2/4:2, 1/4:1
    time_signature = 4;
    beat_list = []
    beat = []
    time = 0
    total_score = 0
    beat_score = 0
    counter = 0
    for i in range(0,len(chromosome)):
        time = time + switcherRhythm(chromosome[i])
        if time < time_signature:
            beat.append(chromosome[i])
        elif time > time_signature:
            beat = []
            time = 0
            counter = counter + 1
        elif time == time_signature:
            beat.append(chromosome[i])
            time = 0
            if len(beat) == 1:
                total_score = 0
            else:
                total_score = total_score + 0.5
            counter = counter + 1
            #check if the beat has been repeated, if yes, then score +1
            for j in beat_list:
                if len(beat) == len(j):
                    for k in range(len(beat)):
                        #stop checking if there is difference
                        if beat[k] != j[k]:
                            beat_score = 0
                            break
                        else:
                            beat_score = beat_score + 1
                #normalise beat score
                beat_score = beat_score/len(beat)
                #stop checking if we have found a similar beat
                if beat_score == 1:
                    break
                if beat_score == 1:
                    total_score = 0.5*beat_score + total_score
                else:
                    beat_list.append(beat)
            beat_score = 0
    fitness = total_score/counter
    return  fitness

def fractal_fitness(chromosome):
    #Treat note/rhythm as a Cantor set. Calculate the similarity for S1, S2, and S3
    #S0 is the whole chromosome
    cover_size = 0.2
    element_length = (1-cover_size)/2 
    #start our construction of Cantor set
    #first set, take the floor
    L1_size = math.ceil(element_length*len(chromosome))
    L10 = chromosome[0:L1_size]
    L11 = chromosome[len(chromosome)-L1_size: len(chromosome)]
    #compare their similarity
    scoreS1 = 0 
    for i in range(0,L1_size):
        if L10[i] == L11[i]:
           scoreS1 = scoreS1 + 1
    #normalise the score
    scoreS1 = scoreS1/L1_size
    #2nd set
    scoreS2 = 0
    L2_size = math.ceil(element_length*element_length*len(chromosome))
    L20 = chromosome[0:L2_size]
    L21 = chromosome[L1_size - L2_size:L1_size]
    L22 = chromosome[len(chromosome)-L1_size:len(chromosome)-L1_size+ L2_size]
    L23 = chromosome[len(chromosome)-L2_size:len(chromosome)]
    for i in range(0,L2_size):
        if L20[i] == L21[i]:
           scoreS2 = scoreS2 + 1
        if L22[i] == L23[i]:
           scoreS2 = scoreS2 + 1
    #normalise the score
    scoreS2 = scoreS2/(2*L2_size)
    #3rd set
    scoreS3 = 0
    L3_size = math.ceil(element_length*element_length*element_length*len(chromosome))
    L30 = chromosome[0:L3_size]
    L31 = chromosome[L2_size - L3_size:L2_size]
    L32 = chromosome[L1_size -L2_size: L1_size-L2_size+L3_size]
    L33 = chromosome[L1_size-L3_size:L1_size]
    L34 = chromosome[len(chromosome)-L1_size:len(chromosome)-L1_size+L3_size]
    L35 = chromosome[len(chromosome)-L1_size+ L2_size - L3_size: len(chromosome)-L1_size+ L2_size]
    L36 = chromosome[len(chromosome)-L2_size - L3_size: len(chromosome)-L2_size]
    L37 = chromosome[len(chromosome)-L3_size: len(chromosome)]
    for i in range(0,L3_size):
        if L30[i] == L31[i]:
           scoreS3 = scoreS3 + 1
        if L32[i] == L33[i]:
           scoreS3 = scoreS3 + 1
        if L34[i] == L35[i]:
           scoreS3 = scoreS3 + 1
        if L36[i] == L37[i]:
           scoreS3 = scoreS3 + 1
    #normalise the score
    scoreS3 = scoreS3/(4*L3_size)
    fitness = 0.5*scoreS1 + 0.3*scoreS2 + 0.2*scoreS3
    return fitness 


#-----------------genetic algorithm function------------------#
def randomChrom(length):
    #This function randomly generate a note chromosome of length l
    chrom = []
    for i in range (0, length):
        chrom.append(random.randint(0, 24)) #Generate random integer from 0 to 12
    return chrom

def randomRChrom(length):
    # This function randomly generate a rhythm chromosome of length L
    Rchrom = []
    for i in range(0,length):
        Rchrom.append(random.randint(0,7))
    return Rchrom

def createNoteNextGen(generation,mutationRate,crossoverRate):
    newGen = []
    gen_size = len(generation)
    # pchro is the paired chromosome and pchro_foit corresponded to it fitness.
    pchro = []
    pchro_fit = []
    
    # pair up all the chromosome
    for i in range(gen_size):
        for j in range(gen_size):
            if j>i:
                pchro.append([generation[i],generation[j]])
                pchro_fit.append([generation[i].getFitness() 
                                        + generation[j].getFitness()])
    
    # start to sort the chromosome according to it fitness in accending order.
    sorted_pchro_fit = sorted(pchro_fit, reverse=True)
    sorted_pchro = []
    len_pchro = len(pchro)
    
    # i is for sorted pchro
    for i in range(len_pchro):
        for j in range(len_pchro):
            if sorted_pchro_fit[i] == pchro_fit[j]:
                sorted_pchro.append(pchro[j])
                # pchro_fit[j] = 0
                break
    
    # create new generation
    for i in range(0,int(gen_size / 2)):
        # x = random.randint(1,len(sorted_pchro)-1)
        newChromosomes = crossover(sorted_pchro[i],crossoverRate)
        newGen.append(Individual(newChromosomes[0]))
        newGen.append(Individual(newChromosomes[1]))
        
    newGen = mutation(newGen, mutationRate)
    return newGen
        
def savechromosome(basic_chromosome):
    with open("basic_chromosome.txt", "wb") as fp:
        pickle.dump(basic_chromosome, fp)
        
def loadchromosome():
    with open("basic_chromosome.txt", "rb") as fp:
        basic_chromosome = pickle.load(fp)
        
    return basic_chromosome
    

def createRhythmNextGen(generation,mutationRate,crossoverRate):
    newGen = []
    gen_size = len(generation)
    # pchro is the paired chromosome and pchro_foit corresponded to it fitness.
    pchro = []
    pchro_fit = []
    
    # pair up all the chromosome
    for i in range(gen_size):
        for j in range(gen_size):
            if j>i:
                pchro.append([generation[i],generation[j]])
                pchro_fit.append([generation[i].getFitness() 
                                        + generation[j].getFitness()])
    
    # start to sort the chromosome according to it fitness in accending order.
    sorted_pchro_fit = sorted(pchro_fit, reverse=True)
    sorted_pchro = []
    len_pchro = len(pchro)
    
    # i is for sorted pchro
    for i in range(len_pchro):
        for j in range(len_pchro):
            if sorted_pchro_fit[i] == pchro_fit[j]:
                sorted_pchro.append(pchro[j])
                # pchro_fit[j] = 0
                break
    
    # create new generation
    for i in range(0,int(gen_size / 2)):
        # x = random.randint(1,len(sorted_pchro)-1)
        newChromosomes = crossover(sorted_pchro[i],crossoverRate)
        newGen.append(RIndividual(newChromosomes[0]))
        newGen.append(RIndividual(newChromosomes[1]))
        
    newGen = Rmutation(newGen, mutationRate)
    return newGen
        

def crossover(individuals,crossoverRate):
    #input: list of two Individuals to cross
    if random.random() > crossoverRate:
        return [individuals[0].getChromosome(), individuals[1].getChromosome()]
    length = len(individuals[0].getChromosome())
    splitpoint = int(length/2)
    return [individuals[0].getChromosome()[:splitpoint]+individuals[1].getChromosome()[splitpoint:],
            individuals[1].getChromosome()[:splitpoint]+individuals[0].getChromosome()[splitpoint:]]
    
def mutation(gen, mutationRate):
    #input: generation list of individuals of size genSize
    #for each individual
    for ind in gen:
        #for each index in the chromosome
        newChrom = ind.getChromosome()
        for i in range(0, len(newChrom)):
            if random.random() < mutationRate:
                #mutate
                newChrom[i] = random.randint(0, 12)
        ind.setChromosome(newChrom)
    return gen    

def Rmutation(gen, mutationRate):
    #input: generation list of individuals of size genSize
    #for each individual
    for ind in gen:
        #for each index in the chromosome
        newChrom = ind.getChromosome()
        for i in range(0, len(newChrom)):
            if random.random() < mutationRate:
                #mutate
                newChrom[i] = random.randint(0, 7)
        ind.setChromosome(newChrom)
    return gen    
#----------------PLAY BACK MUSIC--------------------#
def getRhythm(rhythm_database,length):
    rhythm = []
    for beat in rhythm_database:
        rhythm = beat + rhythm #concatenate the beat
    rhythm = rhythm[:length]
    return rhythm
           
def playMusic(song, rhythm):
    pyglet.options['audio'] = ('openal', 'silent')
    switcherNotes = {
        1: "A3.wav", 
        2: "A3#.wav",
        3: "B3.wav",
        4: "C3.wav",
        5: "C3#.wav",
        6: "D3.wav",
        7: "D3#.wav",
        8: "E3.wav",
        9: "F3.wav",
        10: "F3#.wav",
        11: "G3.wav",
        12: "G3#.wav",
        13: "A4.wav", 
        14: "A4#.wav",
        15: "B4.wav",
        16: "C4.wav",
        17: "C4#.wav",
        18: "D4.wav",
        19: "D4#.wav",
        20: "E4.wav",
        21: "F4.wav",
        22: "F4#.wav",
        23: "G4.wav",
        24: "G4#.wav"
    }
    switcherRhythms = {
        0: 0.75,
        1: 0.25,
        2: 0.5,
        3: 1,
        4: 1.5,
        5: 2,
        6: 3,
        7: 4
    }
    for i in range(0, len(song)):
        totalTime = 0
        while(totalTime < switcherRhythms[rhythm[i]]):
            if song[i] != 0:
                music = pyglet.media.load(switcherNotes[song[i]], streaming=False)
                music.play()
            time.sleep(switcherRhythms[rhythm[i]]*.3)
            totalTime += switcherRhythms[rhythm[i]]

#############################################################################
#--------------Parameter----------------------#
startDatabase = 3 
endDatabase = 14 #
sampleSize = 4
length = 50 #length of the modified note_database list. 
num_chromosome = 10 #number of chromosomes 
gen_size = 10
mutationRate = 0.05
crossoverRate = 0.8
iteration = 500
use_old_chromosme = True # Set it True if want to reuse it
use_database = True

#-----------------Initialization------------------------#
#setup note_database and rhythm database
if use_database == True:
    note_database   = createNoteDatabase(startDatabase, endDatabase,sampleSize)
    rhythm_database = createRhythmDatabase(startDatabase, endDatabase,sampleSize)
    
    counter = 0
    for song in note_database:
        note_database[counter] = modifysize(song,length)
        counter += 1
        
    counter = 0
    for song in rhythm_database:
        rhythm_database[counter] = modifysize(song,length)
        counter += 1
    #Create a score list
    note_score_list(note_database)
    rhythm_score_list(rhythm_database)

#---------------Genetic Algorithm----------------------#
if use_old_chromosme == False:
    NoteGeneration = []
    RhythmGeneration = []
    basic_chromosome = [[],[]]
    #generation 0: all random lists of chromosomes
    
    # save the chromosome into txt file
    for i in range (0, gen_size):
        note = randomChrom(length)
        rhythm = randomRChrom(length)
        NoteGeneration.append(Individual(note))
        RhythmGeneration.append(RIndividual(rhythm))
        
        basic_chromosome[0].append([])
        basic_chromosome[1].append([])
        for j in range(len(note)):
            basic_chromosome[0][-1].append(note[j])
            basic_chromosome[1][-1].append(rhythm[j])
        
    savechromosome(basic_chromosome)
    
else:
    # load pervious run chromosome
    basic_chromosome = loadchromosome()
    NoteGeneration = []
    RhythmGeneration = []
    tem_Nchro = []
    tem_Rchro = []
    for i in range(len(basic_chromosome[0])):
        NoteGeneration.append(Individual(basic_chromosome[0][i]))
        RhythmGeneration.append(RIndividual(basic_chromosome[1][i]))
    
    
#create a list to store the best note chromosome and fitness in every generation
best_note_chromosome = [[]]
best_note_fitness = []
#create a list to store the best rhythm chromosome and fitness in every generation
best_rhythm_chromosome = [[]]
best_rhythm_fitness = []

for j in range(len(NoteGeneration[0].bestChromosome)):
    best_note_chromosome[-1].append(NoteGeneration[0].bestChromosome[j])        
    best_rhythm_chromosome[-1].append(RhythmGeneration[0].bestChromosome[j])

best_note_fitness.append(NoteGeneration[0].bestFitness)
best_rhythm_fitness.append(RhythmGeneration[0].bestFitness)

# record note and rhythm fitness for every iteration
N_fitness = []
R_fitness = []
Note_best_fitness = 0
rhythm_best_fitness = 0

#generation n
for i in range (1,iteration):
    NoteGeneration = createNoteNextGen(NoteGeneration, mutationRate,crossoverRate)
    RhythmGeneration = createRhythmNextGen(RhythmGeneration,mutationRate,crossoverRate)
    best_note_chromosome.append([])
    best_rhythm_chromosome.append([])
    
    for j in range(len(NoteGeneration[0].bestChromosome)):
        best_note_chromosome[-1].append(NoteGeneration[0].bestChromosome[j])        
        best_rhythm_chromosome[-1].append(RhythmGeneration[0].bestChromosome[j])
    
    best_note_fitness.append(NoteGeneration[0].bestFitness)
    best_rhythm_fitness.append(RhythmGeneration[0].bestFitness)
    
    for ind in NoteGeneration:
        if ind.fitness > Note_best_fitness:
            bestNf = ind.fitness
    
    for ind in RhythmGeneration:
        if ind.fitness > rhythm_best_fitness:
            bestRf = ind.fitness

    N_fitness.append(bestNf)
    R_fitness.append(bestRf)
    Note_best_fitness = 0    
    rhythm_best_fitness = 0

N_performance = []
R_performance = []
# find difference between local and global fitness for note
for i in range(len(N_fitness)):
    N_performance.append(N_fitness[i]- best_note_fitness[i])

# find difference between local and global fitness for note
for i in range(len(R_fitness)):
    R_performance.append(R_fitness[i]- best_rhythm_fitness[i])


savefitness = False
if savefitness == True:
    local_fitness = [[],[]]
    for i in range(len(N_fitness)):
        local_fitness[0].append(N_fitness[i])
        local_fitness[1].append(R_fitness[i])
    
    with open("local_fitness", "wb") as fp:
        pickle.dump(local_fitness, fp)
else:
    with open("local_fitness", "rb") as fp:
        pervious_fitness = pickle.load(fp)
        local_fitness = [[],[]]
        for i in range(len(pervious_fitness[0])):
            local_fitness[0].append(pervious_fitness[0][i])
            local_fitness[1].append(pervious_fitness[1][i])

    N_difference = []
    R_difference = []

    # difference between N(n+1) and N(n)
    for i in range(len(N_fitness)):
        N_diff = N_fitness[i] - local_fitness[0][i]
        if N_diff == 0:
            N_difference.append(0)
        else:
            N_difference.append(math.log(abs(N_diff)))    
        
    # difference between R(n+1) and R(n)
    for i in range(len(R_fitness)):
        R_diff = R_fitness[i] - local_fitness[1][i]
        if R_diff == 0:
            R_difference.append(0)
        else:
            R_difference.append(math.log(abs(R_diff)))


#--------------Analysis----------------------------#
#plot note fitness against generation graph
x = range(0,iteration)
'''
print('\n\n Global best fitness in every iteraion')
# plot note fitness against generation graph
plt.plot(x,best_note_fitness)
plt.title('Global Best Note fitness in every Iteration')
plt.xlabel('Iteration')
plt.ylabel('Global Best fitness')
plt.show()

#plot rhythm fitness against generation graph
plt.plot(x,best_rhythm_fitness)
plt.title('Best Rhythm fitness in every Iteration')
plt.xlabel('Iteration')
plt.ylabel('Local Best fitness')
plt.show()
'''
print('\n\n Local best fitness in every iteraion')
# plot note fitness against generation graph
plt.plot(x[1:len(x)],N_fitness)
plt.title('Local Best Note fitness in every Iteration')
plt.xlabel('Iteration')
plt.ylabel('Local Best fitness')
plt.show()

#plot rhythm fitness against generation graph
plt.plot(x[1:len(x)],R_fitness)
plt.title('Local Best Rhythm fitness in every Iteration')
plt.xlabel('Iteration')
plt.ylabel('Local Best fitness')
plt.show()

'''
print('\n\n Lorentz map')
# N(n+1) versus N(n)
plt.plot(N_fitness[0:len(N_fitness)-1],N_fitness[1:len(N_fitness)],'r.')
plt.title('Local Best Note fitness: N(n+1) versus N(n)')
plt.xlabel('N(n)')
plt.ylabel('N(n+1)')
plt.show()

# R(n+1) versus R(n)
plt.plot(R_fitness[0:len(R_fitness)-1],R_fitness[1:len(R_fitness)],'r.')
plt.title('Local Best Rhythm fitness: R(n+1) versus R(n)')
plt.xlabel('R(n)')
plt.ylabel('R(n+1)')
plt.show()
'''

print('\n\n ln(\delta) versus iteration')
# difference between N(n+1) and N(n) and plot it versus iteration
plt.plot(x[1:len(x)],N_difference)
plt.title('ln(N(n+1)- N(n)) versus iteration')
plt.xlabel('Iteration')
plt.ylabel('ln(N(n+1)- N(n))')
plt.show()

# difference between N(n+1) and N(n) and plot it versus iteration
plt.plot(x[1:len(x)],R_difference)
plt.title('ln(R(n+1)- R(n)) versus iteration')
plt.xlabel('Iteration')
plt.ylabel('ln(R(n+1)- R(n))')
plt.show()

'''
print('\n\n Difference between local and global fitness')
# compare local best fitness of note of each iteration to global best
plt.plot(x[1:len(x)],N_performance)
plt.title('Note Performance versus Iteration')
plt.xlabel('Iteration')
plt.ylabel('Note Performance')
plt.show()

# compare local best fitness of Rhythm of each iteration to global best
plt.plot(x[1:len(x)],R_performance)
plt.title('Rhythm Performance versus Iteration')
plt.xlabel('Iteration')
plt.ylabel('Rhythm Performance')
plt.show()
'''
'''
#-------------Play Music-----------------------------#
# rhythm = getRhythm(rhythm_database[5],length)
# playMusic(best_note_chromosome[-1],best_rhythm_chromosome[-1]) #play the best music
playMusic(note_database[0],rhythm_database[0])
'''
