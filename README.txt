This module enables automatical storage of values/preferences to a file
when its values are set/changed*. These values are configured as the 
attributes (named after your own choice) of the class Preferences. 
Upon restarting of the program, these stored values are automatically 
retrieved. The file writes down the values in recognisable format (JSON)

    *Override through 'setattr', which means that methods such as 
    list.append or dict.update do not trigger this automatic behavior,
    where the value is stored to a file.

It is possible to set defaults for these values quite easily. These 
defaults are stored in the file as well. When the values change, these
values can manually be reset to default with the method 
'reset_to_default(*args)'.

It is also possible to incorporate automatic checks, that for example 
can check the instance or format of the saved value automatically. 
This requires overriding the method 'check_before_setting_attribute".

For more information on all the methods and/or examples see the 
docstring [help(Preferences)].


Simple example:

prefs_defaults = { "x":1, 
                   "y":2 }
prefs = Preferences(defaults = prefs_defaults,
                    filename = "preferences_test.txt")
prefs.x, prefs.y = 3,4
# attributes are not required to have defaults
prefs.z = 5   
       
# RESTART program (re-initialize prefs; since defaults are stored, there 
#                  is no real need to initialize these again, although 
#                  setting defaults again will not override old values)
prefs = Preferences(filename = "preferences_test.txt")

# old values have been remembered
assert prefs.x == 3 and prefs.y == 4 and prefs.z == 5

# no arguments means reset ALL values, although unable reset "z"
prefs.reset_to_default() 
assert prefs.x == 1 and prefs.y == 2 and prefs.z == 5




