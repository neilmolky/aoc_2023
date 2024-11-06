import abc
from curses.ascii import SI
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict, deque


class Signal(Enum):
    Zero = 0
    Low = 1
    High = 2

    def flip(self):
        if self.value == 0:
            return Signal(0)
        return Signal((self.value % 2) + 1)

class Module(abc.ABC):
    def __init__(self, name: str = "", destinations: list[str] = []):
        self.name = name
        self.destinations = destinations

    def accept(self, recieved: Signal, states: defaultdict[str, Signal]) -> tuple[dict[str, Signal], dict[str, Signal]]:
        ...

class Void(Module):
    def accept(self, recieved: Signal, states: defaultdict[str, Signal]) -> tuple[dict[str, Signal], dict[str, Signal]]:
        return ({}, {})

class FlipFlop(Module):
    def accept(self, recieved: Signal, states: defaultdict[str, Signal]) -> tuple[dict[str, Signal], dict[str, Signal]]:
        if recieved == Signal.Low:
            state = states[self.name].flip()
            return ({d: state.flip() for d in self.destinations}, {self.name: state})
        return ({}, {})

class Conjunction(Module):
    def accept(self, recieved: Signal, states: defaultdict[str, Signal]) -> tuple[dict[str, Signal], dict[str, Signal]]:
        states: list[Signal] = [states[f"{d} {self.name}"] for d in self.destinations]
        if all([s == Signal.High for s in states]):
            return {d: Signal.Low for d in self.destinations}
        return [Message(Signal.High, self.name, d) for d in self.destinations]
    
    def accept(self, recieved: Signal, state: Signal) -> tuple[Signal, dict[str, Signal]]:
        return ()

    
class Broadcast(Module):
    def accept(self, recieved: Signal, state: Signal = Signal.Zero) -> tuple[Signal, dict[str, Signal]]:
        return [Message(message.signal, self.name, d) for d in self.destinations]
    

MODULES: defaultdict[str, Module] = defaultdict(Void)
STATES: dict[int, defaultdict[str, Signal]] = {}
MESSAGES: dict[int, dict[str, Signal]] = {}

def pressButton(time: int):
    if time in MESSAGES:
        return MESSAGES[time]
    MESSAGES[time] = {"broadcaster": Signal.Low}
    t = time
    while True:
        STATES[t] = defaultdict(lambda: Signal.Low)
        for module_name, signal_recieved in MESSAGES[t].items():
            module = MODULES[module_name]
            new_messages, new_states = module.accept(signal_recieved, STATES[t])

            s = STATES[t][module_name]






def solve(filename: str):
    


    with open(filename) as file:
        for line in file:
            name, destinations = line.strip().split(" -> ")
            if name.startswith("&"):
                modules[name[1:]] = Conjunction(name[1:], destinations.split(", "))
            elif name.startswith("%"):
                modules[name[1:]] = FlipFlop(name[1:], destinations.split(", "))
            elif name == "broadcaster":
                modules[name] = Broadcast(name, destinations.split(", "))

    t = 0
    while True:
        for module_name, signal_recieved in states[t].items():
            new_state, messages = modules[module_name].accept(signal)

        signals: list[Message] = modules["broadcaster"].accept(button_push)
        times.append(0)
        while len(signals) > 0:
            states.appendleft(signals)
            times[-1] += 1
            signals = []
            for s in states[0]:
                signals.extend(modules[s.destination].accept(s))
        if state_non_zero(modules, len(times)):
            break
    print(times)
    for s in states:
        print(s)


        



    

if __name__ == "__main__":
    solve("test1.txt")
