import numpy as np
import random
import sys
sys.path.append("V:/Critical-Services-Routing/src/Settings")
import Settings
sys.path.append("V:\Critical-Services-Routing\src\ChromsomeFunctions")
import ChromosomeBreakerRandom
sys.path.append("V:/Critical-Services-Routing/src/FitnessFunctions")
import Fitness

numRun = Settings.numRun



def main():
    brokenChromosomes = []
    nextPopulation = []
    original_chromosomes = []
    brokenChromosomes,original_chromosomes = ChromosomeBreakerRandom.getChromosome()
    calculatedTotalWaitBefore = []
    calculatedTotalWaitValue = []
    for i in range (100):
        pop_fitness = 0
        current_index = 0
        corresponding_index = 0
        percentGoOn = 0.2
        chromosome_probabilities = []
        if i == 0:
            calculatedChromosomes = Fitness.calculateTotalWaitTime(brokenChromosomes,original_chromosomes,calculatedTotalWaitBefore,calculatedTotalWaitValue)
            print(len(calculatedChromosomes))
        else:
            brokenChromosomes = []
            original_chromosomes = []
            print(nextPopulation)
            for j in range(len(nextPopulation)):
                original_chromosomes.append(nextPopulation[j])
                brokenChromosomes.append(ChromosomeBreakerRandom.breakChromosome(nextPopulation[j],1))
            calculatedChromosomes,calculatedTotalWaitBefore,calculatedTotalWaitValue = Fitness.calculateTotalWaitTime(brokenChromosomes,original_chromosomes,calculatedTotalWaitBefore,calculatedTotalWaitValue)
            print(calculatedChromosomes)
        bestPercentChromosome = []
        bestIndex = int(len(calculatedChromosomes) * percentGoOn)
        copyBestPercentChromosome = calculatedChromosomes[:bestIndex]
        print(bestIndex)
        swapIndexSorted = []

        for j in range(len(copyBestPercentChromosome)):
            pop_fitness += 1/copyBestPercentChromosome[j][0]

        for j in range(len(copyBestPercentChromosome)):
            chromosome_probabilities.append((1/copyBestPercentChromosome[j][0])/pop_fitness)

        for j in range(len(copyBestPercentChromosome)):
            bestPercentChromosome.append(copyBestPercentChromosome[j][1])

        copyBestPercentChromosome = bestPercentChromosome
        nextPopulation = bestPercentChromosome
        #print(nextPopulation)
        #print(len(bestPercentChromosome))
        #print(len(chromosome_probabilities))
        """
        if(copyBestPercentChromosome[0] == copyBestPercentChromosome[1]):
                print("same")
        else:
            print(bestPercentChromosome[0])
            print(bestPercentChromosome[1])
        """
        arrayBestPercentChromosome = np.array(bestPercentChromosome).astype(float)
        arrayChromosome_probabilities = np.array(chromosome_probabilities).astype(float)
        print(len(bestPercentChromosome))

        for j in range (len(calculatedChromosomes) - len(bestPercentChromosome)):
            swapIndex = []
            otherIndex = []
            tempChromosome = []
            randomPair = np.random.choice(len(arrayBestPercentChromosome),2, p = arrayChromosome_probabilities,replace=False)
            #print(randomPair)
            if(bestPercentChromosome[randomPair[0]]==bestPercentChromosome[randomPair[1]]):
                print("same")
            #print(bestPercentChromosome[randomPair[0]])
            #print(bestPercentChromosome[randomPair[1]])
            for k in range(len(bestPercentChromosome[randomPair[0]])):
                #print(randomPair)
                current_index = copyBestPercentChromosome[randomPair[0]][k]
                if current_index % 2 == 0:
                    if random.uniform(0,1) < 0.5:
                       #print(copyBestPercentChromosome[randomPair[0]][1])
                       #print(current_index)
                       #print(k)
                       #print(len(copyBestPercentChromosome[randomPair[0]]))
                       c = copyBestPercentChromosome[randomPair[0]].index(current_index+1)
                       swapIndex.append(current_index)
                       swapIndex.append(current_index+1)
                       #copyBestPercentChromosome[randomPair[0]][1][corresponding_index] = -1
                       #copyBestPercentChromosome[randomPair[0]][1][k] = -1

            #swapIndexSorted = [swapIndex[a] for a in sorted(range(len(bestPercentChromosome[randomPair[1]][1])), key=lambda k: bestPercentChromosome[randomPair[1]][1][k])]
            for k in range(len(bestPercentChromosome[randomPair[1]])):
                #print(k)
                current_index = copyBestPercentChromosome[randomPair[1]][k]
                #print(copyBestPercentChromosome[randomPair[1]][1])
                if current_index in swapIndex:
                    otherIndex.append(current_index)

            #print(otherIndex)
            #print(swapIndex)

            if(otherIndex == swapIndex):
                print("sameBOYO")

            count = 0
            for k in range(len(bestPercentChromosome[randomPair[0]])):
                current_index = copyBestPercentChromosome[randomPair[0]][k]

                if current_index in swapIndex :
                    #print(current_index)
                    #print(count)
                    count += 1
                    #print(len(otherIndex))
                    tempChromosome.append(otherIndex[0])
                    current_index = swapIndex[0]
                    #print(swapIndex[0])
                    #print(copyBestPercentChromosome[randomPair[0]][k])
                    otherIndex.pop(0)
                else:
                    tempChromosome.append(current_index)

            #all_numbers = set(range(200))
            #missing_numbers = all_numbers - set(tempChromosome)
            #print(sorted(list(missing_numbers)))
            if(tempChromosome == bestPercentChromosome[randomPair[0]]):
                print("same loloolol")
                #print(copyBestPercentChromosome[randomPair[0]])
                #print(bestPercentChromosome[randomPair[0]])
            #print(bestPercentChromosome[randomPair[0]])
            #print(copyBestPercentChromosome[randomPair[0]])
            #print (randomPair)
            #print(tempChromosome)
            nextPopulation.append(tempChromosome)
            #print(nextPopulation)

            copyBestPercentChromosome[randomPair[0]] = bestPercentChromosome[randomPair[0]]
        #print(copyBestPercentChromosome)
        #print(nextPopulation)


main()