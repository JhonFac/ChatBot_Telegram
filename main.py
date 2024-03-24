import os

import requests
import telebot
from dotenv import load_dotenv
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot (TELEGRAM_TOKEN)
lista =[]

@bot.message_handler(content_types=["text"])
def bot_mensajes_texto(message):
    """
    The function `bot_mensajes_texto` manages text messages received, including processing commands and
    updating user status based on message content.
    
    :param message: The `message` parameter in the `bot_mensajes_texto` function represents the message
    received by the bot. It contains information such as the text of the message, the chat ID, and other
    relevant details that the bot can use to process and respond to the message appropriately
    :return: The function `bot_mensajes_texto` is returning different values based on the conditions met
    in the code. Here are the possible return scenarios:
    """
    bot.send_chat_action(message.chat.id, "typing")
    user = set_data_list(message)
    
    if message.text.startswith("/"):
        val_comand(message, user)
        return

    if not user['status'] and message.text in ["Not taken off yet", "Already taken off", "Just took off"]:
        process(message, user)
        return

    inval_comand(message, user)

def set_data_list(message):
    """
    The function `set_data_list` initializes a user dictionary with default values and appends it to a
    global list.
    
    :param message: The `message` parameter is typically an object that contains information about a
    message sent in a chat application. It can include details such as the chat ID, sender information,
    message content, and more. In this context, the `message` parameter is used to extract the chat ID
    to set up data
    :return: The function `set_data_list` is returning a dictionary containing information about the
    user. The dictionary includes keys such as 'chat_id', 'frame', 'min_value', 'max_value', 'attempts',
    and 'status'.
    """
    global lista
    chat_id = message.chat.id
    user = get_frame(chat_id)
    if user:
        return user
    user = {
        'chat_id': chat_id, 
        'frame': 0,
        'min_value':0,
        'max_value':61695,
        'attempts':0,
        'status':True
        }
    lista.append(user)
    return user

def get_frame(chat_id):
    """
    The function `get_frame` searches for a user in a list by their chat_id and returns the user if
    found, otherwise returns False.
    
    :param chat_id: The `get_frame` function you provided seems to be searching for a user in a list
    based on the `chat_id` provided. If the user with the specified `chat_id` is found in the `lista`,
    it returns that user. Otherwise, it returns `False`
    :return: The `get_frame` function is returning the user dictionary from the `lista` list that
    matches the provided `chat_id`. If a user with the specified `chat_id` is found, the function
    returns that user dictionary. If no user with the given `chat_id` is found in the list, the function
    returns `False`.
    """
    for user in lista:
        if user['chat_id'] == chat_id:
            return user
    return False

def update_frame(user, min_value:int, max_value:int, current_number:int, attempts:int, status:bool):
    """
    The function `update_frame` updates the user's frame, minimum value, maximum value, number of
    attempts, and status.
    
    :param user: The `user` parameter is a dictionary that contains information about a user. It likely
    includes details such as the user's frame, minimum value, maximum value, number of attempts, and
    status. The `update_frame` function updates these values in the `user` dictionary based on the
    provided parameters
    :param min_value: The `min_value` parameter represents the minimum value allowed in a range. It is
    an integer value that specifies the lower limit of the range within which the `current_number`
    should fall
    :type min_value: int
    :param max_value: The `max_value` parameter in the `update_frame` function represents the maximum
    value allowed for the current number in the user's frame. This value is used to set the upper limit
    for the range within which the user can select a number
    :type max_value: int
    :param current_number: The `current_number` parameter in the `update_frame` function represents the
    current value that will be displayed on the user's frame or screen. It is the number that the user
    is interacting with or trying to update within the specified range of `min_value` and `max_value`
    :type current_number: int
    :param attempts: The `attempts` parameter in the `update_frame` function represents the number of
    attempts made by the user in a particular context or scenario. It is an integer value that keeps
    track of how many times the user has tried to perform a certain action or task
    :type attempts: int
    :param status: The `update_frame` function takes in the following parameters:
    :type status: bool
    """
    user['frame'] = current_number
    user['min_value'] = min_value
    user['max_value'] = max_value
    user['attempts'] = attempts
    user['status'] = status

