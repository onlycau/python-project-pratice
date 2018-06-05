#-*- coding:utf-8 -*-


'''extract from https://www.cnblogs.com/21207-iHome/p/6085334.html'''

class StateMachine:
    def __init__(self): 
        self.handlers = {}        # 状态转移函数字典
        self.startState = None    # 初始状态
        self.endStates = []       # 最终状态集合
    
    # 参数name为状态名,handler为状态转移函数,end_state表明是否为最终状态
    def add_state(self, name, handler, end_state=0):
        name = name.upper() # 转换为大写
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name.upper()

    def run(self, cargo):
        try:
            handler = self.handlers[self.startState]
        except:
            raise InitializationError("must call .set_start() before .run()")
        if not self.endStates:
            raise  InitializationError("at least one state must be an end_state")
        
        # 从Start状态开始进行处理
        while True: 
            (newState, cargo) = handler(cargo)     # 经过状态转移函数变换到新状态
            if newState.upper() in self.endStates: # 如果跳到终止状态,则打印状态并结束循环
                print("reached ", newState)
                break 
            else:                        # 否则将转移函数切换为新状态下的转移函数 
                handler = self.handlers[newState.upper()]   

# 有限状态集合
positive_adjectives = ["great","super", "fun", "entertaining", "easy"]
negative_adjectives = ["boring", "difficult", "ugly", "bad"]

# 自定义状态转变函数
def start_transitions(txt):
    # 过指定分隔符对字符串进行切片,默认为空格分割,参数num指定分割次数
    # 将"Python is XXX"语句分割为"Python"和之后的"is XXX"
    splitted_txt = txt.split(None, 1)  
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
    if word == "Python":   
        newState = "Python_state" # 如果第一个词是Python则可转换到"Python状态"
    else:
        newState = "error_state"  # 如果第一个词不是Python则进入终止状态
    return (newState, txt)        # 返回新状态和余下的语句txt

def python_state_transitions(txt):
    splitted_txt = txt.split(None,1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
    if word == "is":
        newState = "is_state"
    else:
        newState = "error_state"
    return (newState, txt)

def is_state_transitions(txt):
    splitted_txt = txt.split(None,1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
    if word == "not":
        newState = "not_state"
    elif word in positive_adjectives:
        newState = "pos_state"
    elif word in negative_adjectives:
        newState = "neg_state"
    else:
        newState = "error_state"
    return (newState, txt)

def not_state_transitions(txt):
    splitted_txt = txt.split(None,1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
    if word in positive_adjectives:
        newState = "neg_state"
    elif word in negative_adjectives:
        newState = "pos_state"
    else:
        newState = "error_state"
    return (newState, txt)



if __name__== "__main__":
    m = StateMachine()
    m.add_state("Start", start_transitions)      # 添加初始状态
    m.add_state("Python_state", python_state_transitions)
    m.add_state("is_state", is_state_transitions)
    m.add_state("not_state", not_state_transitions)
    m.add_state("neg_state", None, end_state=1)  # 添加最终状态
    m.add_state("pos_state", None, end_state=1)
    m.add_state("error_state", None, end_state=1)
    
    m.set_start("Start") # 设置开始状态
    m.run("Python is great")
    m.run("Python is not fun")
    m.run("Perl is ugly")
    m.run("Pythoniseasy")
