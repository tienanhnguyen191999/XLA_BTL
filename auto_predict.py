from selenium import webdriver
from add_label import  avg_method
import cv2


# return captcha ( numpy )
def getCaptCha(location):
    img = cv2.imread('data/screenshot/screen_shot.png')
    captCha_size = { 'x' : 117, 'y': 45}
    print(location)
    result = img[location['y']: location['y'] + captCha_size['y'] , location['x']: location['x'] + captCha_size['x'] ]
    result = cv2.resize(result, (130,50))

    result = cv2.morphologyEx(result, cv2.MORPH_RECT, None)
    new_img = result.copy()
    new_img[new_img < 5] = 0
    new_img[new_img >=5] = 255
    
    # # Xoa vien ngoai
    w,h,c = new_img.shape
    crop_size = 5
    new_img = new_img[crop_size: w - crop_size, crop_size: h - crop_size]
    cv2.imshow("image", new_img)
    cv2.waitKey()
    cv2.imwrite('data/screenshot/test.png', new_img)

chrome = webdriver.Chrome()
chrome.get("http://tracuunnt.gdt.gov.vn/tcnnt/mstdn.jsp")

chrome.save_screenshot("data/screenshot/screen_shot.png")
location = chrome.find_element_by_css_selector('img').location

avg_method("data/screenshot/screen_shot.png")
getCaptCha(location)

chrome.quit()
