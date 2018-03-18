from tetrislib import Board, Movement, SetShape
VERSION = "0.1"

def test():
    print("NOTE: Starting test scenario (this will NOT be in the final version)")
    input()

    queue = [SetShape("S-shape"),
             Movement("hard_drop"),
             Movement("right", 2),
             Movement("hard_drop"),
             Movement("right",4),
             Movement("hard_drop"),
             Movement("right", 6),
             Movement("hard_drop"),
             Movement("right", 8),
             Movement("hard_drop"),
             SetShape("T-shape"),
             Movement("rotate", 2),
             Movement("hard_drop"),
             SetShape("T-shape"),
             Movement("rotate"),
             Movement("hard_drop"),
             SetShape("T-shape"),
             Movement("right", 2),
             Movement("rotate", 3),
             Movement("hard_drop"),
             SetShape("I-shape"),
             Movement("rotate"),
             Movement("right", 10),
             Movement("hard_drop"),
             SetShape("Z-shape"),
             Movement("rotate"),
             Movement("right",5),
             Movement("hard_drop"),
             SetShape("RevL-shape"),
             Movement("rotate", 2),
             Movement("right", 4),
             Movement("hard_drop"),
             SetShape("L-shape")]

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
