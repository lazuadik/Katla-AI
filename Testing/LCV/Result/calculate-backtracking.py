lcv = [[int(x) for x in i.split(';')] for i in open("Testing/LCV/Result/lcv-backtracking.txt").read().splitlines()]
lcv_noor = [[int(x) for x in i.split(';')] for i in open("Testing/LCV/Result/lcv-noor-backtracking.txt").read().splitlines()]
noor = [[int(x) for x in i.split(';')] for i in open("Testing/LCV/Result/no-ordering-backtracking.txt").read().splitlines()]
ran = [[int(x) for x in i.split(';')] for i in open("Testing/LCV/Result/random-backtracking.txt").read().splitlines()]
# final = [[int(x) for x in i.split(';')] for i in open("Testing/LCV/Result/final-backtracking.txt").read().splitlines()]

lcv_per_step = [0 for _ in range(20)]
lcv_noor_per_step = [0 for _ in range(20)]
noor_per_step = [0 for _ in range(20)]
ran_per_step = [0 for _ in range(20)]
# final_per_step = [0 for _ in range(20)]

for i in lcv:
    for j in range(len(i)):
        lcv_per_step[j] += i[j]
for i in lcv_noor:
    for j in range(len(i)):
        lcv_noor_per_step[j] += i[j]
for i in noor:
    for j in range(len(i)):
        noor_per_step[j] += i[j]
for i in ran:
    for j in range(len(i)):
        ran_per_step[j] += i[j]
# for i in final:
#     for j in range(len(i)):
#         final_per_step[j] += i[j]

f = open("Testing/LCV/Result/value-ordering-summary.csv", "w")
f.write("Jumlah Backtracking\n")
f.write("lcv;")
for i in lcv_per_step:
    f.write(str(i)+';')
f.write('\n')
f.write("lcv + noor;")
for i in lcv_noor_per_step:
    f.write(str(i)+';')
f.write('\n')
f.write("no ordering;")
for i in noor_per_step:
    f.write(str(i)+';')
f.write('\n')
f.write("random;")
for i in ran_per_step:
    f.write(str(i)+';')
f.write('\n')
# f.write("final;")
# for i in final_per_step:
#     f.write(str(i)+';')
# f.write('\n')
# f.write('\n')
f.write('\n')

lcv = [[float(x) for x in i.split(';')] for i in open("Testing/LCV/Result/lcv-convergence.txt").read().splitlines()]
lcv_noor = [[float(x) for x in i.split(';')] for i in open("Testing/LCV/Result/lcv-noor-convergence.txt").read().splitlines()]
noor = [[float(x) for x in i.split(';')] for i in open("Testing/LCV/Result/no-ordering-convergence.txt").read().splitlines()]

lcv_per_step = [0 for _ in range(20)]
lcv_noor_per_step = [0 for _ in range(20)]
noor_per_step = [0 for _ in range(20)]

for i in lcv:
    for j in range(len(i)):
        lcv_per_step[j] += i[j]
for i in lcv_noor:
    for j in range(len(i)):
        lcv_noor_per_step[j] += i[j]
for i in noor:
    for j in range(len(i)):
        noor_per_step[j] += i[j]

f.write("Konvergen\n")
f.write("lcv;")
for i in lcv_per_step:
    f.write(str(i)+';')
f.write('\n')
f.write("lcv + noor;")
for i in lcv_noor_per_step:
    f.write(str(i)+';')
f.write('\n')
f.write("no ordering;")
for i in noor_per_step:
    f.write(str(i)+';')
f.write('\n')

lcv = [int(i) for i in open("Testing/LCV/Result/lcv-step.txt").read().splitlines()]
lcv_noor = [int(i) for i in open("Testing/LCV/Result/lcv-noor-step.txt").read().splitlines()]
noor = [int(i) for i in open("Testing/LCV/Result/no-ordering-step.txt").read().splitlines()]
final = [int(i) for i in open("Testing/LCV/Result/final-step.txt").read().splitlines()]

f.write("Step\n")
f.write(";AVG;MAX;MIN;\n")

lcv_sum = 0
lcv_noor_sum = 0
noor_sum = 0
final_sum = 0
for i in lcv:
    lcv_sum += i
for i in lcv_noor:
    lcv_noor_sum += i
for i in noor:
    noor_sum += i
for i in final:
    final_sum += i
f.write(f"lcv;{lcv_sum/len(lcv):.2f};{max(lcv)};{min(lcv)}\n")
f.write(f"lcv + no ordering;{lcv_noor_sum/len(lcv_noor):.2f};{max(lcv_noor)};{min(lcv_noor)}\n")
f.write(f"no ordering;{noor_sum/len(noor):.2f};{max(noor)};{min(noor)}\n")
f.write(f"final;{final_sum/len(final):.2f};{max(final)};{min(final)}\n")