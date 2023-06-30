import aote

if __name__ == "__main__":
    while True:
        try:
            q = aote.main()
        finally:
            if q == 10:
                continue
            else:
                break
