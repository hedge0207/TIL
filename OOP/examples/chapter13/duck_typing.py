class Duck:

    def quack(self):
        print("quack!")
    
    def swim(self):
        print("swimming")


class Human:
    
    def quack(self):
        print("quack!")
    
    def swim(self):
        print("swmming")

    def write(self):
        print("writing")


def main(duck):
    duck.quack()
    duck.swim()


if __name__ == "__main__":
    main(Duck())
    main(Human())