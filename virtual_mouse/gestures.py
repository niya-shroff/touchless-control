def get_fingers(lm):
    tips = [4, 8, 12, 16, 20]
    fingers = []
    fingers.append(1 if lm[tips[0]].x > lm[tips[0]-1].x else 0)
    for i in range(1, 5):
        fingers.append(1 if lm[tips[i]].y < lm[tips[i]-2].y else 0)
    return fingers

def is_pinch(lm):
    import math
    return math.hypot(lm[8].x - lm[4].x, lm[8].y - lm[4].y) < 0.03