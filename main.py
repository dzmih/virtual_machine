class Execution:
    def __init__(self, default_actions=None):
        self.stack = []
        self.memory = [None] * 1024
        self.default_actions = default_actions or {
        "push": self.push,
        "pop": self.pop,
        "print": self.prnt,
        "prnt": self.prnt,
        "swap": self.swap,
        "dup": self.dup,
        "mul": self.mul,
        "div": self.div,
        "run": self.run,
        "add": self.add,
        "store": self.store,
        "load": self.load,
    }
        
    def process(self, action, *args, custom_actions=None, **kwargs):
        actions = custom_actions or self.default_actions
        return actions.get(action, lambda *a, **k: "unknown")(*args, **kwargs)
    
    def push(self, value):
        try:
            value = int(value)
        except ValueError:
            pass
        self.stack.append(value)
    
    def pop(self):
        return self.stack.pop()
    
    def prnt(self, option):
        option = option.replace(" ", "")
        if option.lower() == "stack":
            print(self.stack)
        if option.lower() == "memory":
            print(self.memory)

    def swap(self):
        if len(self.stack) >= 2:
            self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

    def dup(self):
        if self.stack:
            self.stack.append(self.stack[-1])

    def mul(self):
        if not self.stack:
            return
        t = self.stack[0]
        for i in range(1, len(self.stack)):
            t *= self.stack[i]
        self.stack = [t]

    def div(self):
        if not self.stack:
            return
        t = self.stack[0]
        for i in range(1, len(self.stack)):
            t //= self.stack[i]
        self.stack = [t]
        
    def run(self, program:list[tuple]):
        pc = 0
        while pc < len(program):
            if len(program[pc]) > 1:
                self.process(program[pc][0], program[pc][1])
            if len(program[pc]) == 1:
                self.process(program[pc][0])
            pc += 1

    def add(self):
        if not self.stack:
            return
        t = self.stack[0]
        for i in range(1, len(self.stack)):
            t += self.stack[i]
        self.stack = [t]

    def repl(self):
        while True:
    
            try:
                command = input("Enter Command: ")
                if command.lower() == "exit":
                    break
            except EOFError:
                break
            parts = command.split()
            if not parts:
                continue
            action = parts[0]
            args = parts[1:]
            self.process(action, *args)

    def store(self, address):
        address = int(address)
        value = self.pop()
        self.memory[address] = value

    def load(self, address):
        address = int(address)
        value = self.memory[address]
        self.push(value)
    
    def jump(self, index):
        pass

main_vm = Execution()

# program = [
#     ("push", 5),
#     ("push", 10),
#     ("push", 10),
#     ("push", 6),
#     ("mul",),
#     ("prnt",)
# ]

# main_vm.repl()

