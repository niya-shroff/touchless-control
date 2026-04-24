TIP_IDS = [4, 8, 12, 16, 20]

def get_fingers(lm):
    fingers = []

    # thumb
    fingers.append(1 if lm[TIP_IDS[0]].x > lm[TIP_IDS[0]-1].x else 0)

    # other fingers
    for i in range(1, 5):
        fingers.append(1 if lm[TIP_IDS[i]].y < lm[TIP_IDS[i]-2].y else 0)

    return fingers


def is_pinch(lm):
    return abs(lm[8].x - lm[4].x) < 0.03 and abs(lm[8].y - lm[4].y) < 0.03