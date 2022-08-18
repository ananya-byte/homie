import telebot
import datetime
import traceback
import RPi.GPIO as GPIO
from picamera import PiCamera
import os
import time, datetime
import files
from subprocess import call

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#initialising the  gpio pins, setting them as input and bed_output
#initialising the output pins as zero so that all appliances are off
gym_input,gym_output =
GPIO.setup(gym_output, GPIO.OUT)
GPIO.output(gym_output, 0) #Off initially
GPIO.setup(gym_input, GPIO.IN)

bed_input,bed_output =
GPIO.setup(bed_output, GPIO.OUT)
GPIO.output(bed_output, 0)
GPIO.setup(bed_input, GPIO.IN)

study_input,study_output =
GPIO.setup(study_output, GPIO.OUT)
GPIO.output(study_output, 0)
GPIO.setup(study_input, GPIO.IN)

living_input,living_output =
GPIO.setup(living_output, GPIO.OUT)
GPIO.output(living_output, 0)
GPIO.setup(living_input, GPIO.IN)

dine_input,dine_output =
GPIO.setup(dine_output, GPIO.OUT)
GPIO.output(dine_output, 0)
GPIO.setup(dine_input, GPIO.IN)

predef_host = <host-chat-id>
predefhost_name = '<host-name>'


bot = telebot.TeleBot('<telegram-token>')


@bot.message_handler(commands=['start'])
def start_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    chat_id = message.chat.id
    name = message.chat.first_name
    text = 'Hi! '+name +'. I\'m homie and I love making your living more comfy :)'
    if (files.checkhost(chat_id) or files.checkguest(chat_id)):
        text+='I can help you do a lot of tasks around your house.\n'+'To go through what you can do press /menu \n'+'For further help you can contact my creator pressing /help'
        bot.send_message(chat_id,text)

    else :
        text+= 'You are still not registered as a user of Homie in the current home.So to send a request please press one of the following buttons.'
        keyboard.row(
        telebot.types.InlineKeyboardButton('Request for Approval', callback_data='req-new'))
        bot.send_message(message.chat.id,text, reply_markup=keyboard)


@bot.message_handler(commands=['menu'])
def menu_command(message):
    chat_id = message.chat.id
    keyboard = telebot.types.InlineKeyboardMarkup()
    text = '\nThese are the following commands for homie: To control the appliances press /panel.'
    if files.checkhost(chat_id):
        text+='\n To get live camera feed press /camera.'
    text+='You can always return back here by pressing /menu .'

    bot.send_message(chat_id,text)


@bot.message_handler(commands=['panel'])
def panel_command(message):
    chat_id = message.chat.id
    if (files.checkhost(chat_id) or files.checkguest(chat_id)):
        keyboard = telebot.types.InlineKeyboardMarkup()
        bot.send_message(
           message.chat.id,
           'These are the following commands for each room:' +
           '\n To control the gym lights press /gym.' +
           '\n To control the bedroom and study lights press /bedroom.' +
           '\n To control living room lights press /living' +
           '\n To control dining room lights press /dining'
        )
    else:
        text = 'I\'m sorry, I don\'t understand what you\'re saying. Please return to menu by pressing /menu.'
        bot.send_message(chat_id,text)



@bot.message_handler(commands=['gym'])
def gym_command(message):
    chat_id = message.chat.id
    if (files.checkhost(chat_id)):
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Lights', callback_data='getp-glights')
      )
        bot.send_message(message.chat.id, 'Click on the appliance of choice:', reply_markup=keyboard)
    else:
        text = 'I\'m sorry, I don\'t understand what you\'re saying. Please return to menu by pressing /menu.'
        bot.send_message(chat_id,text)


@bot.message_handler(commands=['bedroom'])
def bedroom_command(message):
    chat_id = message.chat.id
    if (files.checkhost(chat_id)):
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Lights', callback_data='getp-blights')
      )
        keyboard.row(
            telebot.types.InlineKeyboardButton('Study Lights', callback_data='getp-slights'))
        bot.send_message(message.chat.id, 'Click on the appliance of choice:', reply_markup=keyboard)
    else:
        text = 'I\'m sorry, I don\'t understand what you\'re saying. Please return to menu by pressing /menu'
        bot.send_message(chat_id,text)

@bot.message_handler(commands=['living'])
def living_command(message):
    chat_id = message.chat.id
    if (files.checkhost(chat_id) or files.checkguest(chat_id)):
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Lights', callback_data='getp-llights'))
        bot.send_message(message.chat.id, 'Click on the appliance of choice:', reply_markup=keyboard)
    else:
        text = 'I\'m sorry, I don\'t understand what you\'re saying. Please return to menu by pressing /menu'
        bot.send_message(chat_id,text)

@bot.message_handler(commands=['dining'])
def living_command(message):
    chat_id = message.chat.id
    if (files.checkhost(chat_id) or files.checkguest(chat_id)):
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Lights', callback_data='getp-dlights'))
        bot.send_message(message.chat.id, 'Click on the appliance of choice:', reply_markup=keyboard)
    else:
        text = 'I\'m sorry, I don\'t understand what you\'re saying. Please return to menu by pressing /menu.'
        bot.send_message(chat_id,text)

