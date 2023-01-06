import os
import qrcode 
from PIL import Image
from qrcode.main import sys
from pprint import pprint as pp
import numpy as np

def generate_code(data, box_size=10):
    """
    Generate a qr code
    
    Args: 
        data -> string; the data you want to encode into the qr
        optional:
            box_size -> int; the size of the squares that make up the qr

    Returns:
        code -> PilImage; the generated qr code
    """

    try:
        qr = qrcode.QRCode(version=1,box_size=box_size,border=0)
        qr.add_data(data)
        qr.make(fit=True)
        code = qr.make_image(fill_color='black', back_color='white')

    except Exception as e:
        print("generating the qrcode failed: {}".format(str(e)), file=sys.stderr)
        raise e
    return code

def generate_answers(answwer_sheet, box_size=10, offset=0):
    """Generates 2d matrix of 1's and 0's, 1 if the current box is black it counts as 1, if it is white it counts as 0 
        Args:
            answerSheet -> image or string; The answer sheet must be an image, part of a qr code 
            optional:
                box_size -> int; The size of the boxes that make up the qr code
                offset -> int; The amount of pixels from the border to the upper right corner of the center piece of the qr code
        Returns:
            data_array -> list(list(int)); A 2d matrix of integer values
    """
    data_array = []
    input_image = None


    try:
        input_image = Image.open(answwer_sheet)
        input_image = input_image.convert("L")
    except FileNotFoundError as e:
        print("could not open the answer sheet: {}".format(str(e)), file=sys.stderr)
        raise
    w,h = input_image.size
    for i in range(offset+1,w-offset-1,box_size):
        row = []
        for j in range(offset+1,h-offset-1,box_size):
            try:
                r = input_image.getpixel((j, i))
            except Exception as e:
                print(input_image.getpixel)
                print("Could not read pixel: {}".format(str(e)), file=sys.stderr)
                raise
            if(r == 0 ):
                row.append(1)
            else:
                row.append(0)
        data_array.append(row)
    return data_array

def number_from_answer_line(answers):   
    """
    Helper function for making games: converts the sequence of 1's and 0's from each line from binary to decimal
    Args:
        answers -> list; The list of answers to the game
    Returns:
        line_numbers -> list; A list of the generated numbers
    """
    line_numbers = []
    for line in answers:
        string =""
        for element in line:
            string += str(element)
        line_numbers.append(int(string,2))

    return line_numbers
            
def generate_outer(qrimage, box_size=10, offset=0, scale_by = 3):
    """
    Generates and saves the outer (not playable) part of the puzzle
    Args:
        qrimage -> PILImage; The qr image generated from the data
        box_size -> int; The size of each individual cell of the qr; default = 10
        offset -> int; How many cells to let out of the generation; default = 0
        scale_by -> int; The scale factor of the generated outer frame; default = 3
        """
    margin = 8
    image = Image.open(qrimage).convert("RGB") 
    answer_size = int(image.size[0] / box_size - 2*margin)

    x_cut, y_cut = offset+margin*box_size, offset+(margin + answer_size) * box_size
    qr_np_arr = np.array(image)
    qr_np_arr[x_cut:y_cut, x_cut:y_cut] = (255,255,255)

    final = Image.fromarray(qr_np_arr)
    x,y = final.size
    final = final.resize((x*scale_by,y*scale_by))
    final.save('generated_outer.jpg')

if __name__ == "__main__":
    data = None
    with open('tmp.txt','r') as tmp:
        data = tmp.readlines()
    print(data)
    name = 'test.png'
    qr = generate_code(data)
    qr.save('test.png')
    answs = generate_answers(answwer_sheet=name, offset=80)
    pp(answs)
    generate_outer(name)
    number_from_answer_line(answs)
    os.remove(name)

