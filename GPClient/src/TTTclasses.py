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
        res += str(self.btl2)
        res += str(self.btf1)
        res += str(self.btf2)
        res += str(self.btf3)
        res += str(self.btf4)
        res += str(self.btf5)
        res += str(self.bt1)
        res += str(self.bt2)
        res += str(self.bt3)
        return str(res)

    __repr__ = __str__


class btl:
    def __init__(self, whiletruel):
        self.whiletruel = whiletruel

    def __str__(self):
        global currentBtNameIndex, btNames
        currName = btNames[currentBtNameIndex]
        currentBtNameIndex = (currentBtNameIndex + 1) % 10
        return currName + str(self.whiletruel) + "});\n"

    __repr__ = __str__


class btf:
    def __init__(self, whiletruef):
        self.whiletruef = whiletruef

    def __str__(self):
        global currentBtNameIndex, btNames
        currName = btNames[currentBtNameIndex]
        currentBtNameIndex = (currentBtNameIndex + 1) % 10
        return currName + str(self.whiletruef) + "});\n"

    __repr__ = __str__


class bt:
    def __init__(self, whiletrue):
        self.whiletrue = whiletrue

    def __str__(self):
        global currentBtNameIndex, btNames
        currName = btNames[currentBtNameIndex]
        currentBtNameIndex = (currentBtNameIndex + 1) % 10
        return currName + str(self.whiletrue) + "});\n"

    __repr__ = __str__


class while_truel3:
    def __init__(self, wait_forl1,wait_forl2, requestl):
        self.requestl = requestl
        self.wait_forl1 = wait_forl1
        self.wait_forl2 = wait_forl2

    def __str__(self):
        return "while(true){" + str(self.wait_forl1) + str(self.wait_forl2) + str(self.requestl) + "}"
    __repr__ = __str__


class while_truef1:
    def __init__(self, request):
        self.request = request
    def __str__(self):
        return "while(true){" + str(self.request)+ "}"
    __repr__ = __str__


class while_truef2:
    def __init__(self, wait_forf, request):
        self.request = request
        self.wait_forf = wait_forf
    def __str__(self):
        return "while(true){" + str(self.wait_forf) + str(self.request)+ "}"
    __repr__ = __str__


class while_truef3:
    def __init__(self, wait_forf1,wait_forf2, request):
        self.request = request
        self.wait_forf1 = wait_forf1
        self.wait_forf2 = wait_forf2

    def __str__(self):
        return "while(true){" + str(self.wait_forf1) + str(self.wait_forf2) + str(self.request) + "}"
    __repr__ = __str__


class whiletrue:
    def __init__(self, request):
        self.request = request
    def __str__(self):
        return "while(true){" + str(self.request) + "}"
    __repr__ = __str__


class wait_forl:
    def __init__(self, eventl):
        self.eventl = eventl

    def __str__(self):
        return "bp.sync({waitFor:[" + str(self.eventl) + "]});"
    __repr__ = __str__


class wait_forf:
    def __init__(self, Xf):
        self.Xf = Xf

    def __str__(self):
        return "bp.sync({waitFor:[" + str(self.Xf) + "]});"
    __repr__ = __str__


class requestl1:
    def __init__(self, Ol, priority):
        self.Ol = Ol
        self.priority = priority

    def __str__(self):
        return "bp.sync({request:[" + str(self.Ol) + "]}," + str(self.priority) + ");"
    __repr__ = __str__


class requestl2:
    def __init__(self, Ol1, Ol2, priority):
        self.Ol1 = Ol1
        self.Ol2 = Ol2
        self.priority = priority

    def __str__(self):
        return "bp.sync({request:[" + str(self.Ol1) + "," + str(self.Ol2) + "]}," + str(self.priority) + ");"

    __repr__ = __str__


class requestl3:
    def __init__(self, Ol1, Ol2, Ol3, priority):
        self.Ol1 = Ol1
        self.Ol2 = Ol2
        self.Ol3 = Ol3
        self.priority = priority

    def __str__(self):
        return "bp.sync({request:[" + str(self.Ol1) + "," + str(self.Ol2) + "," + str(self.Ol3) + "]}," + str(self.priority) + ");"

    __repr__ = __str__


class requestl4:
    def __init__(self, Ol1, Ol2, Ol3, Ol4, priority):
        self.Ol1 = Ol1
        self.Ol2 = Ol2
        self.Ol3 = Ol3
        self.Ol4 = Ol4
        self.priority = priority

    def __str__(self):
        return "bp.sync({request:[" + str(self.Ol1) + "," + str(self.Ol2) + "," + str(self.Ol3) + "," + str(self.Ol4) + "]}," + str(self.priority) + ");"

    __repr__ = __str__


class Xl:
    def __init__(self, pos1, pos2):
        self.pos1 = pos1
        self.pos2 = pos2

    def __str__(self):
        return "X(f[p[" + str(self.pos1) + "]].x,f[p[" + str(self.pos2) + "]].y)"
    __repr__ = __str__


class Ol:
    def __init__(self, pos1, pos2):
        self.pos1 = pos1
        self.pos2 = pos2

    def __str__(self):
        return "O(f[p[" + str(self.pos1) + "]].x,f[p[" + str(self.pos2) + "]].y)"
    __repr__ = __str__


