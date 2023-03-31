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
    for i in range (100):
        pop_fitness = 0
        current_index = 0
        corresponding_index = 0
        percentGoOn = 0.2
        mutatePercent = 0.1
        mutateIndexPercent = 0.1
        chromosome_probabilities = []
        if i == 0:
            calculatedChromosomes = Fitness.calculateTotalWaitTime(brokenChromosomes,original_chromosomes)
            print(calculatedChromosomes[0][0])
        else:
            brokenChromosomes = []
            original_chromosomes = []
            temp = calculatedChromosomes[:bestIndex]
            for j in range(len(nextPopulation)):
                original_chromosomes.append(nextPopulation[j])
                brokenChromosomes.append(ChromosomeBreakerRandom.breakChromosome(nextPopulation[j],1))
            calculatedChromosomes = []

            for j in range(len(temp)):
                calculatedChromosomes.append(temp[j])

            temp = Fitness.calculateTotalWaitTime(brokenChromosomes,original_chromosomes)

            for j in range(len(temp)):
                calculatedChromosomes.append(temp[j])


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

        nextPopulation = []

        arrayBestPercentChromosome = np.array(bestPercentChromosome).astype(float)
        arrayChromosome_probabilities = np.array(chromosome_probabilities).astype(float)

        for j in range (len(calculatedChromosomes) - len(bestPercentChromosome)):
            swapIndex = []
            otherIndex = []
            tempChromosome = []
            randomPair = np.random.choice(len(arrayBestPercentChromosome),2, p = arrayChromosome_probabilities,replace=False)

            if(bestPercentChromosome[randomPair[0]]==bestPercentChromosome[randomPair[1]]):
                print("same")

            for k in range(len(bestPercentChromosome[randomPair[0]])):

                current_index = copyBestPercentChromosome[randomPair[0]][k]
                if current_index % 2 == 0:
                    if random.uniform(0,1) < 0.5:

                       c = copyBestPercentChromosome[randomPair[0]].index(current_index+1)
                       swapIndex.append(current_index)
                       swapIndex.append(current_index+1)

            for k in range(len(bestPercentChromosome[randomPair[1]])):
                current_index = copyBestPercentChromosome[randomPair[1]][k]

                if current_index in swapIndex:
                    otherIndex.append(current_index)

            if(otherIndex == swapIndex):
                print("sameBOYO")

            count = 0
            for k in range(len(bestPercentChromosome[randomPair[0]])):
                current_index = copyBestPercentChromosome[randomPair[0]][k]

                if current_index in swapIndex :

                    count += 1

                    tempChromosome.append(otherIndex[0])
                    current_index = swapIndex[0]

                    otherIndex.pop(0)
                else:
                    tempChromosome.append(current_index)

            if(tempChromosome == bestPercentChromosome[randomPair[0]]):
                print("same loloolol")

            nextPopulation.append(tempChromosome)

            copyBestPercentChromosome[randomPair[0]] = bestPercentChromosome[randomPair[0]]

        mutateNum = int(len(nextPopulation)*mutatePercent)
        randomChromosomes = random.sample(nextPopulation,mutateNum)
        mutatePopulation = randomChromosomes

        for j in range(len(mutatePopulation)):
            mutateChromosome = mutatePopulation[j]
            mutateIndexNum = int(len(mutateChromosome) * mutateIndexPercent)
            randomIndex = random.sample(mutateChromosome,int(mutateIndexNum/2))

            randomIndex2 = random.sample(mutateChromosome,int(mutateIndexNum/2))
            for i in range(len(randomIndex)):
                index1 = randomIndex[i]
                index_location = mutateChromosome.index(index1)

                index2 = randomIndex2[i]
                index2_location = mutateChromosome.index(index2)
                if(index2 % 2 == 0 and index1 % 2 == 0):
                    corresponding_index = randomIndex[i]+1
                    corresponding_index_location = mutateChromosome.index(corresponding_index)
                    corresponding_index2 = randomIndex2[i]+1
                    corresponding_index2_location = mutateChromosome.index(corresponding_index2)
                    if index2_location < corresponding_index_location and index_location < corresponding_index2_location:
                        mutateChromosome[index_location] = index2
                        mutateChromosome[index2_location] = index1

                elif(index2 % 2 != 0 and index1 % 2 != 0):
                    corresponding_index = randomIndex[i]-1
                    corresponding_index_location = mutateChromosome.index(corresponding_index)
                    corresponding_index2 = randomIndex2[i]-1
                    corresponding_index2_location = mutateChromosome.index(corresponding_index2)
                    if index2_location > corresponding_index_location and index_location > corresponding_index2_location:
                        mutateChromosome[index_location] = index2
                        mutateChromosome[index2_location] = index1

                elif(index2 % 2 == 0 and index1 % 2 != 0):
                    corresponding_index = randomIndex[i]-1
                    corresponding_index_location = mutateChromosome.index(corresponding_index)
                    corresponding_index2 = randomIndex2[i]+1
                    corresponding_index2_location = mutateChromosome.index(corresponding_index2)
                    if index2_location > corresponding_index_location and index_location < corresponding_index2_location:
                        mutateChromosome[index_location] = index2
                        mutateChromosome[index2_location] = index1

                elif(index2 % 2 != 0 and index1 % 2 == 0):
                    corresponding_index = randomIndex[i]+1
                    corresponding_index_location = mutateChromosome.index(corresponding_index)
                    corresponding_index2 = randomIndex2[i]-1
                    corresponding_index2_location = mutateChromosome.index(corresponding_index2)
                    if index2_location < corresponding_index_location and index_location > corresponding_index2_location:
                        mutateChromosome[index_location] = index2
                        mutateChromosome[index2_location] = index1

        for j in range(len(nextPopulation)):
            if nextPopulation[j] in mutatePopulation:
                chromosome_index = mutatePopulation.index(nextPopulation[j])
                nextPopulation[j] = mutatePopulation[chromosome_index]


main()