import subprocess

def main():
    process = subprocess.Popen(['go', 'run', 'spammer-go.go'], stdout=subprocess.PIPE, text=True)

    while True:
        output = process.stdout.readline().strip()
        if output:
            print(output)
            #if output == "Hello World 25":
            #    break

if __name__ == "__main__":
    main()
