
import math

counter = 0

def minimax(depth, index, isMax, scores, maxDepth):
    global counter

    if depth == maxDepth:
        counter += 1
        return scores[index]

    if isMax:
        left = minimax(depth + 1, index * 2, False, scores, maxDepth)
        right = minimax(depth + 1, index * 2 + 1, False, scores, maxDepth)
        return max(left, right)

    else:
        left = minimax(depth + 1, index * 2, True, scores, maxDepth)
        right = minimax(depth + 1, index * 2 + 1, True, scores, maxDepth)
        return min(left, right)


# Leaf node values
scores = [3, 5, 2, 9, 0, 7]

depth = math.ceil(math.log2(len(scores)))

while len(scores) < 2 ** depth:
    scores.append(0)

# Run minimax
answer = minimax(0, 0, True, scores, depth)

print("The optimal value is:", answer)
print("Total leaf evaluations (Minimax):", counter)
