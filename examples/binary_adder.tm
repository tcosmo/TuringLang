# This machine computes the sum of two numbers written
# in binary with LSB to the left, assuming shortest input is padded with 0s
# on the most significant bit side
machine:
  name: binary_adder

  tapes:
    input_1:
      alphabet: ["0", "1"]
    input_2:
      alphabet: ["0", "1"]
    output:
      alphabet: ["0", "1"]

  instructions:
    add_with_no_carry:
      - initial: true
      - ifread:
          input_1: "0"
          input_2: "0"

        then:
          write:
            output: "0"
          move:
            input_1: right
            input_2: right
            output: right
          goto: add_with_no_carry

      - ifread:
          - input_1: "1"
            input_2: "0"

          - input_1: "0"
            input_2: "1"

        then:
          write:
            output: "1"
          move:
            input_1: right
            input_2: right
            output: right
          goto: add_with_no_carry

      - ifread:
          input_1: "1"
          input_2: "1"

        then:
          write:
            output: "0"
          move:
            input_1: right
            input_2: right
            output: right
          goto: add_with_carry

      - ifread:
          - input_1: blank
          - input_2: blank

        then:
          write:
          move:
          goto: halt
          
    add_with_carry:
      - ifread:
          input_1: "0"
          input_2: "0"

        then:
          write:
            output: "1"
          move:
            input_1: right
            input_2: right
            output: right
          goto: add_with_no_carry

      - ifread:
          - input_1: "0"
            input_2: "1"

          - input_1: "1"
            input_2: "0"

        then:
          write:
            output: "0"
          move:
            input_1: right
            input_2: right
            output: right
          goto: add_with_carry

      - ifread:
          input_1: "1"
          input_2: "1"

        then:
          write:
            output: "1"
          move:
            input_1: right
            input_2: right
            output: right
          goto: add_with_carry

      - ifread:
          - input_1: blank
          - input_2: blank

        then:
          write:
            output: "1"
          move:
          goto: halt

    halt:
