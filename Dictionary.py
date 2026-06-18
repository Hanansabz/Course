from shared.word_counting import count_words, top_n_words

n = int(input("Enter the number of top words to display: "))
file_name = "C://Users//Hanan//Course//Storytext.txt"
d = count_words(file_name)
sorted_d = dict(top_n_words(d, n))
for key, value in sorted_d.items():
    print("Words: " + key + " Appears " + str(value) + " times")

input("Press Enter to exit...")
