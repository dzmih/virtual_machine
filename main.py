class StackUnderflowError(Exception):
    pass

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
        "jz": self.jz,
        "sub": self.sub,
        "step": self.step,
        "vm_debug": self.vm_debug,
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
    ############################
        
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
        if len(self.stack) >= 2:
            s = self.stack[-2] * self.stack[-1]
            self.stack[-2:] = [s]
            self.pc += 1
        else:
            raise StackUnderflowError("Stack contains fewer than 2 values.")

    def div(self):
        if len(self.stack) >= 2:
            s = self.stack[-2] / self.stack[-1]
            self.stack[-2:] = [s]
            self.pc += 1
        else:
            raise StackUnderflowError("Stack contains fewer than 2 values.")
        
    def run(self, program: list[tuple]):
        while self.pc < len(program) and self.running:
            instruction = program[self.pc]
            action = instruction[0]
            args = instruction[1:]
            self.process(action, *args)

    def add(self):
        if len(self.stack) >= 2:
            s = self.stack[-2] + self.stack[-1]
            self.stack[-2:] = [s]
            self.pc += 1
        else:
            raise StackUnderflowError("Stack contains fewer than 2 values.")

    def sub(self):
        if len(self.stack) >= 2:
            s = self.stack[-2] - self.stack[-1]
            self.stack[-2:] = [s]
            self.pc += 1
        else:
            raise StackUnderflowError("Stack contains fewer than 2 values.")

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
        self.pc = int(index)
    
    def halt(self):
        self.running = False

    def jz(self, index):
        if len(self.stack) >= 1:
            value = self._pop_stack()
            if value == 0:
                self.pc = int(index)
            else:
                self.pc += 1
        else:
            raise StackUnderflowError("Stack contains fewer than 1 value.")
        
    def step(self, program: list[tuple]):
        input("Press Enter for step")

        instruction = program[self.pc]
        action = instruction[0]
        args = instruction[1:]

        self.process(action, *args)
    
    def vm_debug(self, program):
        while self.running:
            print("####################")
            print(self.pc)
            print(f"Instruction: {program[self.pc][0]} {program[self.pc][1:]}")
            print(self.stack)
            print("####################")
            self.step(program)


main_vm = VirtualMachine()

program = [
    ("push", 0),
    ("jz", 4),
    ("push", 999),
    ("prnt", "stack"),
    ("push", 111),
    ("prnt", "stack"),
    ("halt",),
]

main_vm.vm_debug(program)

