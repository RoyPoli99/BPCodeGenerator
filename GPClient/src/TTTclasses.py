import json
import threading

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

currentBehaviorSetIndex = 1
currentBehaviorIndex = 1
lock = threading.Lock()

class root_wrapper:
    def __init__(self, root):
        self.root = root

    def __str__(self):
        return str(root)

    __repr__ = __str__


class root:
    def __init__(self, *ctxs):
        self.ctxs = ctxs[0]

    def __str__(self):
        global currentBehaviorSetIndex, currentBehaviorIndex
        code = ""
        currentBehaviorSetIndex = 1
        currentBehaviorIndex = 1
        for ctx in self.ctxs:
            code += str(ctx) + "\n"
        currentBehaviorSetIndex = 1
        currentBehaviorIndex = 1
        return str(code)

    __repr__ = __str__


class CTX:
    def __init__(self, single_inputs, behavior_sets):
        self.single_inputs = single_inputs
        self.behavior_sets = behavior_sets

    def __str__(self):
        global currentBehaviorSetIndex, currentBehaviorIndex
        code_behaviors = str(self.behavior_sets)
        code = "var inputs_" + str(currentBehaviorSetIndex) + " = ["
        for single_input in self.single_inputs:
            code += str(single_input) + ",\n"
        code = code[:-2] + "]\n"
        code += "inputs_" + str(currentBehaviorSetIndex) + ".forEach(function (input) {\n"
        code += "behaviorSet" + str(currentBehaviorSetIndex) + "(input);\n"
        code += "});\n"
        currentBehaviorIndex = 1
        currentBehaviorSetIndex += 1
        return code_behaviors + code
    __repr__ = __str__


class BehaviorSet1:
    def __init__(self, behaviors):
        self.behaviors = behaviors

    def __str__(self):
        code = "function behaviorSet" + str(currentBehaviorSetIndex) + "(input) {\n"
        for behavior in self.behaviors:
            code += str(behavior) + "\n"
        return code + "}\n"
    __repr__ = __str__


class BehaviorSet2:
    def __init__(self, behaviors):
        self.behaviors = behaviors

    def __str__(self):
        code = "function behaviorSet" + str(currentBehaviorSetIndex) + "(input) {\n"
        for behavior in self.behaviors:
            code += str(behavior) + "\n"
        return code + "}\n"
    __repr__ = __str__


class BehaviorSet3:
    def __init__(self, behaviors):
        self.behaviors = behaviors

    def __str__(self):
        code = "function behaviorSet" + str(currentBehaviorSetIndex) + "(input) {\n"
        for behavior in self.behaviors:
            code += str(behavior) + "\n"
        return code + "}\n"

    __repr__ = __str__


class BehaviorSet4:
    def __init__(self, behaviors):
        self.behaviors = behaviors

    def __str__(self):
        code = "function behaviorSet" + str(currentBehaviorSetIndex) + "(input) {\n"
        for behavior in self.behaviors:
            code += str(behavior) + "\n"
        return code + "}\n"

    __repr__ = __str__


class BehaviorSet5:
    def __init__(self, behaviors):
        self.behaviors = behaviors

    def __str__(self):
        code = "function behaviorSet" + str(currentBehaviorSetIndex) + "(input) {\n"
        for behavior in self.behaviors:
            code += str(behavior) + "\n"
        return code + "}\n"

    __repr__ = __str__


class BehaviorSet6:
    def __init__(self, behaviors):
        self.behaviors = behaviors

    def __str__(self):
        code = "function behaviorSet" + str(currentBehaviorSetIndex) + "(input) {\n"
        for behavior in self.behaviors:
            code += str(behavior) + "\n"
        return code + "}\n"

    __repr__ = __str__


class BehaviorSet7:
    def __init__(self, behaviors):
        self.behaviors = behaviors

    def __str__(self):
        code = "function behaviorSet" + str(currentBehaviorSetIndex) + "(input) {\n"
        for behavior in self.behaviors:
            code += str(behavior) + "\n"
        return code + "}\n"

    __repr__ = __str__


