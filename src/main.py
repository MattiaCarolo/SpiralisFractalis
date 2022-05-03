from components.App import App
from SpiralisFractalis import *


def main(result):
    
    # root = tk.Tk()
    # MainFrame(root)
    # root.geometry("500x500")
    #for x in result['fract']:
#        process_file(x, result['width'], result['height'],
    #        result['iterations'],'./IMGres/' + get_random_string(12) + '.png')
    app = App(fractal=result)
    app.mainloop()
 
    # canv = Canvas(root, width=500, height=500, bg='white')
    # canv.grid(row=1, column=1)
    
    # frame = Frame(root, height= 400, width=400)
    # root.columnconfigure(3)
    # root.rowconfigure(3)
    # frame.pack()
    # val1 = Label(root)
    # val1.grid(row= 0, column=2)
    
    #scalas = [Scale(root, from_= 0, to= 100) for _ in range(2)]
    
    # scalas[0].grid(row= 0, column=1)
    # scalas[0]['command'] = lambda x: update_val(x, val1)
    # 
    # scalas[1].grid(row= 1, column=1)
# 
    # 
    # img = get_img(".\FractalsEA_FrontEnd\src\images\SF22.jpg", shape= (200,200))
    # label = Label(root, image= img)
    # # label.pack()
    # img2 = get_img(".\FractalsEA_FrontEnd\src\images\SF22.jpg", shape= (200,200))
    # label2 = Label(root, image= img2)
    # # label2.pack()
    # label.grid(row= 0, column= 0)
    # label2.grid(row= 1, column=0)
    # 
    
    
    
    # label.pack()
    # # scalas[0].grid(row= 0,column= 1)
    # 
    # label2.pack()
    # #scalas[1].grid(row=1, column=1)
    
    # label2.pack()
    # label = ttk.Label(root)
    # label['image'] = ImageTk.PhotoImage(Image.open("images\SF22.jpg"))
    # root.mainloop()

if __name__ == "__main__":
    import sys

    # if there is one argument and it's not "-"
    if len(sys.argv) > 1 and sys.argv[1] != '-':
        # process each filename in input
        for filename in sys.argv[1:]:
            result = parse(filename)
            main(result)
            """
            process_file(result['fract'], result['width'],
                         result['height'], result['iterations'],
                         filename.split('.')[0] + '.png')
            """
    else:
        # read contents from stdin
        eval( sys.stdin.read() )
        process_file( fract, width, height, iterations)
