import time


def main():
    start_time = time.time()

    num_generations = 1000

    for generation in range(num_generations):
        print(generation) 
    print("Finished Execution after " + str(time.time()-start_time))





if __name__ == '__main__':
    main()