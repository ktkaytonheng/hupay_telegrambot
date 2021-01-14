import requests
import datetime
from hupayFunctions import *

class BotHandler:
    def __init__(self, token):
            self.token = token
            self.api_url = "https://api.telegram.org/bot{}/".format(token)

    #url = "https://api.telegram.org/bot<token>/"

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_first_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[0]
        else:
            last_update = None

        return last_update


token = '1538662225:AAF_weoXjinWko9-DlgUbqVsTrMuK48pXi4' #Token of your bot
hupay_bot = BotHandler(token) #Your bot's name

greetings = "hello!Hello!hi!Hi!hey!Hey!what's up!What's up!sup!Sup!"


def main():
    new_offset = 0
    print('Now launching Hupay...')
    while True:
        all_updates=hupay_bot.get_updates(new_offset)

        if len(all_updates) > 0:
            for current_update in all_updates:
                print(current_update)
                first_update_id = current_update['update_id']

                try:
                    first_chat_text = current_update['message']['text']
                    first_chat_id = current_update['message']['chat']['id']
                    if 'first_name' in current_update['message']:
                        first_chat_name = current_update['message']['chat']['first_name']
                    elif 'new_chat_member' in current_update['message']:
                        first_chat_name = current_update['message']['new_chat_member']['username']
                    elif 'from' in current_update['message']:
                        first_chat_name = current_update['message']['from']['first_name']
                    else:
                        first_chat_name = "unknown"
                except:
                    continue
                # Commands for bot for both idle and when started
                if first_chat_text in greetings:
                    greetBack(hupay_bot, first_chat_id, first_chat_name)
                    new_offset = first_update_id + 1
                    continue
                elif first_chat_text == "/help" or first_chat_text == "/help@hupay_bot":
                    displayHelp(hupay_bot, first_chat_id)
                    new_offset = first_update_id + 1
                    continue

                # Commands for the bot during idle
                if not getStarted(first_chat_id):
                    if first_chat_text == "/start" or first_chat_text == "/start@hupay_bot":
                        createData(first_chat_id)
                        hupay_bot.send_message(first_chat_id, "Alright, what do you need?")
                    elif first_chat_text == "/stop" or first_chat_text == "/stop@hupay_bot":
                        hupay_bot.send_message(first_chat_id, "Maybe start me first?")

                # Commands for the bot when its started
                else:
                    

                    if first_chat_text.lower() in "kanninakanninakaninakaninaknnknn":
                        if getKNNCount(first_chat_id) == 0:
                            hupay_bot.send_message(first_chat_id, "诶儿子，你不能这么说， 这么说是不好的孩子啊。")
                            updateDBGroupValue(first_chat_id, "knn_count", "1")
                        elif getKNNCount(first_chat_id) == 1:
                            hupay_bot.send_message(first_chat_id, "诶， 不行！")
                            updateDBGroupValue(first_chat_id, "knn_count", "2")
                        elif getKNNCount(first_chat_id) == 2:
                            hupay_bot.send_message(first_chat_id, "<b>诶KANNINA 我GEN你讲!$#%$^!</b>")
                            hupay_bot.send_message(first_chat_id, "<b>BU要JIANGLIAO1!#!$%^#!$</b>")
                            updateDBGroupValue(first_chat_id, "knn_count", "0")
                        new_offset = first_update_id + 1
                        continue
                    else:
                        
                        if not getPayeeAddMode(first_chat_id) and not getPayeeDeleteMode(first_chat_id) and not getBillAddMode(first_chat_id) and not getBillDeleteMode(first_chat_id):
                            if first_chat_text == "/calculate" or first_chat_text == "/calculate@hupay_bot":
                                calcData(hupay_bot, first_chat_id)
                                deleteData(first_chat_id)
                            elif first_chat_text == "/stop" or first_chat_text == "/stop@hupay_bot":
                                deleteData(first_chat_id)
                                updateDBGroupValue(first_chat_id, "started", "False")
                                hupay_bot.send_message(first_chat_id, "Alright let me know if you need me again.")
                            elif first_chat_text == "/start" or first_chat_text == "/start@hupay_bot":
                                hupay_bot.send_message(first_chat_id, "I'm already started! Just let me know what you need.")
                            elif first_chat_text == "/addpayee" or first_chat_text == "/addpayee@hupay_bot":
                                updateDBGroupValue(first_chat_id, "payee_add_mode", "True")
                                hupay_bot.send_message(first_chat_id, "Enter the username of the payee, for e.g. @mikehawk")
                            elif first_chat_text == "/deletepayee" or first_chat_text == "/deletepayee@hupay_bot":
                                updateDBGroupValue(first_chat_id, "payee_delete_mode", "True")
                                hupay_bot.send_message(first_chat_id, "Enter the name of the payee that you want to delete.")
                            elif first_chat_text == "/viewpayees" or first_chat_text == "/viewpayees@hupay_bot":
                                viewPayees(hupay_bot, first_chat_id)
                            elif first_chat_text == "/addbill" or first_chat_text == "/addbill@hupay_bot":
                                updateDBGroupValue(first_chat_id, "bill_add_mode", "True")
                                hupay_bot.send_message(first_chat_id, "Enter the details of the bill in the following format")
                                hupay_bot.send_message(first_chat_id, "for e.g. Mala 20.30 @mikehawk")
                            elif first_chat_text == "/deletebill" or first_chat_text == "/deletebill@hupay_bot":
                                updateDBGroupValue(first_chat_id, "bill_delete_mode", "True")
                                hupay_bot.send_message(first_chat_id, "Enter the name of the bill that you want to delete.")
                            elif first_chat_text == "/viewbills" or first_chat_text == "/viewbills@hupay_bot":
                                viewBills(hupay_bot, first_chat_id)

                        elif getPayeeAddMode(first_chat_id):
                            success = addPayee(first_chat_id, first_chat_text)
                            if success:
                                updateDBGroupValue(first_chat_id, "payee_add_mode", "False")
                                hupay_bot.send_message(first_chat_id, "Payee added successfully!")
                            else:
                                hupay_bot.send_message(first_chat_id, "Something went wrong... try again. \nMake sure to follow the format.")
                        elif getBillAddMode(first_chat_id):
                            success = addBill(first_chat_id, first_chat_text)
                            if success:
                                updateDBGroupValue(first_chat_id, "bill_add_mode", "False")
                                hupay_bot.send_message(first_chat_id, "Bill added successfully!")
                            else:
                                hupay_bot.send_message(first_chat_id, "Something went wrong... try again. \nMake sure to follow the format.")
                        elif getPayeeDeleteMode(first_chat_id):
                            success = deletePayee(first_chat_id, first_chat_text)
                            if success:
                                updateDBGroupValue(first_chat_id, "payee_delete_mode", "False")
                                hupay_bot.send_message(first_chat_id, "Payee deleted successfully!")
                            else:
                                hupay_bot.send_message(first_chat_id, "Something went wrong... try again. \nMake sure to follow the format.")
                        elif getBillDeleteMode(first_chat_id):
                            success = deleteBill(first_chat_id, first_chat_text)
                            if success:
                                updateDBGroupValue(first_chat_id, "bill_delete_mode", "False")
                                hupay_bot.send_message(first_chat_id, "Bill deleted successfully!")
                            else:
                                hupay_bot.send_message(first_chat_id, "Something went wrong... try again. \nMake sure to follow the format.")
                        

                        
                new_offset = first_update_id + 1

sample_command = {
                    'update_id': 162312000, 
                    'message': {
                        'message_id': 114, 
                        'from': {
                            'id': 265858778, 
                            'is_bot': False, 
                            'first_name': 'Kayton', 
                            'username': 'kayleidoscopee', 
                            'language_code': 'en'
                        }, 
                        'chat': {
                            'id': -429054345, 
                            'title': 'TEZ OF KNEWLEDGE', 
                            'type': 'group', 
                            'all_members_are_administrators': True
                        }, 
                        'date': 1610608266, 
                        'text': '/help@hupay_bot', 
                        'entities': [{
                            'offset': 0,
                            'length': 15,
                            'type': 'bot_command'
                        }]
                    }
                }

sample_text = {
                'update_id': 162311945, 
                'message': {
                    'message_id': 5, 
                    'from': {
                        'id': 265858778, 
                        'is_bot': False, 
                        'first_name': 'Kayton', 
                        'username': 'kayleidoscopee', 
                        'language_code': 'en'
                    },
                    'chat': {
                        'id': 265858778, 
                        'first_name': 'Kayton', 
                        'username': 'kayleidoscopee', 
                        'type': 'private'
                    }, 
                    'date': 1610599828, 
                    'text': 'Hi'
                }
              }

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()