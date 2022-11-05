
## `+`
**Vectorizable?** Yes
### Signatures:
- **`list`, `list`**: The element-wise sum of %a and %b is pushed.
- **`int`, `int`**: %a + %b = %res is pushed.
- **`str`, `any`**: %a and %b are appended as strings.
- **`any`, `str`**: %a and %b are appended as strings.

## `*`
**Vectorizable?** Yes
### Signatures:
- **`int`, `int`**: %a × %b = %res is pushed.

## `-`
**Vectorizable?** Yes
### Signatures:
- **`list`, `list`**: The difference of %a and %b is pushed.
- **`list`, `any`**: %b is removed from %a.
- **`str`, `str`**: %b is removed from %a.
- **`int`, `int`**: %a - %b = %res is pushed.

## `/`
**Vectorizable?** Yes
### Signatures:
- **`int`, `int`**: %a ÷ %b = %res is pushed.

## `%`
**Vectorizable?** Yes
### Signatures:
- **`int`, `int`**: %a MOD %b = %res is pushed.

## `&`
**Vectorizable?** Yes
### Signatures:
- **`list`, `list`**: The element-wise AND of %a and %b is pushed.
- **`any`, `any`**: The short-circuiting AND of %a and %b is pushed.

## `|`
**Vectorizable?** Yes
### Signatures:
- **`list`, `list`**: The element-wise OR of %a and %b is pushed.
- **`any`, `any`**: The short-circuiting OR of %a and %b is pushed.

## `j`
**Vectorizable?** Yes
### Signatures:
- **`list`, `str`**: The elements of %a are joined on %b.

## ``l`
**Vectorizable?** Yes
### Signatures:
- **`str`**: %a is cast to a list.

## ``s`
**Vectorizable?** Yes
### Signatures:
- **`any`**: %a is cast to a string.

## ``n`
**Vectorizable?** Yes
### Signatures:
- **`str`**: %a is cast to an integer.

## ``f`
**Vectorizable?** Yes
### Signatures:
- **`str`**: %a is cast to a float, and pushed.
- **`int`**: %a is cast to a float, and pushed.

## `^`
**Vectorizable?** Yes
### Signatures:
- **`int`**: A list of integers from 0 to %a is pushed.

## `u`
**Vectorizable?** Yes
### Signatures:
- **`list`**: Each item of %a is pushed.

## `e`
**Vectorizable?** Yes
### Signatures:
- **`int`**: A list of %a items popped from the stack is pushed.

## `i`
**Vectorizable?** Yes
### Signatures:
- **`list`, `int`**: The %bth item of %a is pushed.
- **`list`, `list`**: A list of elements from %a corresponding to indexes in %b is pushed.

## `p`
**Vectorizable?** Yes
### Signatures:
- **`list`, `int`**: %a is split into %b-item chunks.

## `b`
**Vectorizable?** Yes
### Signatures:
- **None**: The list [0, 1] is pushed.

## `t`
**Vectorizable?** Yes
### Signatures:
- **`any`**: 1 is pushed if the value %a is truthy, else 0 is pushed.

## `f`
**Vectorizable?** Yes
### Signatures:
- **`any`**: 1 is pushed if the value %a is falsy, else 0 is pushed.

## `:`
**Vectorizable?** No
### Signatures:
- **`any`**: A copy of the value %a is pushed.

## ``:`
**Vectorizable?** No
### Signatures:
- **`any`, `any`**: A copy each of the value %a and the value %b are pushed.

## `c`
**Vectorizable?** No
### Signatures:
- **`any`, `any`**: The value %a and the value %b are swapped.

## `r`
**Vectorizable?** No
### Signatures:
- **`any`**: The value %a is moved to the bottom of the stack

## `.`
**Vectorizable?** No
### Signatures:
- **`any`**: The value %a is printed to the console.

## `,`
**Vectorizable?** Yes
### Signatures:
- **None**: The input %ret %res is pushed.

## `;`
**Vectorizable?** Yes
### Signatures:
- **None**: The input int %res is pushed.

## ``d`
**Vectorizable?** Yes
### Signatures:
- **None**: The contents of the stack is printed.
