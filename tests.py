from functions.run_python_file import run_python_file


def main():
    # Test 1: Run main.py without arguments (should show usage instructions)
    print("Result for running 'main.py':")
    result1 = run_python_file("calculator", "main.py")
    print(result1)
    print()

    # Test 2: Run main.py with calculator expression
    print("Result for running 'main.py' with args ['3 + 5']:")
    result2 = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result2)
    print()

    # Test 3: Run tests.py
    print("Result for running 'tests.py':")
    result3 = run_python_file("calculator", "tests.py")
    print(result3)
    print()

    # Test 4: Try to run file outside working directory (should fail)
    print("Result for running '../main.py':")
    result4 = run_python_file("calculator", "../main.py")
    print(result4)
    print()

    # Test 5: Try to run non-existent file (should fail)
    print("Result for running 'nonexistent.py':")
    result5 = run_python_file("calculator", "nonexistent.py")
    print(result5)
    print()


if __name__ == "__main__":
    main()
