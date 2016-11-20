import random

nums = []

balls = [i for i in range(1,50)]
random.shuffle(balls)
nums = balls[:6]

print("Give it a go! You'll probably lose, I'm not accountable:")
print(nums)
print("Note: if these numbers win you the lottery I AM accountable, give me money or I'll call my lawyers")
