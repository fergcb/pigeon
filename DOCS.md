## (`+`) SUM_ITEMS (`list`, `list`)
The element-wise sums of %a and %b are pushed.

## (`+`) ADD (`int`, `int`)
%a+%b is pushed.

## (`+`) CONCAT (`str`, `any`)
%a and %b are appended as strings.

## (`+`) CONCAT (`any`, `str`)
%a and %b are appended as strings.

## (`-`) SUBTRACT_ITEMS (`list`, `list`)
The element-wise differences of %a and %b are pushed.

## (`-`) SUBTRACT (`int`, `int`)
%a-%b is pushed.

## (`-`) REMOVE (`str`, `str`)
%b is removed from %a.

## (`*`) MULTIPLY_ITEMS (`list`, `list`)
The element-wise products of %a and %b are pushed.

## (`*`) MULTIPLY (`int`, `int`)
%a×%b is pushed.

## (`*`) REPEAT (`int`, `Block`)
The block %b is executed %a times:

## (`/`) DIVIDE_ITEMS (`list`, `list`)
The element-wise quotients of %a and %b are pushed.

## (`/`) DIVIDE (`int`, `int`)
%a÷%b is pushed.

## (`%`) MODULO_ITEMS (`list`, `list`)
The element-wise modulus of %a and %b are pushed.

## (`%`) MODULO (`int`, `int`)
%a%%b is pushed.

## (`&`) AND_ITEMS (`list`, `list`)
The element-wise ANDs of %a and %b are pushed.

## (`&`) AND (`any`, `any`)
The short-circuiting AND of %a and %b is pushed.

## (`|`) OR_ITEMS (`list`, `list`)
The element-wise ORs of %a and %b are pushed.

## (`|`) OR (`any`, `any`)
The short-circuiting OR of %a and %b is pushed.

## (`t`) TRUTHY (`any`)
1 is pushed if the any %a is truthy, else 0 is pushed.

## (`f`) FALSY (`any`)
1 is pushed if the any %a is falsy, else 0 is pushed.

## (`j`) JOIN (`list`, `str`)
The elements of %a are joined on %b.

## (`o`) ORDINAL (`str`)
%a is decoded into ascii code point(s).

## (``l`) TO_LIST (`str`)
%a is cast to a list.

## (``s`) TO_STRING (`any`)
%a is cast to a string.

## (``n`) TO_INT (`str`)
%a is cast to an integer.

## (``n`) TO_INT (`float`)
%a is cast to an integer.

## (``f`) TO_FLOAT (`str`)
%a is cast to a float.

## (``f`) TO_FLOAT (`int`)
%a is cast to a float.

## (`^`) RANGE (`int`)
A list of integers from 0 to %a is pushed.

## (`u`) UNWRAP (`list`)
Each item of %a is pushed.

## (`e`) ENLIST (`int`)
A list of %a items popped from the stack is pushed.

## (`i`) INDEX (`list`, `int`)
The %bth item of %a is pushed.

## (`i`) INDEX (`list`, `list`)
A list of elements from %a corresponding to indexes in %b is pushed.

## (`p`) PARTITION (`list`, `int`)
%a is split into %b-item chunks.

## (`U`) UNION (`list`, `list`)
The union of %a and %b is pushed.

## (`N`) UNION (`list`, `list`)
The difference of %a and %b is pushed.

## (`N`) DIFFERENCE (`list`, `any`)
All instances of %b are removed from %a.

## (`b`) BITS
The list [0, 1] is pushed.

## (`:`) DUPLICATE (`any`)
A copy of the any %a is pushed.

## (``:`) DUP_TWO (`any`, `any`)
A copy each of the any %a and the any %b are pushed.

## (`c`) CYCLE (`any`, `any`)
The any %a and the any %b are swapped.

## (`r`) ROTATE (`any`)
The any %a is moved to the bottom of the stack.

## (`#`) VOID (`any`)
The any %a is discarded.

## (`.`) PRINT (`any`)
The any %a is printed to the console.

## (``d`) DUMP
The contents of the stack is printed.

## (`,`) INPUT
An input value is pushed.

## (`;`) INPUT
An integer input is pushed.

## (`v`) SCOPE (`int`, `Block`)
The block %b is executed on a fresh stack with %a arguments, and the results are pushed:

