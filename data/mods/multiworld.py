'''
Template for module
'''

__all__ = ('start', 'stop')
# from kivy.lang import Builder


# KV_CODE = '''
# <Widget>:

# '''


def start(win, ctx):
    win.opacity = 0
    win.clearcolor = [0,0,0,0]



def stop(win, ctx):
    pass