class BehaviorSet8:
    def __init__(self, behaviors):
        self.behaviors = behaviors

    def __str__(self):
        code = "function behaviorSet" + str(currentBehaviorSetIndex) + "(input) {\n"
        for behavior in self.behaviors:
            code += str(behavior) + "\n"
        return code + "}\n"

    __repr__ = __str__


class BehaviorSet9:
    def __init__(self, behaviors):
        self.behaviors = behaviors

    def __str__(self):
        code = "function behaviorSet" + str(currentBehaviorSetIndex) + "(input) {\n"
        for behavior in self.behaviors:
            code += str(behavior) + "\n"
        return code + "}\n"

    __repr__ = __str__


class Behavior1:
    def __init__(self, request, waits):
        self.request = request
        self.waits = waits

    def __str__(self):
        code = ""
        for wait in self.waits:
            code += str(wait) + "\n"
        code += str(self.request) + "\n"
        global currentBehaviorIndex
        curr_name = "bp.registerBThread(\"O_Player_Thread_" + str(currentBehaviorSetIndex) + "_" + str(currentBehaviorIndex) + "\", function(){\n"
        currentBehaviorIndex = currentBehaviorIndex + 1
        return curr_name + code + "});\n"
    __repr__ = __str__


class Behavior2:
    def __init__(self, request, waits):
        self.request = request
        self.waits = waits

    def __str__(self):
        code = ""
        for wait in self.waits:
            code += str(wait) + "\n"
        code += str(self.request) + "\n"
        global currentBehaviorIndex
        curr_name = "bp.registerBThread(\"O_Player_Thread_" + str(currentBehaviorSetIndex) + "_" + str(currentBehaviorIndex) + "\", function(){\n"
        currentBehaviorIndex = currentBehaviorIndex + 1
        return curr_name + code + "});\n"
    __repr__ = __str__


class Behavior3:
    def __init__(self, request, waits):
        self.request = request
        self.waits = waits

    def __str__(self):
        code = ""
        for wait in self.waits:
            code += str(wait) + "\n"
        code += str(self.request) + "\n"
        global currentBehaviorIndex
        curr_name = "bp.registerBThread(\"O_Player_Thread_" + str(currentBehaviorSetIndex) + "_" + str(currentBehaviorIndex) + "\", function(){\n"
        currentBehaviorIndex = currentBehaviorIndex + 1
        return curr_name + code + "});\n"
    __repr__ = __str__


class Behavior4:
    def __init__(self, request, waits):
        self.request = request
        self.waits = waits

    def __str__(self):
        code = ""
        for wait in self.waits:
            code += str(wait) + "\n"
        code += str(self.request) + "\n"
        global currentBehaviorIndex
        curr_name = "bp.registerBThread(\"O_Player_Thread_" + str(currentBehaviorSetIndex) + "_" + str(currentBehaviorIndex) + "\", function(){\n"
        currentBehaviorIndex = currentBehaviorIndex + 1
        return curr_name + code + "});\n"
    __repr__ = __str__


class Behavior5:
    def __init__(self, request, waits):
        self.request = request
        self.waits = waits

    def __str__(self):
        code = ""
        for wait in self.waits:
            code += str(wait) + "\n"
        code += str(self.request) + "\n"
        global currentBehaviorIndex
        curr_name = "bp.registerBThread(\"O_Player_Thread_" + str(currentBehaviorSetIndex) + "_" + str(currentBehaviorIndex) + "\", function(){\n"
        currentBehaviorIndex = currentBehaviorIndex + 1
        return curr_name + code + "});\n"
    __repr__ = __str__


class Behavior6:
    def __init__(self, request, waits):
        self.request = request
        self.waits = waits

    def __str__(self):
        code = ""
        for wait in self.waits:
            code += str(wait) + "\n"
        code += str(self.request) + "\n"
        global currentBehaviorIndex
        curr_name = "bp.registerBThread(\"O_Player_Thread_" + str(currentBehaviorSetIndex) + "_" + str(currentBehaviorIndex) + "\", function(){\n"
        currentBehaviorIndex = currentBehaviorIndex + 1
        return curr_name + code + "});\n"
    __repr__ = __str__


