import random

def get_nonconsecutive_random_numbers(max_num, count):
    # Generate the first random number
    run = True

    while(run):
        random_numbers = random.sample(range(0, max_num), count)
        if(random_numbers[0]+3 <= random_numbers[1] or random_numbers[0]-3 >= random_numbers[1] ):
            return random_numbers

for i in range(10000):
    print(get_nonconsecutive_random_numbers(10, 2))