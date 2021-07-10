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

currentBtNameIndex = 0

class root_wrapper:
    def __init__(self, root):
        self.root = root

    def __str__(self):
        return str(root)

    __repr__ = __str__


class root:

    def __init__(self, btl1,btl2,btf1,btf2,btf3,btf4,btf5,bt1,bt2,bt3):
        self.btl1 = btl1
        self.btl2 = btl2
        self.btf1 = btf1
        self.btf2 = btf2
        self.btf3 = btf3
        self.btf4 = btf4
        self.btf5 = btf5
        self.bt1 = bt1
        self.bt2 = bt2
        self.bt3 = bt3

    def __str__(self):
        res = ""
        res += str(self.btl1)
        res += "bp.sync({request: bp.Event(\"THREAD0\")}, 120);}});\n"
        res += str(self.btl2)
        res += "bp.sync({request: bp.Event(\"THREAD1\")}, 120);}});\n"
        res += str(self.btf1)
        res += "bp.sync({request: bp.Event(\"THREAD2\")}, 120);}});\n"
        res += str(self.btf2)
        res += "bp.sync({request: bp.Event(\"THREAD3\")}, 120);}});\n"
        res += str(self.btf3)
        res += "bp.sync({request: bp.Event(\"THREAD4\")}, 120);}});\n"
        res += str(self.btf4)
        res += "bp.sync({request: bp.Event(\"THREAD5\")}, 120);}});\n"
        res += str(self.btf5)
        res += "bp.sync({request: bp.Event(\"THREAD6\")}, 120);}});\n"
        res += str(self.bt1)
        res += "bp.sync({request: bp.Event(\"THREAD7\")}, 120);}});\n"
        res += str(self.bt2)
        res += "bp.sync({request: bp.Event(\"THREAD8\")}, 120);}});\n"
        res += str(self.bt3)
        res += "bp.sync({request: bp.Event(\"THREAD9\")}, 120);}});\n"
        return str(res)

    __repr__ = __str__


class btA:
    def __init__(self, whiletrue):
        self.whiletrue = whiletrue

    def __str__(self):
        global currentBtNameIndex, btNames
        currName = btNames[currentBtNameIndex]
        currentBtNameIndex = (currentBtNameIndex + 1) % 10
        return currName + str(self.whiletrue)# + "});\n"

    __repr__ = __str__


class btB:
    def __init__(self, whiletrue):
        self.whiletrue = whiletrue

    def __str__(self):
        global currentBtNameIndex, btNames
        currName = btNames[currentBtNameIndex]
        currentBtNameIndex = (currentBtNameIndex + 1) % 10
        return currName + str(self.whiletrue)# + "});\n"

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


class while_trueA:
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


class while_trueC:
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
        return "X(f[p[" + str(self.pos1) + "]].x,f[p[" + str(self.pos1) + "]].y)"
    __repr__ = __str__


class Perm02_O:
    def __init__(self, pos1):
        self.pos1 = pos1

    def __str__(self):
        return "O(f[p[" + str(self.pos1) + "]].x,f[p[" + str(self.pos1) + "]].y)"
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


def rootFunc(btl1,btl2,btf1,btf2,btf3,btf4,btf5,bt1,bt2,bt3):
    return root(btl1,btl2,btf1,btf2,btf3,btf4,btf5,bt1,bt2,bt3)


def btAFunc(while_trueA):
    return btA(while_trueA)


def btBFunc(while_trueB):
    return btB(while_trueB)


def btCFunc(while_trueC):
    return btC(while_trueC)


def while_trueA_0(request):
    return while_trueA([], request)


def while_trueA_1(wait1, request):
    return while_trueA([wait1], request)


def while_trueA_2(wait1, wait2, request):
    return while_trueA([wait1, wait2], request)


def while_trueB_0(request):
    return while_trueB([], request)


def while_trueB_1(wait1, request):
    return while_trueB([wait1], request)


def while_trueB_2(wait1, wait2, request):
    return while_trueB([wait1, wait2], request)


def while_trueC_0(request):
    return while_trueC([], request)


def while_trueC_1(wait1, request):
    return while_trueC([wait1], request)


def while_trueC_2(wait1, wait2, request):
    return while_trueC([wait1, wait2], request)


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