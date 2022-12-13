from program import BarcodeSearcher, BluetoothTester


def test():
    instance = BluetoothTester()
    # instance.run()
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
