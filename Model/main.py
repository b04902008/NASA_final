import time
import random
import subprocess
import shlex
import sys, os
import pymysql

from EventManager import *
from Model.GameObject import *
from Model.StateMachine import *
from MainConst import *
from Controller.const import *

class GameEngine(object):
    """
    Tracks the game state.
    """
    def __init__(self, evManager, AIList):
        """
        evManager (EventManager): Allows posting messages to the event queue.

        Attributes:
            running (bool): True while the engine is online. Changed via Event_Quit().
            state (StateMachine()): control state change, stack data structure.
            AIList (list.str): all AI name list.
            player (list.player()): all player object.
            chunk (list.list.chunk()): all chunk objct.
            TurnTo (int): current player.
        """
        self.evManager = evManager
        evManager.RegisterListener(self)

        self.running = False
        self.state = StateMachine()
        self.AIList = AIList
        self.player = []
        self.chunk = []
        self.TurnTo = 0
        self.floor = 0
        self.pos = None
        self.sh = 0
        self.key = -1

        random.seed(time.time())

    def __str__(self):
        return "Model"

    def notify(self, event):
        """
        Receive events posted to the message queue.
        """
        if isinstance(event, Event_ColorChange):
            self.key = event.key
        elif isinstance(event, Event_FloorChange):
            self.floor = event.floor
            self.key = event.floor + 8
        elif isinstance(event, Event_ChoosePos):
            if not event.pos:
                self.pos = None
            else:
                self.pos = event.pos
        elif isinstance(event, Event_RenewData):
            #ans = os.system('sh wireless.sh')
            ans = subprocess.check_output(["sh", "wireless.sh"])
            self.sh = 0
            subans = ans[0:-1].decode("utf-8").split(' ')
            if subans[0] == "csie":
                if self.floor == 0:
                    print("-1 {} {} {} {}".format(self.pos[1], self.pos[0], subans[1], subans[2]))
                    f_id = -1
                else:
                    print("{} {} {} {} {}".format(self.floor, self.pos[1], self.pos[0], subans[1], subans[2]))
                    f_id = self.floor
            elif subans[0] == "csie-5G":
                if self.floor == 0:
                    print("-2 {} {} {} {}".format(self.pos[1], self.pos[0], subans[1], subans[2]))
                    f_id = -2
                else:
                    print("{} {} {} {} {}".format(self.floor+7, self.pos[1], self.pos[0], subans[1], subans[2]))
                    f_id = self.floor+7
            
            db = pymysql.connect("10.5.5.198", "nasa", "nasa2017", "nasafinal")
            cursor = db.cursor()
            sql_insert = "INSERT INTO sigblock_history(f_id, x_pos, y_pos, rssi, txrate) VALUES(%d, %d, %d, %f, %f)" % (f_id, self.pos[1], self.pos[0], float(subans[1]), float(subans[2]))
            sql_insert2 = "INSERT INTO sigblock(f_id, x_pos, y_pos, rssi, txrate) VALUES(%d, %d, %d, %f, %f)" % (f_id, self.pos[1], self.pos[0], float(subans[1]), float(subans[2]))
            sql_select = "SELECT COUNT(*) as count FROM sigblock WHERE f_id=%d AND x_pos=%d AND y_pos=%d" % (f_id, self.pos[1], self.pos[0])
            sql_update = "UPDATE sigblock SET rssi=%f, txrate=%f WHERE f_id=%d AND x_pos=%d AND y_pos=%d" % (float(subans[1]), float(subans[2]), f_id, self.pos[1], self.pos[0])
            try:
                cursor.execute(sql_insert)
                db.commit()
            except:
                db.rollback()
            cursor.execute(sql_select)
            results = cursor.fetchall()
            if (results[0][0] == 0):
                try:
                    cursor.execute(sql_insert2)
                    db.commit()
                except:
                    db.rollback()
            else:
                try:
                    cursor.execute(sql_update)
                    db.commit()
                except:
                    db.rollback()
            db.close()
        elif isinstance(event, Event_StateChange):
            if not event.state:
                # pop a state
                if not self.state.pop():
                    # false if no more states are left
                    self.evManager.post(Event_Quit())
            else:
                # push a new state on the stack
                self.state.push(event.state)
        elif isinstance(event, Event_Quit):
            self.running = False

    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify(). 
        """
        self.running = True
        self.evManager.post(Event_Initialize())
        self.state.push(STATE_MENU)
        while self.running:
            newTick = Event_EveryTick()
            self.evManager.post(newTick)