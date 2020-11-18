class BaseEvent(object):
    """
    A superclass for any events that might be generated by
    an object and sent to the EventManager.
    """
    def __init__(self):
        self.name = "Generic event"
    def __str__(self):
        return self.name

class Event_Initialize(BaseEvent):
    """
    Tells all listeners to initialize themselves.
    
    Avoid initializing such things within listener __init__ calls 
    to minimize snafus (if some rely on others being yet created.)
    """
    def __init__ (self):
        self.name = "Initialize event"

class Event_EveryTick(BaseEvent):
    def __init__ (self):
        self.name = "Tick event"

class Event_StateChange(BaseEvent):
    """
    Change the model state machine.
    Given a None state will pop() instead of push.
    """
    def __init__(self, state):
        self.name = "State change event"
        self.state = state
    def __str__(self):
        if self.state:
            return '%s pushed %s' % (self.name, self.state)
        else:
            return '%s popped' % (self.name)

class Event_FloorChange(BaseEvent):
    def __init__(self, floor):
        self.name = "Floor change event"
        self.floor = floor

class Event_ColorChange(BaseEvent):
    def __init__(self, key):
        self.name = "Color change event"
        self.key = key

class Event_ChoosePos(BaseEvent):
    def __init__(self, pos):
        self.name = "Choose position event"
        self.pos = pos

class Event_RenewData(BaseEvent):
    def __init__(self):
        self.name = "Renew data event"

class Event_Quit(BaseEvent):
    def __init__ (self):
        self.name = "Quit event"
"""
class Event_Input(BaseEvent):
    #Keyboard or mouse input event.
    def __init__(self, unicodechar, clickpos):
        self.name = "Input event"
        self.char = unicodechar
        self.clickpos = clickpos
    def __str__(self):
        return '%s, char=%s, clickpos=%s' % (self.name, self.char, self.clickpos)
"""
class EventManager(object):
    """
    We coordinate communication between the Model, View, and Controller.
    """
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()

    def RegisterListener(self, listener):
        """
        Adds a listener to our spam list. 
        It will receive Post()ed events through it's notify(event) call. 
        """
        self.listeners[listener] = 1

    def UnregisterListener(self, listener):
        """
        Remove a listener from our spam list.
        This is implemented but hardly used.
        Our weak ref spam list will auto remove any listeners who stop existing.
        """
        if listener in self.listeners.keys():
            del self.listeners[listener]
        
    def post(self, event):
        """
        Post a new event to the message queue.
        It will be broadcast to all listeners.
        """
        for listener in self.listeners.keys():
            # debug # if not isinstance(event, Event_EveryTick) and not isinstance(event, Event_UpdateTroops):
            # debug #     print("notify", str(event), "to", str(listener))
            listener.notify(event)