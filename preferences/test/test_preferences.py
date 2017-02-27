import unittest
import os
import inspect


try:
    from preferences import Preferences
except:
    # This garbage just so to import 'preferences', if it can't be done via the main way.
    import sys
    current_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
    parent_folder = os.path.split(current_folder)[0]
    grandpa_folder = os.path.split(parent_folder)[0]
    if grandpa_folder not in sys.path:
        sys.path.insert(0, grandpa_folder)
    del sys
    del current_folder, parent_folder, grandpa_folder
    from preferences import Preferences



CURRENT_PATH = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
RELATIVE_FOLDER = "stupid_folder_for_testing_dfgd1236lth5viu"
TARGET_FOLDER = os.path.join(CURRENT_PATH, RELATIVE_FOLDER)


def assert_values(self,list_with_values):
    self.assertTrue(self.P.x1 == list_with_values[0])
    self.assertTrue(self.P.x2 == list_with_values[1])
    self.assertTrue(self.P.x3 == list_with_values[2])

def assert_default_values(self):
    self.assertTrue(self.P.x1 == 1)
    self.assertTrue(self.P.x2 == 2)
    self.assertTrue(self.P.x3 == 3)
    
def assert_different_values(self):
    self.assertTrue(self.P.x1 == 4)
    self.assertTrue(self.P.x2 == 5)
    self.assertTrue(self.P.x3 == 6)


def assert_class_works_correctly(self, function = "self.initialize_with_dict"):
    assert_default_values(self)
    
    self.P.x1 = 2
    del self.P
    if function == "self.initialize_with_dict":
        self.P = self.initialize_with_dict()
    else:
        self.P = function()
    self.assertTrue(self.P.x1 == 2)
    

def set_to_different_values(self,list_with_values = (4,5,6)):
    self.P.x1 = list_with_values[0]
    self.P.x2 = list_with_values[1]
    self.P.x3 = list_with_values[2]


class MyTestPrefs(Preferences):
    def check_before_setting_attribute(self, name, value):
        # checks if x1 is integer; otherwise raise TypeError
        if   name == "x1":
            return isinstance(value,int)
        # check if possible to convert value into integer, otherwise raise TypeError
        elif name == "x2":
            if not isinstance(value,int):
                try:
                    value_2 = int(value)
                except:
                    return False
                else:
                    setattr(self,name,value_2)
                    return "pass"
        elif name == "x3":
            raise ValueError
        elif name == "x4":
            return True
        else:
            if not name.startswith("_"):
                error_message = "Apart from x1,x2,x3,x4, no other attributes can be set (but you tried to set '%s'."%name
                raise AttributeError(error_message)
        return True







