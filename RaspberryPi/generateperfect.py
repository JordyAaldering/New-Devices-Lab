import cv2
import numpy as np
import pandas as pd
from code import Code


def read_codes(excel_filename: str):
    """
    Reads the bitstring codes for each card from an excel sheet.
    :param excel_filename: The path to the excel sheet containing the codes.
    :return: The read codes.
    """
    ex = pd.read_excel(excel_filename)
    codes = []

    for index, row in ex.iterrows():
        val = row["Value"]
        if pd.isnull(val):
            # Skip if Value cell is empty
            continue
        offset = row["Offset"]
        c = Code(val) + Code(offset)
        codes.append(str(c))

    return codes


def main():
    """
    Generate a 'perfect' image as it would appear if a photo of a marked deck
    of cards would be cropped and thresholded, as it is in the main
    application's image processing pipeline. This is useful for testing.
    """
    WHITE = 1
    BLACK = 0
    ROW_HEIGHT = 6
    UNIT = 15  # Unit width for code
    SPACER = 20  # Spacer width
    codes = read_codes("Codes.xlsx")
    dimensions = 312, 312, 3  # Height, width, channels (RGB)
    image = np.zeros(dimensions, dtype=np.uint8)  # Initialise black image
    for index, code in enumerate(codes):
        split_code = code.split(" ")

        row_start = index * ROW_HEIGHT
        row_end = index * ROW_HEIGHT + ROW_HEIGHT-1

        # Initialize draw commands with the starter code on the left-hand side
        # The below array means '20 wide white block, followed by 15 wide
        # black block' etc.
        draw = [(WHITE, SPACER), (BLACK, UNIT), (WHITE, UNIT), (BLACK, UNIT),
                (WHITE, SPACER)]

        # Add a black or white block depending on each ternary digit in the
        # code. This results in either a left-hand black block, a right-hand
        # black block or a long black block.
        for s in split_code:
            if s[0] == "0":
                draw.append((WHITE, UNIT))
            else:
                draw.append((BLACK, UNIT))

            if s[1] == "0":
                draw.append((WHITE, UNIT))
            else:
                draw.append((BLACK, UNIT))

            draw.append((WHITE, SPACER))

        start_x = 0
        for d in draw:
            # Draw each white block; the background is black by default.
            end_x = start_x+d[1]
            if d[0] == WHITE:
                cv2.rectangle(image, (start_x, row_start), (end_x, row_end),
                              (255, 255, 255), cv2.FILLED, cv2.LINE_8, 0)

            start_x += d[1]
        # Fill remaining space from the code to the right side of the image
        # with white.
        end_x = dimensions[1]
        cv2.rectangle(image, (start_x, row_start), (end_x, row_end),
                      (255, 255, 255), cv2.FILLED, cv2.LINE_8, 0)

    cv2.imshow("Image", image)
    cv2.imwrite("Perfect.png", image)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
