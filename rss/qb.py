startq_mapping = {1: 1, 4: 4, 7: 7, 10: 10}
startq = startq_mapping.get(10, '')
endq = startq if startq else ''
print(endq)