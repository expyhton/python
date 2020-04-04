import re

EDMAS=["^","/","*","+","-"]

def main():
    exprList = expressionToList('((2^10-2^9)+(10*10+100/2/2)+45+10^2*(100-2))')

    fixNegatives(exprList)
    answer = solve(exprList)
    print(answer)

def solve(expressionList):
    while len(expressionList) > 1:
        if '(' in expressionList:
            indexOpenBracket = getLastOcc(expressionList,'(')
            for indexCloseBracket in range(indexOpenBracket,len(expressionList)):
                if expressionList[indexCloseBracket] == ')':
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
    lastOccurance=expressionList.index(item)
    expressionList.reverse()
    return len(expressionList)- 1 - lastOccurance

def fixNegatives(expressionList):
    for index,item in enumerate(expressionList):
        if index==0 and item=='-':
            popExpressionAndReplace(expressionList,index,index+1, "".join([expressionList[index],expressionList[index+1]]))
        elif index > 0 and item=='-':
            if expressionList[index-1] in EDMAS or expressionList[index-1] == "(":
                popExpressionAndReplace(expressionList,index,index+1, "".join([expressionList[index],expressionList[index+1]]))

def resolveIt(x,y,sign):
    if sign=="^":
        return float(x)**float(y)
    elif sign=="/":
        return float(x)/float(y)
    elif sign=="*":
        return float(x)*float(y)
    elif sign=="+":
        return float(x)+float(y)
    elif sign=="-":
        return float(x)-float(y)

if __name__ == "__main__":
    main()
