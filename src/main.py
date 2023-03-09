import time
import DataGenerator


def main():
    start_time = time.time()

    num_generations = 1000

    print("Finished Execution after " + str(time.time()-start_time))




def generate_chromosome():
    chromosome_length = num_requests*2+1

    with open(data_file,'r') as file:
        request_lines =range(num_hospitals+num_vehicles+4,num_hospitals+num_vehicles+num_requests+4)
        chromosome =[]
        random_numbers = random.sample(range(0, 2001), 2000)

        for i in range(chromosome_length):
            chromosome.append((0,0))

        for i, line in enumerate(file):
            if i+1 in request_lines:
                request_segments = line.strip().split(",")

                if random_numbers[0]>random_numbers[1]:
                    chromosome[random_numbers[0]]=(int(request_segments[3]),int(request_segments[4]))
                    chromosome[random_numbers[1]]=(int(request_segments[1]),int(request_segments[2]))
                else:
                    chromosome[random_numbers[0]]=(int(request_segments[1]),int(request_segments[2]))
                    chromosome[random_numbers[1]]=(int(request_segments[3]),int(request_segments[4]))

                random_numbers.pop(0)
                random_numbers.pop(0)

            elif i+1 > max(request_lines):
                break

        print(chromosome)

generate_chromosome()
if __name__ == '__main__':
    main()
