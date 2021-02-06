# This machine computes the parity of the number of 1s in a binary input
machine:
  name: "palindrome"

  tapes:
    - tape:
        name: "input"
        alphabet: ["0", "1"]
    - tape:
        name: "working"
        alphabet: ["0", "1"]

  instructions:
    - instruction:
        name: "go_at_end_of_input"
        switch:
          - case:
              - read:
                  - { tape: "input", value: "0" }
              - read:
                  - { tape: "input", value: "1" }

            then:
              write:
              move:
                - { tape: "input", direction: right }
              goto: "go_at_end_of_input"

          - case:
              - read:
                  - { tape: "input", value: blank }

            then:
              write:
              move:
                - { tape: "input", direction: left }
              goto: "copy_reversed_input"

    - instruction:
        name: "copy_reversed_input"
        switch:
          - case:
              - read:
                  - { tape: "input", value: "0" }

            then:
              write:
                - { tape: "working", value: "0" }
              move:
                - { tape: "input", direction: left }
                - { tape: "working", direction: right }
              goto: "copy_reversed_input"

          - case:
              - read:
                  - { tape: "input", value: "1" }

            then:
              write:
                - { tape: "working", value: "1" }
              move:
                - { tape: "input", direction: left }
                - { tape: "working", direction: right }
              goto: "copy_reversed_input"

          - case:
              - read:
                  - { tape: "input", value: blank }

            then:
              write:
              move:
                - { tape: "input", direction: right }
                - { tape: "working", direction: left }
              goto: "rewind_working_tape"

    - instruction:
        name: "rewind_working_tape"
        switch:
          - case:
              - read:
                  - { tape: "working", value: "0" }
              - read:
                  - { tape: "working", value: "1" }

            then:
              write:
              move:
                - { tape: "working", direction: left }
              goto: "rewind_working_tape"

          - case:
              - read:
                  - { tape: "working", value: blank }

            then:
              write:
              move:
                - { tape: "working", direction: right }
              goto: "compare_tapes"

    - instruction:
        name: "compare_tapes"
        switch:
          - case:
              - read:
                  - { tape: "input", value: "0" }
                  - { tape: "working", value: "0" }
              - read:
                  - { tape: "input", value: "1" }
                  - { tape: "working", value: "1" }

            then:
              write:
              move:
                - { tape: "input", direction: right }
                - { tape: "working", direction: right }
              goto: "compare_tapes"

          - case:
              - read:
                  - { tape: "input", value: "0" }
                  - { tape: "working", value: "1" }
              - read:
                  - { tape: "input", value: "1" }
                  - { tape: "working", value: "0" }

            then:
              write:
              move:
              goto: "not_palindrome"

          - case:
              - read:
                  - { tape: "input", value: blank }

            then:
              write:
              move:
              goto: "palindrome"

    - instruction:
        name: "not_palindrome"

    - instruction:
        name: "palindrome"
