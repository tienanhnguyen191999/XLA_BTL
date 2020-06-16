from utils import avg_method

# DOI FILE TEST O DAY
for i in range(1, 10000):
    try:
        file_path_for_test = 'data/erase_noise/erase_noise_{no}.png'.format(no=i)
        print(i)
        avg_method(file_path_for_test)
    except:
        pass