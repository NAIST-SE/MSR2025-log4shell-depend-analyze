from . import data_preparation, data_extraction


def main():

    print("\n**** Data Preparation ****")
    data_preparation.main()

    print("\n**** Data Extraction ****")
    data_extraction.main()


if __name__ == "__main__":
    main()
