// This machine computes the parity of the number of 1s in a binary input
machine palindrome:
  tapes:
    tape input:
      alphabet: 0, 1
    tape working:
      alphabet: 0, 1

  initial instruction go_at_end_of_input:
    ifread 0, _:
    ifread 1, _:
      move input right
      goto go_at_end_of_input
    
    ifread blank, _:
      move input left
      goto go_at_end_of_input

  instruction write_working_reverse:
    ifread 0, _:
    ifread 1, _:
      write working 0
      move input left
      move working right
      goto write_working_reverse
    
    ifread blank, _:
      move input right
      move working left
      goto rewind_working

  instruction rewind_working:
    ifread _, 0:
    ifread _, 1:
      move working left
      goto rewind_working
    
    ifread blank, _:
      move working right
      goto compare_tapes

  instruction compare_tapes:
    ifread 0, 0:
    ifread 1, 1:
      move input right
      move working right
      goto compare_tapes
    
    ifread 0, 1:
    ifread 1, 0:
      goto not_palindrome

    ifread blank, blank:
      goto palindrome

  instruction not_palindrome:
  instruction palindrome: