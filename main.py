from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image as CoreImage
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.graphics import Color,Rectangle
from kivy.core.clipboard import Clipboard
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.config import Config

#connecting with kv file
Builder.load_file("pick_color_from_image.kv")

# note that origin of Image will start from bottom left but origin of coreimage will start from top left

class MyImage(Image):
    def on_touch_down(self,touch):
        if (touch.x-self.x)<=self.width and (touch.y-self.y)<=self.height  and (touch.x-self.x)>=0 and (touch.y-self.y)>0 :
            
            
            self.parent.pixel=(self.parent.coreimage.read_pixel((self.texture.width -( touch.x-self.x)*self.parent.ratio[0] ),(self.texture.height-(touch.y-self.y)*self.parent.ratio[1])))
            pixel=self.parent.pixel
            #for black and white images i.e. images without an alpha channel
            if len(pixel)==3:
                pixel.append(1)
            #displaying color in canvas of label
            with self.parent.ids.label.canvas.before:
                Color(*pixel)
                Rectangle(size=self.parent.ids.label.size,pos=self.parent.ids.label.pos)
            self.parent.ids.label.text="(%d, %d , %d , %.2f)"%(pixel[0]*255,pixel[1]*255,pixel[2]*255,pixel[3])
            
            #changing copy btn opacity to 1
            self.parent.ids.copy_btn.opacity=1
            

            

class MyLayout(BoxLayout):
    def choose_image(self,filename):
        
        filechooser=self.ids.filechooser
        if filename:
            if filename[0].split(".")[1]=="png" or filename[0].split(".")[1]=="jpg" or filename[0].split(".")[1]=="jpeg":
                # for getting color of pixel we use read_pixel() and for this the image should be there in the memory and for this we need to make keep_data =True

                self.coreimage=CoreImage(filename[0],keep_data=True,size=(min(self.width,self.height)*0.6,min(self.width,self.height)*0.6))
                self.texture=self.coreimage.texture


                self.image=MyImage(texture=self.texture,size=(min(self.width,self.height)*0.6,min(self.width,self.height)*0.6),size_hint=(None,None ),keep_ratio=False,allow_stretch=True,pos_hint={'center_x':0.5})


                self.remove_widget(filechooser)
                self.add_widget(self.image)

                self.ratio=(self.texture.size[0]/(min(self.width,self.height)*0.6),self.texture.size[1]/(min(self.width,self.height)*0.6))
                self.ids.new_image_btn.opacity=1
        
    def copy_color(self,*args):
        Clipboard.copy("(%.2f, %.2f , %.2f , %.2f)"%(self.pixel[0],self.pixel[1],self.pixel[2],self.pixel[3]))
        
        #animating and changing text of copy_btn to indicate that color has been copied
        self.ids.copy_btn.text="Copied"
        anim=Animation(size=(220,60),duration=0.25)
        anim+=Animation(size=(200,50),duration=0.25)
        
        anim.start(self.ids.copy_btn)
        Clock.schedule_once(self.copy_btn_text_change,0.5)

    def copy_btn_text_change(self,*args):
        
        self.ids.copy_btn.text="Copy"

    def new_image(self,*args):
        self.ids.label.canvas.before.clear()
            
        self.clear_widgets()
        self.add_widget(self.ids.filechooser)
        self.add_widget(self.ids.copy_btn)
        self.add_widget(self.ids.label)
        self.add_widget(self.ids.new_image_btn)

        
        self.ids.new_image_btn.opacity=0
        self.ids.copy_btn.opacity=0


        self.ids.label.text="Choose Image\n\n Made By Aniket Thani"
        
        
        self.ids.filechooser.selection=[]
class ColorPickerApp(App):
    def build(self):
        return MyLayout()

if __name__=="__main__":
    Config.set('graphics','resizable','False')

    ColorPickerApp().run()