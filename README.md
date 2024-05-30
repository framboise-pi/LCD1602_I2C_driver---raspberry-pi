# LCD1602_I2C_driver.py---raspberry-pi
driver version for LCD1602 display on I2C bus

## What's new in my version?
<ul>
  <li>display a progress bar - with options</li>
  <li>scroll text from right to left - with options</li>
  <li>scroll text from left to right - with options</li>
  <li>backlight alarm (multiple on/off sequence) - with option</li>
</ul>

## Examples
### Scroll Right <-> Left
`scroll_rl(text,line=1)`
<i> line is an option, 1 is default value as you can see</i>

```
import LCD1602_I2C_driver.py as driver
lcd1602 = driver.lcd()
lcd1602.scroll_rl("long text to display",2)
```
This will display the text string on line 2.

### BACKLIGHT ALARM
`backlight_alarm(alarms=2)`
<i> by default it switches Backlight 2 times</i>
```
import LCD1602_I2C_driver.py as driver
lcd1602 = driver.lcd()
lcd1602.backlight_alarm()
```

### PROGRESS BAR
<br>

`ShowProgBar(progbar_text="LOADING:", progbar_mini = 0, progbar_maxi = 100)`

<br>

```
import LCD1602_I2C_driver.py as driver
lcd1602 = driver.lcd()
# Create object progressbar
progbar = driver.ProgressBar(lcd1602)
progbar.ShowProgBar("STARTING...")
```
