#!/usr/local/python
import argparse

# global variables
packetSize = 188
bytesPrintedPerLine = 16
numberOfBytesToRead = 2

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', required=True, type=str, dest='file',
                        metavar='<file_path>', help='Your ts file path')
    parser.add_argument('-r', '--readMode', dest="readMode", action='store_true', default=False,
                        help='(Optional) Read the ts only without modifying it')
    parser.add_argument('-w', '--writeMode', dest="writeMode", action='store_true', default=False,
                       help='(Optional) Allow this script to write the ts')
    parser.add_argument('-fp', '--fromPk', type=int, dest='fromPacket', default=1,
                        metavar='<from_packet_no>', help='(Optional, start from scatch if not specified) From where to start searching your packet')
    parser.add_argument('-tp', '--toPk', type=int, dest='toPacket', default=-1,
                        metavar='<to_packet_no>', help='(Optional, til the end if not specified) To where to stop searching your packet')
    parser.add_argument('-pid', '--pid', type=int, dest='pid', default=-1,
                        metavar='<pid>', help='(Optional) Only read/edit packet with this pid')
    parser.add_argument('-b', '--bytePos', type=int, dest='bytePos', default=-1,
                        metavar='<byte_position_to_be_read/edit>', help='(Optional) Starting from this byte position to view/edit in a 188-bytes packet')
    parser.add_argument('-nb', '--newBytes', type=str, dest='newBytes', default="",
                        metavar='<new_bytes>', help='(Optional) The bytes in Hex, say "8F" you want to write into the new ts starting from certain byte position')

    args = parser.parse_args()
    filePath = args.file
    readMode, writeMode = args.readMode, args.writeMode
    fromPk, toPk = args.fromPacket, args.toPacket
    pid, bytePos = args.pid, args.bytePos
    newBytes = args.newBytes
    if writeMode:
        if newBytes == "" or bytePos == -1: 
            print("You have not specified the newBytes or the bytePos, see -h for more help")
            exit()
    return filePath, readMode, writeMode, fromPk, toPk, pid, bytePos, newBytes

#################### For Read Mode ##################
# read ts in an array of hex string, with each item in the array representing 188 bytes in hex format
def readTS(filePath):
    packetArray = []
    with open(filePath, "rb") as f:
        data = f.read().hex().upper()
        packetArray = [data[start:start+packetSize*2] for start in range(0, len(data), packetSize*2)]
    print (str(len(packetArray)) + " packets read.")
    return packetArray

def printPackets(packetArray, fromPk = 1, toPk = -1, pid = -1, bytePos = -1, numberOfBytesToRead = numberOfBytesToRead):
    toPk = toPk if toPk != -1 else packetSize
    for pkIdx in range(0, len(packetArray)):
        eachPk = packetArray[pkIdx]
        pkNo = pkIdx + 1
        pkPID = (int(eachPk[2:4],16)&0x1f) * 256 + int(eachPk[4:6], 16)

        if pkNo >= fromPk and pkNo <= toPk and (pkPID == pid or pid == -1):
            print ("\nPacket " + str(pkNo) + " with pid = " + str(pkPID) + ": ", end="")
            printPacket(eachPk, bytePos)

def printPacket(packetStr, bytePos = -1, numberOfBytesToRead = numberOfBytesToRead):
    for i in range(0, len(packetStr), 2):
        oneByteInPacket = packetStr[i:i+2]
        byteCnt = i / 2 + 1
        if bytePos == byteCnt:
            bytesToBePrinted = packetStr[i:i+2*numberOfBytesToRead]
            print (bytesToBePrinted, end = '')
        elif i % (bytesPrintedPerLine*2) == 0 and bytePos == -1: 
            lineHeader = "\n" + str(int(i/2))
            if i / 2 < 10:      print (lineHeader, end = ' '*7)
            elif i / 2 < 100:   print (lineHeader, end = ' '*6)
            else:               print (lineHeader, end = ' '*5)
        if bytePos == -1: print (oneByteInPacket, end = " ")
    print ()

#################### For Write Mode ##################
def writeToNewTS(content, fileName):
    f = open(fileName, "wb")
    f.write(content)
    f.close()
    print("Successfully wrote to " + fileName)

def createNewTS(packetArray, bytePos, newBytes, fromPk = 1, toPk = -1, pid = -1):
    newTsInOneString = ""
    toPk = toPk if toPk != -1 else packetSize
    for pkIdx in range(0, len(packetArray)):
        eachPk = packetArray[pkIdx]
        pkNo = pkIdx + 1
        pkPID = (int(eachPk[2:4],16)&0x1f) * 256 + int(eachPk[4:6], 16)

        if pkNo >= fromPk and pkNo <= toPk and (pkPID == pid or pid == -1):
            print ("Write " + newBytes + " to Packet " + str(pkNo) + " with pid = " + str(pkPID) + " at bytePos " + str(bytePos))
            startIdx = (bytePos - 1) * 2
            endIdx = startIdx + len(newBytes)
            eachPk = replaceString(eachPk, newBytes, startIdx, endIdx)

        newTsInOneString += eachPk
    return newTsInOneString

def replaceString(str, newSubStr, fromIdx, toIdx=-1):
    toIdx = len(newSubStr) + fromIdx if toIdx == -1 else toIdx 
    return (str[:fromIdx] + newSubStr + str[toIdx:])

def main():
    filePath, readMode, writeMode, fromPk, toPk, pid, bytePos, newBytes = getArgs()

    # filePath = 'testcase.ts'
    # fromPk, toPk, pid, bytePos = 1, 100, 481, 2

    contentInHexStrs = readTS(filePath)
    toPk = toPk if toPk != -1 else len(contentInHexStrs)
    
    if readMode:
        printPackets(contentInHexStrs, fromPk, toPk, pid, bytePos, numberOfBytesToRead)

    if writeMode:
        newContentInHexStr = createNewTS(contentInHexStrs, bytePos, newBytes, fromPk, toPk, pid)
        newContentInBytes = bytes.fromhex(newContentInHexStr)
        outputFile = filePath.split(".ts")[0] + "_output.ts"
        writeToNewTS(newContentInBytes, outputFile)

if __name__ == "__main__":
    main()
