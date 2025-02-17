import subprocess


result = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE)

output = result.stdout.decode('utf-8')
lines = output.splitlines()

users = {}
processes = []

for line in lines:
    words = line.split()

    if len(words) >= 11:
        user = words[0]
        try:
            memory = float(words[3])
        except ValueError:
            memory = 0

        if user in users:
            users[user]['processes'] += 1
            users[user]['memory'] += memory
        else:
            users[user] = {'processes': 1, 'memory': memory}

        try:
            processes.append({
            'user': user,
            'cpu': float(words[2]),
            'memory': memory,
            'name': words[10]
            })
        except ValueError:
            processes.append({
            'user': user,
            'cpu': 0,
            'memory': memory,
            'name': words[10]
            })

print('Отчёт о состоянии системы:')
print('Пользователи системы:', ', '.join(users.keys()))
print('Процессов запущено:', len(processes))

print('Пользовательских процессов:')
for user, data in users.items():
    print(user + ':', data['processes'])

print('Всего памяти используется:', sum(data['memory'] for data in users.values()), 'мб')
print('Всего CPU используется:', sum(process['cpu'] for process in processes), '%')

most_memory_process = max(processes, key=lambda process: process['memory'])
most_cpu_process = max(processes, key=lambda  process: process['cpu'])

print('Больше всего памяти использует:', '({}...)'.format(most_memory_process['name'][:20]), 'мб')
print('Больше всего CPU использует:', '({}...)'.format(most_cpu_process['name'][:20]), 'мб')

import datetime

filename = datetime.datetime.now().strftime('%d-%m-%Y-%H:%M-scan.txt')
with open(filename, 'w') as f:
    f.write('Отчёт о состояние системы:\n')
    f.write('Пользователи системы: {}\n'.format(', '.join(users.keys())))
    f.write('Процессов запущено: {}\n'.format(len(processes)))
    f.write('Пользовательских процессов:\n')
    for user, data in users.items():
        f.write(('{}: {}\n'.format(user, data['processes'])))
    f.write('Всего памяти используется: {} мб\n'.format(sum(data['memory'] for data in  users)))
    f.write('Всего CPU используется: {} %\n'.format(sum(process['cpu'] for process in processes)))
    f.write('Больше всего памяти используется: ({}...) {} мб\n'.format(most_memory_process['name']))
    f.write('Больше всего CPU использует: ({}...) {} мб\n'.format(most_cpu_process['name']))

