#!/usr/bin/python

# --- INITIALIZATION

import os,sys,outputters,getopt,re
from xml.parsers.xmlproc import xmlproc
from split import split
from listsets import listminus
from ddmin import ddmin

PASS       = "PASS"
FAIL       = "FAIL"
UNRESOLVED = "UNRESOLVED"


if __name__ == "__main__":

    # --- Interpreting options

    try:
        sysids=sys.argv[1:]
    except getopt.error,e:
        print "Usage error: "+e
        print usage
        sys.exit(1)

    warnings=1
    entstack=0
    rawxml=0
    
    app=xmlproc.Application()
    p=xmlproc.XMLProcessor()

    tests = {}
    circumstances = []

    def string_to_list(s):
        c = []
        for i in range(len(s)):
            c.append((i, s[i]))
        return c
    
    def mytest(c):
        global tests
        global circumstances
	global p

	f = open('demo/tmp.py', 'w')

        s = ""
        for (index, char) in c:
            s += char
	f.write(s)
	f.close()

        if s in tests.keys():
            return tests[s]

        map = {}
        for (index, char) in c:
            map[index] = char

        x = ""
        for i in range(len(circumstances)):
            if map.has_key(i):
                x += map[i]
            else:
                x += "."

        print "%02i" % (len(tests.keys()) + 1), "Testing", `x`,

	err=0
	try:
            p.parse_resource("demo/tmp.py")
    	except:
            err=1
        
        if s != "" and err==1:
            print FAIL
            tests[s] = FAIL
            return FAIL
        print PASS
        tests[s] = PASS
        return PASS

    # Acting on option settings

    err=outputters.MyErrorHandler(p, p, warnings, entstack, rawxml)
    p.set_error_handler(err)

    if len(sysids)==0:
        print "You must specify a file to parse"
        print usage
        sys.exit(1)
    
    # --- Starting parse    

    print "xmlproc version %s" % xmlproc.version

    for sysid in sysids:
        print
        print "Parsing '%s'" % sysid
        p.set_data_after_wf_error(0)

	circumstances = string_to_list(os.popen("cat "+sysid).read())
	mytest(circumstances)
	print ddmin(circumstances, mytest)

        print "Parse complete, %d error(s)" % err.errors,

        if warnings:
            print "and %d warning(s)" % err.warnings
        else:
            print
    
        err.reset()
        p.reset()
