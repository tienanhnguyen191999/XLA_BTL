# Cut captcha to each word
from PIL import Image
import cv2
import numpy as np
import pytesseract
import time
import string

def splitLetters(letters, spaceBetweenCharacters):
    '''
        Phân chia lại vị trí xuất hiện của các ký tự trong ảnh
    '''
    # 1. Tính số phần tử các ký tự được phát hiện trong ảnh    
    lengthOfLetters = len(letters)
    # 2. Tính chiều rộng trung bình của các ký tự trong chuỗi    
    characterLengthEverage = (letters[lengthOfLetters-1]['end']-letters[0]['start'] - spaceBetweenCharacters)/5
    # 3. Làm tròn chiều rộng trung bình của các ký tự trong chuỗi
    characterLengthEverageRound = int(characterLengthEverage) if ((letters[lengthOfLetters-1]['end']-letters[0]['start'] - spaceBetweenCharacters)/5 - int(characterLengthEverage)) < 0.5 else int(characterLengthEverage) + 1
    # 4. Tách các ký tự bị ghép vào với nhau do bước cắt ảnh chưa chính xác
    for letter in reversed(letters):
        # 1. Tính tỉ lệ số ký tự xuất hiện trong letter này        
        characterRatio = letter['distance']/characterLengthEverage
        # 2. Nếu tỉ lệ này > 1.5 thì có ít nhất 2 ký tự xuất hiện trong letter này
        if characterRatio > 1.5:
            # 3. Làm tròn tỷ lệ số ký tự xuất hiện trong letter
            characterRatio = int(characterRatio) if (characterRatio - int(characterRatio)) < 0.5 else int(characterRatio) + 1
            # 4. Cắt letter ra thành các ký tự con
            for i in range(characterRatio-1):
                letters.append({'start': letter['start'], 'end': letter['start']+characterLengthEverageRound, 'distance': characterLengthEverageRound})
                letter['start'] = letter['start']+characterLengthEverageRound
                letter['distance'] = letter['distance']-characterLengthEverageRound
    # 5. Trả về mảng các ký tự
    return letters

def sortLettersBasedOnAppearence(letters):
    '''
        Sắp xếp lại vị trí các ký tự trong mảng dựa vào sự xuất hiện của chúng
    '''
    return sorted(letters, key = lambda x: x['start'])

def crop(file_path, outpath):
    '''
        Cắt ảnh thành nhiều ảnh chứa từng ký tự con
    '''
    part = 0
    # 1. Mở ảnh    
    img = Image.open(file_path)
    # 2. Lấy kích thước ảnh
    p = img.convert('P')
    w, h = p.size
    spaceBetweenCharacters = 0
    # 3. Lấy ra vị trí của từng ký tự theo: vị trí xuất hiện, vị trí kết thúc, độ rộng của ký tự theo chiều ngang    
    letters = []
    start, end = -1, -1
    found = False
    for i in range(w):
        in_letter = False
        for j in range(h-10):
            if p.getpixel((i,j)) == 1:
                in_letter = True
                break
        if not found and in_letter:
            found = True
            start = i
        if found and not in_letter:
            found = False
            if end > -1:
                spaceBetweenCharacters += (start - end)
            end = i
            letters.append({'start': start, 'end': end, 'distance': end-start})
    # 4. Chỉnh sửa lại vị trí xuất hiện và kết thúc của từng ký tự
    letters = splitLetters(letters, spaceBetweenCharacters)
    # 5. Sắp xếp lại các ký tự trong mảng dựa vào vị trí xuất hiện của chúng
    letters = sortLettersBasedOnAppearence(letters)
    # 6. Cắt ảnh thành các ảnh con chưa từng ký tự    
    # fig = plt.figure(figsize=(5, 10))
    columns = 5
    rows = 2
    i = 0
    for letter in letters:
        if letter['end']-letter['start'] < 40:
            bbox = (letter['start'], 0, letter['end'], h-1)
            crop = img.crop(bbox)
            i = i + 1

            crop.save(outpath + '/' + 'ouput_{}.png'.format(i))
            # Label crop character
            # imgg = cv2.imread(outpath + '/' + 'ouput_{}.png'.format(i), -1)
            # custom_config = r'--oem 3 --psm 6'
            # label = pytesseract.image_to_string(imgg, config=custom_config)
            # cv2.imwrite('data/training_data/{char}/{name}.png'.format(char = label.lower(), name=time.time()), imgg)

def avg_method(file_path_for_test):
    img = crop(file_path_for_test, 'data/split')

# # DOI FILE TEST O DAY
# for i in range(1, 10000):
#     try:
#         file_path_for_test = 'data/erase_noise/erase_noise_{no}.png'.format(no=i)
#         print(i)
#         avg_method(file_path_for_test)
#     except:
#         pass