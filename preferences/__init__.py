"""
Stores preferences to file automatically if values are changed.
These values are attributes of this class.
Also enables automatic checks to be performed on its values, by
overriding method "check_before_changing_attribute".

Author: Arrethra ( https://github.com/arrethra )
Under MIT license
"""



from copy import copy
import json
import os.path
from collections import OrderedDict

  
class Preferences():
    """
    This class stores the values of its attributes in a file. When
    re-initializing this class, the attributes of this class will be set
    to the old values. This can come in handy if you close a program,
    but like to boot up the program under the same preferences in a new
    session.

    Whenever an attribute of this class is set(/changed), this change is
    stored as well.
    (NOTE: This only works by explicitly setting the value. Changing a
    list with append or a dictionary with update will not trigger the
    change to be stored into the file.)

    Arguments:
    defaults:        A dictionary that holds the default values for the
                     attributes. The keys of theses attributes must be
                     the name of the attributes (in string-form).  
    filename:        The file in which the preferences will be stored.
                     Recognizes both relative paths and absolute paths.
                     If it is a relative path, the file will be stored
                     in the same directory as the script that called
                     upon this class.          Default = preferences.txt
    header:          Any details you'd like to mention. This text will
                     appear at the top of the file if specified.
                     Default = ""
    **keyword_defaults:
                     The keywords entered will be set as attributes,
                     while their corresponding value will be set as
                     the default for that attribute. This is another
                     method to initiate attributes and default values.

            
    Here is an example of this class; how the default values can be
    centralized is with the following code (although new defaults can
    be set with the method set_default_values)

    defaults = {"x":2, "y":3}        
    Example1 = Preferences(defaults)

    Example2 = Preferences(x=2, y=2)
    """
    
    _ATTRIBUTES_TO_IGNORE = ("_initialization_complete_of_this_class",
                             "_filename_to_store_the_preferences",
                             "_header_of_this_class",
                             "_ATTRIBUTES_TO_IGNORE") # TODO: make control-attribute that checks if file exists? So you won't get an error if delete_preferences_file is called_upon twice ??
    
    _HEADER_SPLITTER = 40*"#"

    
    def __init__(self, defaults = "dict",
                       filename = "preferences.txt",
                       header   = "",
                       **keyword_defaults
                 ):

        # processing filename
        if not isinstance(filename,(str,bytes)):
            error_message = "Argument 'filename' needs to be a path (either string or bytes) but found type %s."%filename
            raise TypeError(error_message)
        path_to_filename = os.path.split(filename)[0]
        if not os.path.isabs(path_to_filename): #it's not an absolute path, which makes it a relative path
            import inspect

            originating_folder = os.path.split( inspect.stack()[1][1] )[0]
            path = os.path.join(originating_folder , filename) # gets path of place from where this function is called, and join it with the new filename/relative path
            path = os.path.abspath(path) # in case input was not formatted correctly
            path_to_filename = os.path.split(path)[0]
            if not os.path.exists(path_to_filename): # TODO: use os.path.exists()  ??
                error_message = "No such directory: %s."%path_to_filename
                raise FileNotFoundError(error_message)
            else:
                self._filename_to_store_the_preferences = path
        else:
            self._filename_to_store_the_preferences = filename



        self._header_of_this_class = header

        
        saved_values = ""
        try:        
            with open(self._filename_to_store_the_preferences, 'r') as inputfile:
                for line in inputfile:
                    saved_values += line
        except FileNotFoundError:
             text_file = open(self._filename_to_store_the_preferences,'w')
             text_file.close()             
        else:
            saved_values = "".join(saved_values)
            if self._HEADER_SPLITTER in saved_values:
                header_from_file = saved_values.split(self._HEADER_SPLITTER)[0][:-2]
                if not self._header_of_this_class:
                    self._header_of_this_class = header_from_file
                saved_values = saved_values.split(self._HEADER_SPLITTER)[-1]
            saved_values = saved_values.replace("\n","")
            try:
                saved_values = json.loads(saved_values)
            except:
                print("something has gone wrong when trying to read the preferences_file named '%s'. What was read is: \n'%s'"%(
                    self._filename_to_store_the_preferences,saved_values) )
                raise
            else:
                for attr_name in saved_values:
                    setattr(self, attr_name, saved_values[attr_name])
                        
        try:
            self._defaults_of_this_class = OrderedDict(sorted(self._defaults_of_this_class.items(),key = lambda x:x[0]))
        except AttributeError:
            self._defaults_of_this_class = {}  #just initiating this attribute, the method set_default_values sets it

        self._initialization_complete_of_this_class = True

        if isinstance(defaults,dict):            
            self.set_default_values(defaults)
        elif defaults == "dict":
            pass
        else:
            error_message = "The argument defaults should be a dict, but rather found type %s"%(type(defaults))
            raise TypeError(error_message)
        if keyword_defaults:
            self.set_default_values(keyword_defaults)

    # TODO: ehmm, when a list is altered through methods like append or remove (or dicts with upgrade)
    # the __setattr__ is not triggered, and therefore the value in the file is not changed
    # the next link suggests a fix for this, although that is somewhat cumbbersome to integrate
    # http://stackoverflow.com/questions/37799938/what-happens-when-we-editappend-remove-a-list-and-can-we-execute-actions-e

            

    def __setattr__(self,name,value):
        """
        Overrides default behavior for __setattr__. Calls automatically
        upon method write_to_file and check_before_changing_attribute.
        """
        result_of_check = self.check_before_setting_attribute(name,value)
        if result_of_check == "pass":
            pass
        elif result_of_check:
            if callable(value):
                error_message = "You cannot assign functions to attributes of this class, but still you tried to allocate a function to attribute '%s'."\
                                %(type(value),name) #json won't accept functions and such, only predefined numbers and things
                raise TypeError(error_message)
            
            super().__setattr__(name,value)
            
            # during initialization, some values will be set. This should not trigger the file being (over)written
            # Therefor, the attribute "_initialization_complete_of_this_class" is only initialized at the end of __init__
            # If this value is not initialized, access to the file is blocked                
            try:
                self._initialization_complete_of_this_class                
            except AttributeError:
                pass
            else:
                self.write_to_file()
        else:
            error_message = "The change of the attribute '%s' failed the method 'check_before_setting_attribute' in this class; \
                            the value was of type '%s' and of value '%s'."\
                            %(name,type(value),value)
            raise TypeError(error_message)
        

    def write_to_file(self):
        """
        Writes ALL the values to the file.
        This method is automatically called by __setattr__,
        i.e. whenever the value of an attribute is set.
        """
        if self._initialization_complete_of_this_class:
            
            attributes = copy(self.__dict__)
            for x in self._ATTRIBUTES_TO_IGNORE:
                try:
                    del attributes[x] # if this gets into the file, the attribute "_initialization_complete_of_this_class" could be initialized before it is supposed to. This could bring havoc upon method __init__
                except:
                    pass
            attributes = OrderedDict(sorted(attributes.items(), key = lambda x: x[0] if x[0] != "_defaults_of_this_class" else 40*"z"))

            Z = json.dumps(attributes)
            Z = Z[0:Z.index("_defaults_of_this_class")-1].replace(",",",\n") +"\n "+ Z[Z.index("_defaults_of_this_class")-1:].replace(",",",\n"+28*" ") # remark: I am pretty-typing json myself, but json self also has this capability. erghh, too late for that

            if self._header_of_this_class:
                Z = self._header_of_this_class + "\n\n"+self._HEADER_SPLITTER+"\n\n" + Z

            text_file = open(self._filename_to_store_the_preferences, "w")
            text_file.write("%s" % Z) # TODO: right now I rewrite the entire file everytime, but this is time-consuming: I should only overwrite the lines that need overwriting....
            text_file.close()
        return self
            

    def set_default_values(self, *dicts_with_default_values, **kwargs):
        """
        Initializes or updates default values. Note that if the
        attributes already exist, this method will not reset their value
        to default.
        
        Two choices for input are possible:
        -As a dictionary (or multiple), in which the keys must be
         string-equivalents of the attributes you'd like to
         initialize/set. The coupled values will be the default values,
         e.g.  A.set_default_values( { "x":1} )
        -As keyword-argument(s), in which the keyword represents the
         attribute and their value the default-value,
         e.g. A.set_default_values( x = 1 )
        Input accepts multiple dicts and keywords, e.g.
        A.set_default_values( { "x":1}, {"y1":2,"y2":3}, z1=1, z2=2 )
        """
        master_dict = {}
        for dict_with_default_values in dicts_with_default_values:
            if not isinstance(dict_with_default_values, dict):
                error_message = "TODO" # TODO
                raise TypeError(error_message)
            master_dict.update(dict_with_default_values)

        master_dict.update(kwargs)

        dict_copy = self._defaults_of_this_class.copy()
        dict_copy.update( master_dict )
        self._defaults_of_this_class = OrderedDict(sorted(dict_copy.items(),key = lambda x:x[0]))
        
        for x in master_dict:
            if not isinstance(x,str):
                error_message = "Attribute name must be initialized as a string, but found type %s."%type(x)
                raise TypeError(error_message)
            try:
                getattr(self,x)
            except AttributeError:
                setattr(self,x,master_dict[x])
                
        return self # enables chaining

    def _valid_attributes(self):
        """
        Returns current valid attributes as strings, in a list.
        (i.e. excluding the private attributes of this class).
        """
        current_attributes = self.__dict__.keys()
        VALID_ATTRIBUTES = [a for a in current_attributes if not a in self._ATTRIBUTES_TO_IGNORE + ("_defaults_of_this_class",) ]
        return VALID_ATTRIBUTES

    def reset_to_default(self,*attr_names, exclude = None):
        """
        Resets attributes to default value. If attributes are entered
        (their string-equivalent), those attributes will be resetted.        
        If no (non-keyword) input is given, all attributes are reset
        to default. If this latter option failed to reset any attributes
        (i.e. due to absent default values), then these attributes are
        returned by the method.
        If (string-equivalent) attributes for the keyword 'exclude' are
        given, then these attributes will not be reset. These can be
        collected in a list.
        """
        
        names = []
        VALID_ATTRIBUTES = self._valid_attributes()
        if len(attr_names) != 0:
            for attr_name in attr_names:
                if not isinstance(attr_name,list):
                    if isinstance(attr_name,tuple):
                        names += list(attr_name)
                    else:
                        names += [attr_name]
                    
                else:
                    names += attr_name
        else: # if no args input, all attributes will be reset
            names = VALID_ATTRIBUTES

        # handles keyword 'exclude', and filters it/them into correct format
        if not isinstance(exclude,(list,tuple,str,type(None))):
            error_message = "For method 'reset_to_default', the keyword 'exclude' got unexpected "+\
                            "input of type %s. Input should be string (of attribute), possibly "+\
                            "collected in tuple or list."%(type(exclude))
            raise TypeError(error_message)
        if isinstance(exclude,str):
            exclude = [exclude]
        elif isinstance(exclude,type(None)):
            exclude = []
        excluded_names = []

        # exempts the excluded attributes from being reset.
        for exc in exclude:
            assert isinstance(exc,str), exc # TODO  (TODO: check other assert as well, with ctrl-F)
            if not exc in VALID_ATTRIBUTES:
                excluded_names += [exc]
            elif exc in names:
                names.remove(exc)
                
        # error module, for wrongly named attributes    
        if excluded_names: 
            def f(s,m):
                return (m if len(excluded_names)>1  else s)
            error_message = "The attribute%s '%s' you tried to exclude, %s not %svalid attribute%s. Valid attributes are '%s'."\
                   %(f("","s"),"', '".join(exclude), f("is","are"),f(" a",""), f("","s"), "', '".join(VALID_ATTRIBUTES)) 
            raise AttributeError(error_message)

        # collects any attributes that did not have a default value   
        name_error = []        
        for name in names:
            assert isinstance(name,str), "The attributes should be the string-equivalents, but found type %s"%type(name)  # TODO
            try:                
                setattr(self, name, self._defaults_of_this_class[name])                
            except:                
                name_error += [name]

        # resets attributes        
        if attr_names and name_error:
            error_message = "No attributes found named '%s'; valid attributes are '%s'."\
                            %("', '".join(name_error),"', '".join(VALID_ATTRIBUTES))
            raise AttributeError(error_message)

        return name_error # returns any attributes that did not have a default value 


    def check_before_setting_attribute(self,name,value):
        """
        This method is called everytime an attribute is set/changed.
        While the main class has no use for this method, it may
        very well be usefull if overridden due to inheritance. In that
        case, it is possible to incorporate checks into this method, 
        which can check the specifics of the value to which the
        attribute is about to be changed into (see example below).

        Return-values:
        If the value passes the test: -return True (or similar).
        If the value fails  the test: -return False or None (or similar)
                                       to raise a TypeError.
                                      -return "pass" prevents the 
                                       attribute from being changed and
                                       no Error will be raised.
                                       Note that "pass" is a string.
        (Note: When overriding this method, the return must actively be
        set, or otherwise the default return None will trigger an error)
        
        Arguments:
        -name:      The string-equivalent of the attribute that is to be
                    changed.
        -value:     The value to which the attribute will be changed (if
                    succesfull).

        Example of code in such a case (which checks for x to be an
        integer, everytime the value of x changes) :
        
        class MyPreferences(Preferences):                
            def check_before_setting_attribute(self, name , value):
                if name == "x":
                    if not isinstance(value, int):
                        print("'x' should be an integer but found type",
                             type(value),
                             "and as a result, 'x' will not be changed")
                        return "pass"
                return True
        """
        return True


    def _test_if_valid_attribute(self,name): # TODO: expand functionality to other functions, so code is cleaned up there??
        """
        Tests if name is valid attribute of this class.
        If it fails, this method returns an error. (otherwise None)
        You still need to raise error this yourself!
        """
        if not isinstance(name,str):
            error_message = "Input must be string-equivalent to an attribute, but found type %s."\
                            %type(name)
            return TypeError(error_message)
        if not name in self._valid_attributes():
            error_message = "'%s' is not a valid attribute; valid attributes are '%s'"\
                            %(name,"', '".join(sorted(self._valid_attributes())))
            return AttributeError(error_message)


    def set(self, name, value):
        """
        Method to set attribute. Argument 'name' must be
        string-equivalent of attribute.

        For more variable input, or setting multiple attributes, see
        method set_value.
        """
        if isinstance(self._test_if_valid_attribute(name),TypeError): # Error_handling
            raise self._test_if_valid_attribute(name)
        setattr(self,name,value)
        return self


    def set_value(self,*dicts_with_values,**keyword_attributes):
        """
        Method to set multiple attributes at once. Similar to method set
        or function setattr.

        Input can be realized by two means:
        - a dictionary, in which the keys are the string-equivalents
          of the attributes, e.g.  A.set_value( { "x":1} )
        - Keywords, in which the keywords are the attributes, and their
          new values are assigned to them, e.g.  A.set_value( x = 1 )
          
        Input also accepts multiple dicts and/or keywords, e.g.
        A.set_value( { "x":1}, {"y1":2,"y2":3}, z1=1, z2=2 )
        """
        
        # collects input into master_dict, which this method can understand
        master_dict = {}
        if dicts_with_values:
            for dict_with_values in dicts_with_values:
                assert isinstance(dict_with_values, dict) # TODO
                master_dict.update(dict_with_values)
        if keyword_attributes:
            master_dict.update(keyword_attributes)

        # set attributes
        for attribute in master_dict:
            assert isinstance(attribute,str), attribute
            try:
                setattr(self,attribute,master_dict[attribute])
            except:
                raise
        return self


    def get(self,name):
        """
        Gets value of attribute. Method is same as obtaining value of
        attribute directly, or using getattr.
        """
        
        if self._test_if_valid_attribute(name): # Error_handling
            raise self._test_if_valid_attribute(name)

        return getattr(self,name)
    

    def delete_attribute(self,name):
        """        
        Deletes attribute from both class and stored file.
        Also removes any default value of that attribute.
        """ # TODO: should this "override" the __delattr__ ?

        if self._test_if_valid_attribute(name): # Error_handling
            raise self._test_if_valid_attribute(name)
        
        if name in self._defaults_of_this_class.keys():
            del self._defaults_of_this_class[name]
        super().__delattr__(name)
        self.write_to_file()


    def delete_preferences_file(self):
        """
        Deletes the stored file. This method does not destroy this
        class, nor affects any attributes.
        """
        os.remove(self._filename_to_store_the_preferences)
        return self # enables chaining
        

               
