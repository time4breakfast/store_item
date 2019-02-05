#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from sqlite3 import Error
#import gKeep

class Storage:

    def __init__(self):
        print("Connecting to database")
        self.cols = ['product', 'least', 'reorder', 'mhd', 'quantity', 'storageplace']
        self.df = 'test' #pd.DataFrame(columns = self.cols)
        self.stoplc = {'1':'first place'}

    def testing_dummy_function(self, intent_message):
        item = [item.value for item in intent_message.slots.item.all()][0]
        return item

    def createEmptyTable(self):
        # create table
        conn = sqlite3.connect('vorraete.db')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS vorraete (
                                            id integer PRIMARY KEY,
                                            product text NOT NULL,
                                            least integer,
                                            reorder integer,
                                            mhd text,
                                            quantity integer,
                                            storageplace integer);""")
        cur.close()
        del cur
        conn.close()

    def getAmountOf(self, intent_message):
        # get item
        item = [item.value for item in intent_message.slots.Menge.all()][0]
        conn = sqlite3.connect('vorraete.db')
        cur = conn.cursor()
        result = cur.execute("""SELECT quantity FROM vorraete where product = '""" + item.lower() + """'""")
        amount = result.fetchall()[0][0]

        cur.close()
        del cur
        conn.close()
        return self.makeresultsentence('getAmountOf', item, amount)

    # add entry to database
    def addEntryToVorraete(self, intent_message, amount = 1, moreOrLess = True, stoplc = 0, least = 1, reorder = 0, mhd = None):
        """
        Add a new entry
        :param item: Name of the entry, e.g. Tomaten, Spaghetti
        :param amount: how much we have (bought)
        :param least: how much has to be there at least at every point in time
        :param reorder:
        :param mhd:
        :return:
        """

        # check if item is already in storage and if yes get its index
        item = [item.value for item in intent_message.slots.item.all()][0]
        conn = sqlite3.connect('vorraete.db')
        cur = conn.cursor()
        result = cur.execute("""SELECT quantity FROM vorraete where product = '""" + item + """'""")
        amount = result.fetchall()[0][0]
        if amount != 0:
            # update db entry by 1
            amount += 1
            with conn:
                cur.execute("""UPDATE vorraete SET quantity = '""" + str(amount) + """' WHERE product = '""" + item + """'""")
        cur.close()
        del cur
        conn.close()
        return self.makeresultsentence('addEntryToVorraete', item)

    # delete entry from database
    def deleteItemFromVorraete(self, intent_message):
        """
        if an entry should be deleted for good
        :param item:
        :return:
        """
        item = [item.value for item in intent_message.slots.item.all()][0]
        return self.makeresultsentence('deleteItemFromVorraete', item)

    def makeresultsentence(self, caller, item, amount = None):
        resultsentence = 'Die Antwort ist leer.'
        if caller == 'getAmountOf':
            resultsentence = "Wir haben noch " + str(amount) + " " + item
        elif caller == 'addEntryToVorraete':
            resultsentence = "Ich habe " + str(item) + " hinzugefügt."
        elif caller == 'deleteItemFromVorraete':
            resultsentence = 'Ich habe ' + item + 'aus dem Vorrat gelöscht'
        return resultsentence