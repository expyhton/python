import re
import time

EDMAS=["^","/","*","+","-"]

def main():
    tic = time.perf_counter()
    exprList = expressionToList('(1210.44-2-2-2-(-2^2)*(-2+2))-10^2*2+100+299.44')

    #fixNegatives(exprList)
    answer = solve(exprList)
    print(answer)
    toc = time.perf_counter()

    #print(f"{toc:0.8f}-{tic:0.8f} = {toc - tic:0.8f}")

def solve(expressionList):
    while len(expressionList) > 1:
        fixNegatives(expressionList)
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

#String to list
def expressionToList(expression):
    exprList = re.split('([()^*+/-])', expression)

    return popUnwanted(exprList,{""," "})

#Get rid of brackets, and replace with resolved expression
def popExpressionAndReplace(expressionList,start,end, answer):
    if start != 0 and expressionList[start-1].isnumeric(): #insert a '*' if it's hidden (ie 7(7)=14)
        expressionList.insert(start,'*')
        start+=1
        end+=1

    for pop in range(start,end+1):
        expressionList.pop(start)
    expressionList.insert(start,answer)

#Re-structure list to remove unwanted list items. ie '' and ' '
def popUnwanted(expressionList,unwanted):
    expressionList = [listItem for listItem in expressionList if listItem not in unwanted]
    return expressionList

#like rindex for strings
def getLastOcc(expressionList,item):
    expressionList.reverse()
    lastOccurance=expressionList.index(item)
    expressionList.reverse()
    return len(expressionList)- 1 - lastOccurance

#Restructures items to have negative to preform proper substractions
def fixNegatives(expressionList):

    for index,item in enumerate(expressionList):
        if index==0 and item=='-' and expressionList[index+1].isnumeric():
            popExpressionAndReplace(expressionList,index,index+1, "".join([expressionList[index],expressionList[index+1]]))
        elif index > 0 and item=='-':
            if expressionList[index-1] in EDMAS or expressionList[index-1] == "(":
                print(index,")", expressionList)
                popExpressionAndReplace(expressionList,index,index+1, "".join([expressionList[index],expressionList[index+1]]))
            elif index+2 == len(expressionList):
                expressionList[index]= '+'
                expressionList[index+1]= str(float(expressionList[index+1]) * -1)
            elif expressionList[index+2] in "+-" and expressionList[index+1] not in "()^/*+-" and expressionList[index-1] not in "()^/*+-":
                expressionList[index]= '+'
                expressionList[index+1]= str(float(expressionList[index+1]) * -1)                

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
