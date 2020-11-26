import sys, getopt
import patternEncode

def message():
    print('usage: _encoder.py -d <data>')
    print()
    print('available args:')
    print('-d <data>')
    print('-o <outputfile> : output image file, default as \'Output.jpg\'')
    print('-i <inputfile> : use input file if data is from file')

def main(argv):
    data = ''
    inputfile = ''
    outputfile = ''
    haveInput = False
    try:
        opts, args = getopt.getopt(argv,"hi:d:o:",["ifile=","ofile=","data="])
    except getopt.GetoptError:
        message()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            message()
            sys.exit()
        elif opt in ("-d", "--data"):
            data = arg
            haveInput = True
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
    else:
        if len(data) > 0:
            byteData = data.encode('utf_8')
        else:
            with open(inputfile, "rb") as f:
                byte = f.read(1)
                while byte:
                    # print(byte)
                    byteData += byte
                    byte = f.read(1)
    if outputfile == '':
        # message()
        # sys.exit(2)
        outputfile = 'Output.jpg'
    
    patternEncode.encode(byteData, outputfile)

if __name__ == "__main__":
    main(sys.argv[1:])


# 4 2
# 9 8
# 16 18
# 25 32
# 36 50
# X 2(X-1)**2