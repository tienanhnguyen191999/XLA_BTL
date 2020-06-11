from pathlib import  Path
# Tạo thư mục chưa training data
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
for letter in letters+numbers:
    Path("data/training_data/{dir_name}".format(dir_name=letter)).mkdir(parents=True, exist_ok=True)
    