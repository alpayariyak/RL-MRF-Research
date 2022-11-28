import random

from env_utils import *
import numpy as np
from canvas_properties import *
from assets import *
from env_objects import *
from random import random

class MaterialRecoveryFacility:

    def __init__(self, episode_length=180, terminal_score=0, state_output_cells=(x for x in range(3, 32))):
        """
        Material Recovery Facility environment for RL
        :param: episode_length: Length of each episode in seconds.
        :param:terminal_score: Score at which episode should terminate.
        :param: state_output_cells: The cells we want to use on all belts. To calculate which cell an item is in by hand,
        add 250 to X coordinate and divide by 100. Range [0, 32]
        """

        self.episode_length = episode_length
        self.terminal_score = terminal_score
        self.state_output_cells = enumerate_cells(state_output_cells)

        self.to_delete = []
        self.off_screen = {'recyclable': [], 'reject': []}
        self.trash_objects = {}  # Dictionary of current trash objects on belts {trash_object_ID : Trash Object}
        self.total_trash_n = 0
        self.n_unrecyclable_objects = 0
        self.score = 100

        self.action_space_n = len(self.state_output_cells)

        self.terminal_score = 0
        self.terminated = False

        self.agent_fatigue = 0
        self.agent_fatigue_multiplier = 0.001
        self.timeout_multiplier = 0
        self.timeout = 0
        # 3 rows corresponding to 3 belts by 33 columns, each cell containing [n_bad, n_good]
        self.full_grid_state = [[[0, 0] for _ in range(33)] for _ in range(3)]
        # Same as full grid state, but [trash objects] for each cell instead.
        self.full_element_state = [[[] for _ in range(33)] for _ in range(3)]

        self.timestep = 0
        self.stepsize = 0.1  # seconds
        self.create_trash_interval = 0.5 * 1000

        self.belt1, self.belt2, self.belt3 = initialize_belts(self.timestep)
        self.generate_trash()

    def reset(self):
        """
        Resets the game and returns initial state
        :return: state
        """
        self.to_delete = []
        self.trash_objects = {}  # Dictionary of current trash objects on belts {trash_object_ID : Trash Object}
        self.score = 100
        self.timestep = 0
        self.reset_grid()
        self.agent_fatigue = 0
        self.total_trash_n = 0
        self.timeout = 0
        self.generate_trash()
        return self.to_nn_state()

    def step(self, action):
        """
        Material Recovery Facility environment for RL
        :param: action: Length of each episode in seconds.

        :return: state_output_cells: The cells we want to use on all belts. To calculate which cell an item is in by hand,
        add 250 to X coordinate and divide by 100. Range [0, 32]
        """

        while not self.is_time_to_take_a():  # Fast forward timestep(in ms) is of stepsize(in s) * 1000 (conversion to ms)
            self.update_state()

        next_state = self.update_state(action)

        return self.to_nn_state(), reward, self.terminated, self.timestep, self.score


    def is_time_to_take_a(self):
        return self.timestep % (self.stepsize * 1000) != 0


    def update_state(self, action=None):
        """

        :param: action None by default, will run a timestep equal to 1ms in simulator.
        :return: new_state, reward
        """
        self.timeout = min(self.timeout - 1, 0)
        reward = 0

        if self.timestep % self.create_trash_interval == 0:
            self.generate_trash()

        if action:
            self.reset_grid()
            if action != self.action_space_n: # if action is not do nothing
                # self.timeout += timeout
                # self.agent_fatigue += fatigue
                selected_trash = self.get_trash_by_cell(action)

                if not selected_trash or self.missed_by_fatigue(selected_trash):
                    # if there are no trash objects in the selected cell and the agent missed







        self.timestep = + 1

        return self.to_nn_state(), reward

    def get_trash_by_cell(self, action):
        action_y, action_x = self.state_output_cells[action]
        selected_trash = self.full_element_state[action_y][action_x]
        return selected_trash

    def missed_by_fatigue(self, trash_object):
        return random() < self.agent_fatigue * trash_object.miss_probability

    def to_nn_state(self):
        result_state = []
        for cell, [y, x] in self.state_output_cells.items():
            for element in [0, 1]:
                result_state.append(self.full_grid_state[y][x][element])
        result_state.append(self.agent_fatigue)
        return np.array(result_state)

    def generate_trash(self):
        for belt in [self.belt1, self.belt2, self.belt3]:
            self.trash_objects[f'trash_object_{self.total_trash_n}'] = Trash_Object(choice(trash_classes), self, belt)

    def reset_grid(self):
        self.full_grid_state = [[[0, 0] for _ in range(33)] for _ in range(3)]
        self.full_element_state = [[[] for _ in range(33)] for _ in range(3)]

mrf = MaterialRecoveryFacility()
mrf.step(1)