class Behavior7:
    def __init__(self, request, waits):
        self.request = request
        self.waits = waits

    def __str__(self):
        code = ""
        for wait in self.waits:
            code += str(wait) + "\n"
        code += str(self.request) + "\n"
        global currentBehaviorIndex
        curr_name = "bp.registerBThread(\"O_Player_Thread_" + str(currentBehaviorSetIndex) + "_" + str(currentBehaviorIndex) + "\", function(){\n"
        currentBehaviorIndex = currentBehaviorIndex + 1
        return curr_name + code + "});\n"
    __repr__ = __str__


class Behavior8:
    def __init__(self, request, waits):
        self.request = request
        self.waits = waits

    def __str__(self):
        code = ""
        for wait in self.waits:
            code += str(wait) + "\n"
        code += str(self.request) + "\n"
        global currentBehaviorIndex
        curr_name = "bp.registerBThread(\"O_Player_Thread_" + str(currentBehaviorSetIndex) + "_" + str(currentBehaviorIndex) + "\", function(){\n"
        currentBehaviorIndex = currentBehaviorIndex + 1
        return curr_name + code + "});\n"
    __repr__ = __str__


class Behavior9:
    def __init__(self, request, waits):
        self.request = request
        self.waits = waits

    def __str__(self):
        code = ""
        for wait in self.waits:
            code += str(wait) + "\n"
        code += str(self.request) + "\n"
        global currentBehaviorIndex
        curr_name = "bp.registerBThread(\"O_Player_Thread_" + str(currentBehaviorSetIndex) + "_" + str(currentBehaviorIndex) + "\", function(){\n"
        currentBehaviorIndex = currentBehaviorIndex + 1
        return curr_name + code + "});\n"
    __repr__ = __str__


class Request1:
    def __init__(self, events, priority):
        self.events = events
        self.priority = priority

    def __str__(self):
        code = ""
        for event in self.events:
            code += str(event)
            code += ", "
        code = code[:-2]
        return "bp.sync({request:[" + code + "]}," + str(self.priority) + ");"
    __repr__ = __str__


class Request2:
    def __init__(self, events, priority):
        self.events = events
        self.priority = priority

    def __str__(self):
        code = ""
        for event in self.events:
            code += str(event)
            code += ", "
        code = code[:-2]
        return "bp.sync({request:[" + code + "]}," + str(self.priority) + ");"
    __repr__ = __str__


class Request3:
    def __init__(self, events, priority):
        self.events = events
        self.priority = priority

    def __str__(self):
        code = ""
        for event in self.events:
            code += str(event)
            code += ", "
        code = code[:-2]
        return "bp.sync({request:[" + code + "]}," + str(self.priority) + ");"
    __repr__ = __str__


class Request4:
    def __init__(self, events, priority):
        self.events = events
        self.priority = priority

    def __str__(self):
        code = ""
        for event in self.events:
            code += str(event)
            code += ", "
        code = code[:-2]
        return "bp.sync({request:[" + code + "]}," + str(self.priority) + ");"
    __repr__ = __str__


class Request5:
    def __init__(self, events, priority):
        self.events = events
        self.priority = priority

    def __str__(self):
        code = ""
        for event in self.events:
            code += str(event)
            code += ", "
        code = code[:-2]
        return "bp.sync({request:[" + code + "]}," + str(self.priority) + ");"
    __repr__ = __str__


class Request6:
    def __init__(self, events, priority):
        self.events = events
        self.priority = priority

    def __str__(self):
        code = ""
        for event in self.events:
            code += str(event)
            code += ", "
        code = code[:-2]
        return "bp.sync({request:[" + code + "]}," + str(self.priority) + ");"
    __repr__ = __str__


class Request7:
    def __init__(self, events, priority):
        self.events = events
        self.priority = priority

    def __str__(self):
        code = ""
        for event in self.events:
            code += str(event)
            code += ", "
        code = code[:-2]
        return "bp.sync({request:[" + code + "]}," + str(self.priority) + ");"
    __repr__ = __str__


class Request8:
    def __init__(self, events, priority):
        self.events = events
        self.priority = priority

    def __str__(self):
        code = ""
        for event in self.events:
            code += str(event)
            code += ", "
        code = code[:-2]
        return "bp.sync({request:[" + code + "]}," + str(self.priority) + ");"
    __repr__ = __str__


