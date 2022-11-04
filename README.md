# Pigeon
Pigeon is a stack-based esoteric programming language with support for array programming.

## Try it
The following command will execute the "fizzbuzz" Pigeon source file in the examples.
```shell
python pigeon.py run examples/fizzbuzz.pg
```
You can add the `-e` flag to explain the code as it is executed:
```shell
python pigeon.py run -e examples/fizzbuzz.pg
```

## Example
The following snippet is a "FizzBuzz" program in Pigeon.
```
"","Fizz","Buzz","FizzBuzz";^1+::r3%fc5%f2*+ic|"\n"j.
```
The program makes use of array programming techniques to print the integers from 1 to a number entered by the user,
but replacing numbers divisible by 3 with "Fizz", numbers divisible by 5 with "Buzz", and numbers divisible by both
3 and 5 with "FizzBuzz".

The program can be broken down as follows:
```
"","Fizz","Buzz","FizzBuzz"     Push a list of 4 strings
;^                              Input N and push a range [0, N)
1+                              Add 1 to each in the range
::                              Duplicate the range twice
                                  (There are now 3 copies on the stack)
r                               Rotate the stack (put 1 copy of the range to the bottom)
3%                              Apply modulo 3 to each number in the range
                                  Creates a mask where 0 = divisible by 3, 1 = not
f                               Invert the mask (1 = divisible by 3, 0 = not)
c                               Swap the mask for another copy of the range
5%f                             Create a mask where 1 = divisible by 5, 0 = not
2*                              Multiply the mask elements by 2 (2 = disible by 5)
+                               Add the two masks
                                  (3 = divisible by 5 and 3, 2 = divisible by 5, 1 = divisible by 3)
i                               Get the fizzbuzz string according to each number in the list
c                               Swap elements to put a copy of the range on top
|                               Swap empty strings for the corresponding integer in the range
"\n"j                           Join on a newline
.                               Output the result
```