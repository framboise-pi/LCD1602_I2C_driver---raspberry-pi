# -*- coding: utf-8 -*-
# Original code found at:
# https://gist.github.com/DenisFromHR/cc863375a6e19dce359d
# http://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/

"""
###
# original driver code: DenisFromHR (Denis Pleic)
# 2015-02-10, ver 0.1
# progressbar by Dmitry Safonov
# https://custom-characters-for-lcd16x2.streamlit.app/
########
# github.com/framboise-pi ### Camille Lafontaine <codelibre.fr>
# 2024-april LCD1602_I2C_driver.py ver 0.1
#
#
#  ▄▄·       ·▄▄▄▄  ▄▄▄ .▄▄▌  ▪  ▄▄▄▄· ▄▄▄  ▄▄▄ .   ·▄▄▄▄▄▄  
# ▐█ ▌▪▪     ██▪ ██ ▀▄.▀·██•  ██ ▐█ ▀█▪▀▄ █·▀▄.▀·   ▐▄▄·▀▄ █·
# ██ ▄▄ ▄█▀▄ ▐█· ▐█▌▐▀▀▪▄██▪  ▐█·▐█▀▀█▄▐▀▀▄ ▐▀▀▪▄   ██▪ ▐▀▀▄ 
# ▐███▌▐█▌.▐▌██. ██ ▐█▄▄▌▐█▌▐▌▐█▌██▄▪▐█▐█•█▌▐█▄▄▌   ██▌.▐█•█▌
# ·▀▀▀  ▀█▄▀▪▀▀▀▀▀•  ▀▀▀ .▀▀▀ ▀▀▀·▀▀▀▀ .▀  ▀ ▀▀▀  ▀ ▀▀▀ .▀  ▀
#
########
"""

# i2c bus (0 -- original Pi, 1 -- Rev 2 Pi)
I2CBUS = 1

# LCD Address
ADDRESS = 0x27

import smbus
import time
from time import sleep
from re import match

class i2c_device:
   def __init__(self, addr, port=I2CBUS):
      self.addr = addr
      self.bus = smbus.SMBus(port)

# Write a single command
   def write_cmd(self, cmd):
      self.bus.write_byte(self.addr, cmd)
      sleep(0.0001)

# Write a command and argument
   def write_cmd_arg(self, cmd, data):
      self.bus.write_byte_data(self.addr, cmd, data)
      sleep(0.0001)

# Write a block of data
   def write_block_data(self, cmd, data):
      self.bus.write_block_data(self.addr, cmd, data)
      sleep(0.0001)

# Read a single byte
   def read(self):
      return self.bus.read_byte(self.addr)

# Read
   def read_data(self, cmd):
      return self.bus.read_byte_data(self.addr, cmd)

# Read a block of data
   def read_block_data(self, cmd):
      return self.bus.read_block_data(self.addr, cmd)


# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100 # Enable bit
Rw = 0b00000010 # Read/Write bit
Rs = 0b00000001 # Register select bit

class lcd:
   #initializes objects and lcd
   def __init__(self):
      self.lcd_device = i2c_device(ADDRESS)

      self.lcd_write(0x03)
      self.lcd_write(0x03)
      self.lcd_write(0x03)
      self.lcd_write(0x02)

      self.lcd_write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
      self.lcd_write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
      self.lcd_write(LCD_CLEARDISPLAY)
      self.lcd_write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
      sleep(0.2)

   # clocks EN to latch command
   def lcd_strobe(self, data):
      self.lcd_device.write_cmd(data | En | LCD_BACKLIGHT)
      sleep(.0005)
      self.lcd_device.write_cmd(((data & ~En) | LCD_BACKLIGHT))
      sleep(.0001)

   def lcd_write_four_bits(self, data):
      self.lcd_device.write_cmd(data | LCD_BACKLIGHT)
      self.lcd_strobe(data)

   # write a command to lcd
   def lcd_write(self, cmd, mode=0):
      self.lcd_write_four_bits(mode | (cmd & 0xF0))
      self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))

   # write a character to lcd (or character rom) 0x09: backlight | RS=DR<
   # works!
   def lcd_write_char(self, charvalue, mode=1):
      self.lcd_write_four_bits(mode | (charvalue & 0xF0))
      self.lcd_write_four_bits(mode | ((charvalue << 4) & 0xF0))
  
   # put string function with optional char positioning
   def lcd_display_string(self, string, line=1, pos=0):
    if line == 1:
      pos_new = pos
    elif line == 2:
      pos_new = 0x40 + pos
    elif line == 3:
      pos_new = 0x14 + pos
    elif line == 4:
      pos_new = 0x54 + pos

    self.lcd_write(0x80 + pos_new)

    for char in string:
      self.lcd_write(ord(char), Rs)

   # put extended string function. Extended string may contain placeholder like {0xFF} for
   # displaying the particular symbol from the symbol table
   def lcd_display_extended_string(self, string, line):
      if line == 1:
         self.lcd_write(0x80)
      if line == 2:
         self.lcd_write(0xC0)
      if line == 3:
         self.lcd_write(0x94)
      if line == 4:
         self.lcd_write(0xD4)
      # Process the string
      while string:
         # Trying to find pattern {0xFF} representing a symbol
         result = match(r'\{0[xX][0-9a-fA-F]{2}\}', string)
         if result:
            self.lcd_write(int(result.group(0)[1:-1], 16), Rs)
            string = string[6:]
         else:
            self.lcd_write(ord(string[0]), Rs)
            string = string[1:]

   # clear lcd and set to home
   def lcd_clear(self):
      self.lcd_write(LCD_CLEARDISPLAY)
      self.lcd_write(LCD_RETURNHOME)

   # define backlight on/off (lcd.backlight(1); off= lcd.backlight(0)
   def backlight(self, state): # for state, 1 = on, 0 = off
      if state == 1:
         self.lcd_device.write_cmd(LCD_BACKLIGHT)
      elif state == 0:
         self.lcd_device.write_cmd(LCD_NOBACKLIGHT)

   # add custom characters (0 - 7)
   def lcd_load_custom_chars(self, fontdata):
      self.lcd_write(0x40);
      for char in fontdata:
         for line in char:
            self.lcd_write_char(line)