class Request9:
    def __init__(self, events, priority):
        self.events = events
        self.priority = priority

    def __str__(self):
        code = ""
        for event in self.events:
            code += str(event)
            code += ", "
        code = code[:-2]
        return "bp.sync({request:[" + code + "]}," + str(self.priority) + ");"
    __repr__ = __str__


class Wait1:
    def __init__(self, events):
        self.events = events

    def __str__(self):
        code = ""
        for event in self.events:
            code += str(event)
            code += ", "
        code = code[:-2]
        return "bp.sync({waitFor:[" + code + "]});"
    __repr__ = __str__


class Wait2:
    def __init__(self, events):
        self.events = events

    def __str__(self):
        code = ""
        for event in self.events:
            code += str(event)
            code += ", "
        code = code[:-2]
        return "bp.sync({waitFor:[" + code + "]});"
    __repr__ = __str__


class Wait3:
    def __init__(self, events):
        self.events = events

    def __str__(self):
        code = ""
        for event in self.events:
            code += str(event)
            code += ", "
        code = code[:-2]
        return "bp.sync({waitFor:[" + code + "]});"
    __repr__ = __str__


class Wait4:
    def __init__(self, events):
        self.events = events

    def __str__(self):
        code = ""
        for event in self.events:
            code += str(event)
            code += ", "
        code = code[:-2]
        return "bp.sync({waitFor:[" + code + "]});"
    __repr__ = __str__


class Wait5:
    def __init__(self, events):
        self.events = events

    def __str__(self):
        code = ""
        for event in self.events:
            code += str(event)
            code += ", "
        code = code[:-2]
        return "bp.sync({waitFor:[" + code + "]});"
    __repr__ = __str__


class Wait6:
    def __init__(self, events):
        self.events = events

    def __str__(self):
        code = ""
        for event in self.events:
            code += str(event)
            code += ", "
        code = code[:-2]
        return "bp.sync({waitFor:[" + code + "]});"
    __repr__ = __str__


class Wait7:
    def __init__(self, events):
        self.events = events

    def __str__(self):
        code = ""
        for event in self.events:
            code += str(event)
            code += ", "
        code = code[:-2]
        return "bp.sync({waitFor:[" + code + "]});"
    __repr__ = __str__


class Wait8:
    def __init__(self, events):
        self.events = events

    def __str__(self):
        code = ""
        for event in self.events:
            code += str(event)
            code += ", "
        code = code[:-2]
        return "bp.sync({waitFor:[" + code + "]});"
    __repr__ = __str__


class Wait9:
    def __init__(self, events):
        self.events = events

    def __str__(self):
        code = ""
        for event in self.events:
            code += str(event)
            code += ", "
        code = code[:-2]
        return "bp.sync({waitFor:[" + code + "]});"
    __repr__ = __str__


class Event1:
    def __init__(self, event):
        self.event = event

    def __str__(self):
        return str(self.event)
    __repr__ = __str__


class Event2:
    def __init__(self, event):
        self.event = event

    def __str__(self):
        return str(self.event)
    __repr__ = __str__


class Event3:
    def __init__(self, event):
        self.event = event

    def __str__(self):
        return str(self.event)
    __repr__ = __str__


class Event4:
    def __init__(self, event):
        self.event = event

    def __str__(self):
        return str(self.event)
    __repr__ = __str__


class Event5:
    def __init__(self, event):
        self.event = event

    def __str__(self):
        return str(self.event)
    __repr__ = __str__


class Event6:
    def __init__(self, event):
        self.event = event

    def __str__(self):
        return str(self.event)
    __repr__ = __str__


class Event7:
    def __init__(self, event):
        self.event = event

    def __str__(self):
        return str(self.event)
    __repr__ = __str__


class Event8:
    def __init__(self, event):
        self.event = event

    def __str__(self):
        return str(self.event)
    __repr__ = __str__


class Event9:
    def __init__(self, event):
        self.event = event

    def __str__(self):
        return str(self.event)
    __repr__ = __str__


