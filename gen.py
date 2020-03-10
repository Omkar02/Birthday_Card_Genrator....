import io
from io import StringIO
from reportlab import rl_config
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib.colors import black, white, red, pink, green, blue, yellow, lightgrey
from PIL import Image


width, height = (342,890)  # keep for later
post_card = (342,890)
print(A4)
# def add_fold_lines(c):
#     """Add lines to show where to fold card"""
#     # choose some colors
#     c.setFillColor(red)
#     # line settings
#     c.setLineWidth(5)
#     c.setDash(1, 5)  # n points on, m off
#     # draw some lines
#     c.line(width / 2, 0, width / 2, height)  # vertical
#     c.line(0, height / 2, width, height / 2)  # horz.


def put_in_front_picture(c, str_img):
    data = str_img
    with open(data, 'rb') as f:
        b = io.BytesIO(f.read())
        # image_file = io.BytesIO(b)
        img = Image.open(b)
        # resize image:
        img = img.resize((int(width/2 ), int(height/2)), Image.BILINEAR)
        # c.drawImage caused AttributeError: jpeg_fh

        c.drawInlineImage(img, x=width - 300, y=height - 700, width=width / 2,
                          height=height / 2)




def write_text(c, front_text, inside_text):
    # call canvas.getAvailableFonts() to see all fonts
    # change color
    # c.setFillColor(COLOR_FRONT)
    c.setFont("Helvetica", 28)
    line_pos = int(.4 * height)
    # for line in front_text.split('\n'):
    #     c.drawCentredString(3 * (width / 4), line_pos, line)
    #     line_pos -= int(.05 * height)
    # c.setFillColor(black)
    # c.setFont("Helvetica", 16)
    # c.rotate(180)  # write text upside down so it's right when folded.
    line_pos = -3 * (height / 4)
    for line in inside_text.split('\n'):
        c.drawCentredString(-width / 4, line_pos, line)
        line_pos -= int(.05 * height)
    # write branding text
    # c.rotate(180)  # put back to right side up
    c.setFont("Helvetica", 8)
    c.drawCentredString(width / 4, int(.13 * height),
                        "Created while fondly thinking of you at")
    c.drawCentredString(width / 4, int(.1 * height),
                        "http://utilitymill.com/utility/Greeting_Card_Generator")


def generate_card(IMG_FILE, TEXT_FRONT, TEXT_INSIDE):
    """Main function to generate PDF and print to stdout. Designed to be
    run as a CGI application."""
    if not (IMG_FILE):
        print('You must upload an image file or provide a URL to one')

        return

    tmp = io.BytesIO()

    # Canvas Setup
    c = canvas.Canvas('1.pdf', pagesize=post_card, pageCompression=0)
    # If output size is important set pageCompression=1, but remember that, compressed documents
    # will be smaller, but slower to generate. Note that images are always compressed, and this option will only
    # save space if you have a very large amount of text and vector graphics on each page.
    # Do I need 'MacRomanEncoding' for Macs?
    # Note: 0,0 coordinate in canvas is bottom left.
    c.setAuthor('Utility Mill - utilitymill.com/utility/greeting_card_generator')
    c.setTitle('Beautiful, expensive greeting card created at utilitymill.com')

    # add_fold_lines(c) #early feedback says lines aren't necessary. Uncomment here to put them in
    put_in_front_picture(c, IMG_FILE)
    write_text(c, TEXT_FRONT.replace('\r', ''), TEXT_INSIDE.replace('\r', ''))

    # The showPage method saves the current page of the canvas
    c.showPage()
    # The save method stores the file and closes the canvas.
    c.save()

    tmp.seek(0)
    print('Content-Type: application/pdf')
    print(tmp.read())


# generate_card(IMG_FILE, IMG_URL, TEXT_FRONT, TEXT_INSIDE)
generate_card('test.jpg','test_1', 'thank\n')