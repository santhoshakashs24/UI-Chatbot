#!/usr/bin/python3

import re, os, sys, json, time
from datetime import datetime
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, ListProperty, ObjectProperty, OptionProperty
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.config import Config
from kivy.metrics import dp
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
import errno

#--------------Directory Variables----------------#
#Directory where the script resides
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

#Directory where the resources resides
RESOURCE_DIR = os.path.join(SCRIPT_DIR,'resources')

# Function to get the full path for a font file
def get_font_path(font_filename):
    return os.path.join(RESOURCE_DIR, 'fonts', font_filename)

# Get the directory of the current script or executable
if getattr(sys, 'frozen', False):
    # when we are running as a bundle
    bundle_dir = sys._MEIPASS
else:
    # when we are running in a normal Python environment
    bundle_dir = SCRIPT_DIR

#--------------Registering Fonts use----------------#
LabelBase.register(name="Proxima", fn_regular=get_font_path("proximanova_regular.ttf"))
LabelBase.register(name="Nunito", fn_regular=get_font_path("Nunito-Regular.ttf"))
LabelBase.register(name="Nunito-Light", fn_regular=get_font_path("Nunito-Light.ttf"))
LabelBase.register(name="Nunito-Bold", fn_regular=get_font_path("Nunito-Bold.ttf"))

#-------------------KIVY Config---------------------#
Config.set('input','mouse','mouse,multitouch_on_demand')
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
Window.size = (950,750)
Window.minimum_width, Window.minimum_height = Window.size

#-------------------Check if Log Folder Exists---------------------#
def mkdir_p(path):
    try:
        os.makedirs(path,exist_ok=True)
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

#-------------------Logging Configuration---------------------#
logger = logging.getLogger(__name__)
mkdir_p(os.path.join(SCRIPT_DIR,'logs'))
# create handler
handler = TimedRotatingFileHandler(filename=os.path.join(SCRIPT_DIR,'resources','lseg_chatbot.log'),when='D',interval=1,backupCount=15,encoding='utf-8',delay=False)

#create formatter and add to handler
formatter = Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

#add the handler to the named logger
logger.addHandler(handler)

#set the logging.level
logger.info("#" * 60)


#-------------------Read Stock Data File---------------------#
#Try to read the stock exchange data file and load it as stock_exchange_data - list of dictionary
try:
    file_path = os.path.join(RESOURCE_DIR, 'stock_exchange_data.json')
    with open(file_path,'r') as file:
        stock_exchange_data = json.load(file)
    if stock_exchange_data:
        logger.info("Stock Exchange data file read successfully!")
except:
    logger.error("Unable to read Stock data file")
    exit(0);


#-------------------Global Variables---------------------#
navigationOption = ['Main Menu','Go Back']                  #Navigation Options
selectedExchange = ""                                       #To store selected Exchange
selectedStock = ""                                          #To store selected Stock
stockPrice = ""                                             #To store the stock Price for selected Stock

