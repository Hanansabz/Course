def decimal_to_binary(number, bits):
    binary = bin(number) # Convert the decimal number to binary using the built-in bin() function
    binary = binary[2:]  # Remove the '0b' prefix   
    binary = binary.zfill(bits)  # Pad with zeros to fit the specified number of bits
    return binary

def binary_to_negative_binary(binary):
    negative_binary = ''.join('1' if bit == '0' else '0' for bit in binary)  # Invert the bits
    negative_binary = bin(int(negative_binary, 2) + 1)[2:]  # Add 1 to get the two's complement
    return negative_binary 


def main():
    try:
        number = int(input("Enter a decimal number: "))
        bits = int(input("Enter the number of bits for the binary representation: "))

        binary = decimal_to_binary(number, bits)
        negative = binary_to_negative_binary(binary)

        print(f"Decimal: {number}")
        print(f"Binary: {binary}")          
        print(f"Negative Binary: {negative}")
    except ValueError:
        print("Invalid input. Please enter a valid decimal number and number of bits.")
        main()  # Restart the main function to allow the user to try again

if __name__ == "__main__":
    main()

input("Press Enter to exit...")