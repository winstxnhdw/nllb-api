from server import Server


def main():
    """
    Summary
    -------
    exhaust the initialise generator and run the server
    """
    for _ in Server.initialise():
        pass


if __name__ == '__main__':
    main()