def delete_user(user):
    """
    The function `delete_user` removes a specified user from a global list called `lista`.
    
    :param user: The `delete_user` function you provided takes a parameter `user`, which is the user to
    be removed from the `lista` global variable. The function removes the specified user from the list
    """
    global lista
    lista.remove(user)

def process(message, user):
    """
    The function processes a message, checks a number, retrieves an image from a URL, sends the image to
    a chat with a countdown message, and prompts the user with a keyboard markup.
    
    :param message: The `message` parameter in the `process` function seems to be an object that
    contains information related to a message received by the bot. It likely includes details such as
    the text of the message, the chat ID, and other relevant information
    :param user: The `user` parameter seems to be a dictionary containing information about the user. It
    includes the user's frame number and the number of attempts they have made. This information is used
    within the `process` function to construct a URL for fetching a photo, determine the number of
    attempts left, and display
    :return: If the `message.text` is equal to "Just took off", then the function will return without
    executing any further code.
    """
    check_number(message, user)
    if message.text == "Just took off": return
    url = f"https://framex-dev.wadrid.net/api/video/Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)-wbSwFU6tY1c/frame/{user['frame']}/"
    response = requests.get(url)
    foto = response.content
    attempts = 17- user['attempts']
    bot.send_photo(
        message.chat.id,
        foto, 
        "look closely at the image at the countdown on the top-right corner" + f'\n\n You have {attempts} attempts left'
        )

    markup = ReplyKeyboardMarkup(
        input_field_placeholder="Push button",
        resize_keyboard=True,
        row_width=2
    )
    markup.add("Not taken off yet", "Already taken off", "Just took off")
    bot.send_message(message.chat.id, '¿Already taken off?', reply_markup=markup)

def inval_comand(message, user):
    """
    The function `inval_comand` checks the user's status and sends a message with available commands if
    the user has not started the game.
    
    :param message: The `message` parameter in the `inval_comand` function is typically a message object
    that contains information about the incoming message from the user, such as the chat ID, message
    text, sender information, etc. It is used to send responses back to the user or perform actions
    based on the
    :param user: The function `inval_comand` takes two parameters: `message` and `user`. The `user`
    parameter seems to be a dictionary containing information about the user, specifically their
    `status`. The function checks the user's status and sends a message accordingly if the command is
    not available. If
    :return: The function `inval_comand` is returning a message to the user based on the status of the
    user. If the user's status is `start_bot`, it will return a message indicating that the command is
    not available and instruct the user to start the game by typing `/start`. If the user's status is
    not `start_bot`, it will return a message listing the available options.
    """
    start_bot = user['status']
    if start_bot:
        texto_html = '<b>Command not available</b>' + '\n'
        texto_html+= '<i>to start the game type /start</i>' + '\n'
        markup = ReplyKeyboardMarkup(
            input_field_placeholder="Push button",
            resize_keyboard=True
        )
        markup.row("/start")
        bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)
        return

    texto_html = '<b>Command not available, you must choose an option from one of the buttons between:</b>' + '\n'
    texto_html+= '<i>- Not taken off yet</i>' + '\n'
    texto_html+= '<i>- Already taken off</i>' + '\n'
    texto_html+= '<i>- Just took off</i>' + '\n'
    bot.send_message(message.chat.id, texto_html, parse_mode="html")

