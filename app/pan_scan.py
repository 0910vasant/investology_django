from PIL import Image
import pytesseract
import re
# # def get_pan_no():
# regex = "[A-Z]{5}[0-9]{4}[A-Z]{1}"
# p = re.compile(regex)

# all_string = pytesseract.image_to_string(Image.open('mayur_pan1.jpg')).strip()
# pan_string = all_string[-10:]
# # print(all_string)
# if(re.search(p, pan_string) and len(pan_string) == 10):
#     print(f"pan_no = {pan_string}")
#     # return pan_string
# else:
#     print("image is not readable or invalid please upload correct and clear image")




# def get_pan_no():
regex = "[A-Z]{5}[0-9]{4}[A-Z]{1}"
p = re.compile(regex)

all_string = pytesseract.image_to_string(Image.open("H:/Dynamic-Vishva/mfu-docs/new/pan_images/vivek_pan1.jpeg")).strip()
pan_string = all_string[-10:]
# print(all_string)
a = all_string.split("\n")
print(f"before a = {a}")
# a = [i for i in a if re.search(p,i)]
for i in a:
    regex_result = re.search(p,i)
    if regex_result:
        pan_no = regex_result.group()
        break
print(f"pan_no = {pan_no}")





# from pan_aadhar_ocr import Pan_Info_Extractor
# 
# extractor = Pan_Info_Extractor()
# 
# 
# extractor.info_extractor('C:/Users/harsh/Downloads/nayan_pan1.jpg')
