# This machine copies the content of its input tape on its output tape
machine copy:
  tapes:
    input:
      alphabet: ["0", "1"]
    output:
      alphabet: ["0", "1"]

  instructions:
    go_to_end_of_input:
      - initial: true
      - ifread:
          input: "0"

        then:
          write:
          move:
            input: right
            output: right
          goto: go_to_end_of_input

      - ifread:
          input: "1"

        then:
          write:
          move:
            input: right
            output: right
          goto: go_to_end_of_input

      - ifread:
          input: blank

        then:
          write:
          move:
            input: left
            output: left
          goto: copy_input_from_the_end

    copy_input_from_the_end:
      - ifread:
          input: "0"

        then:
          write:
            output: "0"
          move:
            input: left
            output: left
          goto: copy_input_from_the_end

      - ifread:
          input: "1"

        then:
          write:
            output: "1"
          move:
            input: left
            output: left
          goto: copy_input_from_the_end

      - ifread:
          input: blank

        then:
          write:
          move:
          goto: halt
          
    halt:
