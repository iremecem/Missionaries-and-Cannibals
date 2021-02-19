"""
Given problem is all 12 passengers need to cross the river. From these 12 passengers 6 of them are missionaries
and remaining 6 are cannibals. If any given time, missionaries are outnumbered by cannibals, missionary’s life 
will be in danger. The boat can carry 5 people maximum at once. Hence, to carry all passengers across without 
any casualties and without exceeding 7 crossings, our purpose is to show how the limited movement should be used.
"""

import random
import copy

# Set DEBUG to True if you want to see the steps to
DEBUG = False

class State:
    '''
    Saves the number of missionaries and cannibals according to current state, for each side and where the boat is located.
    '''

    def __init__(self, numCannibalsOnWest: int, numMissionariesOnWest: int, botPosition: str, numCannibalsOnEast: int, numMissionariesOnEast: int) -> None:
        """
         Constructor of State class.

         INPUTS:
            numCannibalsOnWest: int -> Number of cannibals on the west side of the river
            numCannibalsOnEast: int -> Number of cannibals on the west side of the river
            numMissionariesOnWest: int -> Number of cannibals on the west side of the river
            numMissionariesOnEast: int -> Number of cannibals on the west side of the river
            botPosition: int -> The parameter that indicates which side of the boat is
         OUTPUTS:
            SELF OBJECT (<type State>)
         """

        # Where the boat is currently at {0: West, 1: East}
        self.boatSide = botPosition

        # Cannibal count on the West side
        self.cannibalsOnWest = numCannibalsOnWest

        # Cannibal count on the East side
        self.cannibalsOnEast = numCannibalsOnEast

        # Missionary count on the West side
        self.missionariesOnWest = numMissionariesOnWest

        # Missionary count on the East side
        self.missionariesOnEast = numMissionariesOnEast

    def __eq__(self, s):
        """
        Private method to override 'equals' method of the State class.

        Checks if the given parameter S is a state or not. For both objects, it collates the given position of boats
        to see their location and, compares number of cannibals to missionaries on a side in order see if they are
        equal. If sides of the boats in given states are equal and a side contains equal number of missionaries and cannibals in both states, then given states are equal.

        For example there could be 5 cannibals on the west side of the each states with equal number of missionaries. However, if the boat is in the different sides of the river, then these states are not equal.

        INPUTS:
          s: State -> State object to compare with.
        OUTPUTS:
          TRUE IF BOTH STATES ARE EQUAL IN THE MANNER OF BOAT SIDE AND PEOPLE COUNT ELSE FALSE
        """

        return isinstance(s, State) and (self.boatSide == s.boatSide) and (
            self.cannibalsOnWest == s.cannibalsOnWest) and (self.missionariesOnWest == s.missionariesOnWest)

    def printCurrentState(self) -> None:
        """
        Method to print current state of the object.
        First prints cannibals then missionaries.

        INPUTS:
          NONE
        OUTPUTS:
          NONE

        EXAMPLE OUTPUT:
        CC      C
        M       MM
        """

        messageLine = ""
        # Looks if cannibals on West greater than 0, adds C for each cannibal on the West side
        if self.cannibalsOnWest > 0:
            messageLine += self.cannibalsOnWest * "C"

        # Looks if cannibals on East greater than 0, adds C for each cannibal on the East side
        if self.cannibalsOnEast > 0:
            messageLine += "\t\t" + self.cannibalsOnEast * "C"

        # Looks if missionaries on West greater than 0, adds M for each missionary on the West side in a new line
        if self.missionariesOnWest >= 0:
            messageLine += "\n" + self.missionariesOnWest * "M"

        # Looks if missionaries on East greater than 0, adds M for each missionary on the East side
        if self.missionariesOnEast > 0:
            messageLine += "\t\t" + self.missionariesOnEast * "M"

        print(messageLine + "\n")

    def isStateSafe(self) -> bool:
        """
        Method to check if the current state of the boat is safe.

        Since cannibals outnumbering missionaries on either side endangers the life of missionaries,
        number of cannibals should not reach the number of missionaries for their safety. Function checks
        that constraint is achieved for the given case.

        INPUTS:
          NONE
        OUTPUTS:
          TRUE IF COUNT OF ANY SIDE OF CANNIBALS ARE LESS THAN OR EQUAL TO MISSIONARIES ELSE FALSE

        """

        if self.missionariesOnEast > 0:
            if self.cannibalsOnEast != 0 and self.cannibalsOnEast > self.missionariesOnEast:
                return False
        if self.missionariesOnWest > 0:
            if self.cannibalsOnWest != 0 and self.cannibalsOnWest > self.missionariesOnWest:
                return False
        # If no missionary in a side, then side is safe
        return True

    def isActionSafe(self, nextState) -> bool:
        """
        Method to check if the current state of the boat crossing is safe

        As cannibal count can not exceed the missionary count, then 
        this condition is also be checked for people on the boat. Function 
        checks that constraint is achieved for the given case.

        INPUTS:
          nextState: State -> State object that holds the information about the boat when crossed
        OUTPUTS:
          TRUE IF COUNT OF CANNIBALS ARE LESS THAN OR EQUAL TO MISSIONARIES ON THE BOAT ELSE FALSE
        """

        # Calculate number of missionaries and cannibals on the boat during crosing
        cannibalCountOnBoat = abs(
            nextState.cannibalsOnWest - self.cannibalsOnEast)
        missionaryCountOnBoat = abs(
            nextState.missionariesOnWest - self.missionariesOnEast)

        # Check if missionaries are endangered
        if missionaryCountOnBoat > 0:
            return missionaryCountOnBoat >= cannibalCountOnBoat
        else:
            return True

    def generateExpansions(self, boatCapacity: int) -> list:
        """

        Method to generate possible crosses of the boat according to the capacity of the boat.
        *****

        INPUTS:
          boatCapacity: int -> NUMBER OF PEOPLE CAN THE BOAT CARRY IN ONE PASS
        OUTPUTS:
          LIST OF POSSIBLE ROUTES TO SOLVE THE PROBLEM.

        """

        expansions = []  # List to hold generated neighbors for the given state

        if self.boatSide == "east":  # if the boat is on the East side
            # For each cannibal n gram
            for i in (range(self.cannibalsOnEast + 1)):
                # Create n grams of missionaries
                for j in (range(self.missionariesOnEast + 1)):
                    # That do not exceed boat capacity
                    if 0 < (i + j) and (i + j) <= boatCapacity:
                        # And create a new state with the generated n grams.
                        expansionToAdd = State(self.cannibalsOnWest + i, self.missionariesOnWest + j,
                                               "west", self.cannibalsOnEast - i, self.missionariesOnEast - j)
                        # If new state is safe and crossing is possible
                        if expansionToAdd.isStateSafe() and self.isActionSafe(expansionToAdd):
                            # Add the neighbor
                            expansions.append(expansionToAdd)
        # Or in the west side
        else:
            # For each cannibal n gram
            for i in (range(self.cannibalsOnWest + 1)):
                # Create n grams of missionaries
                for j in (range(self.missionariesOnWest + 1)):
                    # That do not exceed boat capacity
                    if 0 < (i + j) and (i + j) <= boatCapacity:
                        # And create a new state with the generated n grams.
                        expansionToAdd = State(self.cannibalsOnWest - i, self.missionariesOnWest - j,
                                               "east", self.cannibalsOnEast + i, self.missionariesOnEast + j)
                        # If new state is safe and crossing is possible
                        if expansionToAdd.isStateSafe() and self.isActionSafe(expansionToAdd):
                            # Add the neighbor
                            expansions.append(expansionToAdd)
        # Return generated neighbors
        return expansions

    def getAction(self, prevState, direction: int) -> str:
        """
        Prints the action taken by the boat according to number of passengers and passengers’ type for given state.

        INPUTS:
         prevState: State -> The parameter that holds previous state object.
         direction: int -> The direction that where the boat is headed. {0: East, 1: West}
        OUTPUT:
         THE STRING THAT CONTAINS THE BOAT ACTION IN MANNER OF TYPE OF PASSENGERS AND THEIR COUNTS
        """
        if direction == 1:
            return "SEND " + str(self.cannibalsOnEast - prevState.cannibalsOnEast) + " CANNIBALS " + str(
                self.missionariesOnEast - prevState.missionariesOnEast) + " MISSIONARIES"
        else:
            return "RETURN " + str(self.cannibalsOnWest - prevState.cannibalsOnWest) + " CANNIBALS " + str(
                self.missionariesOnWest - prevState.missionariesOnWest) + " MISSIONARIES"


