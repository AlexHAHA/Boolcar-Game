

chinese_score = [80,81,78,90,67,85,92,78,95,88,99,79,84]
english_score = [85,83,78,93,87,81,92,78,91,78,90,76,84]
program_score = [90,91,88,93,85,85,90,88,95,80,99,89,90]

def score_check(score):
    max_score = 0
    for i in score:
        if max_score < i:
            max_score = i
    return max_score
score_check(chinese_score)
score_check(english_score)
score_check(program_score)