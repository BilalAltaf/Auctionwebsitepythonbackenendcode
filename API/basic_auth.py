__author__ = 'Bilal'

import base64
uname = raw_input("Enter username:")
pword = raw_input("Enter password:")

hd_value = "%s:%s" % (uname, pword)
print "Authorization: Basic",base64.b64encode(hd_value)
print "Authorization: Basic",hd_value.encode("base64")
