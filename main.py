import csv

def load_training_data(file1):
    i = 0
    rain = 0
    no_rain = 0
    with open(file1, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            i += 1
            if row[0] == 'Rain':
                rain += 1
            else:
                no_rain += 1

    b0 = [[0.0], [0.0]]
    b0[0][0] = rain / i
    b0[1][0] = no_rain / i
    return b0
def compute_transition(file1,b0):
    i = 0
    yesterday = ''
    transition = [[0.0,0.0],[0.0,0.0]]
    with open(file1, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
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
        transition[0][1] /= col0_total
        transition[1][0] /= col1_total
        for i in range(2):
            for j in range(2):
                transition[i][j] = round(transition[i][j], 2)
    return transition


if __name__ == '__main__':
    file1 = 'training_data.csv'
    file2 = 'observation.csv'
    b0 = load_training_data(file1)
    transition = compute_transition(file1,b0)
    print(b0)
    print(transition)