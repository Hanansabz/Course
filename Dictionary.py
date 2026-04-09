def read_file_content_to_dictionary(file_name):
    with open(file_name) as file:
        d = {}
        for line in file:
            splitted_line = line.split()
            for word in splitted_line:
                if word in d:
                    d[word] += 1
                else:
                    d[word] = 1
        return d

def sort_dictionary_by_value(d, n):
    l = sorted(d.items(), key=lambda item: item[1], reverse=True)
    l = l[:n] # Keep only the top n items
    sorted_d = dict(l) # Convert the list of tuples back to a dictionary
    return sorted_d

n = int(input("Enter the number of top words to display: "))
file_name = "C://Users//Hanan//Course//Storytext.txt"
d = read_file_content_to_dictionary(file_name)
sorted_d = sort_dictionary_by_value(d, n)
for key, value in sorted_d.items():
    print("Words: " + key + " Appears " + str(value) + " times")

