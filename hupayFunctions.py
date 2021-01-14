import json

def greetBack(bot, chat_id, name):
    bot.send_message(chat_id, "Hello to you too, " + name + "!")

def displayHelp(bot, chat_id):
    bot.send_message(chat_id, "Here are the available commands for me:\n" \
                                "/start - Start the bot\n" \
                                "/stop - Stop the bot and delete the records for this group\n" \
                                "/addpayee - Add a person to the list of payees\n" \
                                "/deletepayee - Delete a person from the list of payees\n" \
                                "/viewpayees - View the current list of payees\n" \
                                "/addbill - Add a bill to the list of bills\n" \
                                "/deletebill - Delete a bill from the list of bills\n" \
                                "/viewbills - View the current list of bills\n" \
                                "/calculate - Calculate the total bill and split among payees\n" \
                                )

# start - Start the bot
# stop - Stop the bot and delete the records for this group
# addpayee - Add a person to the list of payees
# deletepayee - Delete a person from the list of payees
# viewpayees - View the current list of payees
# addbill - Add a bill to the list of bills
# deletebill - Delete a bill from the list of bills
# viewbills - View the current list of bills
# calculate - Calculate how much each person owe or how much they should get back

def getStarted(chat_id):
    database = importJson('hupayDatabase.json')
    try:
        return bool(database[str(chat_id)]['group_values']['started'])
    except: return False

def getPayeeAddMode(chat_id):
    database = importJson('hupayDatabase.json')
    return (database[str(chat_id)]['group_values']['payee_add_mode']) == "True"

def getPayeeDeleteMode(chat_id):
    database = importJson('hupayDatabase.json')
    return (database[str(chat_id)]['group_values']['payee_delete_mode']) == "True"

def getBillAddMode(chat_id):
    database = importJson('hupayDatabase.json')
    return (database[str(chat_id)]['group_values']['bill_add_mode']) == "True"

def getBillDeleteMode(chat_id):
    database = importJson('hupayDatabase.json')
    return (database[str(chat_id)]['group_values']['bill_delete_mode']) == "True"

def getKNNCount(chat_id):
    database = importJson('hupayDatabase.json')
    return int(database[str(chat_id)]['group_values']['knn_count'])

def updateDBGroupValue(chat_id, variable, updated_value):
    database = importJson('hupayDatabase.json')
    database[str(chat_id)]['group_values'][variable] = updated_value
    writeJson('hupayDatabase.json', database)

def importJson(filename):
    with open(filename, 'r') as myFile:
        data = myFile.read()
    
    obj = json.loads(data)
    return obj

def writeJson(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def createData(chat_id):
    database = importJson('hupayDatabase.json')
    newDataEntry = """{"group_values": {"started": "False", "payee_add_mode": "False", "payee_delete_mode": "False", \
        "bill_add_mode": "False", "bill_delete_mode": "False", "knn_count": "0"}, "payees": [], "bills": { }}"""
    database[str(chat_id)] = json.loads(newDataEntry)
    writeJson('hupayDatabase.json', database)

def viewPayees(bot, chat_id):
    database = importJson('hupayDatabase.json')
    current_group = database[str(chat_id)]
    message = ""
    if not current_group['payees']:
        message = "There are no payees for this group currently."
    else:
        message = "The current payees are: \n"
        for payee in current_group['payees']:
            message += payee + "\n"
    bot.send_message(chat_id, message)

def viewBills(bot, chat_id):
    database = importJson('hupayDatabase.json')
    current_group = database[str(chat_id)]
    bills = current_group['bills']
    message = ""
    if not current_group['bills']:
        message = "There are no bills for this group currently."
    else:
        message = "The current bills are: \n"
        for bill_name in bills.keys():
            message += "{} @ {} paid by ${}\n".format(bill_name, bills[bill_name]['bill_amount'], bills[bill_name]['bill_paid_by'])
    bot.send_message(chat_id, message)

def deleteData(chat_id):
    database = importJson('hupayDatabase.json')
    database.pop(str(chat_id))
    writeJson('hupayDatabase.json', database)

def addPayee(chat_id, payee):
    if len(payee.split()) != 1:
        return False
    else:
        database = importJson('hupayDatabase.json')
        database[str(chat_id)]["payees"].append(payee)
        writeJson('hupayDatabase.json', database)
        return True
    
def addBill(chat_id, bill):
    bill_details = bill.split()
    if len(bill_details) != 3:
        return False
    else:
        try:
            float(bill_details[1])
        except:
            return False
        
        
    database = importJson('hupayDatabase.json')
    database[str(chat_id)]["bills"][bill_details[0]] = {"bill_amount": bill_details[1], "bill_paid_by": bill_details[2]}
    writeJson('hupayDatabase.json', database)
    return True

def deletePayee(chat_id, payee):
    try:
        database = importJson('hupayDatabase.json')
        database[str(chat_id)]["payees"].remove(payee)
        writeJson('hupayDatabase.json', database)
        return True
    except: return False

def deleteBill(chat_id, bill):
    try:
        database = importJson('hupayDatabase.json')
        database[str(chat_id)]["bills"].pop(bill)
        writeJson('hupayDatabase.json', database)
        return True
    except: return False

def calcData(bot, chat_id):
    database = importJson('hupayDatabase.json')
    payees = database[str(chat_id)]["payees"]
    no_of_payees = len(payees)                                                                  # number of payees
    bills = database[str(chat_id)]["bills"]
    total_amt = 0
    dict_debts = {}                                                                             # records of how much each person owes 
    for bill_name in bills.keys():
        total_amt += float(bills[bill_name]["bill_amount"])                                     # total bill
        dict_debts[bills[bill_name]["bill_paid_by"]] = -1 * float(bills[bill_name]["bill_amount"])     # negative value for people who paid
    each_payee_amt = total_amt / no_of_payees                                                   # how much each person owes
    for payee in payees:
        if payee in dict_debts.keys():
            dict_debts[payee] += each_payee_amt
        else:
            dict_debts[payee] = each_payee_amt
    
    bot.send_message(chat_id, "All calculated!")
    last_msg = ""
    for payee in dict_debts.keys():
        if dict_debts[payee] >= 0:
            last_msg += "{} owes ${}.\n".format(payee, round(dict_debts[payee], 2))
        else:
            last_msg += "{} should get back ${}.\n".format(payee, round((-1 * dict_debts[payee]), 2))
    print(last_msg)
    bot.send_message(chat_id, last_msg)

    

    


sample_database = {
    12345: {
        "booleans": {
            "started": "False",
            "payee_add_mode": "False",
            "payee_delete_mode": "False",
            "bill_add_mode": "False",
            "bill_delete_mode": "False",
            "knn_count": "0"
        },
        "payees": ["@username1", "@username2", "@username3"],
        "bills": {
            "<bill_name>": {
                "bill_amount": 12.30,
                "bill_paid_by": "<@username>"
            },
            "<bill_name2>": {
                "bill_amount": 9.30,
                "bill_paid_by": "<@username2>"
            }
        }
    }
}

sample_update = {
    'update_id': '162311945', 
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

