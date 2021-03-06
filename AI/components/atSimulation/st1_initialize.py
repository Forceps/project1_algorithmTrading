from AI.networks.actor_critic_network import ActorCriticNetwork
import datetime
import os
import torch
from stock_API.deashinAPI.db_API import MySQL_command
import random
import torch.optim as optim


class St1_initialize_actorCritic:
    """
    초기 설정 함수들을 모아놓았다.
    실제 초기화는 최말단 상속 클래스인 PyMon에서 한다.
    왜냐하면 클래스 인자를 받기 위해서이다.
    """

    def __init__(self):
        self.mysql = MySQL_command()

    def situationInit(self):
        """인자에 영향받지 않는 클래스 변수들을 설정한다."""
        self.step = 0
        self.new_date = None
        self.new_hour = None

        now = datetime.datetime.now()
        self.today = int(now.strftime("%Y%m%d"))
        self.currentHour = int(now.strftime("%H"))
        self.currentMinute = int(now.strftime("%M"))

        self.inputData = None
        self.simulationInit()
        self.ai_act_kinds_state: int = 0
        self.observer_num = self.target_database_name[-1]
        self.momentMoveStep = 0

    def networkSet(self):
        """신경망 가동을 위한 초기 설정"""
        self.weightsFilePath: str = "networkWeights.pt"
        self.optimizer = None

        self.network = ActorCriticNetwork(input_size=1401, policy_network_outsize=self.the_number_of_choices).to(
            self.device
        )
        if self.network_global == None:
            if os.path.exists(self.weightsFilePath):
                self.network.load_state_dict(torch.load(self.weightsFilePath))
            self.optimizer = optim.SGD(self.network.parameters(), lr=0.00025, momentum=0.9, nesterov=True)
        else:
            self.network.load_state_dict(self.network_global.state_dict())
            self.optimizer = optim.SGD(self.network_global.parameters(), lr=0.00025, momentum=0.9, nesterov=True)

        self.accumulatedLoss = 0
        self.globalNetSaveStep = 60 * 5 * random.randint(4, 5) + random.randint(0, 59)

    def simulationInit(self, startDate: int = 20190502):
        """시뮬레이션 하기 위한 클래스 변수들을 설정한다."""
        self.deposit_dp2: float = 1000000
        self.mySituation = [self.deposit_dp2, startDate, 9, 0]  # [d+2예수금, 날짜, 시, 분]
        self.portfolio = [[-1, 0, 0, 0, 0] for _ in range(20)]  # [종목명, 보유량, 수수료 총합, 현재가, 매입가 평균]
        self.new_date: int = 0
        self.new_hour: int = 8

        self.init_value: float = self.deposit_dp2
        self.baselineValue: float = self.currentAssetValue_in_simulation()
        self.interimBaselineValue = self.baselineValue
        self.per15minuteValue = self.baselineValue
        self.inputData_old = None
        self.pi_selected_action = None

        self.codeListInMarket = [0 for _ in range(200)]
        self.exileCodeStack = [0 for _ in range(200)]
        self.pseudoTime = [random.randint(10000000, 90000000), random.randint(1, 9), random.randint(1, 38)]
        self.pseudoTimeReserved = self.pseudoTime[1:]
