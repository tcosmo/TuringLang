// This machine computes the parity of the number of 1s in a binary input
machine parity:
  tapes:
    tape input:
      alphabet: 0, 1
    tape output:
      alphabet: 0, 1

  initial instruction A:
    ifread 0, _:
      move input right
      goto A
    ifread 1, _:
      move input right
      goto B
    ifread blank, _:
      write output 0
      goto halt

  instruction B:
    ifread 0, _:
      move input right
      goto B
    ifread 1, _:
      move input right
      goto A
    ifread blank, _:
      write output 1
      goto halt

  instruction halt: