import sys
import util

COLORS = {
    "red": "\x1b[31m",
    "black": "\x1b[0m"
}

DISPLAY_VERBOSE = False

def message(msg, verbose=False):
    if DISPLAY_VERBOSE or not verbose:
        print '*** %s' % msg

def line():
    print '*' * 80

def error(msg, exit=False, verbose=False):
    if DISPLAY_VERBOSE or not verbose:
        sys.stderr.write('%s*** %s%s\n' % (COLORS['red'], msg, COLORS['black']))
    if exit: sys.exit(-1)
    
def trace(fn):
    def wrapped(*args, **kwargs):
        formatted_args = ", ".join(util.shorten(arg) for arg in args)
        
        if len(kwargs) > 0:
            formatted_kwargs = "%s=%s" % (util.shorten(key), \
                util.shorten(value)) for (key, value) in kwargs.iteritems()
            
            formatted_args += ", %s" % ", ".join(formatted_kwargs)
        
        message("%s(%s)" % (fn.__name__, formatted_args), verbose=True)
        return fn(*args, **kwargs)
        
    return wrapped