# This machine copies the content of its input tape on its output tape
machine:
  name: "copy"

  tapes:
    - tape:
        name: "input"
        alphabet: ["0", "1"]
    - tape:
        name: "output"
        alphabet: ["0", "1"]

  instructions:
    - instruction:
        name: "copy_input"
        switch:
          - case:
              - read:
                  - { tape: "input", value: "0" }

            then:
              write:
                - { tape: "output", value: "0" }
              move:
                - { tape: "input", direction: right }
                - { tape: "output", direction: right }
              goto: "copy_input"

          - case:
              - read:
                  - { tape: "input", value: "1" }

            then:
              write:
                - { tape: "output", value: "1" }
              move:
                - { tape: "input", direction: right }
                - { tape: "output", direction: right }
              goto: "copy_input"

          - case:
              - read:
                  - { tape: "input", value: blank }

            then:
              write:
              move:
              goto: "halt"

    - instruction:
        name: "halt"
