import random
# rand_list =

# list_comprehension_below_10 =

# list_comprehension_below_10 =


rand_list = random.randint(1,20)

list_comprehension_below_10 = [num for num in rand_list if num<10]

list_comprehension_below_10_filter = filter(lambda x:x<10,rand_list)

