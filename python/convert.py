import os

def prepareStr(d):
	
	res=""
	for i in range(0,len(d),2):
		res=res+d[i:i+2]+" "
	return res.strip()	


def hexToByte( hexStr ):
    bytes = []

    hexStr = ''.join( hexStr.split(" ") )

    for i in range(0, len(hexStr), 2):
        bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

    return ''.join( bytes )


data="4546474879"
print hexToByte(prepareStr(data))

