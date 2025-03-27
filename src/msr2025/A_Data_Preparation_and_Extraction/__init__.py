from . import data_extraction, data_preparation

def main():
    print('\n**** Data Extraction ****')
    data_extraction.main()

    print('\n**** Data Preparation ****')
    data_preparation.main()


if __name__ == '__main__':
    main()