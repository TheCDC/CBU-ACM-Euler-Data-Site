import repo_data


def main():
    print("List of users who have solved Euler 001:")
    list_of_users = repo_data.who_solved(1)
    print(', '.join(list_of_users))

if __name__ == '__main__':
    main()
