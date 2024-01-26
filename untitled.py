def print_random_algo_text(choices: Choices) -> None:
    """
    Print random-related text
    """
    print("\n- filling grid with random algorithm")
    if choices.switches:
        print("- optimizing filled grid with switch pairs algorithm")

    if choices.n == 1:
        if choices.breath:
            print("- optimizing filled grid with breath first greedy")
            print(f"- using {choices.m} main {'branch' if choices.m == 1 else 'branches'}")
        elif choices.dijkstra:
            print("- optimizing filled grid with dijkstra")
    else:
        print("- using " + str(choices.n) + " iterations")
        
        if choices.breath:
            print("- optimizing each iteration with breath first greedy")
            print(f"- using {choices.m} main {'branch' if choices.m == 1 else 'branches'}")
        elif choices.dijkstra:
            print("- optimizing each iteration with dijkstra")
        
        print("- finding lowest cost")
        if choices.hist:
            print("- showing histogram plot")

    if len(choices.output) != 0:
        print("- saving output as: '" + choices.output + "'")


def print_greedy_algo_text(choices: Choices) -> None:
    """
    Print greedy-related text
    """
    print("\n- filling grid with greedy algorithm")

    if choices.switches:
        print("- optimizing grid with switch pairs algorithm")
        
    if choices.breath:
        print("- optimizing filled grid with breath first greedy")
        print(f"- using {choices.m} main {'branch' if choices.m == 1 else 'branches'}")
    elif choices.dijkstra:
        print("- optimizing filled grid with dijkstra")
        
    if len(choices.output) != 0:
        print("- saving output as: '" + choices.output + "'")


def print_input_algo_text(choices: Choices) -> None:
    """
    Print input-related text
    """
    print("\n- grid filled with existing output")
    if choices.filename:
        print("- using file: '" + choices.filename.lstrip("-") + "'")
    else:
        print("- using previous run output")

    if choices.switches:
        print("- optimizing grid with switch pairs algorithm")

    if choices.breath:
        print("- optimizing filled grid with breath first greedy")
        print(f"- using {choices.m} main {'branch' if choices.m == 1 else 'branches'}")
    elif choices.dijkstra:
        print("- optimizing filled grid with dijkstra")
        
    if len(choices.output) != 0:
        print("- saving output as: '" + choices.output + "'")


def print_algorithm_text(choices: Choices, algorithm_type: str) -> None:
    """
    Print text related to a specific algorithm type
    """
    # Start with the filling of the grid
    if choices.algorithm not in ["greedy", "random"]:
        print("\n- filling grid with existing output")
        if choices.filename:
            print("- using file: '" + choices.filename.lstrip("-") + "'")
        else:
            print("- using previous run output")
    else:
        print(f"\n- filling grid with " + choices.algorithm + " algorithm")

    # Print specific text for random with iterations
    if choices.n != 1 and choices.algorithm == "random":
        print("- using " + str(choices.n) + " iterations")

        if choices.switches:
            print("- optimizing each iteration with switch pairs algorithm")

        if choices.breath:
            print("- optimizing each iteration with breath first greedy")
            print(f"- using {choices.m} main {'branch' if choices.m == 1 else 'branches'}")
        elif choices.dijkstra:
            print("- optimizing each iteration with dijkstra")
            
        print("- finding lowest cost")
        if choices.hist:
            print("- showing histogram plot")

        if len(choices.output) != 0:
            print("- saving output as: '" + choices.output + "'")

        return 

    # Generic options
    if choices.switches:
        print("- optimizing grid with switch pairs algorithm")

    if choices.breath:
        print("- optimizing filled grid with breath first greedy")
        print(f"- using {choices.m} main {'branch' if choices.m == 1 else 'branches'}")
    elif choices.dijkstra:
        print("- optimizing filled grid with dijkstra")
        
    if len(choices.output) != 0:
        print("- saving output as: '" + choices.output + "'")



