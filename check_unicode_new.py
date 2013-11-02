# -*- coding: utf-8 -*-
import unicodedata, collections, codecs, sys

# load the unicode table
with codecs.open("unicode_ipa.csv", "r", "utf-8") as file:
    ipa = set(line[0] for line in file if not (line.startswith('glyph') or len(line.strip())==0))


# load the file and covnert it into characters
with codecs.open(sys.argv[1], "r", "utf-8") as file:
    # ignore BOM, space separators and unicode stuff
    badchars = collections.Counter(c for c in file.read() if not (c in ipa or c == u'\ufeff' or unicodedata.category(c) in ('Zs', 'Zl'))) 
                                    
    
# now print all the stuff
if len(badchars) == 0:
        print u"\nHooray! No illegal Unicode IPA characters were found in the input file '%s'\n" % sys.argv[1]
else:
    print u"\nThe following table lists the illegal Unicode IPA characters found in the input file '%s'" % sys.argv[1]
    print u"Decimal\tGlyph\tOccurrences"
    for c, number in badchars.iteritems():
        print u"%s\t%s\t%s" % (ord(c), c, number)
    


