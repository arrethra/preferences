import unittest
import os

from preferences import Preferences


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
    

def set_to_different_values(self,list_with_values = (4,5,6)):
    self.P.x1 = list_with_values[0]
    self.P.x2 = list_with_values[1]
    self.P.x3 = list_with_values[2]



# TODO: test Header


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
            self.P # makes sure that we do not start with a preference_file already initialized
    
    
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
        absolute_path = os.path.join(os.getcwd(),self.filename)
        P = Preferences(defaults = self.defaults_with_dict,
                                      filename = absolute_path)        
        return P

    def initialize_with_relative_path(self):
        relative_folder = "preferences"
        relative_path = os.path.join(relative_folder,self.filename)
        absolute_path = os.path.join(os.getcwd(), relative_folder)
        self.assertTrue(os.path.exists(absolute_path)) # if this fails, that means that this test would fail anyway, because I haven't directed it to an existing folder
        
        P = Preferences(defaults = self.defaults_with_dict,
                                      filename = relative_path)
        return P

    def initialize_without_defaults(self):
        P = Preferences(filename = self.filename)
        return P    
        
        



    def test_initialize_with_keywords(self):
        self.P = self.initialize_with_keywords()
        assert_default_values(self)

    def test_initialize_with_dict(self):
        self.P = self.initialize_with_dict()
        assert_default_values(self)
        
    def test_initialize_mixed(self):
        self.P = self.initialize_mixed()
        assert_default_values(self)

    def test_initialize_with_absolute_path(self):
        self.P = self.initialize_with_absolute_path()
        assert_default_values(self)

    def test_initialize_with_relative_path(self):
        self.P = self.initialize_with_relative_path()
        assert_default_values(self)
        
        

    def test_remembrance(self):
        self.P = self.initialize_with_dict()
        assert_default_values(self)
        self.P.x1 = 2
        del self.P
        self.P = self.initialize_with_dict()
        self.assertTrue(self.P.x1 == 2)

    def test_delete_preferences_file(self):        
        self.P = self.initialize_with_dict()
        set_to_different_values(self)
        # delete file, so it forgets old values
        self.tearDown()
        self.P = self.initialize_with_dict()
        # if old values are forgotten, file must be deleted
        self.assertFalse(self.P.x1 == 4)
        self.assertTrue(self.P.x1 == self.defaults_with_dict["x1"])
        
        

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
        

    # TODO: test set_default_values


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

    # todo: test check_value_before_setting.....
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
        assert_values(self,[0,0,0])
    
        
    
        
        
    
        
        

    
        
        
        

    def tearDown(self):
        try:
            self.P.delete_preferences_file()
        except: pass
        try:
            del self.P
        except: pass

if __name__ == '__main__':
    unittest.main()
