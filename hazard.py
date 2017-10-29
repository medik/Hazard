from tetrislib import Board, Movement
VERSION = "0.1"

def main():
    print("Starting Hazard Game Server " + VERSION +
          ", built by Olof Sjödin and/or members of Qnarch")

    print("NOTE: Starting test scenario (this will NOT be in the final version)")
    input()

    queue = []

    queue.append(Movement("hard_drop"))
    queue.append(Movement("right"))
    queue.append(Movement("right"))

    b = Board()
    b.setActiveBlockFromString("S-block")

    for item in queue:
        b.applyAction(item)
        b.update()



if __name__ == "__main__":
    main()
