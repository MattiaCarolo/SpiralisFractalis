from components.App import App
from SpiralisFractalis import *
from components.ga import Fractal


def main(fractals, width, height, numIterations):
    

    app = App(fractals, width, height, numIterations)
    app.mainloop()
 
  



def getFractalsListFromParsedJson(parsedJSON):
    pop = list()
    for fractal in parsedJSON['fract']:
        transformations = list()
        for i, x in enumerate(fractal["weights"]) :
            transform = fractal['matrixes'][i]
            transformations.append([
                transform[0][0],
                transform[1][0],
                transform[0][1],
                transform[1][1],
                transform[0][2],
                transform[1][2],
                x
            ])
        pop.append(Fractal(transformations=transformations))
    return pop


if __name__ == "__main__":
    import sys

    # if there is one argument and it's not "-"
    if len(sys.argv) > 1 and sys.argv[1] != '-':
        # process each filename in input
        for filename in sys.argv[1:]:
            parsedJSON = parse(filename)
            fractals = getFractalsListFromParsedJson(parsedJSON)
            width = parsedJSON['width']
            height = parsedJSON['height']
            numIterations = parsedJSON['iterations']
            #i = 0
            #for fractal in fractals:
            #    i += 1
            #    process_file(fractal, width, height, numIterations, './IMGres/' + str(i) + '.png')
                
            main(fractals, width, height, numIterations)
    else:
        # read contents from stdin
        eval( sys.stdin.read() )
        #process_file( fract, width, height, iterations)