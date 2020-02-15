# curve-index

The purpose of this function is to get coordinate positions of a point on a space filling curve, given the orthant sequence. Translating from alpha space to numeric space


The orthants are labelled a, b, c, etc... from left -> right, top -> bottom to standardize the convention. 

Example:
A Hilbert curve at order 0 starts on a 2x2 grid

The quadrants would be labelled:
```
A B
C D
```

At order 1, the quadrants would expand to the label:
```
Aa Ab  Ba Bb
Ac Ad  Bc Bd

Ca Cd  Da Db
Cc Cd  Dc Dd
```

What are the coordinates of point 'BC'? At a cursory glance, one could tell it's at [1,2] (column/row count starts at 0). Now, what if I give you the point ACBDADCBA? With increasing depth, you're going to want an algorithm to compute this coordinate

This code is separated into three functions of increasing generality.

## WHY DID I DO THIS? 
Used this nifty little algorithm to map the location of a point on a hilbert curve onto an update matrix as part of the 2019 McGill Physics hackathon, and I wanted to keep playing around / generalize it
https://devpost.com/software/bounded-chaos

## hilbert_index(seq)
input: sequence ex. DCAB

output: [x,y] coordinate value of the point

This function hard codes the various transformations that the quadrants a,b,c,d would undergo at increasing depth, and only works for a curve starting at dimensions 2x2 

Let's take the sequence DD, for example. Enumerating through the sequence, I start in quadrant D. Let's say I 'fill' that quadrant with a '1', and the other 'empty' quadrants contain the value '0'. My graph would look something like this:

```
0 0
0 1
```

Moving into the second depth of the sequence, I remain in quadrant D, but each original quadrant now splits into four subsequent quadrants, each labelled A -> D. I now want to put a 1 in sub-quadrant D in the larger quadrant D. It would look like this:

```
0 0  0 0
0 0  0 0 

0 0  0 0
0 0  0 1
```

Recursively 'moving' deeper into sub-quadrants follows a pretty basic pattern. 
The [x,y] coordinates of the point in quadrant D at order 0 (dimensions 2x2) is [1,1]

The [x,y] coordinates of the point in quadrant A at order 0 (dimensions 2x2) is [0,0]
B: [0,1]
C: [1,0]
D: [1,1]

As I increase the depth of the curve (i.e. increase the dimensions of the grid), the way the coordinates change as I move into subsequent quadrants corresponds to the dimension of the grid at the previous depth (how much the grid 'grew' by) with relation to the initial coordinate position.

Following the example of the point DD:
```
Dictionary:
A: [0,0]
B: [0,1]
C: [1,0]
D: [1,1]

D:
dim = 2 (dimensions of the grid at order 0 are 2x2)
order = order of the curve
	  = 0
n = (dim ^ order) (dimension of grid at prev order, which at this level would be a point [0,0])
  = 2^0
  = 1
x coordinate = (previous x coordinate value) + (n * x coordinate value for D from dictionary)
			= 0 + (1 * 1)
			= 1
y coordinate = same thing as above but for y coord of D
coordinate value for D = [1,1]
# this seems pretty banal, but it's the starting point from which all else grows

DD:
dim = 2 
order = 1
n = 2^1
  = 2
x coordinate = (prev. x coord val) + (n * x coord val for D from dictionary)
			 = 1 + (2 * 1)
			 = 3
y coord: same as above but for y coord
coordinate value for DD = [3,3]

```

## curve_index(dimRow, colRow, seq)

Generalized the function to output [x,y] coordinates for a space filling curve on an m * n grid, instead of 2x2. Unfortunately I haven't standardized the labelling to accept any arbitrary number of labels, as I'm constrained to the alphabet (upper + lower case). At most, my n * m curve as it is in this iteration can accept 54 initial states/orthants (27 upper case + 27 lower case letters). I'm not super worried about this because usually the initial stage is pretty simple, not an arbitrarily large grid. I mean, it could be. But it isn't. 

Anyway, in order to calculate the index, I have to narrow the range that the point could be in as I iterate through the input sequence. For example, a 2x3 grid would look like this at order 0:

```
A B C
D E F
```
And like this at order 1:

```
Aa Ab Ac  Ba Bb Bc  Ca Cb Cc
Ad Ae Af  Bd Be Bf  Cd Ce Cf

Da Db Dc  Ea Eb Ec  Fa Fb Fc
Dd De Df  Ed Ee Ef  Fd Fe Ff

```

The rows and columns grow at different rates because of the different dimensions, which is why I have the row dimensions and column dimensions as separate arguments in the function.

A point that is in quadrant A will never be in a row larger than 1/2 of the current row dimension, and will never be in a column larger than 1/3 of the current column dimension. So for a 2x3 grid of order 1, any point starting with the letter A will have to be in either row 0 or 1, and in column 0, 1, or 2. Using this method, I can start narrowing down the range where the point can actually reside.


## curve_index2(seq, dims)
Further generalized to allow for an arbitrary number of dimensions, not just 2 (x,y)

The argument dims accepts a list of values 

ex. dims = [2,2,2] represents a curve that initializes in a 2x2x2 cube 

I also further generalized and condensed the code so I'm not repeating the same thing for each coordinate as in the previous function.

Finally, I further condensed the algorithm used to narrow the range of values in which I search 

A more thorough explanation of how the code actually works:

curve_index2 takes two agruments: a sequence (ex. DCAB) that indicates a point on a space filling curve, and the dimensions of the curve at order 0. So far, this function will only work up to the dimensions of 4x4x3 because I haven't figured out a labelling system larger than the lower case + upper case alphabets. It wasn't a priority to focus on this because the initial curve is often very simple anyway (take the hilbert curve, for example. It starts on with 2x2 dimensions)

