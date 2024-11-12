from random import choice, choices

RULES = {}
nonTerminals = None

def getGrammar(filename):
    global nonTerminals, RULES
    RULES = {}
    nonTerminals = []
    with open(filename, 'r', encoding='utf-8') as file:
        lines = [line.rstrip() for line in file]

    for i in range(len(lines)):
        nonTerminals.append(lines[i][0])
        lines[i] = (lines[i].replace(' ', '')).partition('>')[2]
        RULES[nonTerminals[i]] = lines[i].split('|')
    
    print("Правила: ", RULES)

def assignWeights(grammar):
    weights = {}
    
    for nonT, rules in grammar.items():
        lengths = [len(rule) for rule in rules]
        total_length = sum([1 / length for length in lengths]) 
        weights[nonT] = [(1 / length) / total_length for length in lengths]
    return weights

def check_nonT_in_str(string, nonT):
    result = False
    for i in string:
        if i in nonT:
            result = True
            break
    return result

def generateString(grammar, nonT, max_depth=10):
    string = nonT[0]
    depth = 0
    weights = assignWeights(grammar) 
    
    while check_nonT_in_str(string, nonT) and depth < max_depth:
        new = ""
        for i in string:
            if i in nonT:
                new += choice(RULES[i]) 
            else:
                new += i
        string = new
        depth += 1
    
    if depth == max_depth:
        while check_nonT_in_str(string, nonT):
            new = ""
            for i in string:
                if i in nonT:
                    new += choices(RULES[i], weights[i])[0]  
                else:
                    new += i
            string = new
    
    return string
            
def checkString(string, grammar, max, nonT):
    count = 0
    res = False
    while count != max:
        spy = generateString(grammar, nonT)
        if spy == string:
            res = True
            break
        count += 1
    return res

def checkstring(string, grammar, initial_state="S", max_depth=10):
    index = [0]
    def parse(rule, depth):
        if depth > max_depth:
            return False

        start_index = index[0]
        if rule not in grammar:
            if index[0] < len(string) and string[index[0]] == rule:
                index[0] += 1
                return True
            return False
        if rule in grammar:
            for production in grammar[rule]:
                saved_index = index[0]
                parts = list(production)
                success = all(parse(part, depth + 1) for part in parts)

                if success:
                    return True
                index[0] = saved_index

        index[0] = start_index
        return False

    return parse(initial_state, 0) and index[0] == len(string)
    

while True:
    print(" \
        1. Грамматика 1\n \
        2. Грамматика 2\n \
        3. Грамматика 3\n")

    o = int(input("^: "))

    match o:
        case 1:
            getGrammar('lab3/grammar1.txt')
            print(" \
                    1. Сгенерировать\n \
                    2. Проверить")
            choice1 = input("^: ")
            match choice1:
                case "1":
                    if len(RULES) != 0:
                        s = generateString(RULES, nonTerminals)
                        print("result: ", s)
                    else:
                        print(" :( ")
                case "2":
                    if len(RULES) != 0:
                        s = input("input: ")
                        res = checkString(s, RULES, 100000, nonTerminals)
                        if res == True:
                            print(f'Строка {s} существует :)')
                        else:
                            print(f'Строка {s} не существует :(')
                    else:
                        print(" :( ")
        case 2:
            getGrammar('lab3/grammar2.txt')
            print(" \
                    1. Сгенерировать\n \
                    2. Проверить")
            choice2 = input("^: ")
            match choice2:
                case "1":
                    if len(RULES) != 0:
                        s = generateString(RULES, nonTerminals)
                        print("result: ", s)
                    else:
                        print(" :( ")
                case "2":
                    if len(RULES) != 0:
                        s = input("input: ")
                        res = checkString(s, RULES, 100000, nonTerminals)
                        if res == True:
                            print(f'Строка {s} существует :)')
                        else:
                            print(f'Строка {s} не существует :(')
                    else:
                        print(" :( ")
            
        case 3:
            getGrammar('lab3/grammar3.txt')
            print(" \
                    1. Сгенерировать\n \
                    2. Проверить")
            choice3 = input("^: ")
            match choice3:
                case "1":
                    if len(RULES) != 0:
                        s = generateString(RULES, nonTerminals)
                        print("result: ", s)
                    else:
                        print(" :( ")
                case "2":
                    if len(RULES) != 0:
                        s = input("input: ")
                        res = checkString(s, RULES, 100000, nonTerminals)
                        if res == True:
                            print(f'Строка {s} существует :)')
                        else:
                            print(f'Строка {s} не существует :(')
                    else:
                        print(" :( ")
        
        case _: break
        