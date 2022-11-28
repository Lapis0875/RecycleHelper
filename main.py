from program import BarcodeSearcher


def test():
    from program import BarcodeTester
    instance = BarcodeTester()
    instance.run()
    print("Test done successfully.")


def main():
    """
    main func.
    """
    instance = BarcodeSearcher()
    instance.run()


if __name__ == "__main__":
    test()
    # main()
