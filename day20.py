from dataclasses import dataclass
from typing import List, Union, Dict, Tuple

from aoc_api import get_input, submit


@dataclass(frozen=True)
class Pulse:
    pulse_type: str
    sender_module_id: str
    destination_module_id: str

    def __str__(self) -> str:
        return f'{self.sender_module_id} -{self.pulse_type}-> {self.destination_module_id}'


@dataclass
class Module:
    module_id: str
    module_type: str
    module_destinations: List[str]

    module_state: Union[bool, Dict[str, str], None]

    @staticmethod
    def parse(line: str) -> 'Module':
        module_id_str, right = [t.strip() for t in line.split('->')]
        module_destinations = [t.strip() for t in right.split(',')]
        if module_id_str == 'broadcaster':
            return Module(
                module_id=module_id_str,
                module_type='broadcaster',
                module_destinations=module_destinations,
                module_state=None)

        module_type = module_id_str[0]
        module_id = module_id_str[1:]

        module_state = {} if module_type == '&' else False
        return Module(
            module_id=module_id,
            module_type=module_type,
            module_destinations=module_destinations,
            module_state=module_state)

    def process_pulse(self, pulse: Pulse) -> List[Pulse]:
        if self.module_type == '%' and pulse.pulse_type == 'low':
            self.module_state = not self.module_state
            output_pulse_type = 'high' if self.module_state else 'low'
        elif self.module_type == '%':
            assert pulse.pulse_type == 'high'
            return []
        elif self.module_type == '&':
            self.module_state[pulse.sender_module_id] = pulse.pulse_type
            if all([v == 'high' for v in self.module_state.values()]):
                output_pulse_type = 'low'
            else:
                output_pulse_type = 'high'
        else:
            assert self.module_type == 'broadcaster'
            output_pulse_type = pulse.pulse_type

        return [Pulse(pulse_type=output_pulse_type, sender_module_id=self.module_id, destination_module_id=destination)
                for destination
                in self.module_destinations]


@dataclass(frozen=True)
class CacheKey:
    on_flip_flops: Tuple[str]
    conjunction_memory: Tuple[str]

    @staticmethod
    def build(input: Dict[str, Module]) -> 'CacheKey':
        on_flip_flops = tuple(
            module.module_id for module in input.values() if module.module_type == '%' and module.module_state)

        conjunction_memory = tuple(f'{module.module_id}-{list(module.module_state.values())}' for module in input.values() if module.module_type == '&')

        return CacheKey(
            on_flip_flops=on_flip_flops,
            conjunction_memory=conjunction_memory)


input: Dict[str, Module] = {}


#@cache
def press_button(cache_key: CacheKey) -> Tuple[int, int, bool]:
    global input

    pulses = [Pulse(pulse_type='low', sender_module_id='button', destination_module_id='broadcaster')]
    low_pulses = 0
    high_pulses = 0
    hit_rx_module = False
    while len(pulses) != 0:
        pulse = pulses[0]
        pulses = pulses[1:]

        if pulse.pulse_type == 'high':
            high_pulses += 1
        else:
            assert pulse.pulse_type == 'low'
            low_pulses += 1

        destination_module = input.get(pulse.destination_module_id)
        if destination_module:
            pulses += destination_module.process_pulse(pulse)

        if pulse.destination_module_id == 'rx' and pulse.pulse_type == 'low':
            hit_rx_module = True

    return low_pulses, high_pulses, hit_rx_module


def part1():
    global input

    input = {m.module_id: m for m in get_input(day=20, mapper=Module.parse)}

    # bake in the initial state for conjunctions
    for module_id in input:
        for destination_module_id in input[module_id].module_destinations:
            destination_module = input.get(destination_module_id)
            if destination_module and destination_module.module_type == '&':
                destination_module.module_state[module_id] = 'low'

    low_pulses, high_pulses = 0, 0
    for _ in range(1000):
        round_lp, round_hp, _ = press_button(CacheKey.build(input))
        low_pulses += round_lp
        high_pulses += round_hp

    print(low_pulses, high_pulses)
    answer = low_pulses * high_pulses

    submit(day=20, level=1, answer=answer)


def part2():
    global input

    input = {m.module_id: m for m in get_input(day=20, mapper=Module.parse)}

    # bake in the initial state for conjunctions
    for module_id in input:
        for destination_module_id in input[module_id].module_destinations:
            destination_module = input.get(destination_module_id)
            if destination_module and destination_module.module_type == '&':
                destination_module.module_state[module_id] = 'low'

    button_presses = 0
    while True:
        button_presses += 1
        _, _, hit_rx_button = press_button(CacheKey.build(input))

        if hit_rx_button:
            break

    submit(day=20, level=2, answer=button_presses)


part2()
