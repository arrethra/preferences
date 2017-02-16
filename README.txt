This module enables automatical storage of values/preferences to a file
when its values are set/changed*. These values are configured as the 
attributes (named after your own choice) of the class Preferences. 
Upon restarting of the program, these stored values are automatically 
retrieved. The stored values are written down in the file in 
recognisable format (JSON).

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

prefs_defaults = { "X": 1,
                   "Y": 2 }
prefs = Preferences(defaults = prefs_defaults,
                    filename = "preferences_test.txt")

# At first use, attributes are initialized to default
# If previous uses set them at different values, 
assert prefs.X == 1 and prefs.Y == 2                        # True

# by setting the following attributes, their new values are
# automatically stored into the file
prefs.X = 3
prefs.Y = 4

# attributes can be defined without default values
prefs.Z = 5

# RESTART program (re-initializing 'prefs' gives the same results as
#                  restarting. Since defaults are stored, you are not
#                  required to give them default values again. 
#                  However, when restarting the script, this is 
#                  usually unavoidable. )
prefs = Preferences(defaults = prefs_defaults,
                    filename = "preferences_test.txt")

# old values have been remembered
assert prefs.X == 3 and prefs.Y == 4 and prefs.Z == 5        # True

# Following method resets ALL values (if no arguments are given),
# although it will be unable to reset "Z", as it has no default.
prefs.reset_to_default() 
assert prefs.X == 1 and prefs.Y == 2 and prefs.Z == 5        # True

# If you'd like to remove the stored file, the following method
# would accomplish this. (This removes any old values!!)
# prefs.delete_preferences_file()




