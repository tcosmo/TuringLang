from typing import Union
import yaml
from enum import Enum
import alang.keywords as kw


class TMSpecificationError(Exception):
    pass


class TMHalt(Exception):
    def __init__(self, machine_name,
                 halting_instruction, halting_instruction_pointer):
        self.machine_name = machine_name
        self.halting_instruction = halting_instruction
        self.halting_instruction_pointer = halting_instruction_pointer

        super().__init__(str(self))
    pass

    def __str__(self):
        return (f"Machine `{self.machine_name}` has halted in instruction"
                f" `{self.halting_instruction}`")


class Direction(Enum):
    LEFT: int = -1
    RIGHT: int = 1


BLANK_SYMBOL = None


class Tape:
    def __init__(self):
        self.name: str = ""
        self.alphabet: list[str] = []
        self.tape: dict[int, str] = {}
        self.head_position: int = 0
        self.tape[self.head_position] = BLANK_SYMBOL

    def __str__(self):
        to_return = f"tape `{self.name}`:\n"

        return to_return

    def reset(self):
        self.tape = {}
        self.head_position: int = 0
        self.tape[self.head_position] = BLANK_SYMBOL

    def get_configuration_dict(self):
        min_pos = 0
        max_pos = 0
        for pos in self.tape:
            min_pos = min(min_pos, pos)
            max_pos = max(max_pos, pos)
        to_return = {}
        for i in range(min_pos, max_pos+1):
            value = kw.KW_BLANK
            if i in self.tape:
                value = self.tape[i]
                if not value:
                    value = kw.KW_BLANK
            if i != self.head_position:
                to_return[i] = value
            else:
                to_return[i] = [value, True]
        return to_return

    def check_valid_symbol(self, symb):
        if symb not in self.alphabet:
            raise TMSpecificationError(f"Symbol `{symb}` is not part "
                                       f"of tape `{self.name}`'s alphabet")

    def init_tape(self, configuration: list[str]):
        self.head_position = 0
        for i, symb in enumerate(configuration):
            self.check_valid_symbol(symb)
            self.tape[i] = symb

    def read_equals(self, value: Union[str, None]) -> bool:
        if value:
            self.check_valid_symbol(value)
        return self.tape[self.head_position] == value

    def write(self, value: str):
        self.check_valid_symbol(value)
        self.tape[self.head_position] = value

    def move(self, direction: Direction):
        self.head_position += 1 if direction == Direction.RIGHT else \
            -1
        if self.head_position not in self.tape:
            self.tape[self.head_position] = BLANK_SYMBOL

    def from_yaml_dict(yaml_dict):
        tape = Tape()
        inside_tape = yaml_dict[kw.KW_TAPE]
        tape.name = str(inside_tape[kw.KW_NAME])
        tape.alphabet = str(inside_tape[kw.KW_ALPHABET])
        return tape


class TapeAndValue:
    def __init__(self):
        self.tape_name: str = ""
        self.value: Union[str, None] = BLANK_SYMBOL

    def from_yaml_dict(yaml_dict):
        tape_and_value = TapeAndValue()
        tape_and_value.tape_name = str(yaml_dict[kw.KW_TAPE])

        if yaml_dict[kw.KW_VALUE] == kw.KW_BLANK:
            tape_and_value.value = BLANK_SYMBOL
        else:
            tape_and_value.value = str(yaml_dict[kw.KW_VALUE])

        return tape_and_value


class TapeAndDirection:
    def __init__(self):
        self.tape_name: str = ""
        self.direction: Union[Direction, None] = None

    def from_yaml_dict(yaml_dict):
        tape_and_dir = TapeAndDirection()
        tape_and_dir.tape_name = str(yaml_dict[kw.KW_TAPE])

        if yaml_dict[kw.KW_DIRECTION] == kw.KW_LEFT:
            tape_and_dir.direction = Direction.LEFT
        elif yaml_dict[kw.KW_DIRECTION] == kw.KW_RIGHT:
            tape_and_dir.direction = Direction.RIGHT
        else:
            raise TMSpecificationError(
                f"Unknown tape direction `{yaml_dict[kw.KW_DIRECTION]}`")

        return tape_and_dir


