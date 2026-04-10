import csv
from typing import Any


def load_data(file):
    data = []
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            data.append(row)  # store ALL rows once
    return data
def compute_prio(data):
    rain=0
    no_rain=0
    for i in range(len(data)):
        if data[i][0] == 'Rain':
            rain+=1
        elif data[i][0] == 'NoRain':
            no_rain+=1
    b0 = [[0.0], [0.0]]
    b0[0][0] = rain / len(data)
    b0[1][0] = no_rain / len(data)
    return b0
def compute_transition(data):
    i = 0
    yesterday = ''
    transition = [[0.0,0.0],[0.0,0.0]]
    for row in data:
        if i == 0:
                yesterday = row[0]
                i=i+1
                continue
        else:
                today = row[0]
                if today == yesterday and today == 'Rain':
                    transition[0][0] = transition[0][0] + 1
                elif today == yesterday and today == 'NoRain':
                    transition[1][1] = transition[1][1] + 1
                elif today != yesterday and today == 'Rain':
                    transition[0][1] = transition[0][1] + 1
                elif today != yesterday and today == 'NoRain':
                    transition[1][0] = transition[1][0] + 1
                yesterday = today
    col0_total = transition[0][0] + transition[1][0]

    col1_total = transition[0][1] + transition[1][1]

    transition[0][0] /= col0_total
    transition[1][1] /= col1_total
    transition[0][1] /= col1_total
    transition[1][0] /= col0_total
    for i in range(2):
        for j in range(2):
            transition[i][j] = round(transition[i][j], 2)
    return transition
def observer(data):
    umbrella_rain = 0
    umbrella_no_rain = 0
    no_umbrella_no_rain = 0
    no_umbrella_rain = 0
    raincoat_rain = 0
    no_raincoat_rain = 0
    raincoat_no_rain = 0
    no_raincoat_no_rain = 0
    rain=0
    no_rain=0
    for row in data:
            if row[0] == 'Rain' and  row[1] == 'Umbrella':
                umbrella_rain += 1
                rain+=1
            elif row[0] == 'NoRain' and row[1] == 'Umbrella' :
                umbrella_no_rain += 1
                no_rain+=1
            elif row[0] == 'NoRain' and row[1] == 'NoUmbrella' :
                no_umbrella_no_rain += 1
                no_rain += 1
            elif row[0] == 'Rain' and row[1] == 'NoUmbrella' :
                no_umbrella_rain += 1
                rain += 1
    for row in data:
        if row[0] == 'Rain' and row[2] == 'Raincoat':
            raincoat_rain += 1
        elif row[0] == 'NoRain' and row[2] == 'Raincoat':
            raincoat_no_rain += 1
        elif row[0] == 'NoRain' and row[2] == 'NoRaincoat':
            no_raincoat_no_rain += 1
        elif row[0] == 'Rain' and row[2] == 'NoRaincoat':
            no_raincoat_rain += 1

    umbrella_rain = umbrella_rain /rain
    no_umbrella_rain = no_umbrella_rain / rain
    no_umbrella_no_rain = no_umbrella_no_rain /no_rain
    umbrella_no_rain = umbrella_no_rain /no_rain
    raincoat_rain = raincoat_rain /rain
    no_raincoat_rain = no_raincoat_rain /rain
    no_raincoat_no_rain = no_raincoat_no_rain /no_rain
    raincoat_no_rain = raincoat_no_rain /no_rain
    o1_umbrella=[[round(umbrella_rain,2),0.0],[0.0,round(umbrella_no_rain,2)]]
    o1_no_umbrella=[[round(no_umbrella_rain,2),0.0],[0.0,round(no_umbrella_no_rain,2)]]
    o2_raincoat = [[round(raincoat_rain,2),0.0],[0.0,round(raincoat_no_rain,2)]]
    o2_no_raincoat = [[round(no_raincoat_rain,2),0.0],[0.0,round(no_raincoat_no_rain,2)]]
    return o1_umbrella, o1_no_umbrella , o2_raincoat, o2_no_raincoat