class XEvent1:
    def __init__(self, indx):
        self.indx = indx

    def __str__(self):
        return "X(input[" + str(self.indx) + "].x, input[" + str(self.indx) + "].y)"
    __repr__ = __str__


class XEvent2:
    def __init__(self, indx):
        self.indx = indx

    def __str__(self):
        return "X(input[" + str(self.indx) + "].x, input[" + str(self.indx) + "].y)"
    __repr__ = __str__


class XEvent3:
    def __init__(self, indx):
        self.indx = indx

    def __str__(self):
        return "X(input[" + str(self.indx) + "].x, input[" + str(self.indx) + "].y)"
    __repr__ = __str__


class XEvent4:
    def __init__(self, indx):
        self.indx = indx

    def __str__(self):
        return "X(input[" + str(self.indx) + "].x, input[" + str(self.indx) + "].y)"
    __repr__ = __str__


class XEvent5:
    def __init__(self, indx):
        self.indx = indx

    def __str__(self):
        return "X(input[" + str(self.indx) + "].x, input[" + str(self.indx) + "].y)"
    __repr__ = __str__


class XEvent6:
    def __init__(self, indx):
        self.indx = indx

    def __str__(self):
        return "X(input[" + str(self.indx) + "].x, input[" + str(self.indx) + "].y)"
    __repr__ = __str__


class XEvent7:
    def __init__(self, indx):
        self.indx = indx

    def __str__(self):
        return "X(input[" + str(self.indx) + "].x, input[" + str(self.indx) + "].y)"
    __repr__ = __str__


class XEvent8:
    def __init__(self, indx):
        self.indx = indx

    def __str__(self):
        return "X(input[" + str(self.indx) + "].x, input[" + str(self.indx) + "].y)"
    __repr__ = __str__


class XEvent9:
    def __init__(self, indx):
        self.indx = indx

    def __str__(self):
        return "X(input[" + str(self.indx) + "].x, input[" + str(self.indx) + "].y)"
    __repr__ = __str__


class OEvent1:
    def __init__(self, indx):
        self.indx = indx

    def __str__(self):
        return "O(input[" + str(self.indx) + "].x, input[" + str(self.indx) + "].y)"
    __repr__ = __str__


class OEvent2:
    def __init__(self, indx):
        self.indx = indx

    def __str__(self):
        return "O(input[" + str(self.indx) + "].x, input[" + str(self.indx) + "].y)"
    __repr__ = __str__


class OEvent3:
    def __init__(self, indx):
        self.indx = indx

    def __str__(self):
        return "O(input[" + str(self.indx) + "].x, input[" + str(self.indx) + "].y)"
    __repr__ = __str__


class OEvent4:
    def __init__(self, indx):
        self.indx = indx

    def __str__(self):
        return "O(input[" + str(self.indx) + "].x, input[" + str(self.indx) + "].y)"
    __repr__ = __str__


class OEvent5:
    def __init__(self, indx):
        self.indx = indx

    def __str__(self):
        return "O(input[" + str(self.indx) + "].x, input[" + str(self.indx) + "].y)"
    __repr__ = __str__


class OEvent6:
    def __init__(self, indx):
        self.indx = indx

    def __str__(self):
        return "O(input[" + str(self.indx) + "].x, input[" + str(self.indx) + "].y)"
    __repr__ = __str__


class OEvent7:
    def __init__(self, indx):
        self.indx = indx

    def __str__(self):
        return "O(input[" + str(self.indx) + "].x, input[" + str(self.indx) + "].y)"
    __repr__ = __str__


class OEvent8:
    def __init__(self, indx):
        self.indx = indx

    def __str__(self):
        return "O(input[" + str(self.indx) + "].x, input[" + str(self.indx) + "].y)"
    __repr__ = __str__


class OEvent9:
    def __init__(self, indx):
        self.indx = indx

    def __str__(self):
        return "O(input[" + str(self.indx) + "].x, input[" + str(self.indx) + "].y)"
    __repr__ = __str__


