import random

from utils import user_agents


def get_ua():
    return random.choice(user_agents)
