# ceres
Ceres is a recreational programming language focusing on making fast and short programs to generalize sequences, specifically those commonly showing up on OEIS.

# inputs
Typically, a program should only receive one input, which is the sequence index. However, other inputs which might act as sequence variants will be accessible to the programmer as well.

# sections
Each program can consist of more than one section, only one of which is actually run. A new section is denoted by a character in the following section types. Each section has a different priority, and the section that comes first that has the highest priority that matches the sequence index will be executed.

If the program does not start with a section delimiting character, then it is assumed to match everything and have priority 0.

# literals
Numeric literals and list literals are supported. Exp-10 literals are supported with `[left]ȷ[right] = left * 10 ** right`. `a.` is equivlent to `a.5`. `-` is `-1`, `.` is `.5`, and `-.` is `-.5`. `.a` is what it looks like. `“...”` denotes a base 255 number.

### section types

|Syntax|Description|Priority|
|------|-----------|--------|
|`≺[num]`|Called if the index is strictly less than the number|1|
|`≻[num]`|Called if the index is strictly greater than the number|1|
|`≼[num]`|Called if the index is less than or equal to the number|1|
|`≽[num]`|Called if the index is greater than or equal to the number|1|

### supersection types

|Syntax|Description|Priority|
|------|-----------|--------|
|`∀[mode][mode]`|Called if both of the following modes are matched|Maximum of the two priorities|

# verbs
`x, y` represent the top and second-from-top (left and right) elements for a dyad. `z` represents the top (element) for a monad.

|Command|Description|Vectorization Depth|
|-------|-----------|-------------------|
|`Ḏ`|Duplicate top of stack (if the stack is empty, pulls the next command line argument onto the stack)|0|
|`P`|Is the `z` a prime?|inf|
|`Ṗ`|Largest prime that is not greater than `z`|inf|
|`Ṕ`|Smallest prime that is not less than `z`|inf|
|`B`|Binary digits|inf|
|`Ḃ`|Binary digits to integer|-1|
|`D`|Decimal digits|inf|
|`Ḋ`|Decimal digits to integer|-1|
|`E`|All element of `z` or the entire stack are equal|0|
|`F`|Flatten|0|
|`I`|Deltas of `z` or the entire stack|0|
|`J`|Range of length|0|
|`K`|Same shape with increasing elements|0|
|`L`|Length|0|
|`Ḷ`|Lowered range `0..z-1`|inf|
|`İ`|Inclusive range `0..z`|inf|
|`R`|Range `1..z`|inf|
|`Ē`|Exclusive range `1..z-1`|inf|
|`S`|Sum of `z` or the entire stack|0|
|`Ṡ`|Cumulative sum of `z` or the entire stack|0|
|`∘`|Product of `z` or the entire stack|0|
|`Z`|Zip of `z` or the entire stack|0|
|`d`|Arbitrary base digits|0|
|`ḋ`|Arbitrary base digits to integer|0|
|`m`|Mold left like right|0|
|`r`|Inclusive range|inf|
|`z`|Zip with filler|0|
|`ż`|Zip; interleave|0|
|`ÆU`|Reverse each of `z` or the entire stack|1|
|`ÆW`|Wrap the entire stack into an array|0|
|`Æw`|Push each element of `z` or the entire stack individually|0|
|`ÆṘ`|Reverse `z` or the entire stack|0|
|`ÆP`|`chr`|inf|
|`Æp`|Index into the codepage|inf|
|`ŒḂ`|Bounce; returns `z[:-1] + z[::-1]`|0|
|`ŒB`|Bounce; returns `z[:-1] + z[::-1]`|1|
|`+`|Addition|inf|
|`_`|Subtraction|inf|
|`*`|Exponentiation|inf|
|`⨉`|Multiplication|inf|
|`^`|Bitwise XOR|inf|
|`&`|Bitwise AND|inf|
|`[pipe]`|Bitwise OR (someone figure out how to make markdown stop being stupid)|inf|
|`%`|Modulo|inf|
|`=`|Equals|inf|
|`∈`|Contains|0|
|`~`|Bitwise NOT|inf|
|`¬`|Logical NOT|inf|
|`⁺`|Increment|inf|
|`⁻`|Decrement|inf|
|`⁼`|Equals|0|
|`!`|Factorial|0|

# adverbs

|Command|Description|
|-------|-----------|
|`$`|Last two verbs joined|
|`€`|Map using the last verb over `z` or the entire stack|
|`₤`|Map using the last verb over `x` with `y` as the second argument|
|`ʀ`|Map using the last verb over `y` with `x` as the first argument|
|`⨰`|Map using the last verb over ever pair of `x` and `y`|
|`⨅`|Get the `z`-th positive integer that satisfies the last predicate|
|`⨆`|Get the `z`-th positive integer that does not satisfy the last predicate|
|`░`|Filter positive|
|`▓`|Filter negative|
|`/`|Reduce|
|`∃`|There exists a value that satisfies the predicate|
|`∄`|There does not exist a value that satisfies the predicate|
