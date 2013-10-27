""" 
Script to check for non-legal Unicode-IPA characters.

For use with Python version 3 or greater.

"""

class UnicodeIpaTester:
    def __init__(self):
        self.hash = {}
        self.data = open("unicode_ipa.csv", "r")
        header = self.data.readline()
        for line in self.data:
            line = line.strip()
            tokens = line.split("\t")
            decimal = tokens[2].strip()
            decimal = int(decimal)
            if not decimal in self.hash:
                self.hash[decimal] = 1
            else:
                self.hash[decimal] += 1

    def compare(self, inputhash):
        c = 0
        for k, v in inputhash.items():
            if not k in self.hash:
                print("NON-IPA: ", k, v, chr(k))
                c += 1
        if not c == 0:
            print("total: ", c)

    def compare_string(self, decimal):
        if not decimal in self.hash:
            return decimal

if __name__=="__main__":
    import sys, unicodedata
    uipa = UnicodeIpaTester()
    # uipa.compare({58:1, 76:1, 77:1, 7725:2})

    test_hash = {}
    file = open(sys.argv[1], "r")
    for line in file:
        line = line.strip()
        if line.startswith("#"):
            continue

        for char in line:
            if char == " ":
                continue
            if not char == "":
                decimal = uipa.compare_string(ord(char))
                if not decimal == None:
                    # print("NON-IPA: ", decimal, chr(decimal))
                    if not decimal in test_hash:
                        test_hash[decimal] = 1
                    else:
                        test_hash[decimal] += 1

    if len(test_hash) == 0:
        print("\nHooray! No illegal Unicode IPA characters were found in the input: "+sys.argv[1]+"\n")
    else:
        print("\nThe following table lists the illegal Unicode IPA characters found in the input: "+sys.argv[1]+"\n")
        print("Decimal"+"\t"+"Glyph"+"\t"+"Occurrences") 
        for k, v in test_hash.items():
            print(str(k)+"\t"+chr(k)+"\t"+str(v))
        print("\n")
