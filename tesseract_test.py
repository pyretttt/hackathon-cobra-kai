import cv2 #предварительно нужно установить pip install opencv-python
import pytesseract #предварительно нужно установить tesseract и pip install pytesseract
import pandas as pd
import os

#для запуска под Windows нужно активировать строчку ниже и прописать корректный путь к tesseract.exe
#pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' 


path_img = '/Users/pavelokhotnikov/Downloads/SROIE2019/test/img/' #путь к фапке с картинками
path_csv = '/Users/pavelokhotnikov/Downloads/SROIE2019/test/orc_csv/' #путь к папке для сохранения считанных данных в csv

config = r'--oem 3 --psm 6'

for files in os.walk(path_img):
    for file in files[2]:
        fl = path_img+file
        img = cv2.imread(fl)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        df =pytesseract.image_to_data(img, config = config, output_type='data.frame') #output_type='data.frame' - выводит в датафрейм
        df.to_csv(path_csv+file+".csv", index=False) #сохраняем в CSV
        
print("сохранение считанных данных завершено в папку", path_csv)

"""ниже код для вывода на экран картинки чека с рамками распознаных слов, и распознаного текста, сейчас 
    отключено так как выше код обрабатывает сразу все файлы из папки, а тут лучше указать на один конкретный файл"""        
# data =pytesseract.image_to_data(img, config = config)
# for i, el in enumerate(data.splitlines()):
#     if i == 0:
#         continue
#     el=el.split()
#     try:
#         x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])
#         cv2.rectangle(img, (x,y), (w+x, h+y), (0,0,255),1) # выводит рамки распознаных слов на картинку
#         # cv2.putText(img, el[11], (x,y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 1) # выводит распознанный текст на картинку
    
#     except IndexError:
#         print('Операция была пропущена')    
        
# print(data)

# cv2.imshow('Result', img) #выводит в отдельное окно обработанную картинку
# cv2.waitKey(0) #выставляет задержку действия программы до нажатия любой клафиши при просмотре картинки