class SingleInput1:
    def __init__(self, cells):
        self.cells = cells

    def __str__(self):
        code = "["
        for cell in self.cells[:-1]:
            code += str(cell) + ", "
        code += str(self.cells[len(self.cells) - 1]) + "]"
        return code
    __repr__ = __str__


class SingleInput2:
    def __init__(self, cells):
        self.cells = cells

    def __str__(self):
        code = "["
        for cell in self.cells[:-1]:
            code += str(cell) + ", "
        code += str(self.cells[len(self.cells) - 1]) + "]"
        return code
    __repr__ = __str__


class SingleInput3:
    def __init__(self, cells):
        self.cells = cells

    def __str__(self):
        code = "["
        for cell in self.cells[:-1]:
            code += str(cell) + ", "
        code += str(self.cells[len(self.cells) - 1]) + "]"
        return code
    __repr__ = __str__


class SingleInput4:
    def __init__(self, cells):
        self.cells = cells

    def __str__(self):
        code = "["
        for cell in self.cells[:-1]:
            code += str(cell) + ", "
        code += str(self.cells[len(self.cells) - 1]) + "]"
        return code
    __repr__ = __str__


class SingleInput5:
    def __init__(self, cells):
        self.cells = cells

    def __str__(self):
        code = "["
        for cell in self.cells[:-1]:
            code += str(cell) + ", "
        code += str(self.cells[len(self.cells) - 1]) + "]"
        return code
    __repr__ = __str__


class SingleInput6:
    def __init__(self, cells):
        self.cells = cells

    def __str__(self):
        code = "["
        for cell in self.cells[:-1]:
            code += str(cell) + ", "
        code += str(self.cells[len(self.cells) - 1]) + "]"
        return code
    __repr__ = __str__


class SingleInput7:
    def __init__(self, cells):
        self.cells = cells

    def __str__(self):
        code = "["
        for cell in self.cells[:-1]:
            code += str(cell) + ", "
        code += str(self.cells[len(self.cells) - 1]) + "]"
        return code
    __repr__ = __str__


class SingleInput8:
    def __init__(self, cells):
        self.cells = cells

    def __str__(self):
        code = "["
        for cell in self.cells[:-1]:
            code += str(cell) + ", "
        code += str(self.cells[len(self.cells) - 1]) + "]"
        return code
    __repr__ = __str__


class SingleInput9:
    def __init__(self, cells):
        self.cells = cells

    def __str__(self):
        code = "["
        for cell in self.cells[:-1]:
            code += str(cell) + ", "
        code += str(self.cells[len(self.cells) - 1]) + "]"
        return code
    __repr__ = __str__


class Cell:
    def __init__(self, pos1, pos2):
        self.pos1 = pos1
        self.pos2 = pos2

    def __str__(self):
        return "{x: " + str(self.pos1) + ", y: " + str(self.pos2) + "}"
    __repr__ = __str__


class Position:
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)
    __repr__ = __str__


class Index1:
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)
    __repr__ = __str__


class Index2:
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)
    __repr__ = __str__


class Index3:
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)
    __repr__ = __str__


class Index4:
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)
    __repr__ = __str__


class Index5:
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)
    __repr__ = __str__


class Index6:
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)
    __repr__ = __str__


class Index7:
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)
    __repr__ = __str__


class Index8:
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)
    __repr__ = __str__


class Index9:
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)
    __repr__ = __str__


class Priority:
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)
    __repr__ = __str__


def root_wrapper_func(root):
    return root_wrapper(root)


def root_func(*ctxes):
    return root(ctxes)


def ctx_func(behavior_set, *single_inputs):
    return CTX(single_inputs, behavior_set)


def behavior_set_func1(*behaviors):
    return BehaviorSet1(behaviors)


def behavior_set_func2(*behaviors):
    return BehaviorSet2(behaviors)


def behavior_set_func3(*behaviors):
    return BehaviorSet3(behaviors)


def behavior_set_func4(*behaviors):
    return BehaviorSet4(behaviors)


def behavior_set_func5(*behaviors):
    return BehaviorSet5(behaviors)


def behavior_set_func6(*behaviors):
    return BehaviorSet6(behaviors)


def behavior_set_func7(*behaviors):
    return BehaviorSet7(behaviors)


