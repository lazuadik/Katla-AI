# Num of Step
brute = [int(i) for i in open("Testing/CSP/Result/brute-prune-step.txt").read().splitlines()]
csp = [int(i) for i in open("Testing/CSP/Result/csp-step.txt").read().splitlines()]

worst_brute = 0
best_brute = brute[0]
sum_brute = 0

worst_csp = 0
best_csp = csp[0]
sum_csp = 0

# print(len(brute), len(csp))

for i in range(len(brute)):
    if worst_brute < brute[i]:
        worst_brute = brute[i]
    if best_brute > brute[i]:
        best_brute = brute[i]
    if worst_csp < csp[i]:
        worst_csp = csp[i]
    if best_csp > csp[i]:
        best_csp = csp[i]
    sum_brute += brute[i]
    sum_csp += csp[i]

f = open("Testing/CSP/Result/csp-brute-summary.csv", "w")
f.write(";CSP;Brute and Prune\n")
f.write(f"AVG;{sum_csp/len(csp):.2f};{sum_brute/len(brute):.2f}\n")
f.write(f"WORST;{worst_csp};{worst_brute}\n")
f.write(f"BEST;{best_csp};{best_brute}\n")
f.write(f"\n")
f.write(f"\n")

# Choosing Word (Time Exec)
f.write(f"Chosing Word\n")
f.write(f"CSP;Brute and Prune\n")
csp = [i for i in open("Testing/CSP/Result/csp-choose.txt").read().splitlines()]
brute = [i for i in open("Testing/CSP/Result/brute-prune-choose.txt").read().splitlines()]

csp_per_step = [0 for _ in range(max(worst_csp, worst_brute))]
brute_per_step = [0 for _ in range(max(worst_csp, worst_brute))]
csp_count = [0 for _ in range(max(worst_csp, worst_brute))]
brute_count = [0 for _ in range(max(worst_csp, worst_brute))]

for i in csp:
    temp = i.split(';')
    for j in range(len(temp)):
        csp_per_step[j] += float(temp[j])
        csp_count[j] += 1
    
for i in brute:
    temp = i.split(';')
    for j in range(len(temp)):
        brute_per_step[j] += float(temp[j])
        brute_count[j] += 1

print(max(worst_csp, worst_brute), len(csp_per_step), len(brute_per_step))
for x in range(max(worst_csp, worst_brute)):
    f.write(f"{csp_per_step[x]/csp_count[x]:.2f};{brute_per_step[x]/brute_count[x]:.2f}\n")

f.write(f"\n")
f.write(f"\n")

# Feedback Response (Time Exec)
f.write(f"Feedback Response\n")
f.write(f"CSP;Brute and Prune\n")
csp = [i for i in open("Testing/CSP/Result/csp-feedback-response.txt").read().splitlines()]
brute = [i for i in open("Testing/CSP/Result/brute-prune-feedback-response.txt").read().splitlines()]

csp_per_step = [0 for _ in range(worst_csp)]
brute_per_step = [0 for _ in range(max(worst_csp, worst_brute))]
csp_count = [0 for _ in range(max(worst_csp, worst_brute))]
brute_count = [0 for _ in range(max(worst_csp, worst_brute))]
for i in csp:
    temp = i.split(';')
    for j in range(len(temp)):
        csp_per_step[j] += float(temp[j])
        csp_count[j] += 1

for i in brute:
    temp = i.split(';')
    for j in range(len(temp)):
        brute_per_step[j] += float(temp[j])
        brute_count[j] += 1
        
for x in range(max(worst_csp, worst_brute)):
    f.write(f"{csp_per_step[x]/csp_count[x]:.2f};{brute_per_step[x]/brute_count[x]:.2f}\n")

f.write(f"\n")
f.write(f"\n")


# Solve Game (Time Exec)
f.write(f"Solve Game\n")
f.write(f"CSP;Brute and Prune\n")
csp = [i for i in open("Testing/CSP/Result/csp-solve.txt").read().splitlines()]
brute = [i for i in open("Testing/CSP/Result/brute-prune-solve.txt").read().splitlines()]

worst_brute = 0
best_brute = float(brute[0])
sum_brute = 0

worst_csp = 0
best_csp = float(csp[0])
sum_csp = 0

for i in range(len(brute)):
    if worst_brute < float(brute[i]):
        worst_brute = float(brute[i])
    if best_brute > float(brute[i]):
        best_brute = float(brute[i])
    if worst_csp < float(csp[i]):
        worst_csp = float(csp[i])
    if best_csp > float(csp[i]):
        best_csp = float(csp[i])
    sum_brute += float(brute[i])
    sum_csp += float(csp[i])

f.write(";CSP;Brute and Prune\n")
f.write(f"AVG;{sum_csp/len(csp):.2f};{sum_brute/len(brute):.2f}\n")
f.write(f"WORST;{worst_csp:.2f};{worst_brute:.2f}\n")
f.write(f"BEST;{best_csp:.2f};{best_brute:.2f}\n")