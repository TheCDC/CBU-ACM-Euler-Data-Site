import repo_data


def main():
    print("List of users who have solved Euler 001:")
    print(', '.join(repo_data.who_solved(1)))

if __name__ == '__main__':
    main()
