import subprocess

def run_current_rule():
    result = subprocess.run(['python', 'scripts/current_rule.py'], capture_output=True, text=True)
    return float(result.stdout.strip())
def run_enhanced_rule():
    result = subprocess.run(['python', 'scripts/enhanced_rule.py'], capture_output=True, text=True)
    return float(result.stdout.strip())

def main():
    num_runs = 200
    results = []

    for _ in range(num_runs):
        result = run_current_rule()
        results.append(result)

    average_result = sum(results) / num_runs
    print(f'Average result after {num_runs} runs: {average_result}')

def main2():
    num_runs = 200
    results = []

    for _ in range(num_runs):
        result = run_enhanced_rule()
        results.append(result)

    average_result = sum(results) / num_runs
    print(f'Average result after {num_runs} runs: {average_result}')

main()
main2()