class Debug:
    """
    Class to print necessary debug messages when needed.
    """

    def __init__(self, isDebug: bool) -> None:
        self.debug = isDebug
        """
        Constructor of the Debug class.

        INPUTS:
            isDebug: bool -> Parameter to enable debug options of the class
        OUTPUTS:
            SELF OBJECT (<type Debug>)
        """
        if isDebug:
            print("Debugger created...")

    def printStartMessage(self, counter: int, state: State) -> None:
        """
        Method to print start message for debug purposes.
        Prints current iteration count and the properties
        of the given state.

        INPUTS:
            counter: int -> Iteration count given through parameters
            state: State -> State object given through parameters
        OUTPUTS:
            NONTE
        """
        if self.debug:
            print("***************************")
            print("ITERATION #", counter - 1)
            print("---CURRENT STATE---")
            state.printCurrentState()

    def printFinishMessage(self, counter: int, pathLength: int) -> None:
        """
        Method to print finish message if the execution finished properly.
        Prints number of iterations to find the solution along with the
        length of the path of the solution.

        INPUTS:
            counter: int -> Iteration count given through the paramters
            pathLength: int -> Length of the solution path given through the parameters
        OUTPUTS
            NONE
        """
        if self.debug:
            print("---FINISHED EXECUTION---")
            print("SOLUTION FOUND IN:", counter - 1, "ITERATIONS")
            print("SOLUTION STEP COUNT: ",
                  pathLength - 1, "STEPS")
            print("***************************\n")

    def printErrorFinishMessage(self, pathLength: int) -> None:
        """
        Method to print a warning message if a possible solution is found
        but the solution is not the best one.

        INPUTS:
            pathLength: int -> The length of the solution that found wrong
        OUTPUTS:
            NONE
        """
        if self.debug:
            print("\n!!!FOUND NON-OPTIMAL SOLUTION, CONTINUE SEARCHING!!!")
            print("REASON: PATH LENGTH IS ",
                  pathLength - 1, "\n")

    def printExpansionsMessage(self, expansions: list) -> None:
        """
        Method to print the possible expansions created from the given State. 
        Henceforth, prints all the neighbors of the given state (if any).

        INPUTS:
            expansions: list -> List of possible expansions of a state.
        OUTPUTS:
            NONE
        """
        if self.debug:
            print("\n---GENERATED NEIGHBORS---")
            if len(expansions) == 0:
                print("No neighbors generated for this state...")
            else:
                for i, neighbor in enumerate(expansions):
                    print("***NEIGHBOR #", i, "***")
                    neighbor.printCurrentState()


