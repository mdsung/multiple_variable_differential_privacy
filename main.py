import timeit
import access
from diffPrivacy import diffPrivacy


if __name__ == "__main__":
    start = timeit.default_timer()
    epsilon = 5
    method = "HM"

    # read_filename, method = args_parser()
    data_path = "./data/"
    read_filename = "targetfile.csv"
    raw_data = access.read_file(data_path + read_filename, False) ## matrix 반환
    ## Apply Differential Privacy
    dp = diffPrivacy(epsilon, raw_data, method) ## epsilon, matrix, method
    
    # Output file save
    output_path = "./outcome/"
    write_filename = access.make_write_filename(read_filename, "norm", epsilon)
    access.write_file(dp.normdf, output_path + write_filename)
    
    write_filename = access.make_write_filename(read_filename, "DP", epsilon)
    access.write_file(dp.newdf, output_path + write_filename)

    # 실행 코드

    stop = timeit.default_timer()
    print(f"Total Time the algorithm spent:{stop - start}s")