@bot.message_handler(commands=['camera'])
def camera_command(message):
    chat_id = message.chat.id
    if files.checkhost(chat_id):
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Picture', callback_data='getc-picture'),
            telebot.types.InlineKeyboardButton('Video', callback_data='getc-video')
      )
        keyboard.row(
            telebot.types.InlineKeyboardButton('Menu', callback_data='getc-menu')
      )
        bot.send_message(message.chat.id, 'Click on the choice:', reply_markup=keyboard)
    else:
        text = 'I\'m sorry, I don\'t understand what you\'re saying. Please return to menu by pressing /menu.'
        bot.send_message(chat_id,text)


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    if data.startswith('getp'):  #to access the appliances or back to menu
        get_ex1_callback(query)
    elif data.startswith('turn-')and (data.endswith('-on')): #to switch on the appliance
        get_ex2_callback(query)
    elif data.startswith('turn-')and (data.endswith('-off')): #to switch on the appliance
        get_ex3_callback(query)
    elif data.startswith('getc'): #camera commands
        get_ex4_callback(query)
    elif data.startswith('req'): #request for approval to predef host
        get_ex5_callback(query)
    elif data.startswith('reg'): #registeration of user as host or guest
        get_ex6_callback(query)



def get_ex1_callback(query):  #callback query for appliances
    bot.answer_callback_query(query.id)
    send_exchange1_result(query.message, query.data[5:])

def get_ex2_callback(query): #call back query to turn on appliance
    bot.answer_callback_query(query.id)
    a = query.data[5:]
    send_exchange2_result(query.message, a[:-3],'on',a)

def get_ex3_callback(query): #callback query to turn off appliance
    bot.answer_callback_query(query.id)
    a = query.data[5:]
    send_exchange2_result(query.message, a[:-4],'off',a)

def get_ex4_callback(query):
    bot.answer_callback_query(query.id)
    send_exchange3_result(query.message, query.data[5:])


def get_ex5_callback(query): #callback query message to access camera
    bot.answer_callback_query(query.id)
    send_exchange4_result(query.message, query.data[4:])

def get_ex6_callback(query):
    bot.answer_callback_query(query.id)
    send_exchange5_result(query.message, query.data[4:])

def send_exchange1_result(message, ex_code):
    keyboard = telebot.types.InlineKeyboardMarkup()
    bot.send_chat_action(message.chat.id, 'typing')
    if ((ex_code)== 'glights'):
        messag = ""
        if (GPIO.input(gym_input)==1):
            messag = '\nThe gym light is already switched on.'
        elif (GPIO.input(gym_input)==0):
            messag= '\nThe gym light is currently switched off.'
        keyboard.row(
        telebot.types.InlineKeyboardButton('Switch On', callback_data='turn-glights-on'),
        telebot.types.InlineKeyboardButton('Switch Off', callback_data='turn-glights-off'))
        keyboard.row(
        telebot.types.InlineKeyboardButton('Menu', callback_data='getp-menu'))
        bot.send_message(message.chat.id, messag+'Click on choice:', reply_markup=keyboard)
    elif ((ex_code)== 'blights'):
        messag = ""
        if (GPIO.input(bed_input)==1):
            messag = 'The bedroom is already switched on.'
        elif (GPIO.input(bed_input)==0):
            messag = 'The bedroom is currently switched off.'
        keyboard.row(
        telebot.types.InlineKeyboardButton('Switch On', callback_data='turn-blights-on'),
        telebot.types.InlineKeyboardButton('Switch Off', callback_data='turn-blights-off'))
        keyboard.row(
        telebot.types.InlineKeyboardButton('Menu', callback_data='getp-menu'))
        bot.send_message(message.chat.id, messag+'Click on choice:', reply_markup=keyboard)
    elif ((ex_code)== 'slights'):
        messag = ""
        if (GPIO.input(study_input)==1):
            messag = 'The study light is already switched on.'
        elif (GPIO.input(btlights_input)==0):
            messag = 'The study light is currently switched off.'
        keyboard.row(
        telebot.types.InlineKeyboardButton('Switch On', callback_data='turn-slights-on'),
        telebot.types.InlineKeyboardButton('Switch Off', callback_data='turn-slights-off'))
        keyboard.row(
        telebot.types.InlineKeyboardButton('Menu', callback_data='getp-menu'))
        bot.send_message(message.chat.id, messag+'Click on choice:', reply_markup=keyboard)
    elif ((ex_code)== 'llights'):
        messag = ""
        if (GPIO.input(living_input)==1):
            messag = 'The Living-Room Lighting is already switched on.'
        elif (GPIO.input(living_input)==0):
            messag = 'The Living-Room Lighting is currently switched off.'
        keyboard.row(
        telebot.types.InlineKeyboardButton('Switch On', callback_data='turn-llights-on'),
        telebot.types.InlineKeyboardButton('Switch Off', callback_data='turn-llights-off'))
        keyboard.row(
        telebot.types.InlineKeyboardButton('Menu', callback_data='getp-menu'))
        bot.send_message(message.chat.id, messag+'Click on choice:', reply_markup=keyboard)
    elif ((ex_code)== 'dlights'):
        messag = ""
        if (GPIO.input(dine_input)==1):
            messag = 'The Dining-Room Lighting is already switched on.'
        elif (GPIO.input(dine_input)==0):
            messag = 'The Dining-Room Lighting is currently switched off.'
        keyboard.row(
        telebot.types.InlineKeyboardButton('Switch On', callback_data='turn-dlights-on'),
        telebot.types.InlineKeyboardButton('Switch Off', callback_data='turn-dlights-off'))
        keyboard.row(
        telebot.types.InlineKeyboardButton('Menu', callback_data='getp-menu'))
        bot.send_message(message.chat.id, messag+'Click on choice:', reply_markup=keyboard)
    elif ((ex_code)=='menu'):
        menu_command(message)


