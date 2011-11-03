import optparse
import collections
import traceback
import inspect
import sys
from helpers import *

_tasks = {}
_parser = optparse.OptionParser()
_option_names = set([])
options = {}
    
def task(fn):
    def wrapper(*args, **kwargs):
        console.line()
        console.message("Running %s" % fn.__name__)
        return fn(*args, **kwargs)

    setattr(inspect.getmodule(fn), fn.__name__, wrapper)
    _tasks[fn.__name__] = wrapper
    return wrapper
    
def add_option(short_name, long_name, default, type='bool', nargs=None, choices=None, help=None):
    if not short_name.startswith("-"):
        short_name = "-" + short_name
    if not long_name.startswith("--"):
        long_name = "--" + long_name
    
    kwargs = {
        "default": default,
        "nargs": nargs,
        "choices": choices,
        "help": help
    }

    if type == "bool":
        kwargs["action"] = "store_true"
    else:
        kwargs["action"] = "store"
        kwargs["type"] = type

    _parser.add_option(short_name, long_name, **kwargs)
    _option_names.add(long_name[2:])
    
add_option("-v", "--verbose", default=False, help="Verbose output")

def main():
    opts, tasks = _parser.parse_args()
    
    if opts.verbose:
        console.DISPLAY_VERBOSE = True
        
    for opt_name in _option_names:
        options[opt_name] = getattr(opts, opt_name)
    
    if len(tasks) == 0:
        if not "default" in _tasks:
            msg = "No tasks given, and no 'default' task exists"
            console.error(msg, exit=True)
            
        tasks = ["default"]
    else:
        for task in tasks:
            if not task in _tasks:
                console.error("No task '%s' exists" % task, exit=True)
    
    try:
        for task in tasks:
            try:
                _tasks[task]()
            except error.ProletarianException, e:
                console.error(e.message, exit=True)
    except KeyboardInterrupt:
        #Write black out to make sure there's no dangling red left
        sys.stderr.write(console.COLORS['black'])
        
        console.error("Received keyboard interrupt; aborting")
    except Exception:
        # exc_type, exc_value, exc_tb = sys.exc_info()
        # 
        # console.error("Traceback (most recent call last):")
        # 
        # while exc_tb is not None:
        #     filename = exc_tb.tb_frame.f_code.co_filename
        #     line = exc_tb.tb_lineno
        #     callee = exc_tb.tb_frame.f_code.co_name
        #     exc_tb = exc_tb.tb_next
        #     verbose = filename.find('proletarian/__init__.py') >= 0 and callee == "wrapper"
        #     
        #     console.error('  File "%s", line %s, in %s' % (filename, line, callee), verbose=verbose)
        #     
        #     try:
        #         with open(filename) as f:
        #             console.error("    %s" % f.readlines()[line - 1].strip(), verbose=verbose)
        #     except Exception, e:
        #         pass
        #     
        # footer = exc_value.__class__.__name__
        #     
        # try:
        #     if exc_value.message:
        #         footer += ": %s" % exc_value.message
        # except:
        #     pass
        #     
        # console.error(footer)
        
        for line in traceback.format_exc().split("\n"):
            console.error(line)
        
        sys.exit(-2)