if __name__ == "__main__":    

    # EXAMPLE 2: change value of input through method check_before_setting_attribute:
    class MyPrefs(Preferences):
        def check_before_setting_attribute(self,name,value):
            if name == "ExampleInteger":
                if not isinstance(value,int):
                    try:
                        A = int(value)
                    except:
                        return False
                    else:                        
                        setattr(self,name,A)
                        return "pass"
                elif isinstance(value,int):
                    pass
                else:
                    return False
            return True
        
    
    filename_ex2 = "preferences - example2.txt"
    a = MyPrefs(filename = filename_ex2 ,ExampleInteger = 1)
    a.ExampleInteger = "2" # test that strings get converted into integers
    assert isinstance(a.ExampleInteger , int), a.ExampleInteger
    try:
        a.ExampleInteger = "str" # test if this raises a TypeError (like it should). If so, it is ignored in this example 
    except TypeError: pass
    else: raise Exception
    a.delete_preferences_file()





    
    # testing main functionality
    filename = "preferences__Ignore_me_Im_just_part_of_a_test.txt"
    try: #begin with clean sheet
        os.remove(filename)
    except FileNotFoundError:
        pass
    a = Preferences(filename = filename )
    a.x = 5
    a.y = 6
    del a # forgets the variable...
    a = Preferences(filename = filename)
    assert a.x == 5 # ...but the value has been remembered
    assert a.reset_to_default(), a.reset_to_default() # No defaults have been set. Therefor the reset_to_default SHOULD return the variables it wasn't able to reset
    assert not a.set_default_values({"x":1,"y":6}).reset_to_default()

    # tests header-option
    a = Preferences(filename = filename, header = "test phase")
    a.x = 5
    del a
    a = Preferences(filename = filename, header = "test phase, changed header")

    b = Preferences(filename = filename, header = "test phase, changed header", x=10)
    b.reset_to_default("x")     
    assert b.x == 10

    b.set_value(x = 11)
    assert b.x == 11
    b.set_value({"x":12})
    assert b.x == 12
    b.set("x",1)
    assert b.x==1

    b.set("x",2)
    assert b.x==2
    b.set_default_values(x=-1)
    assert b.x != -1
    assert b.x == b.get("x")
    
    
    # testing delete_attribute
    b.set_default_values(g=5)
    b.delete_attribute("g")
    try:
        b.g
        raise Exception("shouldn't still have an attribute 'g'")
    except AttributeError:
        pass

    del b
    b = Preferences(filename = filename, header = "test phase, changed header", x=10)
    try:
        b.g
        raise Exception("shouldn't still have an attribute 'g'")
    except AttributeError:
        pass
    b.delete_preferences_file()
    
