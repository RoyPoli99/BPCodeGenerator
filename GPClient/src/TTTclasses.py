import json

btNames = ["bp.registerBThread(\"AddThirdO(<\"+f[p[0]].x+\",\"+f[p[0]].y+\">,\"+\"<\"+f[p[1]].x+\",\"+f[p[1]].y+\">,\"+\"<\"+f[p[2]].x+\",\"+f[p[2]].y+\">)\",function(){",
           "bp.registerBThread(\"PreventThirdX(<\"+f[p[0]].x+\",\"+f[p[0]].y+\">,\"+\"<\"+f[p[1]].x+\",\"+f[p[1]].y+\">,\"+\"<\"+f[p[2]].x+\",\"+f[p[2]].y+\">)\",function(){",
           "bp.registerBThread(\"PreventFork22X(<\"+f[p[0]].x+\",\"+f[p[0]].y+\">,\"+\"<\"+f[p[1]].x+\",\"+f[p[1]].y+\">)\",function(){",
           "bp.registerBThread(\"PreventFork02X(<\"+f[p[0]].x+\",\"+f[p[0]].y+\">,\"+\"<\"+f[p[1]].x+\",\"+f[p[1]].y+\">)\",function(){",
           "bp.registerBThread(\"PreventFork20X(<\"+f[p[0]].x+\",\"+f[p[0]].y+\">,\"+\"<\"+f[p[1]].x+\",\"+f[p[1]].y+\">)\",function(){",
           "bp.registerBThread(\"PreventFork00X(<\"+f[p[0]].x+\",\"+f[p[0]].y+\">,\"+\"<\"+f[p[1]].x+\",\"+f[p[1]].y+\">)\",function(){",
           "bp.registerBThread(\"PreventForkdiagX(<\"+f[p[0]].x+\",\"+f[p[0]].y+\">,\"+\"<\"+f[p[1]].x+\",\"+f[p[1]].y+\">)\",function(){",
           "bp.registerBThread(\"Center\",function(){",
           "bp.registerBThread(\"Corners\",function(){",
           "bp.registerBThread(\"Sides\",function(){"
           ]

currentBtLineIndex = 1
currentBtOtherIndex = 1

class root_wrapper:
    def __init__(self, root):
        self.root = root

    def __str__(self):
        return str(root)

    __repr__ = __str__


class root:

    def __init__(self, btgLine,btgOther):
        self.btgLine = btgLine
        self.btgOther = btgOther

    def __str__(self):
        global currentBtLineIndex, currentBtOtherIndex
        currentBtLineIndex = 1
        currentBtOtherIndex = 1
        res = ""
        res += str(self.btgLine)
        # res += "bp.sync({request: bp.Event(\"THREAD0\")}, 120);}});\n"
        res += str(self.btgOther)
        # res += "bp.sync({request: bp.Event(\"THREAD1\")}, 120);}});\n"
        return str(res)

    __repr__ = __str__


class btGroupLine:
    def __init__(self, bts):
        self.bts = bts

    def __str__(self):
        code_str = ""
        for bt in self.bts:
            code_str += str(bt) + "\n"
        return code_str

    __repr__ = __str__


class btGroupOther:
    def __init__(self, bts):
        self.bts = bts

    def __str__(self):
        code_str = ""
        for bt in self.bts:
            code_str += str(bt) + "\n"
        return code_str

    __repr__ = __str__


class btLine:
    def __init__(self, whiletrue):
        self.whiletrue = whiletrue

    def __str__(self):
        global currentBtLineIndex
        currName = "bp.registerBThread(\"O_Player_Line_" + str(currentBtLineIndex) + "\", function(){"
        currentBtLineIndex = currentBtLineIndex + 1
        return currName + "\n" + str(self.whiletrue)# + "});\n"

    __repr__ = __str__


class btOther:
    def __init__(self, whiletrue):
        self.whiletrue = whiletrue

    def __str__(self):
        global currentBtOtherIndex
        currName ="bp.registerBThread(\"O_Player_Other_" + str(currentBtOtherIndex) + "\", function(){"
        currentBtOtherIndex = currentBtOtherIndex + 1
        return currName + "\n" + str(self.whiletrue)# + "});\n"

    __repr__ = __str__


class btC:
    def __init__(self, whiletrue):
        self.whiletrue = whiletrue

    def __str__(self):
        global currentBtNameIndex, btNames
        currName = btNames[currentBtNameIndex]
        currentBtNameIndex = (currentBtNameIndex + 1) % 10
        return currName + str(self.whiletrue)# + "});\n"

    __repr__ = __str__


