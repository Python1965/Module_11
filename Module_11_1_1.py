# from matplotlib import pyplot as plt
# from random import randint
#
# # Данные для графика
# x = []
# for i in range(5):
#     x.append(randint(1,20))#генерируем данные х
# print(x)
#
# y = []
# for i in range(5):
#     y.append(randint(1,20))#генерируем данные y
# print(y)
# # Создание графика
# plt.plot(x, y, label='кривая', marker='o') #построение кривой по заданым координатам
#
# # Настройка графика
# plt.title('Случайный график') # наименование графика
# plt.xlabel('X')#обозначаем ось х
# plt.ylabel('Y')#обозначаем ось у
# plt.grid(True)#размечаем сетку на графике
# plt.legend()#подписываем название кривой
#
# # Показ графика
# plt.show()
# print(" код matplotlib завершён ")

from PIL import Image
from PIL import ImageFilter

im = Image.open('bear.jpg')#открываем изображение
print(im.format, im.size, im.mode)#узнаем размеры и параметры
w, h = im.size
im1 = im.resize((w//2, h//2))# уменьшаем изображение в 2 раза
im1 = im1.convert("1")#преобразовываем изображение в двухцветное
out = im1.filter(ImageFilter.DETAIL)#улучшаем изображение
out.show()#выводим изображение на экран
out.save('bear1.jpg')#сохраняем переделаное