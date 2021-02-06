# This machine computes the sum of two numbers written
# in binary with LSB to the left, assuming shortest input is padded with 0s
# on the most significant bit side
machine:
  name: binary_adder

  tapes:
    - tape:
        name: "input_1"
        alphabet: ["0", "1"]
    - tape:
        name: "input_2"
        alphabet: ["0", "1"]
    - tape:
        name: "output"
        alphabet: ["0", "1"]

  instructions:
    - instruction:
        name: "add_with_no_carry"
        switch:
          - case:
              - read:
                  - { tape: "input_1", value: "0" }
                  - { tape: "input_2", value: "0" }

            then:
              write:
                - { tape: "output", value: "0" }
              move:
                - { tape: "input_1", direction: right }
                - { tape: "input_2", direction: right }
                - { tape: "output", direction: right }
              goto: "add_with_no_carry"

          - case:
              - read:
                  - { tape: "input_1", value: "0" }
                  - { tape: "input_2", value: "1" }
              - read:
                  - { tape: "input_1", value: "1" }
                  - { tape: "input_2", value: "0" }

            then:
              write:
                - { tape: "output", value: "1" }
              move:
                - { tape: "input_1", direction: right }
                - { tape: "input_2", direction: right }
                - { tape: "output", direction: right }
              goto: "add_with_no_carry"

          - case:
              - read:
                  - { tape: "input_1", value: "1" }
                  - { tape: "input_2", value: "1" }

            then:
              write:
                - { tape: "output", value: "0" }
              move:
                - { tape: "input_1", direction: right }
                - { tape: "input_2", direction: right }
                - { tape: "output", direction: right }
              goto: "add_with_carry"

          - case:
              - read:
                  - { tape: "input_1", value: blank }

            then:
              write:
              move:
              goto: "halt"

    - instruction:
        name: "add_with_carry"
        switch:
          - case:
              - read:
                  - { tape: "input_1", value: "0" }
                  - { tape: "input_2", value: "0" }

            then:
              write:
                - { tape: "output", value: "1" }
              move:
                - { tape: "input_1", direction: right }
                - { tape: "input_2", direction: right }
                - { tape: "output", direction: right }
              goto: "add_with_no_carry"

          - case:
              - read:
                  - { tape: "input_1", value: "0" }
                  - { tape: "input_2", value: "1" }
              - read:
                  - { tape: "input_1", value: "1" }
                  - { tape: "input_2", value: "0" }

            then:
              write:
                - { tape: "output", value: "0" }
              move:
                - { tape: "input_1", direction: right }
                - { tape: "input_2", direction: right }
                - { tape: "output", direction: right }
              goto: "add_with_carry"

          - case:
              - read:
                  - { tape: "input_1", value: "1" }
                  - { tape: "input_2", value: "1" }

            then:
              write:
                - { tape: "output", value: "1" }
              move:
                - { tape: "input_1", direction: right }
                - { tape: "input_2", direction: right }
                - { tape: "output", direction: right }
              goto: "add_with_carry"

          - case:
              - read:
                  - { tape: "input_1", value: blank }

            then:
              write:
                - { tape: "output", value: "1" }
              move:
              goto: "halt"

    - instruction:
        name: "halt"
