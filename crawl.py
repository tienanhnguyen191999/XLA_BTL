import urllib.request
import  time

for i in range(1,10000):
    print(i)
    time.sleep(0.1)
    urllib.request.urlretrieve("http://tracuunnt.gdt.gov.vn/tcnnt/captcha.png", f"data/origin/origin_{i}.png")


