import sys
import re

def word_frequency(file_name, top_n):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
            words = text.split()
            word_freq = {}     #{word:count}

            for word in words:
                word = re.sub(r'[^\w\s]', '', word).lower()  # Remove punctuation and convert to lowercase

                if word in word_freq:
                    word_freq[word] += 1
                else:
                    word_freq[word] = 1

        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)   #("Hello": 5,"word": 3)

        print(f"Top {top_n} Most Frequent Words:")
        for i, (word, freq) in enumerate(sorted_words[:top_n], 1):
            print(f"{i}. {word} - {freq} times")

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

input("Press Enter to exit...")