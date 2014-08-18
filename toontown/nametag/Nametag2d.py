from direct.task.Task import Task
import math
from pandac.PandaModules import *

from toontown.margins.MarginVisible import MarginVisible
from toontown.nametag import Nametag
from toontown.nametag import NametagGlobals


class Nametag2d(Nametag.Nametag, MarginVisible):
    CONTENTS_SCALE = 0.25

    CHAT_TEXT_WORD_WRAP = 8

    ARROW_OFFSET = -1.0
    ARROW_SCALE = 1.5

    def __init__(self):
        Nametag.Nametag.__init__(self)
        MarginVisible.__init__(self)

        self.arrow = None

        self.hideThought()
        self.contents.setScale(Nametag2d.CONTENTS_SCALE)
        self.setChatWordWrap(Nametag2d.CHAT_TEXT_WORD_WRAP)

    def destroy(self):
        Nametag.Nametag.destroy(self)

        if self.arrow:
            self.arrow.removeNode()
            self.arrow = None

    def getChatBalloonModel(self):
        return NametagGlobals.chatBalloon2dModel

    def getChatBalloonWidth(self):
        return NametagGlobals.chatBalloon2dWidth

    def getChatBalloonHeight(self):
        return NametagGlobals.chatBalloon2dHeight

    def tick(self, task):
        if (self.getCell() is None) or (self.arrow is None):
            return Task.cont

        if (self.avatar is None) or self.avatar.isEmpty():
            return Task.cont

        if hasattr(base, 'localAvatar'):
            me = base.localAvatar
        else:
            me = base.cam
        location = self.avatar.getPos(me)
        rotation = me.getQuat(base.cam)

        camSpacePos = rotation.xform(location)
        arrowRadians = math.atan2(camSpacePos[0], camSpacePos[1])
        arrowDegrees = (arrowRadians/math.pi) * 180

        self.arrow.setR(arrowDegrees - 90)
        return Task.cont

    def drawChatBalloon(self):
        self.setChatText(self.getText() + ': ' + self.getChatText())

        # When a chat balloon is active, we need a slightly higher priority in
        # the margin system:
        self.setPriority(1)

        if self.arrow is not None:
            self.arrow.removeNode()
            self.arrow = None

        Nametag.Nametag.drawChatBalloon(self)

        # Calculate the center of the TextNode:
        left, right, bottom, top = self.chatTextNode.getFrameActual()
        center = self.contents.getRelativePoint(
            self.chatBalloon.textNodePath,
            ((left+right) / 2.0, 0, (bottom+top) / 2.0))

        # Translate the chat balloon along the inverse:
        self.chatBalloon.setPos(self.chatBalloon, -center)

    def drawNametag(self):
        Nametag.Nametag.drawNametag(self)

        self.setPriority(0)

        # Add an arrow:
        self.arrow = NametagGlobals.arrowModel.copyTo(self.contents)
        self.arrow.setZ(Nametag2d.ARROW_OFFSET + self.nameTextNode.getBottom())
        self.arrow.setScale(Nametag2d.ARROW_SCALE)
        self.arrow.setColor(self.nametagColor[0][0])