#-------------------Component Classes---------------------#
# Command Class is User Selected Values - MDLabel Type with properties
class Command(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "Proxima"
    font_size = 28

# Response Class is Values Displayed by BOT - BoxLayout Type with Bot Image & properties
class Response(BoxLayout):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "Proxima"
    font_size = 24
    icon_source = StringProperty(os.path.join(RESOURCE_DIR, 'images','chatbot.ico'))

# Option Class to display available option - MDFillRoundFlatButton Type with disable button option once clicked
class Option(MDFillRoundFlatButton):
    scroll = ObjectProperty()
    id = NumericProperty()
    text = StringProperty() 
    type = OptionProperty('exchange',options=['exchange','stock','navigation'])    #Types of Options are defined based on which response is returned
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "Proxima"
    font_size = 18
    
    def disable_Button(self):
        global screen_manager
        item = screen_manager.get_screen('chats').ids.chat_list
        for w in item.children:
            try:
                if w.type == self.type:
                    w.disabled = True
            except:
                pass

#-------------------Main Class---------------------#
class LsegChatbot(MDApp):
    logo_source = StringProperty(os.path.join(RESOURCE_DIR, 'images','lseg_logo_rgb_pos.png'))  #LSEG Image location
    
    def navigationOption(self, *args):
        """Navigation Option to go back to Main Menu or previous option"""
        
        global navigationOption
        for i in range(len(navigationOption)):
            opt = Option(id=i,scroll=screen_manager.get_screen('chats').ids.chat_list,text=navigationOption[i],type="navigation",size_hint_x=LsegChatbot.contentSize(navigationOption[i]),halign = "center")
            screen_manager.get_screen('chats').chat_list.add_widget(opt)
        
    def getStockExchanges():
        """Gets stockExchanges from the stock_exchange_data list of dictionaries"""
        
        global stock_exchange_data
        stockExchanges = []
        for data in stock_exchange_data:
            stockExchanges.append(data['stockExchange'])
        return stockExchanges
            
    def stockExchangeOptions(self, *args):
        """Displays stock Exchanges for User to select on screen """
        
        message = f"Please select a Stock Exchange."
        screen_manager.get_screen('chats').chat_list.add_widget(Response(text=message,size_hint_x=LsegChatbot.contentSize(message),halign="center"))
        stockExchanges = LsegChatbot.getStockExchanges()
        for index,exchange in enumerate(stockExchanges):
            opt = Option(id=index,scroll=screen_manager.get_screen('chats').ids.chat_list,text=exchange,type="exchange",size_hint_x=LsegChatbot.contentSize(exchange),halign = "center")
            screen_manager.get_screen('chats').chat_list.add_widget(opt)
        logger.info(f"Stock Exchanges Displayed")
            
    def getStocksInExchange():
        """Gets just topStocks data from select stock_exchange"""
        
        global stock_exchange_data, selectedExchange
        stock_dict = {data['stockExchange']: data for data in stock_exchange_data}
        exchangeData = stock_dict.get(selectedExchange)
        if exchangeData:
            return exchangeData['topStocks']
        else:
            return None

    def getStocksInExchangeList():
        """Gets stockNames from all stocks in topStocks data"""
        
        stocksData = LsegChatbot.getStocksInExchange()
        stocks = []
        if stocksData:
            for data in stocksData:
                stocks.append(data['stockName'])
            return stocks
        else:
            return None
            
    def stockOptions(self, *args):
        """Displays stocks based on selected Stock Exchange on screen """
        
        global stock_exchange_data
        stocksData = LsegChatbot.getStocksInExchange()
        if stocksData:
            message = f"Please select a stock."
            screen_manager.get_screen('chats').chat_list.add_widget(Response(text=message,size_hint_x=LsegChatbot.contentSize(message),halign="center"))
            for index, stockData in enumerate(stocksData):
                opt = Option(id=index,scroll=screen_manager.get_screen('chats').ids.chat_list,text=stockData['stockName'],type="stock",size_hint_x=LsegChatbot.contentSize(stockData['stockName']),halign = "center")
                screen_manager.get_screen('chats').chat_list.add_widget(opt)
            logger.info("Stock Options Displayed")
        else:
            logger.error("No stocks found for the exchange")
            
    def displayStockPrice(self, *args):
        """Displays stock price for selected Stock """
        
        global selectedStock,stockPrice
        message = f"Stock Price of {selectedStock} is {stockPrice}. Please select an option."
        screen_manager.get_screen('chats').chat_list.add_widget(Response(text=message,size_hint_x=LsegChatbot.contentSize(message),halign="center"))
        logger.info(f"Stock Price Displayed for {selectedStock} - {stockPrice}")
        Clock.schedule_once(self.navigationOption,1)    
    
    def response(self, *args):
        """Handles all the Bot Responses"""
        
        global screen_manager, stock_exchange_data, selectedExchange, selectedStock
        logger.info(f"Selected Option: {value}")
        response = ""
        if value in LsegChatbot.getStockExchanges():
            Clock.schedule_once(self.stockOptions,1)
        elif value in LsegChatbot.getStocksInExchangeList():
            Clock.schedule_once(self.displayStockPrice,1)
        else:
            logger.info(f"Invalid Option")
        
    def optionSelect(self,id,type):
        """Handles Option Selection from User to assign values and invoke response method"""
        
        global screen_manager, selectedExchange, selectedStock,stockPrice, navigationOption, value
        if type == "exchange":
            selectedExchange = LsegChatbot.getStockExchanges()[id]
            value = selectedExchange
            size = LsegChatbot.contentSize(value)
            screen_manager.get_screen('chats').chat_list.add_widget(Command(text=value, size_hint_x=size, halign="center"))
            Clock.schedule_once(self.response, 1)
        elif type == "stock":
            selectedStock = LsegChatbot.getStocksInExchange()[id]['stockName']
            stockPrice = LsegChatbot.getStocksInExchange()[id]['price']
            value = selectedStock
            size = LsegChatbot.contentSize(value)
            screen_manager.get_screen('chats').chat_list.add_widget(Command(text=value, size_hint_x=size, halign="center"))
            Clock.schedule_once(self.response, 1)
        elif type == "navigation":
            if navigationOption[id] == 'Main Menu':
                Clock.schedule_once(self.stockExchangeOptions, 3)
            elif navigationOption[id] == 'Go Back':
                Clock.schedule_once(self.stockOptions,1)
        else:
            Clock.schedule_once(self.response, 1)
                 
        
    def contentSize(content):
        """Determines the length of the Text and defines the size for chatbot screen"""
        size = 0
        if len(content) < 6:
            size = .12
        elif len(content) < 11:
            size = .15    
        elif len(content) < 16:
            size = .20
        elif len(content) < 21:
            size = .25
        elif len(content) < 30:
            size = .30
        elif len(content) < 40:
            size = .40
        else:
            size = .45
        return size    
    
    def build(self):
        """Method which invokes the Chatbot screen & Welcome Message"""
        
        global screen_manager
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        logger.info(f"Session Start Time: {dt_string}")
        #Intializing Kivy Screen Manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file(os.path.join(bundle_dir, 'Chats.kv')))
        message = f"Hello! Welcome to LSEG. I'm here to help you."
        screen_manager.get_screen('chats').chat_list.add_widget(Response(text=message,size_hint_x=LsegChatbot.contentSize(message),halign="center"))
        Clock.schedule_once(self.stockExchangeOptions, 3)
        
        return screen_manager
    
    
if __name__=="__main__":
   LsegChatbot().run()
