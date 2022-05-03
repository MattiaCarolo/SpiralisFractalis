from components.App import App




def main():
    
    # root = tk.Tk()
    # MainFrame(root)
    # root.geometry("500x500")
   
    app = App()
    app.mainloop()
 
    # canv = Canvas(root, width=500, height=500, bg='white')
    # canv.grid(row=1, column=1)
    
    # frame = Frame(root, height= 400, width=400)
    # root.columnconfigure(3)
    # root.rowconfigure(3)
    # frame.pack()
    #val1 = Label(root)
    #val1.grid(row= 0, column=2)
    
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
    main()
