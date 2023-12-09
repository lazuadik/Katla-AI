# Count Backtracking Func
fc = [[int(x) for x in i.split(';')] for i in open("Testing/forward checking/Result/forward-checking-backtracking.txt").read().splitlines()]
nof = [[int(x) for x in i.split(';')] for i in open("Testing/forward checking/Result/no-filtering-backtracking.txt").read().splitlines()]

f = open("Testing/forward checking/Result/filtering-summary.csv", "w")
f.write(f"Count Backtracking\n")
f.write(f"Forward Checking;No Filtering\n")

fc_max_step = max([len(_) for _ in fc])
nof_max_step = max([len(_) for _ in nof])
fc_per_step = [0 for _ in range(max(fc_max_step, nof_max_step))]
nof_per_step = [0 for _ in range(max(fc_max_step, nof_max_step))]
fc_count = [0 for _ in range(max(fc_max_step, nof_max_step))]
nof_count = [0 for _ in range(max(fc_max_step, nof_max_step))]

for i in fc:
    for j in range(len(i)):
        fc_per_step[j] += float(i[j])
        fc_count[j] += 1

for i in nof:
    for j in range(len(i)):
        nof_per_step[j] += float(i[j])
        nof_count[j] += 1

for x in range(max(fc_max_step, nof_max_step)):
    if fc_count[x] == 0:
        fc_count[x] = 1
    if nof_count[x] == 0:
        nof_count[x] = 1
    f.write(f"{fc_per_step[x]/fc_count[x]:.2f};{nof_per_step[x]/nof_count[x]:.2f}\n")

f.write(f"\n")
f.write(f"\n")

f.write(f"Convergence Time\n")
f.write(f"Forward Checking;No Filtering\n")
fc = [[float(x) for x in i.split(';')] for i in open("Testing/forward checking/Result/forward-checking-convergen.txt").read().splitlines()]
nof = [[float(x) for x in i.split(';')] for i in open("Testing/forward checking/Result/no-filtering-convergen.txt").read().splitlines()]

fc_max_step = max([len(_) for _ in fc])
nof_max_step = max([len(_) for _ in nof])
fc_per_step = [0 for _ in range(max(fc_max_step, nof_max_step))]
nof_per_step = [0 for _ in range(max(fc_max_step, nof_max_step))]
fc_count = [0 for _ in range(max(fc_max_step, nof_max_step))]
nof_count = [0 for _ in range(max(fc_max_step, nof_max_step))]

for i in fc:
    for j in range(len(i)):
        fc_per_step[j] += float(i[j])
        fc_count[j] += 1

for i in nof:
    for j in range(len(i)):
        nof_per_step[j] += float(i[j])
        nof_count[j] += 1

for x in range(max(fc_max_step, nof_max_step)):
    if fc_count[x] == 0:
        fc_count[x] = 1
    if nof_count[x] == 0:
        nof_count[x] = 1
    f.write(f"{fc_per_step[x]/fc_count[x]:.2f};{nof_per_step[x]/nof_count[x]:.2f}\n")

f.write(f"Solved Time\n")
fc = [float(i) for i in open("Testing/forward checking/Result/forward-checking-solve.txt").read().splitlines()]
nof = [float(i) for i in open("Testing/forward checking/Result/no-filtering-solve.txt").read().splitlines()]

worst_fc = 0
best_fc = float(fc[0])
sum_fc = 0

worst_nof = 0
best_nof = float(nof[0])
sum_nof = 0

for i in range(len(fc)):
    if worst_fc < float(fc[i]):
        worst_fc = float(fc[i])
    if best_fc > float(fc[i]):
        best_fc = float(fc[i])
    if worst_nof < float(nof[i]):
        worst_nof = float(nof[i])
    if best_nof > float(nof[i]):
        best_nof = float(nof[i])
    sum_fc += float(fc[i])
    sum_nof += float(nof[i])

f.write(";Forward Checking;No Filtering\n")
f.write(f"AVG;{sum_fc/len(fc):.2f};{sum_nof/len(nof):.2f}\n")
f.write(f"WORST;{worst_fc:.2f};{worst_nof:.2f}\n")
f.write(f"BEST;{best_fc:.2f};{best_nof:.2f}\n")

f.write('\n')
f.write('\n')
f.write(f"Count Conflict\n")
f.write(f"Forward Checking;No Filtering\n")
fc = [[int(x) for x in i.split(';')] for i in open("Testing/forward checking/Result/forward-checking-conflict.txt").read().splitlines()]
nof = [[int(x) for x in i.split(';')] for i in open("Testing/forward checking/Result/no-filtering-conflict.txt").read().splitlines()]

fc_max_step = max([len(_) for _ in fc])
nof_max_step = max([len(_) for _ in nof])
fc_per_step = [0 for _ in range(max(fc_max_step, nof_max_step))]
nof_per_step = [0 for _ in range(max(fc_max_step, nof_max_step))]
fc_count = [0 for _ in range(max(fc_max_step, nof_max_step))]
nof_count = [0 for _ in range(max(fc_max_step, nof_max_step))]

for i in fc:
    for j in range(len(i)):
        fc_per_step[j] += float(i[j])
        fc_count[j] += 1

for i in nof:
    for j in range(len(i)):
        nof_per_step[j] += float(i[j])
        nof_count[j] += 1

for x in range(max(fc_max_step, nof_max_step)):
    if fc_count[x] == 0:
        fc_count[x] = 1
    if nof_count[x] == 0:
        nof_count[x] = 1
    f.write(f"{fc_per_step[x]/fc_count[x]:.2f};{nof_per_step[x]/nof_count[x]:.2f}\n")