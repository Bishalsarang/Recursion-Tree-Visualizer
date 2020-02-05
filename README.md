# Recursion Visualiser
Recursion visualiser is a python tool that draws recursion tree for recursive function with very less code changes.

## Example
### 1.  Fibonacci
Let's draw the recursion tree for fibonacci number.
Here is how the simple code looks like
```python
def fib(n):
	if n <= 1:
		return n
	return fib(n - 1) + fib(n - 2)
	
print(fib(6))
```

Now we want to draw the recursion tree for this function. It is as simple as adding a decorator
```python
# Author: Bishal Sarang

# Import Visualiser class from module visualiser
from visualiser import Visualiser as vs

# Add decorator
# Decorator accepts arguments: ignore_args and show_argument_name
@vs(ignore_args=['node_num'])
def fib(n, node_num):
    if n <= 1:
        return n
    
    # Increment decorator class node_count before each function calls
    vs.node_count += 1
    left = fib(n=n - 1, node_num=vs.node_count)
	
	# node_count is incremented
    vs.node_count += 1
    right = fib(n=n - 2, node_num=vs.node_count)
    return left + right

# Call function
print(fib(n=6, node_num=0))

# Save recursion tree to a file
vs.write_image("fibonacci.png")
```
Here are the changes required:

 - Change function signature from `fib(n)` to `fib(n, node_num)`
 - Add decorator Visualiser which accepts arguments `ignore_args` and `show_argument_name`
 - Before each function calls make sure to increment `node_count` argument of decorator class 
 - Change every function calls to pass as keyword arguments.
 - Write the image

Here is how the recursion tree looks like:
![enter image description here](https://github.com/sarangbishal/Recursion-Visualizer/blob/master/examples/fibonacci.png)

## 2. Make sum
This is taken from one of my answers on quora where I had to manually  draw recursion tree. Using Visualiser with very less changes I was able to draw the following tree.
![enter image description here](https://github.com/sarangbishal/Recursion-Visualizer/blob/master/examples/make_sum.png)


## Installation
The only dependency for recursin visualiser is Graphviz which you can download from [here](https://www.graphviz.org/download/)



-   Download  [graphviz binary](https://www.graphviz.org/download/)
-   Add graphviz bin to path manually or by adding the following line on your script. Change the installation directory according to your installation path

```
# Set it to bin folder of graphviz
os.environ["PATH"] += os.pathsep +  'C:/Program Files (x86)/Graphviz2.38/bin/'
```
-   Install all the requirements

```
pip install -r requirements.txt
```

See the examples inside `example` toknow how to use


## TODO:
	
 - [x] Minimal working version
 - [ ] Refactor
 - [ ] Handle base cases
 - [ ] Make more beautful trees