class Path:
    """
    Path class holds a list of all possible paths and  adds new states into path.
    """

    def __init__(self, lst: list = []) -> None:
        """
        Constructor of the Path class.

        INPUTS:
            lst: list = [] (default) -> Initial list object to hold generated path from a node
        OUTPUTS:
            SELF OBJECT (<type Path>) 
        """
        self.states = lst

    def contains(self, state: State) -> bool:
        """
        Checks whether the given State has already exists in the path or not

        INPUTS: 
            state:  State -> The state object to be checked for
        OUTPUTS:
            TRUE IF STATE ALREADY EXISTS
            FALSE OTHERWISE
        """
        if state in self.states:
            return True
        return False

    def getTerminalState(self) -> State:
        """
        Gets the terminal state from the path

        INPUTS: 
            NONE
        OUTPUTS:
            LAST ELEMENT OF TYPE STATE IN THE PATH 
        """
        return self.states[-1]

    def add(self, state: State) -> bool:
        """
        Adds new state to the path unless it exists in the path

        INPUTS: 
            state:  State -> The state object to be added to the path
        OUTPUTS:
            TRUE IF NEW STATE IS ADDED SUCCESSFULLY
            FALSE OTHERWISE
        """
        if not self.contains(state):
            self.states.append(state)
            return True
        return False

    def getLength(self) -> int:
        """
        Gets the length of the path

        INPUTS:
            NONE
        OUTPUTS:
            INTEGER THAT REPRESENTS THE LENGTH OF THE LIST
        """
        return len(self.states)

    def getContent(self) -> list:
        """
        Gets the contents of the Path

        INPUTS:
            NONE
        OUTPUT:
            PATH OF STATES IN A LIST FORM
        """
        return self.states

    def printCurrentPath(self) -> None:
        """
        Prints the current path saved in the object

        INPUTS:
            NONE
        OUTPUTS:
            DISPLAYS THE CURRENT PATH IF THE PATH IS NOT EMPTY 
        """

        # If not empty
        if self.getLength() != 0:
            # Print the state of the first element
            self.states[0].printCurrentState()

            # For the rest of the states
            for index in range(1, len(self.states)):
                # Get current and previous states for printing the actions between states
                state = self.states[index]
                prevState = self.states[index - 1]

                # If boat is on the west side of the river
                if index % 2 == 1:
                    print(state.getAction(prevState, 1))
                # If boat is on the east side of the river
                else:
                    print(state.getAction(prevState, 0))

                # Print the contents of the selected state in the interation
                state.printCurrentState()
        # If list is empty
        else:
            print("The path is empty")


