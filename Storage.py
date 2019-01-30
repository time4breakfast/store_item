#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from sqlite3 import Error
#import pandas as pd
#import gKeep

class Storage:

    def __init__(self):
        print("Connecting to database")
        self.cols = ['product', 'least', 'reorder', 'mhd', 'quantity', 'storageplace']
        self.df = 'test' #pd.DataFrame(columns = self.cols)
        self.stoplc = {'1':'first place'}

    def testing_dummy_function(self, intent):
        print(intent)
        item = intent.get('slots')[0].get('value').get('value').lower()

        item = [item.value.encode('utf8') for item in intent.slots.item.all()][0]
        return "Hallo"

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

    def getDataFrameFromDB(self, db_name, tablename = 'vorraete'):
        try:
            conn = sqlite3.connect(db_name)
            cur = conn.cursor()
            res = cur.execute("SELECT * FROM " + tablename)
            #self.df = pd.DataFrame(res.fetchall())
            #self.df.columns = self.cols
            conn.close()
            return self.df
        except Error as e:
            print(e)

    def getAmountOf(self, intent):
        # get item
        print(intent)
        #itemlist = [item.value.encode('utf8') for item in intent.slots.item.all()][0]
        #item = itemlist

        #conn = sqlite3.connect('vorraete.db')
        #cur = conn.cursor()
        #result = cur.execute("""SELECT quantity FROM vorraete where product = '""" + item + """'""")
        #amount = result.fetchall()[0][0]

        #cur.close()
        #del cur
        #conn.close()
        return intent

    # add entry to database
    def addEntryToVorraete(self, item, amount = 1, moreOrLess = True, stoplc = 0, least = 1, reorder = 0, mhd = None):
        """
        Add a new entry
        :param item: Name of the entry, e.g. Tomaten, Spaghetti
        :param amount: how much we have (bought)
        :param least: how much has to be there at least at every point in time
        :param reorder:
        :param mhd:
        :return:
        """

        self.df = self.df.reset_index(drop = True)

        # check if item is already in storage and if yes get its index
        tempdf = self.df[self.df['product'] == str(item).lower()]
        if tempdf.shape[0] > 0:
            idx = tempdf.index[0]
            item = str(item).lower()

            # get current amount and add to shoppinglist if necessary
            cur_amount = tempdf[tempdf['product'] == item]['quantity'].iloc[0]
            least = tempdf[tempdf['product'] == item]['least'].iloc[0]
            if cur_amount < least:
                amount = least - cur_amount + 1
                #gKeep.gKeep.addItemToShoppingList(item, amount)

            # update db entry
            if moreOrLess:
                self.df['quantity'][idx] += int(amount)
            else:
                self.df['quantity'][idx] -= int(amount)
            if mhd:
                print("you still need to implement this")

            try:
                conn = sqlite3.connect('vorraete.db')
                #tdf = tdf.drop(columns=['id'])
                tdf = self.df.reset_index(drop = True)
                tdf.to_sql('vorraete', conn, if_exists = 'replace', index = False)
                conn.close()
                print('changed quantity of ' + str(item) + " by " + str(amount))
            except Error as e:
                print(e)
            return self.df
        else:
            _id = self.df.shape[0] + 1
            item = str(item).lower()

            # self.df = self.df.append(pd.DataFrame([[_id, item, least, reorder, mhd, amount, stoplc]], columns = self.cols))
            #self.df = self.df.append(pd.DataFrame([[item, least, reorder, mhd, amount, stoplc]], columns=self.cols))
            self.df = self.df.reset_index(drop=True)
            # tdf = self.df.drop(columns=['id'])
            try:
                conn = sqlite3.connect('vorraete.db')
                self.df.to_sql('vorraete', conn, if_exists='replace', index=False)
                print("Added " + str(item) + " to storage.")
                conn.close()
            except Error as e:
                print(e)

    # delete entry from database
    def deleteItemFromVorraete(self, item):
        """
        if an entry should be deleted for good
        :param item:
        :return:
        """
        tempdf = self.df[self.df['product'] == str(item).lower()]
        if tempdf.shape[0] > 0:
            idx = tempdf.index[0]
            item = str(item).lower()

            try:
                self.df = self.df.drop(axis=0, index=idx)
                self.df = self.df.reset_index(drop=True)
                #tdf = self.df.drop(columns=['id'])
                conn = sqlite3.connect('vorraete.db')
                self.df.to_sql('vorraete', conn, if_exists='replace', index=False)
                conn.close()
            except Error as e:
                print(e)
            return self.df
        else:
            return "Could not locate item."