The number of possible states are given by the dimensions provided. Let's use the Hilbert curve as an example again. I have 2*2 = 4 initial possible states 

The transformation matrix basically indexes the coordinates in the initial grid 

For a 3x2, the coordinates would be: 

```
0,0 | 0,1 
- - - - 
1,0 | 1,1
- - - - 
2,0 | 2,1
```
So my transformation matrix for that 3x2 grid would look something like this:

```
[[0, 0]
[0, 1]
[1, 0]
[1, 1]
[2, 0]
[2, 1]]
```
The user inputs the sequence of the point they're interested in and the dimensions of the initial grid, but the labels are dynamically generated by me. Given the total number of possible states calculated earlier, I create a string of all the labels. In out 3x2 example, there are 6 total labels: a, b, c, d, e, f arranged in the following formate:

```
a | b 
- - - 
c | d
- - - 
e | f
```

Next step is to create a dictionary that pairs the labels with the transform coordinates. For 3x4, it would look like this:
```
{a: [0, 0]
b: [0, 1]
c: [1, 0]
d: [1, 1]
e: [2, 0]
f: [2, 1]}
```

Now we can easily reference that orthant c at order 0 has the coordinates [1, 0]

As we reach the end of the curve index 2 function, the result is calculated one dimension at a time, passed to the calculate index 2 function written above.

As stated earlier, the primary role of this function is to narrow down the range of rows/columns/whatever until you zero in on the row/column/whatever where a particular sequence is located

### calcIndex2

let's continue using the example:
seq = 'facd'
dims = 3 x 2

I know this point is on a grid of size 81 rows x 16 columns. Only one dimension is passed to this function at a time. We'll focus on the 3 rows as an example.

I can calculate that there are 81 rows by taking the original number or rows (3) and raising it to the power of 4 (the sequence given is 4 letters long, meaning the respective curve is of order 3 (started counting at 0). 

order 0 is a 3x2 grid
order 1 is a 9x4 grid
order 2 is a 27x8 grid
order 3 is an 81x16 grid

I'm not going to write out the whole matrix. I should upload a handdrawn diagram, it's easiest to understand. For now, please refer to the following to illustrate a rough idea of how the whole grid is labelled. Somewhere in there is the sequence "facd". We are looking for its respective coordinates.

```
aaaa | aaab | aaba | aabb | abaa | abab | ... | bbaa | bbab | bbba | bbbb
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
aaac | aaad | aabc | ...
- - - - - - - - - - - - -
.
.				.				
.				  .
caaa | caab | ...
- - - - - - - - - - 
.					    ... | facd | ...
.
.							     - - - - - - -
							    | fffe | ffff
							      
```

So. I know I have 81 rows that grew from 3 rows. I create a range that steps from 0 to 81 three times, recording those values. Basically divide 81 into three ranges.

The ranges are: 0-26, 27-53, and 53-80 and can be stored in an array that looks like this:

[0, 27, 54, 81]

Next, for each value in the sequence "facd", I narrow the range where my point could be by eliminating the range where it ~ isn't ~

Back to the dictionary. 

f: [2, 1] 

What this tells us is we can find the row for "f" in the last third of any order grid, and the column in the 2nd half of any order grid. That allows us to eliminate first two thirds from 0 - 81 in our search.

Now we're only looking between the values 54 and 81. Split equally into three again ([54, 63, 72, 81] and refine the search.
Now we've moved onto the 2nd letter: "a"

In the dictionary, a points to the value [0,0]

(remember, this value has information for both row and column, but at the moment I'm only interested in rows)

This tells me orthant 'a' is in the first third of the given range

So now I narrow my search again between 54 to 63.

Repeat until I reach the last letter. 

This function returns the row value '58' for 'facd' with a 3x2 order 0 grid.


In this example, calcIndex2 is called twice; once for row and once for column.

The final result outputs: [58, 9], which is the coordinate value at which 'facd' is located, given a curve that starts on a 3x2 grid (order 0)

## One last algorithm:

So far I've used two kinds of logic to calculate the coordinate values. One method enumerates backwards through a given sequence, situates it on a grid, and calculates the position by adding how much the grid grows by as you increase its order, in relation to rule assigned to the letter label. The 2nd method starts with a range of rows/columns/whatever where the point could be, and eliminates where it's definitely ~ not ~ to narrow in on the final value.

The last idea is as follows:

Using the example seq: 'facd', dims: 3x2, find row: (remember, I start counting at 0)

- In order 3 grid there are 81 rows. The top row of orthant 'f' is row 54
- In order 2 grid there are 27 rows. The top row of orthant 'a' is row 0
- In order 1 grid there are 9 rows. The top row of orthant 'c' is row 3
- In order 0 grid there are 3 rows. The top row of orthant 'd' is row 1

54 + 0 + 3 + 1 = 58

Same same but different.

Probably won't implement this, unless I need to use this function again and I'm optimizing for speed. It may or may not be faster than the previous implememntations. It may or may not matter.

## TODO
- Clean up documentation. I realize this probably wasn't the clearest explanation I could have given. I'm not a mathematician, so it's all very clear in my pencil and paper notebook, but the written notation/terminology eludes me somewhat. This would absolutely be easier to explain/understand step by step in a video. Alas.
- come up with better numbering system for labels
- error checks: ensure input dims are integers, seq is string of valid characters
- make nice interface that can take user input (either CLI or webpage)














