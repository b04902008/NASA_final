import pygame as pg
import time

import Model.main as model
from EventManager import *
from MainConst import *
from View.const import *

class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """
    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.

        Attributes:
            isinitialized (bool)
            screen (pg.Surface)
            clock (Clock)
            smallfont (pg,font.Font)
        """
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model

        self.isinitialized = False
        self.screen = None
        self.clock = None
        self.smallfont = None
        self.mediumfont = None
        self.bigfont = None

    def __str__(self):
        return "View"

    def notify(self, event):
        """
        Receive events posted to the message queue.
        """
        if isinstance(event, Event_EveryTick) and self.isinitialized:
            cur_state = self.model.state.peek()
            if cur_state == model.STATE_MENU:
                self.RenderBasic()
                self.RenderMenu()
            elif cur_state == model.STATE_RENEW:
                self.RenderBasic()
                self.RenderRenew()
            pg.display.set_caption(GameCaption)
            # limit the redraw speed to 30 frames per second
            self.clock.tick(FramePerSec)
        elif isinstance(event, Event_Initialize):
            self.initialize()
        elif isinstance(event, Event_Quit):
            # shut down the pygame graphics
            self.isinitialized = False
            pg.quit()
    
    def RenderBasic(self):
        """
        Render the background.
        """
        # draw backgound
        self.screen.fill(Color_White)
        pg.draw.rect(self.screen, Color_SeaGreen, [0, 0, 900, 120])
        pg.draw.rect(self.screen, Color_White, [100+30, 25, 70, 70])
        pg.draw.rect(self.screen, Color_White, [100+140, 25, 70, 70])
        pg.draw.rect(self.screen, Color_White, [100+250, 25, 70, 70])
        pg.draw.rect(self.screen, Color_White, [100+360, 25, 70, 70])
        pg.draw.rect(self.screen, Color_White, [100+470, 25, 70, 70])
        pg.draw.rect(self.screen, Color_White, [100+580, 25, 70, 70])
        pg.draw.rect(self.screen, Color_White, [100+690, 25, 70, 70])
        # load image
        picture1 = pg.image.load('View/image/floor{}.jpg'.format(self.model.floor))
        (SurfaceX1, SurfaceY1) = picture1.get_size()
        PosX1 = 100
        PosY1 = 120 + (480 - SurfaceY1)/2
        self.screen.blit(picture1, (PosX1, PosY1))
        picture2 = pg.image.load('View/image/icon.jpg')
        (SurfaceX2, SurfaceY2) = picture2.get_size()
        PosX2 = 725
        PosY2 = 250
        self.screen.blit(picture2, (PosX2, PosY2))
        # "Floor Plan"
        words1 = self.mediumfont.render("Floor", True, Color_White)
        (SurfaceX1, SurfaceY1) = words1.get_size()
        words2 = self.mediumfont.render("Plan", True, Color_White)
        (SurfaceX2, SurfaceY2) = words2.get_size()
        PosX1 = 25
        PosY1 = (120 - SurfaceY1 - SurfaceY2)/2
        PosX2 = PosX1
        PosY2 = PosY1+SurfaceY1
        self.screen.blit(words1, (PosX1, PosY1))
        self.screen.blit(words2, (PosX2, PosY2))
        # "B1"~"6F"
        words = self.bigfont.render("B1", True, Color_Black)
        (SurfaceX, SurfaceY) = words.get_size()
        PosX = 130 + (70 - SurfaceX)/2
        PosY = 25 + (70 - SurfaceY)/2
        self.screen.blit(words, (PosX, PosY))
        for i in range(1, 7):
            words = self.bigfont.render("{}F".format(i), True, Color_Black)
            (SurfaceX, SurfaceY) = words.get_size()
            PosX = 130 + 110*i + (70 - SurfaceX)/2
            PosY = 25 + (70 - SurfaceY)/2
            self.screen.blit(words, (PosX, PosY))

    def RenderMenu(self):
        """
        Render the game menu.
        """
        # "B1"~"6F"
        i = self.model.key
        if i%8 == 0:
            if i == 0:
                pg.draw.rect(self.screen, Color_LightGray, [130, 25, 70, 70])
            elif i == 8:
                pg.draw.rect(self.screen, Color_Gray, [130, 25, 70, 70])
            words = self.bigfont.render("B1", True, Color_Black)
            (SurfaceX, SurfaceY) = words.get_size()
            PosX = 130 + (70 - SurfaceX)/2
            PosY = 25 + (70 - SurfaceY)/2
            self.screen.blit(words, (PosX, PosY))
        elif i%8 > 0 and i%8 <7: 
            if i < 7:
                pg.draw.rect(self.screen, Color_LightGray, [130+110*i, 25, 70, 70])
            elif i > 8:
                i -= 8
                pg.draw.rect(self.screen, Color_Gray, [130+110*i, 25, 70, 70])
            words = self.bigfont.render("{}F".format(i), True, Color_Black)
            (SurfaceX, SurfaceY) = words.get_size()
            PosX = 130 + 110*i + (70 - SurfaceX)/2
            PosY = 25 + (70 - SurfaceY)/2
            self.screen.blit(words, (PosX, PosY))
        # key
        pg.draw.rect(self.screen, Color_Silver, [725, 150, 100, 50])
        words1 = self.mediumfont.render("renew", True, Color_Black)
        (SurfaceX1, SurfaceY1) = words1.get_size()
        PosX1 = 725 + (100 - SurfaceX1)/2
        PosY1 = 150 + (50 - SurfaceY1)/2
        self.screen.blit(words1, (PosX1, PosY1))
        # write some words
        words2 = self.smallfont.render("choose the floor &", True, Color_Black)
        (SurfaceX2, SurfaceY2) = words2.get_size()
        PosX2 = 725 + (100 - SurfaceX2)/2
        PosY2 = 200
        self.screen.blit(words2, (PosX2, PosY2))
        words3 = self.smallfont.render("click the button above", True, Color_Black)
        (SurfaceX3, SurfaceY3) = words3.get_size()
        PosX3 = 725 + (100 - SurfaceX3)/2
        PosY3 = 200 + SurfaceY2
        self.screen.blit(words3, (PosX3, PosY3))
        # update surface
        pg.display.flip()

    def RenderRenew(self):
        """
        Render the renew screen.
        """
        # key
        if self.model.pos:
            if self.model.sh == 1:
                pg.draw.rect(self.screen, Color_LightGray, [725, 150, 100, 50])
                words1 = self.mediumfont.render("wait", True, Color_Gray)
            else:
                pg.draw.rect(self.screen, Color_Silver, [725, 150, 100, 50])
                words1 = self.mediumfont.render("start", True, Color_Black)
        else:
            pg.draw.rect(self.screen, Color_LightGray, [725, 150, 100, 50])
            words1 = self.mediumfont.render("start", True, Color_Gray)
        (SurfaceX1, SurfaceY1) = words1.get_size()
        PosX1 = 725 + (100 - SurfaceX1)/2
        PosY1 = 150 + (50 - SurfaceY1)/2
        self.screen.blit(words1, (PosX1, PosY1))
        # write some words
        if self.model.pos:
            if self.model.sh == 1:
                words2 = self.smallfont.render("Updating...", True, Color_Black)
            else:
                words2 = self.smallfont.render("click the button to start", True, Color_Black)
        else:
            words2 = self.smallfont.render("doesn't choose the position", True, Color_Black)
        (SurfaceX2, SurfaceY2) = words2.get_size()
        PosX2 = 725 + (100 - SurfaceX2)/2
        PosY2 = 200
        self.screen.blit(words2, (PosX2, PosY2))
        # draw lines
        hStart = [chunkStart[0]+trans[0], chunkStart[1]+trans[1]]
        hEnd = [hStart[0]+chunkNum[0]*chunkSize[0], hStart[1]]
        pg.draw.line(self.screen, Color_Black, hStart, hEnd, 1)
        for j in range(chunkNum[1]):
            hStart[1] += chunkSize[1]
            hEnd[1] += chunkSize[1]
            pg.draw.line(self.screen, Color_Black, hStart, hEnd, 1)
        vStart = [chunkStart[0]+trans[0], chunkStart[1]+trans[1]]
        vEnd = [vStart[0], vStart[1]+chunkSize[1]*chunkNum[1]]
        pg.draw.line(self.screen, Color_Black, vStart, vEnd, 1)
        for i in range(chunkNum[0]):
            vStart[0] += chunkSize[0]
            vEnd[0] += chunkSize[0]
            pg.draw.line(self.screen, Color_Black, vStart, vEnd, 1)
        # draw chunk
        if self.model.pos:
            GridPointX = chunkStart[0] + trans[0] + chunkSize[0] * self.model.pos[0]
            GridPointY = chunkStart[1] + trans[1] + chunkSize[1] * self.model.pos[1]
            start = [GridPointX+1, GridPointY+int(chunkSize[1])/2]
            end = [GridPointX+int(chunkSize[0])-1, start[1]]
            pg.draw.line(self.screen, Color_Gray, start, end, int(chunkSize[1])-1)
        # update surface
        pg.display.flip()

    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """
        result = pg.init()
        pg.font.init()
        pg.display.set_caption(GameCaption)
        self.screen = pg.display.set_mode(ScreenSize)
        self.clock = pg.time.Clock()
        self.smallfont = pg.font.Font(None, 25)
        self.mediumfont = pg.font.Font(None, 45)
        self.bigfont = pg.font.Font(None, 75)
        self.isinitialized = True