def findSafeCrossing(initialState: State, goalState: State, boatCapacity: int, numCrossings: int) -> Path:
    """
    Applies a non-deterministic search algorithm for a given initial state from the parameters and checks if the possible solutions that reaches to a goal state that given 
    from the parameters. 

    The function contains a queue object in order to keep track of the possible paths.
    Until the queue length reaches to zero, in each iteration, the first element, which
    is a Path itself is selected from the queue and will be removed. If the terminal
    state of the selected Path is equal to goal state, then the algorithm has found the
    solution and returns the path found. However, if it is not equal to the goal state,
    then the possible neighbors of the terminal are generated and new paths will be added
    to the queue in random positions. This randomness is the main cause for the non- deterministic search.

    Additionally, while adding the paths that generated with the neighbors of the state
    selected, hence we are adding neighbors to a Path object, the add method of the Path
    object itself looks if there are any instance of the same State has already been inserted
    or not. This is the way that the function prevents looping.

    In order to find a solution with a path length of 7, the algorithm tries to find as
    many solutions as possible and selects the first one that has a length of 7 crossings.
    If any solutions found that more than length 7 and if the DEBUG mode of the script is
    enabled, this function will print the solution, but continues until the desired amount 
    crossings with expected solution is found.

    INPUTS:
        initialState: State -> Initial node parameter given as a start point
        goalState: State -> Final node to be reached for
        boatCapacity: int -> The capacity of the board
        numCrossings: int -> The number of maximum crossings
    OUTPUTS:
        SOLUTION PATH IF FOUND ANY
    """
    pathToReachGoal = Path()

    queue = []
    queue.append(Path([initialState]))
    counter = 0

    debugger = Debug(DEBUG)

    while len(queue) != 0:  # While queue is not empty

        if counter == 10000:
            print("\nNo solution found in 10000 iterations, probably the solution is impossible to reach, exiting....\n")
            exit(1)

        counter += 1  # Increment step for showing iteration count

        # Get the path in the front of the queue and delete it from the queue
        currentPath = queue[0]
        queue.remove(currentPath)

        # Get the state in the last visited part in the current path
        currentState = currentPath.getTerminalState()

        # If debugger is enabled, then print a fancy starting message
        debugger.printStartMessage(counter, currentState)

        # If the goal state reached with the selected terminal
        if currentState == goalState:
            # And if the Path length is numCrossings (numCrossings + 1 INCLUDING STARTING STATE)
            if (currentPath.getLength() == numCrossings + 1):
                # Assign the return value
                pathToReachGoal = currentPath
                # Print a fancy ending message if debugger is enabled
                debugger.printFinishMessage(
                    counter, currentPath.getLength())
                break
            else:
                # Else, found another solution with different length,
                # print a fancy warning message.
                debugger.printErrorFinishMessage(currentPath.getLength())

        # Extend the terminal node
        expansions = currentState.generateExpansions(boatCapacity)

        # Print the expansions of the terminal node
        debugger.printExpansionsMessage(expansions)

        # Create new paths and add them to the random places in the queue
        for expansion in expansions:
            # Deep copy the Path in order to make changes permanent
            pathToAdd = copy.deepcopy(currentPath)
            # If new neighbor to add does not creates a loop
            if pathToAdd.add(expansion):
                # Add the path to a random place in the queue
                randomIndex = random.randint(0, len(queue))
                queue.insert(randomIndex, pathToAdd)

    return pathToReachGoal


# MAIN
if __name__ == "__main__":
    # Get the necessary inputs from the command prompt
    numC = int(input("Please enter number of cannibals: "))
    numM = int(input("Please enter number of missionaries: "))
    boatCapacity = int(input("Please enter the capacity of the boat: "))
    maxNumCross = int(input("Please enter the desired number of crossings to find a solution: "))

    # Initialize debug mode if prompted
    programMode = input(
        "Please press key 'S' for executing the program in single-stepping mode: ")
    DEBUG = (programMode == "S" or programMode == "s")

    # Starting state
    initialState = State(numC, numM, "west", 0, 0)

    # State to reach in the end (For compare purposes)
    goalState = State(0, 0, "east", numC, numM)

    # Generate possible solutions for the problem
    pathToReachGoal = findSafeCrossing(initialState, goalState, boatCapacity, maxNumCross)

    # Print the solution (if found)
    print("\n---SOLUTION MAP---")
    pathToReachGoal.printCurrentPath()
