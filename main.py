from problems.counting_point_mutations.HammingDistance import HammingDistance


data_input = open('data/counting_point_mutations/rosalind_hamming.txt', "r")
separate_data = [data.strip() for data in data_input.readlines()]
data_input.close()
hamming_distance_information_pack = HammingDistance(separate_data[0], separate_data[1])

if __name__ == '__main__':
    hamming_distance_result = hamming_distance_information_pack.calculate_hamming_distance()
    print(hamming_distance_result)
