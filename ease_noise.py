import cv2 

for i in range(1, 10000):
    file_path = 'data/origin/origin_{no}.png'.format(no=i)
    file_path_erase_noise = 'data/erase_noise/erase_noise_{no}.png'.format(no=i)
    
    # Xoá đường ngang dọc
    try:
        image = cv2.imread(file_path, -1)
        image = cv2.morphologyEx(image, cv2.MORPH_RECT, None)
        new_img = image.copy()
        new_img[new_img < 5] = 0
        new_img[new_img >=5] = 255
        
        # Xoa vien ngoai
        w,h,c = new_img.shape
        crop_size = 5
        new_img = new_img[crop_size: w - crop_size, crop_size: h - crop_size]
        cv2.imwrite(file_path_erase_noise, new_img)
    except:
        pass