class Xf:
    def __init__(self, pos1, pos2):
        self.pos1 = pos1
        self.pos2 = pos2

    def __str__(self):
        return "X(f[p[" + str(self.pos1) + "]].x,f[p[" + str(self.pos2) + "]].y)"
    __repr__ = __str__


class request1:
    def __init__(self, O, priority):
        self.O = O
        self.priority = priority

    def __str__(self):
        return "bp.sync({request:[" + str(self.O) + "]}," + str(self.priority) + ");"
    __repr__ = __str__


class request2:
    def __init__(self, O1, O2, priority):
        self.O1 = O1
        self.O2 = O2
        self.priority = priority

    def __str__(self):
        return "bp.sync({request:[" + str(self.O1) + "," + str(self.O2) + "]}," + str(self.priority) + ");"

    __repr__ = __str__


class request3:
    def __init__(self, O1, O2, O3, priority):
        self.O1 = O1
        self.O2 = O2
        self.O3 = O3
        self.priority = priority

    def __str__(self):
        return "bp.sync({request:[" + str(self.O1) + "," + str(self.O2) + "," + str(self.O3) + "]}," + str(self.priority) + ");"

    __repr__ = __str__


class request4:
    def __init__(self, O1, O2, O3, O4, priority):
        self.O1 = O1
        self.O2 = O2
        self.O3 = O3
        self.O4 = O4
        self.priority = priority

    def __str__(self):
        return "bp.sync({request:[" + str(self.O1) + "," + str(self.O2) + "," + str(self.O3) + "," + str(self.O4) + "]}," + str(self.priority) + ");"

    __repr__ = __str__


class O:
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


def btlFunc3(while_true_l3):
    return btl(while_true_l3)


def btfFunc1(while_true_f1):
    return btf(while_true_f1)


def btfFunc2(while_true_f2):
    return btf(while_true_f2)


def btfFunc3(while_true_f3):
    return btf(while_true_f3)


def btFunc(while_true):
    return bt(while_true)

# while_truel3
def while_truel3Func1(waitforl1, waitforl2, requestl):
    return while_truel3(waitforl1, waitforl2, requestl)


def while_truel3Func2(waitforl1, waitforl2, requestl):
    return while_truel3(waitforl1, waitforl2, requestl)


def while_truel3Func3(waitforl1, waitforl2, requestl):
    return while_truel3(waitforl1, waitforl2, requestl)


def while_truel3Func4(waitforl1, waitforl2, requestl):
    return while_truel3(waitforl1, waitforl2, requestl)
# done while_truel3

# while_truef1
def while_truef1Func1(request):
    return while_truef1(request)


def while_truef1Func2(request):
    return while_truef1(request)


def while_truef1Func3(request):
    return while_truef1(request)


def while_truef1Func4(request):
    return while_truef1(request)
# done while_truef1

# while_truef2
def while_truef2Func1(waitforf, request):
    return while_truef2(waitforf, request)


def while_truef2Func2(waitforf, request):
    return while_truef2(waitforf, request)


def while_truef2Func3(waitforf, request):
    return while_truef2(waitforf, request)


def while_truef2Func4(waitforf, request):
    return while_truef2(waitforf, request)
# done while_truef2

# while_truef3
def while_truef3Func1(waitforf1, waitforf2, request):
    return while_truef3(waitforf1, waitforf2, request)


def while_truef3Func2(waitforf1, waitforf2, request):
    return while_truef3(waitforf1, waitforf2, request)


def while_truef3Func3(waitforf1, waitforf2, request):
    return while_truef3(waitforf1, waitforf2, request)


def while_truef3Func4(waitforf1, waitforf2, request):
    return while_truef3(waitforf1, waitforf2, request)
# done while_truef3


def while_trueFunc1(request):
    return whiletrue(request)


def while_trueFunc2(request):
    return whiletrue(request)


def while_trueFunc3(request):
    return whiletrue(request)


def while_trueFunc4(request):
    return whiletrue(request)


def wait_forlFuncX(xl):
    return wait_forl(xl)


def wait_forlFuncO(ol):
    return wait_forl(ol)


def wait_forfFuncX(xf):
    return wait_forf(xf)


# request
def request1Func(o, priority):
    return request1(o, priority)


def request2Func(o1, o2, priority):
    return request2(o1, o2, priority)


def request3Func(o1, o2, o3, priority):
    return request3(o1, o2, o3, priority)


def request4Func(o1, o2, o3, o4, priority):
    return request4(o1, o2, o3, o4, priority)
# done request


# requestl
def requestl1Func(o, priority):
    return requestl1(o, priority)


def requestl2Func(o1, o2, priority):
    return requestl2(o1, o2, priority)


def requestl3Func(o1, o2, o3, priority):
    return requestl3(o1, o2, o3, priority)


def requestl4Func(o1, o2, o3, o4, priority):
    return requestl4(o1, o2, o3, o4, priority)
# done requestl


def xlFunc(pos1, pos2):
    return Xl(pos1, pos2)


def xfFunc(pos1, pos2):
    return Xf(pos1, pos2)


def olFunc(pos1, pos2):
    return Ol(pos1, pos2)


def oFunc(pos1, pos2):
    return O(pos1, pos2)


def posFunc(pos):
    return pos


def posfFunc(pos):
    return pos


def priorityFunc(priority):
    return priority