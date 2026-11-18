if __name__ == "__main__":
    from app import benchmark
    from app import main
    from config import DEBUG_TIMING

    if DEBUG_TIMING:
        benchmark()
    main()