from tetrislib import Board
VERSION = "0.1"

def main():
    print("Starting Hazard Game Server " + VERSION +
          ", built by Olof Sjödin and/or members of Qnarch")

    b = Board()
    b.setActiveBlockFromString("S-block")
    for i in range(41):
        b.update()



if __name__ == "__main__":
    main()