def mat_multiply(A, B):

    rows_A = 2
    cols_B = len(B[0])
    result = [[0.0] * cols_B for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(2):
                result[i][j] += A[i][k] * B[k][j]
    return result

def filtering(obsevation,transition, b0,o1_umbrella, o1_no_umbrella , o2_raincoat, o2_no_raincoat,output_file ):
    with open(output_file, 'a') as f:
        bn = b0
        for i, row in enumerate(obsevation):
            o1 = row[0]
            o2 = row[1]
            result = mat_multiply(transition, bn)
            if o2 != 'None':
                if o2 == 'Raincoat':
                    result = mat_multiply(o2_raincoat,result)
                elif o2 == 'NoRaincoat':
                    result = mat_multiply(o2_no_raincoat, result)
            if o1 != 'None':
                if o1 == 'Umbrella':
                    result = mat_multiply(o1_umbrella, result)
                elif o1 == 'NoUmbrella':
                    result = mat_multiply(o1_no_umbrella, result)
            total = result[0][0] + result[1][0]
            bn[0][0] = result[0][0]/total
            bn[1][0] = result[1][0]/total
            line1 = f"==={i + 1}==="
            line2 = f"[{o1},{o2}]"
            line3 = f"Updated Belief: [{round(bn[0][0], 2)}, {round(bn[1][0], 2)}]"
            print(line1);
            f.write(line1 + '\n')
            print(line2);
            f.write(line2 + '\n')
            print(line3);
            f.write(line3 + '\n')
        final = f"Final Belief: [{round(bn[0][0], 2)}, {round(bn[1][0], 2)}]"
        print(final)
        f.write(final + '\n')
    return bn
def cross_validate(test_data, b0, transition, o1_umbrella, o1_no_umbrella, o2_raincoat, o2_no_raincoat, output_file):
    bn = b0
    total_correct = 0
    with open(output_file, 'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ground_truth', 'predicted', 'p_rain', 'p_norain', 'correct', 'total_correct', 'accuracy'])
        for i, row in enumerate(test_data):
            ground_truth = row[0]
            o1 = row[1]
            o2 = row[2]
            result = mat_multiply(transition, bn)
            if o2 != 'None':
                if o2 == 'Raincoat':
                    result = mat_multiply(o2_raincoat, result)
                elif o2 == 'NoRaincoat':
                    result = mat_multiply(o2_no_raincoat, result)
            if o1 != 'None':
                if o1 == 'Umbrella':
                    result = mat_multiply(o1_umbrella, result)
                elif o1 == 'NoUmbrella':
                    result = mat_multiply(o1_no_umbrella, result)
            total = result[0][0] + result[1][0]
            bn[0][0] = result[0][0] / total
            bn[1][0] = result[1][0] / total

            if bn[0][0]>bn[1][0]:
                predicted= 'Rain'
            else:
                predicted= 'NoRain'

            correct = predicted == ground_truth
            if correct:
                total_correct += 1
            accuracy = total_correct / (i+1)
            writer.writerow([ground_truth,predicted,round(bn[0][0],2),round(bn[1][0],2), correct, total_correct, accuracy])




if __name__ == '__main__':
    file1 = 'training_data.csv'
    file2 = 'observations.csv'
    data = load_data(file1)
    observation = load_data(file2)
    b0 = compute_prio(data)
    transition = compute_transition(data)
    o1_umbrella, o1_no_umbrella, o2_raincoat, o2_no_raincoat = observer(data)
    with open('Output.txt', 'w') as f:
        f.write("Belief Vector:\n")
        f.write(f"{b0[0][0]}\n{b0[1][0]}\n")
        f.write("Transition Model:\n")
        f.write(f"{round(transition[0][0], 2)} {round(transition[0][1], 2)}\n")
        f.write(f"{round(transition[1][0], 2)} {round(transition[1][1], 2)}\n")
        f.write("O1(Umbrella):\n")
        f.write(f"{round(o1_umbrella[0][0], 2)} {round(o1_umbrella[0][1], 2)}\n")
        f.write(f"{round(o1_umbrella[1][0], 2)} {round(o1_umbrella[1][1], 2)}\n")
        f.write("O1(NoUmbrella):\n")
        f.write(f"{round(o1_no_umbrella[0][0], 2)} {round(o1_no_umbrella[0][1], 2)}\n")
        f.write(f"{round(o1_no_umbrella[1][0], 2)} {round(o1_no_umbrella[1][1], 2)}\n")
        f.write("O2(Raincoat):\n")
        f.write(f"{round(o2_raincoat[0][0], 2)} {round(o2_raincoat[0][1], 2)}\n")
        f.write(f"{round(o2_raincoat[1][0], 2)} {round(o2_raincoat[1][1], 2)}\n")
        f.write("O2(NoRaincoat):\n")
        f.write(f"{round(o2_no_raincoat[0][0], 2)} {round(o2_no_raincoat[0][1], 2)}\n")
        f.write(f"{round(o2_no_raincoat[1][0], 2)} {round(o2_no_raincoat[1][1], 2)}\n")

    bn = filtering(observation, transition, b0, o1_umbrella, o1_no_umbrella, o2_raincoat, o2_no_raincoat,'Output.txt')
    print(f"Final Belief: [{round(bn[0][0], 2)}, {round(bn[1][0], 2)}]")

    train = data[:700]
    test = data[700:]
    b0 = compute_prio(train)
    transition = compute_transition(train)
    o1_umbrella_cv, o1_no_umbrella_cv, o2_raincoat_cv, o2_no_raincoat_cv = observer(train)
    cross_validate(test,b0,transition,o1_umbrella_cv, o1_no_umbrella_cv, o2_raincoat_cv, o2_no_raincoat_cv,'cross_validation.csv')



