# ceres
Ceres is a recreational programming language focusing on making fast and short programs to generalize sequences, specifically those commonly showing up on OEIS.

# inputs
Typically, a program should only receive one input, which is the sequence index. However, other inputs which might act as sequence variants will be accessible to the programmer as well.

# sections
Each program can consist of more than one section, only one of which is actually run. A new section is denoted by a character in the following section types. Each section has a different priority, and the section that comes first that has the highest priority that matches the sequence index will be executed.

If the program does not start with a section delimiting character, then it is assumed to match everything and have priority 0.

### section types (TO-DO)

# computation modes
Each section has a mode. The default mode is `function_of_index`, and the other modes are `index_satisfies` and `index_dissatisfies`. `index_satisfies` gets the `n`-th positive integer that satisfies the section's code and `index_dissatisfies` gets the `n`-th positive integer that doesn't satisfy the section's code.

# indexing
If the code starts with `!` and then a number literal, the `!num` is ignored and `num` is subtracted from the index. If the code starts with `?` and then a number literal, the `?num` is ignored and `num` is added to the index.
