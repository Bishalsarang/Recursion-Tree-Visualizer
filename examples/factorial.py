from visualiser.visualiser import Visualiser as vs


# Add decorator
# Decorator accepts optional arguments: ignore_args , show_argument_name, show_return_value and node_properties_kwargs
@vs()
def fact(n):
    if n <= 1:
        return n
    return n * fact(n=n - 1)


def main():
    # Call function
    print(fact(n=6))
    # Save recursion tree to a file
    vs.make_animation("factorial.gif", delay=2)


if __name__ == "__main__":
    main()
