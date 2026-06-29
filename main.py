class VirtualMachine:
    def __init__(self, default_actions=None):
        self.stack = []
        self.memory = [None] * 1024
        self.pc = 0
        self.running = True
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
        "jump": self.jump,
        "halt": self.halt,
    }
        
    #Private
    def _push_stack(self, value):
        try:
            value = int(value)
        except ValueError:
            pass
        self.stack.append(value)

    def _pop_stack(self):
        return self.stack.pop() 

    

        
    def process(self, action, *args, custom_actions=None, **kwargs):
        actions = custom_actions or self.default_actions
        return actions.get(action, lambda *a, **k: "unknown")(*args, **kwargs)
    
    def push(self, value):
        try:
            value = int(value)
        except ValueError:
            pass
        self.stack.append(value)
        self.pc += 1
    
    def pop(self):
        self.pc += 1
        return self.stack.pop() 
    
    def prnt(self, option):
        option = option.replace(" ", "")
        if option.lower() == "stack":
            print(self.stack)
        if option.lower() == "memory":
            print(self.memory)
        self.pc += 1

    def swap(self):
        if len(self.stack) >= 2:
            self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
        self.pc += 1

    def dup(self):
        if self.stack:
            self.stack.append(self.stack[-1])
        self.pc += 1

    def mul(self):
        if not self.stack:
            return
        t = self.stack[0]
        for i in range(1, len(self.stack)):
            t *= self.stack[i]
        self.stack = [t]
        self.pc += 1

    def div(self):
        if not self.stack:
            return
        t = self.stack[0]
        for i in range(1, len(self.stack)):
            t //= self.stack[i]
        self.stack = [t]
        self.pc += 1
        
    def run(self, program:list[tuple]):
        while self.pc < len(program) and self.running:
            if len(program[self.pc]) > 1:
                self.process(program[self.pc][0], program[self.pc][1])
            if len(program[self.pc]) == 1:
                self.process(program[self.pc][0])

    def add(self):
        if not self.stack:
            return
        t = self.stack[0]
        for i in range(1, len(self.stack)):
            t += self.stack[i]
        self.stack = [t]
        self.pc += 1

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
        value = self._pop_stack()
        self.memory[address] = value
        self.pc += 1

    def load(self, address):
        address = int(address)
        value = self.memory[address]
        self._push_stack(value)
        self.pc += 1
    
    def jump(self, index):
        self.pc = index
    
    def halt(self):
        self.running = False


main_vm = VirtualMachine()

program = [
    ("push", 5),
    ("push", 10),
    ("add",),
    ("prnt", "stack"),
    ("jump", 0),
    ("halt",)
]

main_vm.run(program)

