import re

txt =  """<?php
class MyClass {
    function abc(){ $i=5;
    $z=$i*2;
    echo "One '$=".$z;}
}
?>""".splitlines()

token = []

currentLine = 1

def inBetweenQuotes(txt):

    patterns = '.*"'
    regText = re.search(patterns, txt)
    
    placement = regText.span()

    return txt[placement[0]: placement[1]]

def functionName(txt):

    patterns = ".*\("
    regText = re.search(patterns, txt)
    
    placement = regText.span()

    return txt[placement[0]: placement[1] - 1]

def bracketFunctions(txt):

    if "(" in txt:
        functionsName = functionName(txt)
        token.append([currentLine, "type-identifier", functionsName])
        token.append([currentLine, "Opening Brackets"])

    if ")" in txt:
        token.append([currentLine, "Closing Brackets"])

    if "{" in txt:
        token.append([currentLine, "Opening Curly Brackets"])

    if "}" in txt:
        token.append([currentLine, "Closing Curly Brackets"])

def hasAssignment(txt: str):

    assigmnet = txt.replace("=", " = ")
    assigmnet = assigmnet.replace("*", " * ")
    assigmnetSplit = assigmnet.split(" ")
    
    for asp in assigmnetSplit:
        
        if asp[0] == "$":
            token.append([currentLine, "variable"])
            token.append([currentLine, "type-identifier", asp[1:]])
            
        elif asp == "=":
            token.append([currentLine, "assign"])
    
        elif asp == "*":
            token.append([currentLine, "multiplication"])

        else:

            removeChars = ";})"

            for rvChar in removeChars:
                asp = asp.replace(rvChar, "") 

            if asp.isdigit():
                token.append([currentLine, "Number", asp])

            else:
                token.append([currentLine, "String", asp])

for i in txt:
    
    newTxt = i.split(" ")
    print(newTxt)
    container = ""

    for j in newTxt:

        if j == "<?php":
            token.append([currentLine, "php-opening-tag"])

        if j != ''  and j[0] =='"':
            container = container + j

        if j != '' and '"' in j[1:]:
            container = container + inBetweenQuotes(j)
            token.append([currentLine, "String Literal", container])

        if "." in j:
            token.append([currentLine, "concatenate"])

            afterConcate = j.index(".")
            afterConcateTxt = j[afterConcate + 1:]

            hasAssignment(afterConcateTxt)

            if ";" in afterConcateTxt:
                token.append([currentLine, "semicolon"])

            bracketFunctions(afterConcateTxt)

        elif j == "class":
            token.append([currentLine, "class"])

        elif j == "function":
            token.append([currentLine, "function"])

        elif j == "?>":
            token.append([currentLine, "php-closing-tag"])

        elif j == "echo":
            token.append([currentLine, "print-output"])

        elif "=" in j:
            hasAssignment(j)

            if ";" in j:
                token.append([currentLine, "semicolon"])

        elif ";" in j:
            token.append([currentLine, "semicolon"])

        elif re.match("[a-zA-Z]+", j) and "(" not in j:
            token.append([currentLine, "type-identifier", j])

        else:
            bracketFunctions(j)

    currentLine += 1

print(token)
