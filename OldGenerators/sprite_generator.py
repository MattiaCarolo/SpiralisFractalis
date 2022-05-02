from PIL import Image, ImageDraw
import random, sys

origDimension = 1500

r = lambda: random.randint(50,215) # lambda function to pick a random color level
rc = lambda: (r(), r(), r()) # lambda function to pick a random color based on RGB scale
listSym = []

'''

'''
def create_mirrored_square(border, draw, randColor, element, size):
    if (element == int(size/2)):    
        draw.rectangle(border, randColor)  
    elif (element > int(size/2)):    
        draw.rectangle(border,listSym.pop())
    else:    
        listSym.append(randColor)    
        draw.rectangle(border, randColor)

'''
create_sprite method

@border = Tuple containing the coordinates of the upper left and bottom right corners
@draw = If I understood correctly is the image in which we draw
@size = Size of the whole sprite

same work of main but here we introduce @i counter. @i serves as an
'''
def create_sprite(border, draw, size):
    x0, y0, x1, y1 = border  
    squareSize = (x1-x0)/size  
    randColors = [rc(), rc(), rc(), (0,0,0), (0,0,0), (0,0,0)]  
    element = 0
    for y in range(0, size):
        element = 0
        for x in range(0, size):      
            topLeftX = x*squareSize + x0      
            topLeftY = y*squareSize + y0      
            botRightX = topLeftX + squareSize      
            botRightY = topLeftY + squareSize
            create_mirrored_square((topLeftX, topLeftY, botRightX, botRightY), draw, random.choice(randColors), element, size)  
            element = element + 1    

'''
main method 

@size = Dimension of the sprite in px
@number = Number of sprites per row
@imgSize = Size of the squared image in px

The main method has 3 steps:
    - Dividing the image on equal squares to draw the different sprites
    - For every square created it will call "create_sprite" in order to draw inside the generated square
    - Saves the final image after all the sprites are drawed
'''
def main(size, invaders, imgSize):  
    origDimension = imgSize # Size of the sprites  
    origImage = Image.new('RGB', (origDimension, origDimension)) # Creates RGB squared image
    draw = ImageDraw.Draw(origImage)

    invaderSize = origDimension/invaders  
    padding = invaderSize/size

    print("Gesu perche non vuoi andare tu")

    '''
    For now we work by passing the top left and bottom right corner.
    This because the coordinates will serve both as dimensions and as coordinates for the box of each sprite 
    '''
    for x in range(0, invaders):    
        for y in range(0, invaders): 
            topLeftX = x*invaderSize + padding/2      
            topLeftY = y*invaderSize + padding/2      
            botRightX = topLeftX + invaderSize - padding      
            botRightY = topLeftY + invaderSize - padding
            create_sprite((topLeftX, topLeftY, botRightX, botRightY), draw, size) #does a similar thing tracing a grid for the sprite
    origImage.save("../Images/Sprites/"+str(size)+"x"+str(size)+"-"+str(invaders)+"-"+str(imgSize)+".jpg")

if __name__ == "__main__":  
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))