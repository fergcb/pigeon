## (`` * ``) REPEAT (`` a: int ``, `` b: Block ``) -> `void`
The block `b` is executed `a` times:

## (`` * ``) PAD (`` a: str ``, `` b: int ``) -> `` str ``:
`a` is repeated `b` times.

## (`` * ``) REPEAT (`` a: list ``, `` b: int ``) -> `` list ``:
`a` is repeated `b` times.

## (`` * ``) MULTIPLY_ITEMS (`` a: list ``, `` b: list ``) -> `` list ``:
The element-wise products of `a` and `b` are pushed.

## (`` * ``) MULTIPLY (`` a: int/float ``, `` b: int/float ``) -> `` int/float ``:
`a`×`b` is pushed.

## (`` v ``) SCOPE (`` a: int ``, `` b: Block ``) -> `void`
The block `b` is executed on a fresh stack with `a` arguments, and the results are pushed:

## (`` ? ``) IF (`` a: any ``, `` b: Block ``) -> `void`
The block `b` is executed if `a` is truthy:

## (`` / ``) REDUCE (`` a: list ``, `` b: Block ``) -> `void`
The block `b` is executed on each element of `a` and the previous result. The final result is pushed:

## (`` / ``) SPLIT (`` a: list ``, `` b: any ``) -> `` list ``:
`a` is split into chunks delimited by `b`.

## (`` / ``) SPLIT (`` a: str ``, `` b: any ``) -> `` list ``:
`a` is split into chunks delimited by `b`.

## (`` / ``) DIVIDE_ITEMS (`` a: list ``, `` b: list ``) -> `` list ``:
The element-wise quotients of `a` and `b` are pushed.

## (`` / ``) DIVIDE (`` a: int/float ``, `` b: int/float ``) -> `` int/float ``:
`a`÷`b` is pushed.

## (`` \ ``) SCAN (`` a: list ``, `` b: Block ``) -> `void`
The block `b` is executed one each element of `a` and the previous result. The results list is pushed:

## (`` w ``) WHILE (`` a: Block ``) -> `void`
The block `a` is executed while the element on the top of the stack is truthy:

## (`` m ``) MAP (`` a: list ``, `` b: Block ``) -> `void`
The block `b` is mapped over the elements of `a`:

## (`` = ``) LESS_THAN (`` a: any ``, `` b: any ``) -> `` int ``:
1 is pushed if `a` == `b`, else 0 is pushed.

## (`` < ``) LESS_THAN (`` a: int/float ``, `` b: int/float ``) -> `` int ``:
1 is pushed if `a` < `b`, else 0 is pushed.

## (`` < ``) LESS_THAN (`` a: list ``, `` b: list ``) -> `` int ``:
1 is pushed if `a` is shorter than `b`, else 0 is pushed.

## (`` > ``) LESS_THAN (`` a: int/float ``, `` b: int/float ``) -> `` int ``:
1 is pushed if `a` > `b`, else 0 is pushed.

## (`` > ``) LESS_THAN (`` a: list ``, `` b: list ``) -> `` int ``:
1 is pushed if `a` is longer than `b`, else 0 is pushed.

## (`` [ ``) MIN (`` a: list ``) -> `` any ``:
The smallest element of `a` is pushed.

## (`` [ ``) MIN (`` a: list ``, `` b: int ``) -> `` any ``:
The smallest `b` elements of `b` are pushed.

## (`` ] ``) MIN (`` a: list ``) -> `` any ``:
The greatest element of %b is pushed.

## (`` ] ``) MIN (`` a: list ``, `` b: int ``) -> `` any ``:
The greatest `b` elements of `b` are pushed.

## (`` + ``) CONCAT (`` a: str ``, `` b: any ``) -> `` str ``:
`a` and `b` are appended as strings.

## (`` + ``) CONCAT (`` a: any ``, `` b: str ``) -> `` str ``:
`a` and `b` are appended as strings.

## (`` + ``) SUM_ITEMS (`` a: list ``, `` b: list ``) -> `void`
The element-wise sums of `a` and `b` are pushed.

## (`` + ``) ADD (`` a: int/float ``, `` b: int/float ``) -> `` int/float ``:
`a`+`b` is pushed.

## (`` - ``) REMOVE (`` a: str ``, `` b: str ``) -> `` str ``:
`b` is removed from `a`.

## (`` - ``) SUBTRACT_ITEMS (`` a: list ``, `` b: list ``) -> `` list ``:
The element-wise differences of `a` and `b` are pushed.

## (`` - ``) SUBTRACT (`` a: int/float ``, `` b: int/float ``) -> `` int/float ``:
`a`-`b` is pushed.

## (`` j ``) JOIN (`` a: list ``, `` b: str ``) -> `` str ``:
The elements of `a` are joined on `b`.

## (`` o ``) ORDINAL (`` a: str ``) -> `` int/list ``:
`a` is decoded into ascii code point(s).

## (`` F ``) FIELDS (`` a: str ``) -> `` list ``:
`a` is split on whitespace.

## (`` p ``) PAD (`` a: str ``, `` b: int ``) -> `` str ``:
`a` is padded on both sides with spaces to be `b` chars long.

## (`` `l ``) TO_LIST (`` a: str ``) -> `` list ``:
`a` is cast to a list.

## (`` `s ``) TO_STRING (`` a: any ``) -> `` str ``:
`a` is cast to a string.

## (`` `n ``) TO_INT (`` a: str ``) -> `` int ``:
`a` is cast to an integer.