class ReadCase:
    def __init__(self):
        self.read_instructions: list[TapeAndValue] = []

    def match(self, tapes) -> bool:
        for read_instr in self.read_instructions:
            tape_name, value = read_instr.tape_name, read_instr.value
            if tape_name not in tapes:
                raise TMSpecificationError(f"In read instruction: "
                                           f"tape `{tape_name}`"
                                           " does not exists")

            if not tapes[tape_name].read_equals(value):
                return False
        return True

    def from_yaml_dict(yaml_dict):
        read_instr = ReadCase()

        tape_seen = {}
        for tape_and_value in yaml_dict:
            read_instr.read_instructions.append(
                TapeAndValue.from_yaml_dict(tape_and_value))
            if read_instr.read_instructions[-1].tape_name in tape_seen:
                raise TMSpecificationError(
                    "Two different read instructions are given for the same"
                    "tape in the same read case, that's illegal!")

        return read_instr


class SwitchCase:
    def __init__(self):
        self.read_cases: list[ReadCase] = []
        self.write_instructions: list[TapeAndValue] = []
        self.move_instructions: list[TapeAndDirection] = []
        self.goto_instruction: Union[str, None] = None

    def match(self, tapes) -> bool:
        for read_case in self.read_cases:
            if read_case.match(tapes):
                return True
        return False

    def apply(self, tapes) -> Union[str, None]:
        for write_instruction in self.write_instructions:
            tape_name = write_instruction.tape_name
            value = write_instruction.value
            if tape_name not in tapes:
                raise TMSpecificationError(f"In write instruction: "
                                           f"tape `{tape_name}`"
                                           " does not exists")
            tapes[tape_name].write(value)

        for move_instruction in self.move_instructions:
            tape_name, direction = move_instruction.tape_name,\
                move_instruction.direction
            if tape_name not in tapes:
                raise TMSpecificationError(f"In move instruction: "
                                           f"tape `{tape_name}`"
                                           " does not exists")
            tapes[tape_name].move(direction)

        return self.goto_instruction

    def from_yaml_dict(yaml_dict):
        switch = SwitchCase()
        yaml_dict_inside = yaml_dict[kw.KW_CASE]
        for read_case in yaml_dict_inside:
            switch.read_cases.append(
                ReadCase.from_yaml_dict(read_case[kw.KW_READ]))

        then_dict = yaml_dict[kw.KW_THEN]

        if then_dict[kw.KW_WRITE]:
            tape_seen = {}
            for write_instruction in then_dict[kw.KW_WRITE]:
                switch.write_instructions.append(
                    TapeAndValue.from_yaml_dict(write_instruction))

                if switch.write_instructions[-1].tape_name in tape_seen:
                    raise TMSpecificationError(
                        "Two different write instructions are given for the "
                        "same tape in the same switch case, that's illegal!")

                tape_seen[switch.write_instructions[-1].tape_name] = True

        if then_dict[kw.KW_MOVE]:
            tape_seen = {}
            for move_instruction in then_dict[kw.KW_MOVE]:
                switch.move_instructions.append(
                    TapeAndDirection.from_yaml_dict(move_instruction))

                if switch.move_instructions[-1].tape_name in tape_seen:
                    raise TMSpecificationError(
                        "Two different move instructions are given for the "
                        "same tape in the same switch case, that's illegal!")

                tape_seen[switch.move_instructions[-1].tape_name] = True

        switch.goto_instruction = str(
            then_dict[kw.KW_GOTO]) if then_dict[kw.KW_GOTO] else None
        return switch


