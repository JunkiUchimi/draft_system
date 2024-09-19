import subprocess

def run_current_rule():
    # 出力結果を改行で分割して、2つの値を取得する
    result = subprocess.run(['python', 'scripts/current_rule.py'], capture_output=True, text=True)
    values = result.stdout.strip().split('\n')  # 改行区切りで分割
    return float(values[0]), float(values[1])

def run_enhanced_rule():
    # 同様に、出力結果を改行で分割して、2つの値を取得する
    result = subprocess.run(['python', 'scripts/enhanced_rule.py'], capture_output=True, text=True)
    values = result.stdout.strip().split('\n')  # 改行区切りで分割
    return float(values[0]), float(values[1])

def main():
    num_runs = 100
    results1 = []
    results2 = []

    for _ in range(num_runs):
        result1, result2 = run_current_rule()
        results1.append(result1)
        results2.append(result2)

    average_result1 = sum(results1) / num_runs
    average_result2 = sum(results2) / num_runs
    print(f'全球団の合計値 {average_result1}')
    print(f'球団aの値 {average_result2}')

def main2():
    num_runs = 100
    results1 = []
    results2 = []

    for _ in range(num_runs):
        result1, result2 = run_enhanced_rule()
        results1.append(result1)
        results2.append(result2)

    average_result1 = sum(results1) / num_runs
    average_result2 = sum(results2) / num_runs
    print(f'全球団の合計値 {average_result1}')
    print(f'球団aの値 {average_result2}')

main()
main2()
