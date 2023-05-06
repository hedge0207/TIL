from quackable import Quackable
from goose import Goose
from goose_adapter import GooseAdapter
from quack_counter import QuackCounter
from duck_factory import CountingDuckFactory
from flock import Flock
from observer import QuackLogist


class Simulator:
    def simulate(self, duck_factory):
        
        red_head_duck: Quackable = duck_factory.create_red_head_duck()
        rubber_duck: Quackable = duck_factory.create_rubber_duck()
        duck_call: Quackable = duck_factory.create_duck_call()
        goose: Quackable = GooseAdapter(Goose())

        flock_of_ducks = Flock()

        flock_of_ducks.add(red_head_duck)        
        flock_of_ducks.add(rubber_duck)        
        flock_of_ducks.add(duck_call)        
        flock_of_ducks.add(goose)        

        flock_of_mallards = Flock()

        mallard_duck_one: Quackable = duck_factory.create_mallard_duck()
        mallard_duck_two: Quackable = duck_factory.create_mallard_duck()
        mallard_duck_three: Quackable = duck_factory.create_mallard_duck()
        mallard_duck_four: Quackable = duck_factory.create_mallard_duck()
        flock_of_mallards.add(mallard_duck_one)
        flock_of_mallards.add(mallard_duck_two)
        flock_of_mallards.add(mallard_duck_three)
        flock_of_mallards.add(mallard_duck_four)
        
        # flock_of_mallards을 flock_of_ducks에 추가한다.
        flock_of_ducks.add(flock_of_mallards)

        quack_logist = QuackLogist()
        flock_of_ducks.register_observer(quack_logist)
        self._simulate(flock_of_ducks)

        print("number of quack: ", QuackCounter.get_quacks())

    # 다형성을 활용하여 어떤 Quackable이 전달되든 quack() 메서드를 호출할 수 있게 한다.
    def _simulate(self, duck: Quackable):
        duck.quack()


if __name__ == "__main__":
    simulator = Simulator()
    duck_factory = CountingDuckFactory()
    simulator.simulate(duck_factory)