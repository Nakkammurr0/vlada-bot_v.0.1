from vkbottle import AudioUploader, Bot, DocUploader, Message, PhotoUploader
import requests
from vkbottle import *
import PIL
from PIL import Image, ImageDraw, ImageFont
import random
import dem
import sys
import time
try:
    import vk
except:
    print('Выполните установку модуля vk! (pip3 install vk)')
import os

bot=Bot('токен группы встав да')
print("[Модули] Модуль vkbottle успешно импортирован")
print("[Модули] Модуль pillow успешно импортирован")
print("[Модули] Модули Image успешно импортирован")
print("[Модули] Модуль random успешно импортирован")
print("[Модули] Модуль dem успешно импортирован")
print("[Модули] Модуль sys успешно импортирован")
print("[Модули] Модуль time успешно импортирован")
print("[Модули] Модуль vk успешно импортирован")
print("[Модули] Модуль os успешно импортирован")

dialogs = {}
wait = []

photo_uploader = PhotoUploader(bot.api, generate_attachment_strings=True) 

@bot.on.message_handler(text='Текст <name>')
async def photo(ans: Message, name):
    try:
        photo1 = Image.open("rectangle.png")
    except:
        await ans('Ошибка')

    
    idraw = ImageDraw.Draw(photo1)
    font = ImageFont.truetype("arial.ttf", size=52)
    idraw.text((400, 200), name, font=font)
    photo1.save('photo1_watermarked.png')
    photo = await photo_uploader.upload_message_photo('photo1_watermarked.png')
    await ans('Держите фото:', attachment=photo)

@bot.on.message(text="/дем <str1>//<str2>")
async def wrapper(ans: Message, str1, str2):
    if ans.attachments and ans.attachments[0].photo:
                photo = ans.attachments[0].photo.sizes[-1].url
                p = requests.get(photo)
                out = open(r'img.jpg', "wb")
                out.write(p.content)
                out.close()
                dem.makeImage(str1=str1, str2=str2)
                photo = await photo_uploader.upload_message_photo('result.jpg')
                return await ans(f'Ваш демотиватор:', attachment=photo)
    else:
            await ans(f'Прикрепите фотографию и попробуйте снова!')

@bot.on.message(text="/дем <str1>")
async def wrapper(ans: Message, str1):
    if ans.attachments and ans.attachments[0].photo:
                str2 = ''
                photo = ans.attachments[0].photo.sizes[-1].url
                p = requests.get(photo)
                out = open(r'img.jpg', "wb")
                out.write(p.content)
                out.close()
                dem.makeImage(str1=str1, str2=str2)
                photo = await photo_uploader.upload_message_photo('result.jpg')
                return await ans(f'Ваш демотиватор:', attachment=photo)
    else:
            await ans(f'Прикрепите фотографию и попробуйте снова!')

@bot.on.message(text='/старт', lower = True)
async def start(ans: Message):
    if ans.from_id not in wait and ans.from_id not in dialogs:
        if not wait:
                       await ans('Вы попали в очередь! Ожидайте собеседника.\n Отменить очередь - /отменапоиска')
                       wait.append(ans.from_id)
        else:
            dialogs[ans.from_id] = wait[0]
            dialogs[wait[0]] = ans.from_id
            await bot.api.messages.send(peer_id=ans.from_id, random_id=0, message='Мы вам нашли собеседника!')
            await bot.api.messages.send(peer_id=wait[0], random_id=0, message='Мы вам нашли собеседника!')
            del wait[0]

@bot.on.message(text='/отменапоиска', lower = True)
async def otmena(ans: Message):
    if ans.from_id in wait:
        del wait[wait.index(ans.from_id)]
        await ans('Вы остановили поиск.')
    else:
        await ans('Вы не в очереди!')

@bot.on.message(text='/стоп', lower = True)
async def stop(ans: Message):
    if ans.from_id in dialogs:
        await bot.api.messages.send(peer_id=ans.from_id, random_id=0, message='Диалог был остановлен.')
        await bot.api.messages.send(peer_id=dialogs[ans.from_id], random_id=0, message='Собеседник остановил диалог.')
        del dialogs[dialogs[ans.from_id]]
        del dialogs[ans.from_id]
    else:
        await ans('У вас нет собеседника!')

@bot.on.message()
async def all(ans: Message):
    if ans.from_id in dialogs:
        await bot.api.messages.send(peer_id=dialogs[ans.from_id], random_id=0, message='Собеседник: ' + ans.text)
    if ans.from_id in wait:
        await ans('Вы уже ищите собеседника! \n /отменапоиска - отменить поиск')



@bot.on.message(text="Привет")
async def hello1(ans: Message):
    await ans(f'Привет!')

@bot.on.message(text="")
async def hello2(ans: Message):
    if ans.attachments and ans.attachments[0].photo:
        await ans(f'Воу! Вложения?', attachment='photo-172005511_457239065')
















#@bot.on.message(text="Клавиатура")
#async def hello3(ans: Message):
#    name_buttons = [[{'text': f'1 строчка 1 кнопка'},
#                    {'text': f'1 строчка 2 кнопка', 'color': 'positive'},
#                    {'text': f'1 строчка 3 кнопка'}],
#                    [{'text': f'2 строчка 1 кнопка'},
#                    {'text': f'2 строчка 2 кнопка', 'color': 'primary'}]]
#    name_keyboard = keyboard_gen(name_buttons, one_time=False)
#    await ans(f'Клавиатура:', keyboard=name_keyboard)

#@bot.on.message_handler(text='Текст <name>')
#async def photo(ans: Message, name):
#    try:
#        photo = Image.open("rectangle.png")
#    except:
#        await ans('Ошибка')
#        sys.exit(1)
#    
#    idraw = ImageDraw.Draw(photo)
#    font = ImageFont.truetype("arial.ttf", size=52)
#    idraw.text((400, 200), name, font=font)
#    photo.save('photo1_watermarked.png')
#    photo1 = await photo_uploader.upload_message_photo('photo1_watermarked.png')
#    await ans('Держите фото:', attachment=photo1)

bot.run_polling()
