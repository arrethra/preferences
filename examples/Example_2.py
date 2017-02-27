# need to import from another folder; this block enables that
import sys, os, inspect
current_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
parent_folder = os.path.split(current_folder)[0]
if parent_folder not in sys.path:
    sys.path.insert(0, parent_folder)
del sys, os, inspect, current_folder, parent_folder


###### EXAMPLE 2 #####
# The method check_before_setting_attribute can perform automatic checks
# or even alter values of attributes, while you try to set attributes
from preferences import Preferences

class MyPrefs(Preferences):
    def check_before_setting_attribute(self,name,value):
        """
        Whenever you try to set the value of an attribute, this method
        checks that attribute, and acts if it violates the conditions
        you have written.
        """
        
        if   name == "X":
            # if "X" is not an integer, an error will be raised by __setattr__
            if not isinstance(value,int):                
                return False     
        elif name == "Y":
            # if "Y" is not an integer, it will try to convert it to an
            # an integer (e.g. because it was a string with the number "1")
            # Otherwise __setattr__ raises an error  
            if not isinstance(value, int):
                try:    new_value = int(value)
                except: return False
                else:   # if conversion succeeded, the new_value is manually
                        # set. However, to stop it from setting the current
                        # value, the string "pass" is returned (while
                        # avoiding an error being raised)
                        setattr(self,name,new_value)
                        return "pass"        
        return True

    
prefs = MyPrefs(filename = "preferences - example2.txt",
                X = 1, Y = 2)

prefs.X = 5                              # succeeds
prefs.Y = 6                              # succeeds

try:              prefs.X = "1"          # fails
except TypeError: pass

prefs.Y = "1"                            # succeeds, but the code above has 
assert isinstance(prefs.Y, int)          # automatically converted the string
                                         # into integer

try:              prefs.Y = "random txt" # fails
except TypeError: pass

# deletes the stored file. 
prefs.delete_preferences_file()
