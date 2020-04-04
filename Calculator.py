import re

OPENBRACKET = '('
CLOSEBRACKET = ')'
EXPONENT="^"
DIVISION="/"
MULTIPLY="*"
PLUS="+"
MINUS="-"

EDMAS=[EXPONENT,DIVISION,MULTIPLY,PLUS,MINUS]

def main():

    exprList = expressionToList('((2^10-2^9)+(10*10+100/2/2)+45+10^2*(100-2))')
    answer = solve(exprList)
    print(answer)

def solve(expressionList):
    while len(expressionList) > 1:
        if OPENBRACKET in expressionList:
            indexOpenBracket = getLastOcc(expressionList,OPENBRACKET)
            for indexCloseBracket in range(indexOpenBracket,len(expressionList)):
                if expressionList[indexCloseBracket] == CLOSEBRACKET:
                    break
            answer = solve(expressionList[indexOpenBracket+1:indexCloseBracket])
            popExpressionAndReplace(expressionList,indexOpenBracket,indexCloseBracket,answer)
        else:
            for sign in EDMAS:
                if sign in expressionList:
                    signIndex = expressionList.index(sign)
                    answer = str(resolveIt(expressionList[signIndex-1],expressionList[signIndex+1],sign))
                    popExpressionAndReplace(expressionList,signIndex-1, signIndex+1,answer)
                    break
    return expressionList[0]

def expressionToList(expression):
    exprList = re.split('([()^*+/-])', expression)

    return popUnwanted(exprList,{""," "})

def popExpressionAndReplace(expressionList,start,end, answer):
    for pop in range(start,end+1):
        expressionList.pop(start)
    expressionList.insert(start,answer)

def popUnwanted(expressionList,unwanted):
    expressionList = [listItem for listItem in expressionList if listItem not in unwanted]
    return expressionList


def getLastOcc(expressionList,item):
    expressionList.reverse()
    try:
        lastOccurance=expressionList.index(item)
    except ValueError:
        expressionList.reverse()
        return -1
    expressionList.reverse()
    return len(expressionList)- 1 - lastOccurance

def resolveIt(x,y,sign):
    if sign==EXPONENT:
        return int(x)**int(y)
    elif sign==DIVISION:
        return int(int(x)/int(y))
    elif sign==MULTIPLY:
        return int(x)*int(y)
    elif sign==PLUS:
        return int(x)+int(y)
    elif sign==MINUS:
        return int(x)-int(y)

if __name__ == "__main__":
    main()