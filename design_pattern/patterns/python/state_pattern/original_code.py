class GumballMachine:
    SOLD_OUT = 0
    NO_QUARTER = 1
    HAS_QUARTER = 2
    SOLD = 3

    def __init__(self, count):
        self.state = self.SOLD_OUT
        # 캡슐의 개수를 저장하기 위한 변수
        self.count = count
        # 캡슐 개수가 0보다 크면 동전이 들어오길 기다리는 상태가 된다.
        if count > 0:
            self.state = self.NO_QUARTER

    def insert_quarter(self):
        if self.state == self.HAS_QUARTER:
            print("이미 동전이 들어가 있습니다.")
        elif self.state == self.NO_QUARTER:
            self.state = self.HAS_QUARTER
            print("동전을 넣으셨습니다.")
        elif self.state == self.SOLD_OUT:
            print("남아 있는 캡슐이 없습니다. 다음에 이용해주세요.")
        elif self.state == self.SOLD:
            print("캡슐을 내보내고 있습니다.")

    def eject_quarter(self):
        if self.state == self.HAS_QUARTER:
            self.state = self.NO_QUARTER
            print("동전이 반환됩니다.")
        elif self.state == self.NO_QUARTER:
            print("반환 할 동전이 없습니다.")
        elif self.state == self.SOLD_OUT:
            print("반환할 동전이 없습니다. 동전이 반환되지 않습니다.")
        elif self.state == self.SOLD:
            print("이미 캡슐을 뽑으셨습니다.")
    
    # 손잡이를 돌리는 메서드
    def turn_crank(self):
        if self.state == self.SOLD:
            print("손잡이는 한 번만 돌려주세요")
        elif self.state == self.NO_QUARTER:
            print("먼저 동전을 넣어주세요")
        elif self.state == self.SOLD_OUT:
            print("매진되었습니다.")
        elif self.state == self.HAS_QUARTER:
            print("손잡이를 돌리셨습니다.")
            self.state = self.SOLD
            self.dispense()

    # 캡슐을 내보내는 메서드
    def dispense(self):
        if self.state == self.SOLD:
            print("캡슐을 내보내고 있습니다.")
            self.count -= 1
            if self.count == 0:
                print("이제 남은 알맹이가 없습니다.")
                self.state = self.SOLD_OUT
            else:
                self.state = self.NO_QUARTER
        # 아래의 세 경우는 오류가 나는 상황이다.
        elif self.state == self.NO_QUARTER:
            print("먼저 동전을 넣어주세요")
        elif self.state == self.SOLD_OUT:
            print("매진되었습니다.")
        elif self.state == self.HAS_QUARTER:
            print("알맹이를 내보낼 수 없습니다.")


