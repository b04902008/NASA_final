import pygame as pg

import Model.main as model
from EventManager import *
from MainConst import *
from Controller.const import *

class Control(object):
    """
    Handles control input.
    """
    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model

    def __str__(self):
        return "Controller"

    def notify(self, event):
        """
        Receive events posted to the message queue.
        """
        if isinstance(event, Event_EveryTick):
            # Called for each game tick. We check our keyboard presses here.
            for event in pg.event.get():
                # handle window manager closing our window
                if event.type == pg.QUIT:
                    self.evManager.post(Event_Quit())
                else:
                    cur_state = self.model.state.peek()
                    if cur_state == model.STATE_MENU:
                        self.CtrlMenu(event)
                    elif cur_state == model.STATE_RENEW:
                        self.CtrlRenew(event)

    def CtrlMenu(self, event):
        """
        Handles menu events.
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.evManager.post(Event_StateChange(None))
        elif event.type == pg.MOUSEMOTION:
            if event.pos[1] > 25 and event.pos[1] < 95:
                if event.pos[0] > 130 and event.pos[0] < 200:
                    self.evManager.post(Event_ColorChange(0))
                elif event.pos[0] > 240 and event.pos[0] < 310:
                    self.evManager.post(Event_ColorChange(1))
                elif event.pos[0] > 350 and event.pos[0] < 420:
                    self.evManager.post(Event_ColorChange(2))
                elif event.pos[0] > 460 and event.pos[0] < 530:
                    self.evManager.post(Event_ColorChange(3))
                elif event.pos[0] > 570 and event.pos[0] < 640:
                    self.evManager.post(Event_ColorChange(4))
                elif event.pos[0] > 680 and event.pos[0] < 750:
                    self.evManager.post(Event_ColorChange(5))
                elif event.pos[0] > 790 and event.pos[0] < 860:
                    self.evManager.post(Event_ColorChange(6))
                else:
                    self.evManager.post(Event_ColorChange(-1))
            elif event.pos[1] > 150 and event.pos[1] < 200:
                if event.pos[0] > 725 and event.pos[0] < 825:
                    self.evManager.post(Event_ColorChange(7))
                else:
                    self.evManager.post(Event_ColorChange(-1))
            else:
                    self.evManager.post(Event_ColorChange(-1))
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if event.pos[1] > 25 and event.pos[1] < 95:
                if event.pos[0] > 130 and event.pos[0] < 200:
                    self.evManager.post(Event_FloorChange(0))
                elif event.pos[0] > 240 and event.pos[0] < 310:
                    self.evManager.post(Event_FloorChange(1))
                elif event.pos[0] > 350 and event.pos[0] < 420:
                    self.evManager.post(Event_FloorChange(2))
                elif event.pos[0] > 460 and event.pos[0] < 530:
                    self.evManager.post(Event_FloorChange(3))
                elif event.pos[0] > 570 and event.pos[0] < 640:
                    self.evManager.post(Event_FloorChange(4))
                elif event.pos[0] > 680 and event.pos[0] < 750:
                    self.evManager.post(Event_FloorChange(5))
                elif event.pos[0] > 790 and event.pos[0] < 860:
                    self.evManager.post(Event_FloorChange(6))
            elif event.pos[1] > 150 and event.pos[1] < 200:
                if event.pos[0] > 725 and event.pos[0] < 825:
                    self.evManager.post(Event_StateChange(model.STATE_RENEW))
        elif event.type == pg.MOUSEBUTTONUP:
            if event.pos[1] > 25 and event.pos[1] < 95:
                if event.pos[0] > 130 and event.pos[0] < 200:
                    self.evManager.post(Event_ColorChange(0))
                elif event.pos[0] > 240 and event.pos[0] < 310:
                    self.evManager.post(Event_ColorChange(1))
                elif event.pos[0] > 350 and event.pos[0] < 420:
                    self.evManager.post(Event_ColorChange(2))
                elif event.pos[0] > 460 and event.pos[0] < 530:
                    self.evManager.post(Event_ColorChange(3))
                elif event.pos[0] > 570 and event.pos[0] < 640:
                    self.evManager.post(Event_ColorChange(4))
                elif event.pos[0] > 680 and event.pos[0] < 750:
                    self.evManager.post(Event_ColorChange(5))
                elif event.pos[0] > 790 and event.pos[0] < 860:
                    self.evManager.post(Event_ColorChange(6))
                else:
                    self.evManager.post(Event_ColorChange(-1))
            elif event.pos[1] > 150 and event.pos[1] < 200:
                if event.pos[0] > 725 and event.pos[0] < 825:
                    self.evManager.post(Event_ColorChange(7))
                else:
                    self.evManager.post(Event_ColorChange(-1))
            else:
                    self.evManager.post(Event_ColorChange(-1))

    def CtrlRenew(self, event):
        """
        Handles renew events.
        """
        if event.type == pg.KEYDOWN:
            # escape to exit
            if event.key == pg.K_ESCAPE:
                self.evManager.post(Event_StateChange(None))
                self.evManager.post(Event_ChoosePos(None))
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if event.pos[0] >= 725 and event.pos[0] <= 825:
                if event.pos[1] >= 150 and event.pos[1] <= 200:
                    if self.model.pos:
                        self.model.sh = 1
                        self.evManager.post(Event_EveryTick())
                        self.evManager.post(Event_RenewData())
                        self.evManager.post(Event_StateChange(None))
                        self.evManager.post(Event_ChoosePos(None))
            if event.pos[0] > chunkStart[0]+trans[0] and event.pos[1] > chunkStart[1]+trans[1]:
                if (event.pos[0]-chunkStart[0]-trans[0])%chunkSize[0] and (event.pos[1]-chunkStart[1]-trans[1])%chunkSize[1]:
                    posX = (event.pos[0] - chunkStart[0] - trans[0]) / chunkSize[0]
                    posY = (event.pos[1] - chunkStart[1] - trans[1]) / chunkSize[1]
                    if posX < chunkNum[0] and posY < chunkNum[1]:
                        pos = (int(posX), int(posY))
                        self.evManager.post(Event_ChoosePos(pos))