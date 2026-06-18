## -CLASS LEARNING- ##

# list_comprehension_even = [x for x in range(1, 31) if x % 2 == 0]
# print(list_comprehension_even)

# list_comprehension_3_not_4 = [x for x in range(1, 51) if x % 3 == 0 and x % 4 != 0]
# print(list_comprehension_3_not_4)

# def mystery_function(n):
#     function = [x for x in range(1, n+1) if x % 2 == 1]
#     return sum(function)

# print(mystery_function(5))

# numbers = [1, 2, 3, 4, 5]
# print(list(map(lambda x: x*10, numbers)))

# numbers = [1, 5, 10, 15, 20, 25, 30]
# print(list(filter(lambda x: x > 10 and x % 5 == 0, numbers)))


#test the PIL library to show an image~
# from PIL import Image 

# img = Image.open(r"C:\Users\Hanan\Course\virustest\takashi.jpg")
# img.show()
# print(img.size)
# print(img.format)

# import cv2
# import numpy as np
# from PIL import ImageGrab
# print("Starting screen stream... Press 'q' to stop.")

# while True:
#     # 1. Take a screenshot of the whole screen
#     img = ImageGrab.grab()
    
#     # 2. Convert the image into a NumPy array
#     frame = np.array(img)
    
#     # 3. Pillow uses RGB color, but OpenCV needs BGR color
#     frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
#     # 4. Show the live stream in an OpenCV window
#     cv2.imshow("Live Screen Stream", frame_bgr)
    
#     # 5. Stop the stream if the user presses the 'q' key
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Clean up and close all windows
# cv2.destroyAllWindows()