class while_trueLine:
    def __init__(self, waits, request):
        self.request = request
        self.waits = waits

    def __str__(self):
        code_str = ""
        for wait in self.waits:
            code_str += str(wait) + "\n"
        code_str += str(self.request) + "\n"
        return "while(true){\n" + code_str + "}\n});"
    __repr__ = __str__


class while_trueB:
    def __init__(self, waits, request):
        self.request = request
        self.waits = waits

    def __str__(self):
        code_str = ""
        for wait in self.waits:
            code_str += str(wait)
        code_str += str(self.request)
        return "while(true){" + code_str# + "}"
    __repr__ = __str__


class while_trueOther:
    def __init__(self, waits, request):
        self.request = request
        self.waits = waits

    def __str__(self):
        code_str = ""
        for wait in self.waits:
            code_str += str(wait) + "\n"
        code_str += str(self.request) + "\n"
        return "while(true){\n" + code_str + "}\n});"
    __repr__ = __str__


class wait02:
    def __init__(self, events):
        self.events = events

    def __str__(self):
        code_str = ""
        for event in self.events:
            code_str += str(event)
            code_str += ", "
        code_str = code_str[:-2]
        return "bp.sync({waitFor:[" + code_str + "]});"
    __repr__ = __str__


class wait01:
    def __init__(self, events):
        self.events = events

    def __str__(self):
        code_str = ""
        for event in self.events:
            code_str += str(event)
            code_str += ", "
        code_str = code_str[:-2]
        return "bp.sync({waitFor:[" + code_str + "]});"
    __repr__ = __str__


class waitC:
    def __init__(self, events):
        self.events = events

    def __str__(self):
        code_str = ""
        for event in self.events:
            code_str += str(event)
            code_str += ", "
        code_str = code_str[:-2]
        return "bp.sync({waitFor:[" + code_str + "]});"
    __repr__ = __str__


class request02:
    def __init__(self, events, priority):
        self.events = events
        self.priority = priority

    def __str__(self):
        code_str = ""
        for event in self.events:
            code_str += str(event)
            code_str += ", "
        code_str = code_str[:-2]
        return "bp.sync({request:[" + code_str + "]}," + str(self.priority) + ");"
    __repr__ = __str__


class request01:
    def __init__(self, events, priority):
        self.events = events
        self.priority = priority

    def __str__(self):
        code_str = ""
        for event in self.events:
            code_str += str(event)
            code_str += ", "
        code_str = code_str[:-2]
        return "bp.sync({request:[" + code_str + "]}," + str(self.priority) + ");"
    __repr__ = __str__


class requestC:
    def __init__(self, events, priority):
        self.events = events
        self.priority = priority

    def __str__(self):
        code_str = ""
        for event in self.events:
            code_str += str(event)
            code_str += ", "
        code_str = code_str[:-2]
        return "bp.sync({request:[" + code_str + "]}," + str(self.priority) + ");"
    __repr__ = __str__


class Perm02:
    def __init__(self, event):
        self.event = event

    def __str__(self):
        return str(self.event)
    __repr__ = __str__


class Perm02_X:
    def __init__(self, pos1):
        self.pos1 = pos1

    def __str__(self):
        return "X(l[" + str(self.pos1) + "].x,l[" + str(self.pos1) + "].y)"
    __repr__ = __str__


class Perm02_O:
    def __init__(self, pos1):
        self.pos1 = pos1

    def __str__(self):
        return "O(l[" + str(self.pos1) + "].x,l[" + str(self.pos1) + "].y)"
    __repr__ = __str__


class Perm01:
    def __init__(self, event):
        self.event = event

    def __str__(self):
        return str(self.event)
    __repr__ = __str__


class Perm01_X:
    def __init__(self, pos1):
        self.pos1 = pos1

    def __str__(self):
        return "X(f[p[" + str(self.pos1) + "]].x,f[p[" + str(self.pos1) + "]].y)"
    __repr__ = __str__


class Perm01_O:
    def __init__(self, pos1):
        self.pos1 = pos1

    def __str__(self):
        return "O(f[p[" + str(self.pos1) + "]].x,f[p[" + str(self.pos1) + "]].y)"
    __repr__ = __str__


class Concrete:
    def __init__(self, event):
        self.event = event

    def __str__(self):
        return str(self.event)
    __repr__ = __str__


class Concrete_X:
    def __init__(self, pos1, pos2):
        self.pos1 = pos1
        self.pos2 = pos2

    def __str__(self):
        return "X(" + str(self.pos1) + "," + str(self.pos2) + ")"
    __repr__ = __str__