def val_comand(message, user):
    """
    The function `val_comand` handles user commands related to restarting the challenge and providing
    instructions for a rocket launch video analysis task.
    
    :param message: The `message` parameter in the `val_comand` function seems to be an object that
    contains information about a message sent in a chat. It likely includes details such as the text of
    the message, the chat ID, and other relevant information related to the message
    :param user: The `user` parameter in the `val_comand` function seems to be a dictionary containing
    information about the user's status and data related to the challenge. The function checks the
    user's status and processes the message accordingly. If the user is not currently in the challenge
    and sends "/restart", it
    :return: The function `val_comand` is returning different responses based on the conditions
    provided.
    """

    start_bot = user['status']

    if not start_bot and message.text == "/restart":  
        delete_user(user)
        user = set_data_list(message)
        texto_html = '<b>OKAY.!</b>' + '\n'
        texto_html+= "<b>let's start again</b>" + '\n'
        texto_html+= '<b>This is the challenge</b>' + '\n'
        texto_html+= '<i>We have a video of a rocket launch and we want to know at which frame exactly is the rocket launched,</i>' + '\n'
        texto_html+= '<i>which you can tell by looking at the countdown in the upper right corner of the video and also when the speed of the rocket is 1km/h and T+ 00:00:01</i>' + '\n'
        texto_html+= '<b><u>you have 16 attempts to find it</u></b>' + '\n\n'
        user['status'] = False
        bot.reply_to(message, texto_html, parse_mode="html")
        process(message, user)
        return

    if start_bot:
        texto_html = '<b>This is the challenge</b>' + '\n'
        texto_html+= '<i>We have a video of a rocket launch and we want to know at which frame exactly is the rocket launched,</i>' + '\n'
        texto_html+= '<i>which you can tell by looking at the countdown in the upper right corner of the video and also when the speed of the rocket is 1km/h and T+ 00:00:01</i>' + '\n'
        texto_html+= '<b><u>you have 16 attempts to find it</u></b>' + '\n\n'
        texto_html+= '<b>If at any point you want to start again, type /restart</b>'
        user['status'] = False
        bot.reply_to(message, texto_html, parse_mode="html")
        process(message, user)
        return
    
    texto_html = '<b>Command not available, you must choose an option from one of the buttons between:</b>' + '\n'
    texto_html+= '<i>- Not taken off yet</i>' + '\n'
    texto_html+= '<i>- Already taken off</i>' + '\n'
    texto_html+= '<i>- Just took off</i>' + '\n'
    bot.send_message(message.chat.id, texto_html, parse_mode="html")

def check_number(message, user):
    """
    The function `check_number` updates and checks a user's input against a range of values to determine
    if a specific condition is met.
    
    :param message: The `message` parameter in the `check_number` function is used to receive input or
    messages from the user. It contains information such as the text of the message, chat ID, and other
    relevant details related to the conversation with the user. In this context, it seems like the
    function is processing
    :param user: The `user` parameter in the `check_number` function seems to be a dictionary containing
    the following keys and their corresponding values:
    :return: The function `check_number` is returning the updated current number after processing the
    user input and updating the frame information.
    """
    min_value = int(user['min_value'])
    max_value = int(user['max_value'])
    attempts = int(user['attempts']) + 1
    current_number = int(user['frame'])
    comparison = message.text

    if attempts > 16 or comparison == 'Just took off':
        if current_number in [39612, 39613]:
            texto_html = '<b>Found..!</b>' + '\n'
            texto_html+= '<i>The frame just when the rocket 🚀 takes off</i>' + '\n'
            texto_html+= "<b>If you want to try again /start</b>" + '\n'
        else:
            texto_html = '<b>Oh no.!</b>' + '\n'
            texto_html+= '<i>his is not the frame 😨 when the rocket 🚀 takes offi</i>' + '\n'
            texto_html+= "<b>let's start again /start</b>" + '\n'
      
        update_frame(user, 0, 61695, 0, 0, True)
        markup = ReplyKeyboardMarkup(
        input_field_placeholder="Push button",
        resize_keyboard=True
        )
        markup.row("/start")
        bot.send_message(message.chat.id, texto_html, parse_mode="html", reply_markup=markup)
        return
  
    elif comparison == 'Not taken off yet':
        min_value = current_number + 1
    elif comparison == 'Already taken off':
        max_value = current_number - 1
    
    current_number = (min_value + max_value) // 2
    if max_value - min_value == 1:
        current_number += 1
    

    update_frame(
        user,
        min_value,
        max_value,
        current_number,
        attempts,
        user['status']
    )
    return current_number

if __name__ == '__main__':
    print('Iniciando el bot')
    bot.infinity_polling()
    print('Fin')
