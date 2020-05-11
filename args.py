def args_parser():
    """
    Command line Argument를 받는다. 
    1st args : csv file name
    2nd args : method (HM, PM, Duchi)
    """
    parser = argparse.ArgumentParser(description='The CSV file for apply Differential Privacy')
    parser.add_argument('filename',
                        type=str,
                        default='Null', ## if filename is null: filename = "random_data"로 입력
                        metavar='File_name',
                        help='Which file do you want to apply DP?',
                        )
    parser.add_argument('--op', 
                        type=str, 
                        default='HM',
                        choices=['PM','HM'],
                        help='Which DP method do you want to apply?',
                        )
    args = parser.parse_args()

    return args.filename, args.op