class TestPreferences(unittest.TestCase):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # (tries to) makes sure that there is no preference file initiated before starting this test
        self.tearDown()

    filename = "preferences_example.txt"
    defaults_with_dict =  {"x1":1,
                           "x2":2,
                           "x3":3}
    set_to_new_value   =  {"x1":4,
                           "x2":5,
                           "x3":6}

    def setUp(self):
        with self.assertRaises(AttributeError):
            self.P # makes sure that we do not start with this class already initialized

    # creates a folder, for our relative path...
    def setUpClass():
        if not os.path.exists(TARGET_FOLDER):
            os.makedirs(TARGET_FOLDER)
    
    def initialize_with_dict(self):
        self.defaults_with_dict =  {"x1":1,
                                    "x2":2,
                                    "x3":3}
        P = Preferences(defaults = self.defaults_with_dict,
                        filename = self.filename)
        return P    

    def initialize_with_keywords(self):
        P = Preferences(filename = self.filename,
                        x1 = 1, x2 = 2, x3 = 3)
        return P

    def initialize_mixed(self):
        P = Preferences(defaults = {"x1":1,"x2":2},
                        filename = self.filename,
                                                  x3 = 3)
        return P

    def initialize_with_absolute_path(self):
        absolute_path = os.path.join(CURRENT_PATH,self.filename)
        P = Preferences(defaults = self.defaults_with_dict,
                                      filename = absolute_path)        
        return P

    def initialize_with_relative_path(self):

        relative_path = os.path.join(RELATIVE_FOLDER, self.filename)
        absolute_path = os.path.join(CURRENT_PATH, RELATIVE_FOLDER)
        self.assertTrue(os.path.exists(absolute_path)) # if this fails, that means that this test would fail anyway, because I haven't directed it to an existing folder
        
        P = Preferences(defaults = self.defaults_with_dict,
                                      filename = relative_path)
        return P

    def initialize_without_defaults(self):
        P = Preferences(filename = self.filename)
        return P
    
    def initialize_with_header(self,header_text = "some random text"):
        P = Preferences(defaults = self.defaults_with_dict ,
                        header = header_text,
                        filename = self.filename)
        return P
    

    def test_initialize_with_keywords(self):
        self.P = self.initialize_with_keywords()
        assert_default_values(self)
        assert_class_works_correctly(self)

    def test_initialize_with_dict(self):
        self.P = self.initialize_with_dict()
        assert_default_values(self)
        assert_class_works_correctly(self)
        
    def test_initialize_mixed(self):
        self.P = self.initialize_mixed()
        assert_default_values(self)
        assert_class_works_correctly(self)

    def test_initialize_with_absolute_path(self):
        self.P = self.initialize_with_absolute_path()
        assert_default_values(self)
        assert_class_works_correctly(self,self.initialize_with_absolute_path)

    def test_initialize_with_relative_path(self):
        
        self.P = self.initialize_with_relative_path()       
        assert_default_values(self)
        assert_class_works_correctly(self, self.initialize_with_relative_path)     
        
    def test_initialize_with_header(self):
        random_text = "sdasdfasdfasdfasdiufsd bkcseigr r iuhsad  rf asdfklgh  rufh as as jgha a as jh aas as f khs s askh as  ak hh   kha a  a kha   a kasfsfsdfasdfk hadf \n"+\
                      "aslhjfasd   sdfghbass d asrgasefkjjsd  ;ohh safljh i  ousadf  ;jjhdf lasdf ijhsadf l iadhf oasdf h"
        self.P = self.initialize_with_header(random_text)
        assert_default_values(self)
        assert_class_works_correctly(self)
        
        self.P.reset_to_default()        
        assert_class_works_correctly(self,lambda:self.initialize_with_header(random_text))
        file_name_ = self.P._filename_to_store_the_preferences
        file_string = ""
        with open(file_name_) as inputfile:
            for line in inputfile:
                file_string += line
        self.assertTrue(file_string.startswith(random_text))





  
        
        

    def test_remembrance(self):
        self.P = self.initialize_with_dict()
        assert_default_values(self)
        assert_class_works_correctly(self)


    def test_delete_preferences_file(self):        
        self.P = self.initialize_with_dict()
        set_to_different_values(self)
        # delete file, so it forgets old values
        self.tearDown()
        self.P = self.initialize_with_dict()
        # if old values are forgotten, file must be deleted
        self.assertFalse(self.P.x1 == 4)
        self.assertTrue(self.P.x1 == self.defaults_with_dict["x1"])
        
        self.P.delete_preferences_file()
        self.P.delete_preferences_file()
        
        

    def test_reset_to_default(self):
        self.P = self.initialize_with_dict()
        set_to_different_values(self)
        self.P.reset_to_default()        
        assert_default_values(self)        
        
        self.tearDown()

        # values are initialized without defaults.
        # this means that no defaults can be reset

        self.P = self.initialize_without_defaults()
        set_to_different_values(self)
        self.P.reset_to_default()
        assert_different_values(self)

        self.tearDown()

        self.P = self.initialize_with_dict()
        set_to_different_values(self)
        self.P.reset_to_default("x1")
        assert_values(self,[1,5,6])

        self.tearDown()

        self.P = self.initialize_with_dict()
        set_to_different_values(self)
        self.P.reset_to_default(["x1","x2"])
        assert_values(self,[1,2,6])

        self.tearDown()

        self.P = self.initialize_with_dict()
        set_to_different_values(self)
        self.P.reset_to_default(["x1","x2"],"x3")
        assert_values(self,[1,2,3])

        self.tearDown()

        self.P = self.initialize_with_dict()
        set_to_different_values(self)
        # this code is ugly, and should never happen, but someone might give this as input
        self.P.reset_to_default(["x1","x2"],exclude="x3")
        assert_values(self,[1,2,6])

        self.tearDown()

        self.P = self.initialize_with_dict()
        set_to_different_values(self)
        # this code is ugly, and should never happen, but someone might give this as input
        self.P.reset_to_default(["x1","x2"],exclude=["x2","x3"])
        assert_values(self,[1,5,6])
        
        self.tearDown()

        self.P = self.initialize_with_dict()
        set_to_different_values(self)
        self.P.reset_to_default(exclude = ["x1"])
        assert_values(self,[4,2,3])
        



    def test_delete_attribute(self):
        self.P = self.initialize_with_dict()
        self.P.delete_attribute("x1")
        with self.assertRaises(AttributeError):
            self.P.x1
        del self.P
        self.P = self.initialize_without_defaults()
        with self.assertRaises(AttributeError):
            self.P.x1
        self.assertTrue(self.P.x2 == 2)


    def test_set(self):
        i=0
        for foo in [self.initialize_with_dict,
                    self.initialize_without_defaults]:
            self.P = foo()
            for key in self.set_to_new_value.keys():
                self.P.set(key,self.set_to_new_value[key])
            assert_different_values(self)

            if i == 0:
                self.P.delete_preferences_file()
                del self.P
                i+=1


    # todo: for most functions, check error_handling... ?
                
    def test_set_value_with_dict(self):
        self.P = self.initialize_without_defaults()
        self.P.set_value(self.set_to_new_value)
        assert_different_values(self)

    def test_set_value_with_keyword(self):
        self.P = self.initialize_without_defaults()
        self.P.set_value(x1=4, x2=5, x3=6)
        assert_different_values(self)

    def test_get(self):
        self.P = self.initialize_with_dict()
        self.assertTrue(self.P.get("x1") == self.P.x1)

    def test_set_default_values(self):        
        self.P = self.initialize_without_defaults()
        self.P.set_default_values(self.defaults_with_dict)
        assert_default_values(self)

        self.P.set_default_values(x1=4, x2=5, x3=6)
        assert_default_values(self)
        self.P.reset_to_default()
        assert_different_values(self)

        self.P.set_default_values({"x1":0},{"x3":0},x2=0).reset_to_default()
        assert_values(self,[0,0,0])        
        
        self.P.set_default_values({"x1":"da"},{"x3":0},x2=0).reset_to_default()
        assert_values(self,["da",0,0])

        set_to_different_values
        del self.P
        self.P = self.initialize_without_defaults()
        self.P.reset_to_default()
        assert_values(self,["da",0,0])


    def test_check_before_setting_attribute(self):
        self.P = MyTestPrefs(filename = self.filename)
        with self.assertRaises(TypeError):
            self.P.set("x1","bla")
        self.P.x1 = 5
        self.P.x2 = "3"
        self.assertTrue(isinstance(self.P.x2,int))
        self.P.x2 = 6
        self.assertTrue(self.P.x2 == 6)
        with self.assertRaises(TypeError):
            self.P.x2 = ["h"]
        with self.assertRaises(ValueError):
            self.P.x3 = 5
        self.P.x4= 5
        self.P.x4 = "h"
        self.P.x4 = []  # can be anything
        with self.assertRaises(AttributeError):
            self.P.stupid_attribute = ["h"]

        # also works when setting through set
        with self.assertRaises(TypeError):
            self.P.set(x2 = ["h"])


        
        
        

    def tearDown(self):
        try:    self.P
        except: pass
        else:   self.P.delete_preferences_file()
        
        try:    del self.P
        except: pass

    # a folder has been created for this class, time to delete that folder
    def tearDownClass():
        if os.path.exists(TARGET_FOLDER):
            os.rmdir(TARGET_FOLDER) # if folder not empty, will give error IIRC




def run_test_preferences():
        unittest.main()

if __name__ == '__main__':
    run_test_preferences()
