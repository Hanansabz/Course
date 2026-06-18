import sys
from shared.word_counting import count_words, print_word_frequencies


def word_frequency(file_name, top_n):
    try:
        word_freq = count_words(file_name)
        print(f"Top {top_n} Most Frequent Words:")
        print_word_frequencies(word_freq, top_n=top_n)
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    

if __name__ == "__main__":
    if len(sys.argv) !=3:
        print("Usage: python sys.py <file_name> <top_n>")
    else:
        file_name = sys.argv[1]
        try:
            top_n = int(sys.argv[2])
            if top_n<1:
                print("Error: top_n must be a positive number.")
            else:
                word_frequency(file_name, top_n)
        except ValueError:
            print("Error: top_n must be an integer.")

input("[~Use a Terminal for this application~] Press Enter to exit...")
