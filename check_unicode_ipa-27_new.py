# -*- coding: utf-8 -*-

""" 
Script to check for non-legal Unicode-IPA characters.

For use with Python version 2.

"""

import codecs

class UnicodeIpaTester:
    def __init__(self):
        self.hash = {}
        self.data = codecs.open("unicode_ipa.csv", "r", "utf-8")
        header = self.data.readline()
        for line in self.data:
            line = line.strip()
            tokens = line.split("\t")
            decimal = tokens[2].strip()
            decimal = int(decimal)
            if not self.hash.has_key(decimal):
                self.hash[decimal] = 1
            else:
                self.hash[decimal] += 1

    def compare(self, inputhash):
        c = 0
        for k, v in inputhash.iteritems():
            if not self.hash.has_key(k):
                print("NON-IPA: ", k, v, chr(k))
                c += 1
        if not c == 0:
            print("total: ", c)

    def compare_string(self, decimal):
        if not self.hash.has_key(decimal):
            return decimal

if __name__=="__main__":
    import sys, unicodedata, codecs
    uipa = UnicodeIpaTester()
    # uipa.compare({58:1, 76:1, 77:1, 7725:2})

    test_hash = {}
    file = codecs.open(sys.argv[1], "r", "utf-8")
    for line in file:
        line = line.strip()
        for char in line:
            # print char, hex(ord(char))
            # sys.exit()
            if char == " " or char == u'\ufeff': # ignore space or BOM
                continue
            if not char == "":
                decimal = uipa.compare_string(ord(char))
                if not decimal == None:
                    if not test_hash.has_key(decimal):
                        test_hash[decimal] = 1
                    else:
                        test_hash[decimal] += 1

    if len(test_hash) == 0:
        print("\nHooray! No illegal Unicode IPA characters were found in the input: "+sys.argv[1]+"\n")
    else:
        print("\nThe following table lists the illegal Unicode IPA characters found in the input: "+sys.argv[1]+"\n")
        print("Decimal"+"\t"+"Glyph"+"\t"+"Occurrences") 
        file.close()
        out = codecs.open('invalid_uc.txt', "w", "utf-8")
        for k, v in test_hash.items():
            line = u'%s\t%s\t%s' % (unicode(k), unichr(k), unicode(v))
            print line
            out.write(line + u'\n')
            #out.write(str(k).encode("utf-8")+"\t"+unichr(k).encode("utf-8")+"\t"+str(v).encode("utf-8") + '\n')
            #print(str(k).encode("utf-8")+"\t"+unichr(k).encode("utf-8")+"\t"+str(v).encode("utf-8") + '\n')
            #print( str(k).encode("utf-8")+"\t"+unichr(k).encode("utf-8")+"\t"+str(v).encode("utf-8"))
        print("\n")
        out.close()
