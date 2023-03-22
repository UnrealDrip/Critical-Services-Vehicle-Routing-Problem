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
    for i in range (1000):
        pop_fitness = 0
        current_index = 0
        corresponding_index = 0
        percentGoOn = 0.2
        mutatePercent = 0.1
        mutateIndexPercent = 0.1
        chromosome_probabilities = []
        if i == 0:
            calculatedChromosomes = Fitness.calculateTotalWaitTime(brokenChromosomes,original_chromosomes)
            print(len(calculatedChromosomes))
            #print(calculatedChromosomes[0][0])
        else:
            brokenChromosomes = []
            original_chromosomes = []
            temp = calculatedChromosomes[:bestIndex]
            #print(temp)
            for j in range(len(nextPopulation)):
                original_chromosomes.append(nextPopulation[j])
                brokenChromosomes.append(ChromosomeBreakerRandom.breakChromosome(nextPopulation[j],1))
            calculatedChromosomes = []
            #print(len(brokenChromosomes),"brokenChromosomes")
            #print(nextPopulation)
            for j in range(len(temp)):
                calculatedChromosomes.append(temp[j])
            #print(len(calculatedChromosomes))
            temp = Fitness.calculateTotalWaitTime(brokenChromosomes,original_chromosomes)
            #print(temp)
            for j in range(len(temp)):
                calculatedChromosomes.append(temp[j])

            #print(len(calculatedChromosomes))
            calculatedChromosomes.sort(key=lambda x: x[0])
            print(i,calculatedChromosomes[0][0])
        bestPercentChromosome = []
        bestIndex = int(len(calculatedChromosomes) * percentGoOn)
        copyBestPercentChromosome = calculatedChromosomes[:bestIndex]
        swapIndexSorted = []

        for j in range(len(copyBestPercentChromosome)):
            pop_fitness += 1/copyBestPercentChromosome[j][0]

        for j in range(len(copyBestPercentChromosome)):
            chromosome_probabilities.append((1/copyBestPercentChromosome[j][0])/pop_fitness)

        for j in range(len(copyBestPercentChromosome)):
            bestPercentChromosome.append(copyBestPercentChromosome[j][1])

        copyBestPercentChromosome = bestPercentChromosome
        #print(len(calculatedChromosomes) - len(bestPercentChromosome))
        nextPopulation = []
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
            #print(swapIndexSorted)

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

        mutateNum = int(len(nextPopulation)*mutatePercent)
        randomChromosomes = random.sample(nextPopulation,mutateNum)
        mutatePopulation = randomChromosomes
        print(mutatePopulation)
        for j in range(len(mutatePopulation)):
            mutateChromosome = mutatePopulation[j]
            mutateIndexNum = int(len(mutateChromosome) * mutateIndexPercent)
            randomIndex = random.sample(mutateChromosome,int(mutateIndexNum/2))
            print(mutateChromosome)
            randomIndex2 = random.sample(mutateChromosome,int(mutateIndexNum/2))
            for i in range(len(randomIndex)):
                index1 = randomIndex[i]
                index_location = mutateChromosome.index(index1)
                corresponding_index = randomIndex[i]+1
                corresponding_index_location = mutateChromosome.index(corresponding_index)

                index2 = randomIndex2[i]
                index2_location = mutateChromosome.index(index2)
                corresponding_index2 = randomIndex2[i]+1
                corresponding_index2_location = mutateChromosome.index(corresponding_index2)

                if(index2 % 2 == 0 and index1 % 2 == 0):
                    if index2_location < corresponding_index_location and index_location < corresponding_index2_location:
                        mutateChromosome[index_location] = index2
                        mutateChromosome[index2_location] = index1
                        print("mutate",index2,index1)
                elif(index2 % 2 != 0 and index1 % 2 != 0):
                    if index2_location > corresponding_index_location and index_location > corresponding_index2_location:
                        mutateChromosome[index_location] = index2
                        mutateChromosome[index2_location] = index1
                        print("mutate",index2,index1)
                elif(index2 % 2 == 0 and index1 % 2 != 0):
                    if index2_location > corresponding_index_location and index_location < corresponding_index2_location:
                        mutateChromosome[index_location] = index2
                        mutateChromosome[index2_location] = index1
                        print("mutate",index2,index1)
                elif(index2 % 2 != 0 and index1 % 2 == 0):
                    if index2_location < corresponding_index_location and index_location > corresponding_index2_location:
                        mutateChromosome[index_location] = index2
                        mutateChromosome[index2_location] = index1
                        print("mutate",index2,index1)
                print(mutateChromosome)

        for j in range(len(nextPopulation)):
            if nextPopulation[j] in mutatePopulation:
                chromosome_index = mutatePopulation.index(nextPopulation[j])
                nextPopulation[j] = mutatePopulation[chromosome_index]
        #print(copyBestPercentChromosome)
        #print(len(nextPopulation),"nextPopulation")


main()