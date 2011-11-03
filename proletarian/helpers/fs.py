import sys
import os
import shutil
import console

def remove_dir(dir, ignore_errors=False):
    console.message("Removing directory '%s'" % dir)
    shutil.rmtree(dir, ignore_errors)
    
def normalize_cwd():
    set_cwd(sys.path[0])

def set_cwd(dir):
    console.message("Setting working directory to %s" % dir)
    os.chdir(dir)
    
def move(src, dest):
    console.message("Moving file/directory '%s' to '%s'" % (src, dest))
    shutil.move(src, dest)
    
def copy(src, dest):
    console.message("Copying file/directory '%s' to '%s'" % (src, dest))
    
    if os.path.isfile(src):
        shutil.copy(src, dest)
    else:
        shutil.copytree(src, dest)
    
def make_dir(dir):
    console.message("Making directory '%s'" % dir)
    os.mkdir(dir)

def make_dir_rec(struct, root='.'):
    if isinstance(struct, dict):
        for dir, children in struct.iteritems():
            path = os.path.join(root, dir)
            make_dir(path)
            make_dir_rec(children, root=path)
    else:
        for dir in struct:
            path = os.path.join(root, dir)
            make_dir(path)