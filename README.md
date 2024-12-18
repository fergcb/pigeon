# Pigeon
Pigeon is a stack-based esoteric programming language with support for array programming.

[**View the Pigeon instruction set**](DOCS.md)

## Try it
The following command will execute the "fizzbuzz" Pigeon source file in the examples.
```shell
python pigeon.py run examples/fizzbuzz.pg
```
Or, you can pass in a string of code to run as a command-line argument. Here is an example that computes a nth fibonacci number:
```shell
python pigeon.py exec "01;{2{+}v}*"
```
You can add the `-e` flag to explain the code as it is executed:
```shell
python pigeon.py run -e examples/fizzbuzz.pg # OR
python pigeon.py exec -e "01;{2{+}v}*"
```
To provide an input file, use the `-i` flag. The specified file will be read and added to the stack before the program is executed.
```shell
python pigeon.py run aoc/01.pg -i aoc/01.txt # OR
python pigeon.py exec "FE/{``n{+}/}m]" -i aoc/01.txt
```

## Examples
### Quine
```
0
```

In Pigeon, the value on top of the stack at the end of execution is implicitly printed.
This means that the shortest quine in Pigeon is `0`.
This program pushes the integer `0` to the stack, then prints it.
In fact, any single decimal digit is a valid 1-byte quine in Pigeon.

### Fibonacci
```
01;{2{+}v}*
```
This program inputs a number `n` from the user, and computes the `n`th number in the Fibonacci sequence.

The program can be broken down as follows.
```
01;{2{+}v}*     Input an integer n and print the nth Fibonacci number

01              The numbers 0 and 1 are pushed to the stack
  ;{     }*     The nested code is executed a number of times input by the user
    2{ }v         A new stack is created with 2 values from the top of the parent stack
                  and the nested code is executed on the new stack
      +             The 2 values are added together
                Implicitly print the result
```

### Factorial
```
;^1+{*}/
```

This program inputs an integer `n`, and outputs the factorial of `n`.

The program can be broken down as follows:

```
;^1+{*}/    Input an integer and print its factorial

;^          Input an integer and generate the range [0..n)
  1+        Add one to each number in the range (=> [1..n])
    {*}/    Apply a multiplicative reduction
            Implicitly print the result
```