#########
#
# NEW 2024 SECTION UNDER HERE.
#
#########

   # scroll text right to left - line 1 by default
   def scroll_rl(self,text,line=1):
      str_empty = " " * 16
      # starting 4 digits later is more readable
      text = "    "+text
      for i in range (0, len(text)):
         text_display = text[i:(i+16)]
         self.lcd_display_string(text_display,line)
         time.sleep(0.4)
         self.lcd_display_string(str_empty,line)
         
   # scroll text right to left - line 1 by default
   def scroll_lr(self,text,line=1):
      str_empty = " " * 16
      for i in range (0, len(text)):
         text_display = padded_string[((len(text)-1)-i):-i]
         self.lcd_display_string(text_display,1)
         sleep(0.4)
         self.lcd_display_string(padding[(15+i):i], 1)
   
   # switch backlight on/off - 2 times by default
   def backlight_alarm(self,alarms=2):
      for i in range(alarms):
         self.backlight(0)
         time.sleep(0.5)
         self.backlight(1)
         time.sleep(0.5)
         
class ProgressBar:
   def __init__(self, lcd):
      self.lcd = lcd
      self.char_1_data = ["01111",
      "11000",
      "10011",
      "10111",
      "10111",
      "10011",
      "11000",
      "01111"]
      
      self.char_2_data = ["01111",
      "11000",
      "10000",
      "10000",
      "10000",
      "10000",
      "11000",
      "01111"]
                  
      self.char_3_data = ["11111",
      "00000",
      "11011",
      "11011",
      "11011",
      "11011",
      "00000",
      "11111"]
      
      self.char_4_data = ["11111",
      "00000",
      "00000",
      "00000",
      "00000",
      "00000",
      "00000",
      "11111"]
                  
      self.char_5_data = ["11110",
      "00011",
      "11001",
      "11101",
      "11101",
      "11001",
      "00011",
      "11110"]
      # Progessbar Right empty character. Code {0x05}.
      self.char_6_data = ["11110",
      "00011",
      "00001",
      "00001",
      "00001",
      "00001",
      "00011",
      "11110"]
      # Unused - Data for custom character #7. Code {0x06}
      self.char_7_data = ["11111",
      "10001",
      "10001",
      "10001",
      "10001",
      "10001",
      "10001",
      "11111"]
      # Unused - Data for custom character #8. Code {0x07}
      self.char_8_data = ["11111",
      "10001",
      "10001",
      "10001",
      "10001",
      "10001",
      "10001",
      "11111"]
      # 8 digits kept, 6 are used yet
      self.chars_list = [self.char_1_data, self.char_2_data, self.char_3_data, self.char_4_data,
         self.char_5_data, self.char_6_data, self.char_7_data, self.char_8_data]

      # load 8 characters adresses to RAM
      char_load_cmds = [0x40, 0x48, 0x50, 0x58, 0x60, 0x68, 0x70, 0x78]

      for char_num in range(8):
         self.lcd.lcd_write(char_load_cmds[char_num])

         for line_num in range(8):
            line = self.chars_list[char_num][line_num]
            binary_str_cmd = "0b000{0}".format(line)
            self.lcd.lcd_write(int(binary_str_cmd, 2), Rs)
         
   def ShowProgBar(self,progbar_text="LOADING:", MIN = 0, MAX = 100):
     
      progbar_value = 0
      progbar_delta = 5
      progbar_cells = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      progbar_showing = True
      
      self.lcd.lcd_display_string(progbar_text, 1)

      while progbar_showing is True:
         progbar_string = ""
         for i in range(10):
            if i == 0:#first/left rounded cell
                if progbar_cells[i] == 0:
                    progbar_string = progbar_string + "{0x01}"#empty cell
                else:
                    progbar_string = progbar_string + "{0x00}"#full cell
            elif i == 9:
                # Right character
                if progbar_cells[i] == 0:
                    # Right empty character
                    progbar_string = progbar_string + "{0x05}"
                else:
                    # Right full character
                    progbar_string = progbar_string + "{0x04}"
            else:
                # Central character
                if progbar_cells[i] == 0:
                    # Central empty character
                    progbar_string = progbar_string + "{0x03}"
                else:
                    # Central full character
                    progbar_string = progbar_string + "{0x02}"
         
         # Print
         self.lcd.lcd_display_extended_string(progbar_string + " {0}% ".format(progbar_value), 2)
         
         # Update the charge and recalculate bar_repr
         progbar_value += progbar_delta
         if (progbar_value >= MAX) or (progbar_value <= MIN):
            progbar_delta = -1 * progbar_delta
            
         for i in range(10):
            if progbar_value >= ((i + 1) * 10):
               progbar_cells[i] = 1
            else:
               progbar_cells[i] = 0
               
         if (progbar_value >= MAX):
            progbar_showing = False
            self.lcd.lcd_clear()
      
         # Wait for some time
         sleep(0.1)
