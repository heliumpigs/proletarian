import subprocess
import threading
import console
import error
import sys
import multiprocessing
import time

def _attach_stderr_listener(task):
    def scanner():
        while task.returncode == None:
            line = task.stderr.readline()
            if line == "": return
            
            try:
                sys.stderr.write('%s%s%s' % (console.COLORS['red'], line, console.COLORS['black']))
            except KeyboardInterrupt:
                #Write black out to make sure there's no dangling red left
                sys.stderr.write(console.COLORS['black'])
    
    thread = threading.Thread(target=scanner)
    thread.start()
    return thread
            
def run_async(args):
    console.message("Running async task: %s" % " ".join(args))
    p = subprocess.Popen(args, stderr=subprocess.PIPE, bufsize=1)
    _attach_stderr_listener(p)
    return p

def run(args, timeout=None, stdout=None, exit_on_error=True):
    console.message("Running task: %s" % " ".join(args))
    p = subprocess.Popen(args, stdout=stdout, stderr=subprocess.PIPE, bufsize=1)
    
    thread = _attach_stderr_listener(p)
    
    if timeout is not None:
        thread.join(timeout)
        p.poll()
        
        if p.returncode == None:
            p.kill()
            
            if exit_on_error:
                raise error.ProletarianBuildException("Process '%s' timed out after %s seconds" % (args[0], timeout))
            else:
                console.error("Process '%s' failed to finish in the specified time (%s seconds)" % (args[0], timeout))
    else:
        thread.join()
        
        #Uses a busy waiting loop instead of communicate() or wait() because 
        #this should not happen frequently (i.e. the thread should join when
        #the process terminates) and it has less risk of starvation.
        while p.returncode != 0:
            time.sleep(0.1)
            p.poll()
        
    if exit_on_error and p.returncode != 0:
        raise error.ProletarianBuildException("Process '%s' had a non-zero return code (%s)" % (args[0], p.returncode))
        
def run_code(block, *configs):
    processes = []

    for config in configs:
        processes.extend([multiprocessing.Process(target=config[0]) for _ in xrange(config[1])])

    for process in processes:
        process.start()

    if block:        
        for process in processes:
            process.join()
    else:
        return processes

def run_code_or_fail(processes):
    for process in filter(lambda p: p.is_alive(), processes):
        process.join()

    for process in processes:
        if process.exitcode != 0:
            console.error("Process had a non-zero return code (%s)" % process.exitcode, exit=True)