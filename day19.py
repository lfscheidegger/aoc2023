from dataclasses import dataclass
from typing import List, Dict, Optional

from aoc_api import get_input_chunks, submit
from intervals import Interval, intersection


@dataclass(frozen=True)
class Part:
    x_rating: int
    m_rating: int
    a_rating: int
    s_rating: int

    @staticmethod
    def parse(part_str: str) -> 'Part':
        tokens = part_str[1:-1].split(',')
        return Part(
            x_rating=int(tokens[0].split('=')[1]),
            m_rating=int(tokens[1].split('=')[1]),
            a_rating=int(tokens[2].split('=')[1]),
            s_rating=int(tokens[3].split('=')[1]))

    def get_rating(self, rating_type: str) -> int:
        if rating_type == 'x':
            return self.x_rating
        elif rating_type == 'm':
            return self.m_rating
        elif rating_type == 'a':
            return self.a_rating
        elif rating_type == 's':
            return self.s_rating

        raise ValueError(rating_type)

    def process(self, workflows: Dict[str, 'Workflow']) -> str:
        next_workflow_id = 'in'
        while True:
            workflow = workflows[next_workflow_id]
            next_workflow_id = workflow.process(self)
            if next_workflow_id in ['A', 'R']:
                return next_workflow_id

    def get_part_value(self) -> int:
        return self.x_rating + self.m_rating + self.a_rating + self.s_rating


@dataclass(frozen=True)
class Instruction:
    rating_type: str
    condition: str
    amount: int
    next_workflow_id: str

    @staticmethod
    def parse(instruction_str: str) -> 'Instruction':
        if ':' in instruction_str:
            condition_str, then_str = instruction_str.split(':')
            rating_type = condition_str[0]
            condition = condition_str[1]  # '<' or '>'
            amount = int(condition_str[2:])
            next_workflow_id = then_str
            return Instruction(rating_type, condition, amount, next_workflow_id)

        return Instruction(rating_type='', condition='', amount=0, next_workflow_id=instruction_str)

    def process(self, part: Part) -> Optional[str]:
        if self.rating_type == '':
            return self.next_workflow_id

        rating_to_check = part.get_rating(self.rating_type)
        if self.condition == '>' and rating_to_check > self.amount:
            return self.next_workflow_id
        elif self.condition == '<' and rating_to_check < self.amount:
            return self.next_workflow_id
        return None


@dataclass(frozen=True)
class Workflow:
    name: str
    instructions: List[Instruction]

    @staticmethod
    def parse(workflow_str: str) -> 'Workflow':
        name, rest = workflow_str.split('{')
        instructions = [Instruction.parse(token) for token in rest[:-1].split(',')]
        return Workflow(name=name, instructions=instructions)

    def process(self, part: Part) -> str:
        for instruction in self.instructions:
            processed = instruction.process(part)
            if processed is not None:
                return processed

        raise ValueError(f'Workflow {self} failed to process part {part}')


def count_possibilities(
        intervals: Dict[str, Interval],
        workflow_id: str,
        instruction_idx: int,
        workflows: Dict[str, Workflow]) -> int:
    if workflow_id == 'A':
        return interval_count(intervals)
    elif workflow_id == 'R':
        return 0

    instruction = workflows[workflow_id].instructions[instruction_idx]
    next_workflow_id = instruction.next_workflow_id

    if instruction.rating_type == '':
        return count_possibilities(intervals, next_workflow_id, 0, workflows)

    result = 0

    interval_to_break = instruction.rating_type
    if instruction.condition == '>':
        if_intervals = dict(intervals)
        if_intervals[interval_to_break] = \
            intersection([if_intervals[interval_to_break]], [Interval(instruction.amount + 1, 4001)])[0]

        result += count_possibilities(
            if_intervals,
            next_workflow_id,
            0,
            workflows)

        else_intervals = dict(intervals)
        else_intervals[interval_to_break] = \
            intersection([else_intervals[interval_to_break]], [Interval(1, instruction.amount + 1)])[0]

        result += count_possibilities(
            else_intervals,
            workflow_id,
            instruction_idx + 1,
            workflows)
    elif instruction.condition == '<':
        if_intervals = dict(intervals)
        if_intervals[interval_to_break] = \
            intersection([if_intervals[interval_to_break]], [Interval(1, instruction.amount)])[0]

        result += count_possibilities(
            if_intervals,
            next_workflow_id,
            0,
            workflows)

        else_intervals = dict(intervals)
        else_intervals[interval_to_break] = \
            intersection([else_intervals[interval_to_break]], [Interval(instruction.amount, 4001)])[0]

        result += count_possibilities(
            else_intervals,
            workflow_id,
            instruction_idx + 1,
            workflows)

    return result


def interval_count(intervals: Dict[str, Interval]) -> int:
    return (intervals['x'].right - intervals['x'].left) *\
        (intervals['m'].right - intervals['m'].left) *\
        (intervals['a'].right - intervals['a'].left) *\
        (intervals['s'].right - intervals['s'].left)


def part1():
    workflow_strs, part_strs = get_input_chunks(19)
    workflows = {workflow.name: workflow for workflow in [Workflow.parse(workflow_str) for workflow_str in workflow_strs]}
    parts = [Part.parse(part_str) for part_str in part_strs]

    accepted_parts = [part for part in parts if part.process(workflows) == 'A']
    answer = sum([part.get_part_value() for part in accepted_parts])

    submit(day=19, level=1, answer=answer, really=True)


def part2():
    workflow_strs, part_strs = get_input_chunks(19)
    workflows = {workflow.name: workflow for workflow in [Workflow.parse(workflow_str) for workflow_str in workflow_strs]}

    answer = count_possibilities({
        'x': Interval(1, 4001),
        'm': Interval(1, 4001),
        'a': Interval(1, 4001),
        's': Interval(1, 4001),
    }, 'in', 0, workflows)

    submit(day=19, level=2, answer=answer)


part2()
