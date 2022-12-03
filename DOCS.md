## (`*`) REPEAT (`a: int`, `b: Block`)
The block `b` is executed `a` times:

## (`*`) PAD (`a: str`, `b: int`)
`a` is repeated `b` times.

## (`*`) PAD (`a: list`, `b: int`)
`a` is repeated `b` times.

## (`*`) MULTIPLY_ITEMS (`a: list`, `b: list`)
The element-wise products of `a` and `b` are pushed.

## (`*`) MULTIPLY (`a: int/float`, `b: int/float`)
`a`×`b` is pushed.

## (`v`) SCOPE (`a: int`, `b: Block`)
The block `b` is executed on a fresh stack with `a` arguments, and the results are pushed:

## (`?`) IF (`a: any`, `b: Block`)
The block `b` is executed if `a` is truthy:

## (`/`) REDUCE (`a: list`, `b: Block`)
The block `b` is executed on each element of `a` and the previous result. The final result is pushed:

## (`/`) SPLIT (`a: list`, `b: any`)
`a` is split into chunks delimited by `b`.

## (`/`) SPLIT (`a: str`, `b: any`)
`a` is split into chunks delimited by `b`.

## (`/`) DIVIDE_ITEMS (`a: list`, `b: list`)
The element-wise quotients of `a` and `b` are pushed.

## (`/`) DIVIDE (`a: int/float`, `b: int/float`)
`a`÷`b` is pushed.

## (`\`) SCAN (`a: list`, `b: Block`)
The block `b` is executed one each element of `a` and the previous result. The results list is pushed:

## (`w`) WHILE (`a: Block`)
The block `a` is executed while the element on the top of the stack is truthy:

## (`m`) MAP (`a: list`, `b: Block`)
The block `b` is mapped over the elements of `b`:

## (`=`) LESS_THAN (`a: any`, `b: any`)
1 is pushed if `a` == `b`, else 0 is pushed.

## (`<`) LESS_THAN (`a: int/float`, `b: int/float`)
1 is pushed if `a` < `b`, else 0 is pushed.

## (`<`) LESS_THAN (`a: list`, `b: list`)
1 is pushed if `a` is shorter than `b`, else 0 is pushed.

## (`>`) LESS_THAN (`a: int/float`, `b: int/float`)
1 is pushed if `a` > `b`, else 0 is pushed.

## (`>`) LESS_THAN (`a: list`, `b: list`)
1 is pushed if `a` is longer than `b`, else 0 is pushed.

## (`[`) MIN (`a: list`)
The smallest element of `a` is pushed.

## (`[`) MIN (`a: list`, `b: int`)
The smallest `b` elements of `b` are pushed.

## (`]`) MIN (`a: list`)
The greatest element of %b is pushed.

## (`]`) MIN (`a: list`, `b: int`)
The greatest `b` elements of `b` are pushed.

## (`+`) CONCAT (`a: str`, `b: any`)
`a` and `b` are appended as strings.

## (`+`) CONCAT (`a: any`, `b: str`)
`a` and `b` are appended as strings.

## (`+`) SUM_ITEMS (`a: list`, `b: list`)
The element-wise sums of `a` and `b` are pushed.

## (`+`) ADD (`a: int/float`, `b: int/float`)
`a`+`b` is pushed.

## (`-`) REMOVE (`a: str`, `b: str`)
`b` is removed from `a`.

## (`-`) SUBTRACT_ITEMS (`a: list`, `b: list`)
The element-wise differences of `a` and `b` are pushed.

## (`-`) SUBTRACT (`a: int/float`, `b: int/float`)
`a`-`b` is pushed.

## (`j`) JOIN (`a: list`, `b: str`)
The elements of `a` are joined on `b`.

## (`o`) ORDINAL (`a: str`)
`a` is decoded into ascii code point(s).

## (`F`) FIELDS (`a: str`)
`a` is split on whitespace.

## (`p`) PAD (`a: str`, `b: int`)
`a` is padded on both sides with spaces to be `b` chars long.

## (`p`) PARTITION (`a: list`, `b: int`)
`a` is split into `b`-item chunks.

## (``l`) TO_LIST (`a: str`)
`a` is cast to a list.

## (``s`) TO_STRING (`a: any`)
`a` is cast to a string.

## (``n`) TO_INT (`a: str`)
`a` is cast to an integer.

## (``n`) TO_INT (`a: int/float`)
`a` is cast to an integer.

## (``f`) TO_FLOAT (`a: str`)
`a` is cast to a float.

## (``f`) TO_FLOAT (`a: int/float`)
`a` is cast to a float.

## (`^`) RANGE (`a: int`)
A list of integers from 0 to `a` is pushed.

## (`u`) UNWRAP (`a: list`)
Each item of `a` is pushed.

## (`e`) ENLIST (`a: int`)
A list of `a` items popped from the stack is pushed.

## (`i`) INDEX (`a: list`, `b: int`)
The `b`th item of `a` is pushed.

## (`i`) INDEX (`a: list`, `b: list`)
A list of elements from `a` corresponding to indexes in `b` is pushed.

## (`U`) UNION (`a: list`, `b: list`)
The union of `a` and `b` is pushed.

## (`N`) UNION (`a: list`, `b: list`)
The difference of `a` and `b` is pushed.

## (`N`) DIFFERENCE (`a: list`, `b: any`)
All instances of `b` are removed from `a`.

## (`N`) NEWLINE
The newline character, "
", is pushed.

## (`z`) ZIP (`a: list/str`, `b: list/str`)
`a` is zipped with `b`.

## (`b`) BITS
The list [0, 1] is pushed.

## (`E`) EMPTY_STRING
The empty string is pushed.

## (`:`) DUPLICATE (`a: any`)
A copy of the value `a` is pushed.

## (``:`) DUP_TWO (`a: any`, `b: any`)
A copy each of the value `a` and the value `b` are pushed.

## (`c`) CYCLE (`a: any`, `b: any`)
The value `a` and the value `b` are swapped.

## (`r`) ROTATE (`a: any`)
The value `a` is moved to the bottom of the stack.

## (`#`) VOID (`a: any`)
The value `a` is discarded.

## (`.`) PRINT (`a: any`)
The value `a` is printed to the console.

## (``d`) DUMP
The contents of the stack is printed.

## (`,`) INPUT
An input value is pushed.

## (`;`) INPUT
An integer input is pushed.

## (`%`) MODULO_ITEMS (`a: list`, `b: list`)
The element-wise modulus of `a` and `b` are pushed.

## (`%`) MODULO (`a: int/float`, `b: int/float`)
`a`%`b` is pushed.

## (`&`) AND_ITEMS (`a: list`, `b: list`)
The element-wise ANDs of `a` and `b` are pushed.

## (`&`) AND (`a: any`, `b: any`)
The short-circuiting AND of `a` and `b` is pushed.

## (`|`) OR_ITEMS (`a: list`, `b: list`)
The element-wise ORs of `a` and `b` are pushed.

## (`|`) OR (`a: any`, `b: any`)
The short-circuiting OR of `a` and `b` is pushed.

## (`t`) TRUTHY (`a: any`)
1 is pushed if the value `a` is truthy, else 0 is pushed.

## (`f`) FALSY (`a: any`)
1 is pushed if the value `a` is falsy, else 0 is pushed.

