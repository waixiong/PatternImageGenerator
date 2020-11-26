import sys, getopt
import patternDecode

def message():
    print('usage: _decoder.py -d <data>')
    print()
    print('available args:')
    print('-o <outputfile> : optional output text file')
    print('-i <inputfile> : input jpeg image file')

def main(argv):
    data = ''
    inputfile = ''
    outputfile = ''
    haveInput = False
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile=","data="])
    except getopt.GetoptError:
        message()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            message()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            haveInput = True
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    # print('Data is', data)
    # print('Input file is', inputfile)
    # print('Output file is', outputfile)

    # Either data or inputfile
    byteData = b''
    if not haveInput:
        message()
        sys.exit(2)
    
    data = patternDecode.decode(inputfile)
    if len(data) == 0:
        print('Error in decoding')
    if len(outputfile) > 0:
        with open(inputfile, "wb") as f:
            f.write(data)
    else:
        print(data)
    

if __name__ == "__main__":
    main(sys.argv[1:])