class Instruction:
    def __init__(self):
        self.name: str = ""
        self.switch_cases: list[SwitchCase] = []

    def run(self, tapes: list[Tape]) -> Union[str, None]:
        goto = None
        for switch_case in self.switch_cases:
            if switch_case.match(tapes):
                goto = switch_case.apply(tapes)
                break
        return goto

    def from_yaml_dict(yaml_dict):
        instr = Instruction()
        inside_dict = yaml_dict[kw.KW_INSTRUCTION]
        instr.name = str(inside_dict[kw.KW_NAME])

        if kw.KW_SWITCH in inside_dict:
            for switch_case in inside_dict[kw.KW_SWITCH]:
                instr.switch_cases.append(
                    SwitchCase.from_yaml_dict(switch_case))

        return instr


class TuringMachine:
    def __init__(self):
        self.name: str = ""
        self.tapes: dict[str, Tape] = {}
        self.instructions: list[Instruction] = []
        self.instruction_pointer: int = 0
        self.reverse_instruction_table: dict[str, int] = {}

    def init_tape(self, tape_name: str, configuration: list[str]):
        if tape_name not in self.tapes:
            raise TMSpecificationError(f"Tape `{tape_name}` does not exist.")
        self.tapes[tape_name].init_tape(configuration)

    def reset(self):
        self.instruction_pointer = 0
        for tape_name in self.tapes:
            self.tapes[tape_name].reset()

    def get_configuration_dict(self):
        instr_name = self.instructions[self.instruction_pointer].name
        to_return = {'configuration': {'machine': self.name,
                                       'current_instruction': instr_name,
                                       'instruction_pointer':
                                       self.instruction_pointer},
                     'tapes': {}}
        for tape_name in self.tapes:
            to_return['tapes'][tape_name] = self.tapes[tape_name]\
                .get_configuration_dict()
        return to_return

    def __str__(self) -> str:
        return yaml.dump(self.get_configuration_dict(), sort_keys=False)

    def step(self):
        goto = self.instructions[self.instruction_pointer].run(self.tapes)

        if goto is None:
            instr_name = self.instructions[self.instruction_pointer].name
            raise TMHalt(self.name, instr_name, self.instruction_pointer)

        self.instruction_pointer = self.reverse_instruction_table[goto]

    def from_file(file_path):
        with open(file_path) as f:
            machine_spec = yaml.load(f, Loader=yaml.FullLoader)

        return TuringMachine.from_yaml_dict(machine_spec)

    def from_yaml_dict(yaml_dict):
        tm = TuringMachine()

        machine_dict_inside = yaml_dict[kw.KW_MACHINE]

        tm.name = str(machine_dict_inside[kw.KW_NAME])

        unique_tape_name = {}
        for tape_dict in machine_dict_inside[kw.KW_TAPES]:
            the_tape = Tape.from_yaml_dict(tape_dict)
            tm.tapes[the_tape.name] = the_tape
            if the_tape.name in unique_tape_name:
                raise TMSpecificationError(
                    f"Two tapes have the same name `{the_tape.name}`,"
                    "that's illegal!")
            unique_tape_name[the_tape.name] = True

        unique_instruction_name = {None: True}
        for instruction_dict in machine_dict_inside[kw.KW_INSTRUCTIONS]:
            tm.instructions.append(
                Instruction.from_yaml_dict(instruction_dict))
            if tm.instructions[-1].name in unique_instruction_name:
                raise TMSpecificationError(
                    "Two instructions have the same name "
                    f"`{tm.instructions[-1].name}`, that's illegal!")
            unique_instruction_name[tm.instructions[-1].name] = True

        for i, instruction in enumerate(tm.instructions):
            for switch_case in instruction.switch_cases:
                if switch_case.goto_instruction not in unique_instruction_name:
                    raise TMSpecificationError(
                        f"Instruction `{instruction.name}` has a goto "
                        f"`{switch_case.goto_instruction}` referring to an "
                        "inexistent instruction")
            tm.reverse_instruction_table[instruction.name] = i

        return tm
