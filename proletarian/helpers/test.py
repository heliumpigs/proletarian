import proletarian
import error
import console
import inspect
import util

class _AssertRaisesContext(object):
    def __init__(self, expected):
        self.expected = expected
        
        try:
            self.error_name = self.expected.__name__
        except AttributeError:
            self.error_name = str(self.expected)
        
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        if type is None:
            raise error.ProletarianTestException("%s not raised" % \
                self.error_name)
            
        if not isinstance(value, self.expected):
            return False
            
        return True

@console.trace
def assert_equal(expected, actual):
    if expected != actual:
        raise error.ProletarianTestException("Expected '%s' but got '%s'" % \
            (util.shorten(expected), util.shorten(actual)))

@console.trace    
def assert_not_equal(first, second):
    if expected == actual:
        raise error.ProletarianTestException("Expected '%s' != '%s'" % \
            (util.shorten(first), util.shorten(second)))
    
@console.trace
def assert_true(value):
    if value != True:
        raise error.ProletarianTestException("Expected '%s' to be true" % \
            util.shorten(value))
    
@console.trace
def assert_false(value):
    if value != False:
        raise error.ProletarianTestException("Expected '%s' to be false" % \
            util.shorten(value))
    
@console.trace
def assert_in(container, value):
    if value not in container:
        raise error.ProletarianTestException("Expected '%s' to be in '%s'" % \
            (util.shorten(value), util.shorten(container)))
    
@console.trace
def assert_not_in(container, value):
    if value in container:
        raise error.ProletarianTestException("Expected '%s' to not be in '%s'" % (util.shorten(value), util.shorten(container)))
    
@console.trace
def assert_is_instance(value, type):
    if not isinstance(value, type):
        raise error.ProletarianTestException("Expected '%s' to be of type '%s'" % (util.shorten(value), util.shorten(type)))
    
@console.trace
def assert_not_is_instance(type, value):
    if isinstance(value, type):
        raise error.ProletarianTestException("Expected '%s' to not be of type '%s'" % (util.shorten(value), util.shorten(type)))
    
@console.trace
def assert_raises(exception):
    return _AssertRaisesContext(exception)
    
def main():
    @proletarian.task
    def default():
        for name, callback in proletarian._tasks.iteritems():
            if name != "default":
                callback()
            
    proletarian.main()