
class HammingDistance:

    def __init__(self, first_data_to_evaluate, second_data_to_evaluate):
        self.first_data_to_evaluate = first_data_to_evaluate
        self.second_data_to_evaluate = second_data_to_evaluate
        self.hamming_distance_result = 0

    def calculate_hamming_distance(self):
        try:
            if len(self.first_data_to_evaluate) != len(self.second_data_to_evaluate):
                raise ValueError("To calculate the Hamming Distance is need to send two string with equal length.")
        except ValueError:
            exit('Could not complete Hamming Distance request')

        list_first_data = list(self.first_data_to_evaluate)
        list_second_data = list(self.second_data_to_evaluate)
        my_count = 0

        for first_fragment_data, second_fragment_data in zip(list_first_data, list_second_data):
            if first_fragment_data != second_fragment_data:
                self.hamming_distance_result += 1
            my_count -= 1

        return self.hamming_distance_result