def behavior_set_func8(*behaviors):
    return BehaviorSet8(behaviors)


def behavior_set_func9(*behaviors):
    return BehaviorSet9(behaviors)


def behavior_func1(request, *waits):
    return Behavior1(request, waits)


def behavior_func2(request, *waits):
    return Behavior2(request, waits)


def behavior_func3(request, *waits):
    return Behavior3(request, waits)


def behavior_func4(request, *waits):
    return Behavior4(request, waits)


def behavior_func5(request, *waits):
    return Behavior5(request, waits)


def behavior_func6(request, *waits):
    return Behavior6(request, waits)


def behavior_func7(request, *waits):
    return Behavior7(request, waits)


def behavior_func8(request, *waits):
    return Behavior8(request, waits)


def behavior_func9(request, *waits):
    return Behavior9(request, waits)


def request_func1(priority, *events):
    return Request1(events, priority)


def request_func2(priority, *events):
    return Request2(events, priority)


def request_func3(priority, *events):
    return Request3(events, priority)


def request_func4(priority, *events):
    return Request4(events, priority)


def request_func5(priority, *events):
    return Request5(events, priority)


def request_func6(priority, *events):
    return Request6(events, priority)


def request_func7(priority, *events):
    return Request7(events, priority)


def request_func8(priority, *events):
    return Request8(events, priority)


def request_func9(priority, *events):
    return Request9(events, priority)


def wait_func1(*events):
    return Wait1(events)


def wait_func2(*events):
    return Wait2(events)


def wait_func3(*events):
    return Wait3(events)


def wait_func4(*events):
    return Wait4(events)


def wait_func5(*events):
    return Wait5(events)


def wait_func6(*events):
    return Wait6(events)


def wait_func7(*events):
    return Wait7(events)


def wait_func8(*events):
    return Wait8(events)


def wait_func9(*events):
    return Wait9(events)


def event_func1(event):
    return Event1(event)


def event_func2(event):
    return Event2(event)


def event_func3(event):
    return Event3(event)


def event_func4(event):
    return Event4(event)


def event_func5(event):
    return Event5(event)


def event_func6(event):
    return Event6(event)


def event_func7(event):
    return Event7(event)


def event_func8(event):
    return Event8(event)


def event_func9(event):
    return Event9(event)


def x_event_func1(indx):
    return XEvent1(indx)


def x_event_func2(indx):
    return XEvent2(indx)


def x_event_func3(indx):
    return XEvent3(indx)


def x_event_func4(indx):
    return XEvent4(indx)


def x_event_func5(indx):
    return XEvent5(indx)


def x_event_func6(indx):
    return XEvent6(indx)


def x_event_func7(indx):
    return XEvent7(indx)


def x_event_func8(indx):
    return XEvent8(indx)


def x_event_func9(indx):
    return XEvent9(indx)


def o_event_func1(indx):
    return OEvent1(indx)


def o_event_func2(indx):
    return OEvent2(indx)


def o_event_func3(indx):
    return OEvent3(indx)


def o_event_func4(indx):
    return OEvent4(indx)


def o_event_func5(indx):
    return OEvent5(indx)


def o_event_func6(indx):
    return OEvent6(indx)


def o_event_func7(indx):
    return OEvent7(indx)


def o_event_func8(indx):
    return OEvent8(indx)


def o_event_func9(indx):
    return OEvent9(indx)


def single_input_func1(*cells):
    return SingleInput1(cells)


def single_input_func2(*cells):
    return SingleInput2(cells)


def single_input_func3(*cells):
    return SingleInput3(cells)


def single_input_func4(*cells):
    return SingleInput4(cells)


def single_input_func5(*cells):
    return SingleInput5(cells)


def single_input_func6(*cells):
    return SingleInput6(cells)


def single_input_func7(*cells):
    return SingleInput7(cells)


def single_input_func8(*cells):
    return SingleInput8(cells)


def single_input_func9(*cells):
    return SingleInput9(cells)


def cell_func(pos1, pos2):
    return Cell(pos1, pos2)


def index_func(indx):
    return indx


def position_func(pos):
    return pos


def priority_func(priority):
    return priority
