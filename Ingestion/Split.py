inputfile = "lexusnexus.txt"  #or whatever the filename is
fread = open(inputfile)
count = 0
fwrite = open("LexisNexis%s" % (count), 'w') #open new file called lexusnexis + count 
for line in fread: #loop throught input file
    if "of 1144 DOCUMENTS" in line: #when your read in the header line stop and close
        fwrite.close()
        count = count + 1
        fwrite = open("LexisNexis%s" % (count), 'w') #open new file
        fwrite.write(line) 
    else:
        fwrite.write(line)
fwrite.close()
fread.close()