## (`` `n ``) TO_INT (`` a: int/float ``) -> `` int ``:
`a` is cast to an integer.

## (`` `f ``) TO_FLOAT (`` a: str ``) -> `` float ``:
`a` is cast to a float.

## (`` `f ``) TO_FLOAT (`` a: int/float ``) -> `` float ``:
`a` is cast to a float.

## (`` ^ ``) RANGE (`` a: int ``) -> `` list ``:
A list of integers from 0 to `a` is pushed.

## (`` u ``) UNWRAP (`` a: list ``) -> `` tuple ``:
Each item of `a` is pushed.

## (`` _ ``) FLATTEN (`` a: list ``) -> `` list ``:
A list of each scalar nested in `a` is pushed.

## (`` e ``) ENLIST (`` a: int ``) -> `` list ``:
A list of `a` items popped from the stack is pushed.

## (`` i ``) INDEX (`` a: list ``, `` b: int ``) -> `` any ``:
The `b`th item of `a` is pushed.

## (`` i ``) INDEX (`` a: list ``, `` b: list ``) -> `` list ``:
A list of elements from `a` corresponding to indexes in `b` is pushed.

## (`` @ ``) INDEX_OF (`` a: list ``, `` b: list ``) -> `` any ``:
The index of each item of `b` in `a` is pushed.

## (`` @ ``) INDEX_OF (`` a: list ``, `` b: any ``) -> `` any ``:
The index of `b` in `a` is pushed.

## (`` @ ``) INDEX_OF (`` a: str ``, `` b: any ``) -> `` any ``:
The index of the substring `b` in `a` is pushed.

## (`` P ``) PARTITION (`` a: list/str ``, `` b: int/float ``) -> `` list ``:
`a` is split into `b`-item chunks.

## (`` U ``) UNION (`` a: list/str ``, `` b: list/str ``) -> `` list ``:
The union of `a` and `b` is pushed.

## (`` N ``) UNION (`` a: list/str ``, `` b: list/str ``) -> `` list ``:
The difference of `a` and `b` is pushed.

## (`` N ``) DIFFERENCE (`` a: list ``, `` b: any ``) -> `` list ``:
All instances of `b` are removed from `a`.

## (`` l ``) LENGTH (`` a: list/str ``) -> `` int ``:
The length of `a` is pushed.

## (`` d ``) DEDUPLICATE (`` a: list ``) -> `` list ``:
A list of the unique items in `a` are pushed.

## (`` z ``) ZIP (`` a: list/str ``, `` b: list/str ``) -> `` list ``:
`a` is zipped with `b`.

## (`` S ``) SUM (`` a: list ``) -> `` any ``:
The sum of all elements of `a` is pushed.

## (`` C ``) COMBINATIONS (`` a: list/str ``, `` b: int ``) -> `` list ``:
The length-`b` combinations of `a` are pushed.

## (`` b ``) BITS -> `` list ``:
The list [0, 1] is pushed.

## (`` E ``) EMPTY_STRING -> `` str ``:
The empty string is pushed.

## (`` n ``) NEWLINE -> `` str ``:
The newline character, "
", is pushed.

## (`` s ``) SPACE -> `` str ``:
A space, " ", is pushed.

## (`` A ``) ALPHANUMERIC -> `` str ``:
The string of alphanumeric ascii characters is pushed.

## (`` : ``) DUPLICATE (`` a: any ``) -> `` tuple ``:
A copy of the value `a` is pushed.

## (`` `: ``) DUP_TWO (`` a: any ``, `` b: any ``) -> `` tuple ``:
A copy each of the value `a` and the value `b` are pushed.

## (`` c ``) CYCLE (`` a: any ``, `` b: any ``) -> `` tuple ``:
The value `a` and the value `b` are swapped.

## (`` r ``) ROTATE (`` a: any ``) -> `void`
The value `a` is moved to the bottom of the stack.

## (`` # ``) VOID (`` a: any ``) -> `void`
The value `a` is discarded.

## (`` . ``) PRINT (`` a: any ``) -> `void`
The value `a` is printed to the console.

## (`` `d ``) DUMP -> `void`
The contents of the stack is printed.

## (`` , ``) INPUT -> `void`
An input value is pushed.

## (`` ; ``) INPUT -> `void`
An integer input is pushed.

## (`` % ``) MODULO_ITEMS (`` a: list ``, `` b: list ``) -> `` list ``:
The element-wise modulus of `a` and `b` are pushed.

## (`` % ``) MODULO (`` a: int/float ``, `` b: int/float ``) -> `` int/float ``:
`a`%`b` is pushed.

## (`` & ``) AND_ITEMS (`` a: list ``, `` b: list ``) -> `` list ``:
The element-wise ANDs of `a` and `b` are pushed.

## (`` & ``) AND (`` a: any ``, `` b: any ``) -> `` any ``:
The short-circuiting AND of `a` and `b` is pushed.

## (`` | ``) OR_ITEMS (`` a: list ``, `` b: list ``) -> `` list ``:
The element-wise ORs of `a` and `b` are pushed.

## (`` | ``) OR (`` a: any ``, `` b: any ``) -> `` any ``:
The short-circuiting OR of `a` and `b` is pushed.

## (`` t ``) TRUTHY (`` a: any ``) -> `` int ``:
1 is pushed if the value `a` is truthy, else 0 is pushed.

## (`` f ``) FALSY (`` a: any ``) -> `` int ``:
1 is pushed if the value `a` is falsy, else 0 is pushed.