def send_exchange2_result(message, ex1_code, ex2_code,ex_code):
    stat = -1
    keyboard = telebot.types.InlineKeyboardMarkup()
    bot.send_chat_action(message.chat.id, 'typing')
    if ex2_code == 'on':
        stat = 1
    elif ex2_code == 'off':
        stat = 0
    text = "The appliance is " + ex2_code ".\n"
    if ((ex1_code)== 'glights'):
        GPIO.output(gym_output, stat)
    elif ((ex1_code)== 'blights'):
        GPIO.output(bedroom_output, stat)
    elif ((ex1_code)== 'slights'):
        GPIO.output(study_output, stat)
    elif ((ex1_code)== 'llights'):
        GPIO.output(living_output, stat)
    elif ((ex1_code)== 'dlights'):
        GPIO.output(dine_output, stat)
    bot.send_message(message.chat.id,text)


def send_exchange3_result(message, ex_code):
    keyboard = telebot.types.InlineKeyboardMarkup()
    bot.send_chat_action(message.chat.id, 'typing')
    if ((ex_code)== 'picture'):
        path = "/home/pi/Live/img.jpg"
        if os.path.exists(path) == True:
            os.remove(path)
        camera = PiCamera()
        time.sleep(2)
        camera.capture(path)
        camera.close()
        print("Done.")
        photo = open(path, 'rb')
        bot.send_photo(message.chat.id, photo)
        photo.close()
        camera.close()
    elif ((ex_code)=='video'):
        path = "/home/pi/Pictures/video.h264"
        apath = "/home/pi/Pictures/video1.mp4"
        if os.path.exists(path) == True:
            os.remove(path)
        if os.path.exists(apath) == True:
            os.remove(apath)
        camera = PiCamera()
        time.sleep(2)
        print("Start recording...")
        camera.start_recording(path)
        camera.wait_recording(5)
        camera.stop_recording()
        print("Done.")
        command = "MP4Box -add "+path+" " + apath
        call([command], shell=True)
        print("Video converted.")
        video = open(apath, 'rb')
        bot.send_video(message.chat.id, video)
        video.close()
        camera.close()
    elif ((ex_code)=='menu'):
        menu_command(message)



def send_exchange4_result(message, ex_code):
    keyboard = telebot.types.InlineKeyboardMarkup()
    chat_id = message.chat.id
    name = message.chat.first_name
    bot.send_chat_action(message.chat.id, 'typing')
    if ((ex_code)=='new'):
        print('sending request to host')
        text ='Hi! '+predefhost_name+', '+name+' is trying to access you\'re homie as a family member'
        text+='.Do you appve him/her as a family member or guest or none..'
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
        telebot.types.InlineKeyboardButton('Member', callback_data='reg-mem-'+str(chat_id)+'-'+name),
        telebot.types.InlineKeyboardButton('Guest', callback_data='reg-gue-'+str(chat_id)+'-'+name),
        telebot.types.InlineKeyboardButton('None', callback_data='reg-none')
  )
    bot.send_message(predef_host,text, reply_markup=keyboard)




def send_exchange5_result(message, ex_code):
    keyboard = telebot.types.InlineKeyboardMarkup()
    bot.send_chat_action(message.chat.id, 'typing')
    ex_code_status = ex_code[0:3]
    check = ex_code.rindex('-')
    chat_id = int(ex_code[4:check])
    name = ex_code[check-1:]
    print(ex_code)
    if ((ex_code_status)== 'mem'):
        files.appendhost(chat_id,name)
        bot.send_chat_action(chat_id, 'typing')
        text = 'Congrats :)'+'you can freely communicate with me. Please press /menu to know what you can do. '
        bot.send_message(chat_id,text)
        print('Member added')
    elif ((ex_code_status)=='gue'):
        files.appendguest(chat_id,name)
        text = 'Congrats :)'+'you can freely communicate with me. Please press /menu to know what you can do.'
        bot.send_message(chat_id,text)
        print('Guest added')
    print('d value changed')


bot.polling(none_stop=True)
