from collections import deque
from config import (CONSENSUS_WINDOW, MIN_POSITIVE_FRAMES)

buffer = deque(maxlen=CONSENSUS_WINDOW)

def update_decision(has_detection):
    buffer.append(1 if has_detection else 0)
    if len(buffer)>CONSENSUS_WINDOW:
        return False
    return sum(buffer)>=MIN_POSITIVE_FRAMES