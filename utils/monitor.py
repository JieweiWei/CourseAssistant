import pythoncom, pyHook, time
import os

from screenshot import window_capture

def onMouseEvent(event):
    if str(event.MessageName) == 'mouse left up':
        print 'fetch mouse event'
        file_name = window_capture(_dpath)
        shared_handler.send_updates('/static/screenshot/' + file_name);
    return True

def onKeyboardEvent(event):
    if str(event.Key) == 'Up' or str(event.Key) == 'Down' or\
    str(event.Key) == 'Left' or str(event.Key) == 'Right':
        print 'fetch keyboard event'
        file_name = window_capture(_dpath)
        shared_handler.send_updates('/static/screenshot/' + file_name);
    return True

def main(dpath, handler):
    print 'start to screen monitoring...'
    global _dpath
    _dpath = dpath
    global shared_handler
    shared_handler = handler
    hm = pyHook.HookManager()
    hm.MouseAll = onMouseEvent
    hm.HookMouse()
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()