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

Recursively 'moving' deeper into sub-quadrants follows a pretty basic pattern. The [x,y] coordinates of the point in quadrant D at order 0 (dimensions 2x2) is [1,1]

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

Generalized the function to output [x,y] coordinates for a space filling curve on an m * n grid, instead of 2x2. Unfortunately I haven't standardized the labelling to accept any arbitrary number of labels, as I'm constrained to the alphabet (upper + lower case). At most, my n * m curve as it is in this iteration can accept 52 initial states/orthants (27 upper case + 27 lower case letters). I'm not super worried about this because usually the initial stage is pretty simple, not an arbitrarily large grid. I mean, it could be. But it isn't. 

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

## TODO
- Clean up documentation. I realize this probably wasn't the clearest explanation I could have given. I'm not a mathematician, so it's all very clear in my pencil and paper notebook, but the written notation eludes me somewhat. Maybe the best format for me would be a youtube video
- come up with better numbering system for labels
- error checks: ensure input dims are integers, seq is string of valid characters
- make nice interface that can take user input (either CLI or webpage)












