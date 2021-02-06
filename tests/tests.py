import unittest
import alang


class TestSampleTuringMachines(unittest.TestCase):
    def test_copy(self):
        copy_machine = alang.TuringMachine.from_file("examples/copy.tm")
        copy_machine.init_tape('input', ["0", "1", "0", "0", "1"])
        for i in range(10):
            try:
                copy_machine.step()
            except alang.TMHalt as e:
                for key in copy_machine.tapes["input"].tape:
                    self.assertEqual(copy_machine.tapes["input"].tape[key],
                                     copy_machine.tapes["output"].tape[key])
                    self.assertEqual(len(copy_machine.tapes["input"].tape),
                                     len(copy_machine.tapes["output"].tape))
                self.assertEqual(e.halting_instruction, "halt")
        self.assertEqual(True, False)

    def test_palindrome(self):
        palindrome_machine = alang.TuringMachine.from_file(
            "examples/palindrome.tm")

        nb_success = 0

        tests = [(["0", "1", "0", "0", "1"], False),
                 ((["1", "0", "0", "1"], True))]

        for test in tests:
            palindrome_machine.reset()
            palindrome_machine.init_tape(
                'input', test[0])
            for i in range(30):
                try:
                    palindrome_machine.step()

                except alang.TMHalt as e:
                    self.assertEqual(
                        e.halting_instruction, "palindrome"
                        if test[1] else "not_palindrome")
                    nb_success += 1
                    break

        self.assertEqual(nb_success, len(tests))
