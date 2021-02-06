# This machine computes the parity of the number of 1s in a binary input
machine:
  name: "parity"

  tapes:
    - tape:
        name: "input"
        alphabet: ["0", "1"]
    - tape:
        name: "output"
        alphabet: ["0", "1"]

  instructions:
    - instruction:
        name: "even"
        switch:
          - read:
              - case:
                  - { tape: "input", value: "0" }

            then:
              write:
              move:
                - { tape: "input", direction: right }
              goto: "even"

          - read:
              - case:
                  - { tape: "input", value: "1" }

            then:
              write:
              move:
                - { tape: "input", direction: right }
              goto: "odd"

          - read:
              - case:
                  - { tape: "input", value: blank }

            then:
              write:
                - { tape: "output", value: "0" }
              move:
              goto: "halt"

    - instruction:
        name: "odd"
        switch:
          - read:
              - case:
                  - { tape: "input", value: "0" }

            then:
              write:
              move:
                - { tape: "input", direction: right }
              goto: "odd"

          - read:
              - case:
                  - { tape: "input", value: "1" }

            then:
              write:
              move:
                - { tape: "input", direction: right }
              goto: "even"

          - read:
              - case:
                  - { tape: "input", value: blank }

            then:
              write:
                - { tape: "output", value: "1" }
              move:
              goto: "halt"
