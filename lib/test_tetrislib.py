from tetrislib import Board, Movement, SetBlock
VERSION = "0.1"

def test():
    print("NOTE: Starting test scenario (this will NOT be in the final version)")
    input()

    queue = [SetBlock("S-block"),
             Movement("hard_drop"),
             Movement("right", 2),
             Movement("hard_drop"),
             Movement("right",4),
             Movement("hard_drop"),
             Movement("right", 6),
             Movement("hard_drop"),
             Movement("right", 8),
             Movement("hard_drop"),
             SetBlock("T-block"),
             Movement("rotate", 2),
             Movement("hard_drop"),
             SetBlock("T-block"),
             Movement("rotate"),
             Movement("hard_drop"),
             SetBlock("T-block"),
             Movement("right", 2),
             Movement("rotate", 3),
             Movement("hard_drop"),
             SetBlock("I-block"),
             Movement("rotate"),
             Movement("right", 10),
             Movement("hard_drop"),
             SetBlock("Z-block"),
             Movement("rotate"),
             Movement("right",5),
             Movement("hard_drop"),
             SetBlock("RevL-block"),
             Movement("rotate", 2),
             Movement("right", 4),
             Movement("hard_drop"),
             SetBlock("L-block")]

    b = Board()

    for item in queue:
        b.applyAction(item)
        b.update()


def main():
    print("Starting Hazard Game Server " + VERSION +
          ", built by Olof Sjödin and/or members of Qnarch")
    test()





if __name__ == "__main__":
    main()
