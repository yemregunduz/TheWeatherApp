from tkinter import *
from PIL import ImageTk,Image
import requests
import tkinter as tk
url = 'http://api.openweathermap.org/data/2.5/weather'
apiKey = '3ea96a7555748ffb22671d9269aeaa8f'
iconUrl = 'http://openweathermap.org/img/wn/{}@2x.png'


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='black',justify = 'center'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.justify = justify
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

def getWeather(city):
    params = {'q':city,'appid':apiKey,'lang':'tr'}
    data = requests.get(url=url,params=params).json()
    if data:
        city = data['name'].capitalize()
        country = data['sys']['country']
        temp = int(data['main']['temp']-273.15)
        icon = data['weather'][0]['icon']
        condition= data['weather'][0]['description']
        return (city,country,temp,icon,condition)
    else: 
        locationLabel['text'] = 'Lütfen geçerli bir şehir giriniz.'

def main():
    city = cityEntry.get()
    weather = getWeather(city)
    if weather:
        locationLabel['text'] = '{},{}'.format(weather[0],weather[1])
        tempLabel['text'] = '{}°C'.format(weather[2])
        conditionLabel['text'] = weather[4]
        icon = ImageTk.PhotoImage(Image.open(requests.get(iconUrl.format(weather[3]),stream=True).raw))
        iconLabel.configure(image=icon)
        iconLabel.image = icon
        
app = Tk()

app.geometry('300x450')
app.title('Hava Durumu')

cityEntry = EntryWithPlaceholder(app,placeholder='Şehir ismi giriniz.',justify='center')
cityEntry.pack(fill=BOTH,ipady=10,padx=18,pady=5)


searchButton = Button(app,text='Search',font=('Arial',15),command=main)
searchButton.pack(fill=BOTH,ipady=10,padx=20)

iconLabel = Label(app)
iconLabel.pack()

locationLabel = Label(app,font=('Arial',40))
locationLabel.pack()

tempLabel = Label(app,font=('Arial',50,'bold'))
tempLabel.pack()

conditionLabel = Label(app,font=('Arial',20))
conditionLabel.pack()

app.mainloop()