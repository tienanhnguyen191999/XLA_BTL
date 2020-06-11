import urllib.request

for i in range(1,100):
    print(i)
    urllib.request.urlretrieve("http://tracuunnt.gdt.gov.vn/tcnnt/captcha.png?uid=34e5d672-0947-4636-b0bc-3a18c5517361", f"data/origin/origin_{i}.png")