class Concrete_O:
    def __init__(self, pos1, pos2):
        self.pos1 = pos1
        self.pos2 = pos2

    def __str__(self):
        return "O(" + str(self.pos1) + "," + str(self.pos2) + ")"
    __repr__ = __str__


class position:
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)
    __repr__ = __str__


class positionf:
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)
    __repr__ = __str__


class priority:
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)
    __repr__ = __str__


def root_wrapperFunc(root):
    return root_wrapper(root)


def rootFunc(btgLine, btgOther):
    return root(btgLine,btgOther)


def btLineGroupFunc(*bts):
    return btGroupLine(bts)


def btOtherGroupFunc(*bts):
    return btGroupOther(bts)


def btLineFunc(while_trueA):
    return btLine(while_trueA)


def btOtherFunc(while_trueB):
    return btOther(while_trueB)


def btCFunc(while_trueC):
    return btC(while_trueC)


def while_trueLine_0(request):
    return while_trueLine([], request)


def while_trueLine_1(wait1, request):
    return while_trueLine([wait1], request)


def while_trueLine_2(wait1, wait2, request):
    return while_trueLine([wait1, wait2], request)


def while_trueB_0(request):
    return while_trueB([], request)


def while_trueB_1(wait1, request):
    return while_trueB([wait1], request)


def while_trueB_2(wait1, wait2, request):
    return while_trueB([wait1, wait2], request)


def while_trueOther_0(request):
    return while_trueOther([], request)


def while_trueOther_1(wait1, request):
    return while_trueOther([wait1], request)


def while_trueOther_2(wait1, wait2, request):
    return while_trueOther([wait1, wait2], request)


def wait02_1(ev1):
    return wait02([ev1])


def wait02_2(ev1, ev2):
    return wait02([ev1, ev2])


def wait02_3(ev1, ev2, ev3):
    return wait02([ev1, ev2, ev3])


def wait02_4(ev1, ev2, ev3, ev4):
    return wait02([ev1, ev2, ev3, ev4])


def wait01_1(ev1):
    return wait01([ev1])


def wait01_2(ev1, ev2):
    return wait01([ev1, ev2])


def wait01_3(ev1, ev2, ev3):
    return wait01([ev1, ev2, ev3])


def wait01_4(ev1, ev2, ev3, ev4):
    return wait01([ev1, ev2, ev3, ev4])


def waitC_1(ev1):
    return waitC([ev1])


def waitC_2(ev1, ev2):
    return waitC([ev1, ev2])


def waitC_3(ev1, ev2, ev3):
    return waitC([ev1, ev2, ev3])


def waitC_4(ev1, ev2, ev3, ev4):
    return waitC([ev1, ev2, ev3, ev4])


def request02_1(ev1, prio):
    return request02([ev1], prio)


def request02_2(ev1, ev2, prio):
    return request02([ev1, ev2], prio)


def request02_3(ev1, ev2, ev3, prio):
    return request02([ev1, ev2, ev3], prio)


def request02_4(ev1, ev2, ev3, ev4, prio):
    return request02([ev1, ev2, ev3, ev4], prio)


def request01_1(ev1, prio):
    return request01([ev1], prio)


def request01_2(ev1, ev2, prio):
    return request01([ev1, ev2], prio)


def request01_3(ev1, ev2, ev3, prio):
    return request01([ev1, ev2, ev3], prio)


def request01_4(ev1, ev2, ev3, ev4, prio):
    return request01([ev1, ev2, ev3, ev4], prio)


def requestC_1(ev1, prio):
    return requestC([ev1], prio)


def requestC_2(ev1, ev2, prio):
    return requestC([ev1, ev2], prio)


def requestC_3(ev1, ev2, ev3, prio):
    return requestC([ev1, ev2, ev3], prio)


def requestC_4(ev1, ev2, ev3, ev4, prio):
    return requestC([ev1, ev2, ev3, ev4], prio)


def Perm02_X_Func(pos1):
    return Perm02_X(pos1)


def Perm02_O_Func(pos1):
    return Perm02_O(pos1)


def Perm02_Func(other):
    return Perm02(other)


def Perm01_X_Func(pos1):
    return Perm01_X(pos1)


def Perm01_O_Func(pos1):
    return Perm01_O(pos1)


def Perm01_Func(other):
    return Perm01(other)


def Concrete_X_Func(pos1, pos2):
    return Concrete_X(pos1, pos2)


def Concrete_O_Func(pos1, pos2):
    return Concrete_O(pos1, pos2)


def Concrete_Func(other):
    return Concrete(other)


def posFunc(pos):
    return pos


def posfFunc(pos):
    return pos


def priorityFunc(priority):
    return priority