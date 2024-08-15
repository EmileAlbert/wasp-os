# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2020 Daniel Thompson

import wasp
import icons
import fonts
import watch
import time
from micropython import const

_FRAC_TIME_MS = const(20000)
_PERIOD_TIME_MS = const(60000)

_STATE_IDLE = const(0)
_STATE_LOW = const(1)
_STATE_HIGH = const(2)


_Y_CENTER = const(120+40-36) # center + status bar height + font height


class Run20App():

    """Template application
    .. data:: ICON = RLE2DATA
       Applications can optionally provide an icon for display by the
       launcher. Applications that expect to be installed on the quick
       ring will not be listed by the launcher and need not provide any
       icon. When no icon is provided the system will use a default
       icon.
       The icon is an opportunity to differentiate your application from others
       so supplying an icon is strongly recommended. The icon, when provided,
       must not be larger than 96x64.
    """
    NAME = 'Run8020'
    ICON = icons.app

    def __init__(self):

        ''' Initialize the application'''

        self.button_down = 0
        self.button_up = 0

        #self._timer = wasp.widgets.Stopwatch_s(_Y_CENTER)
        self._timer = wasp.widgets.Stopwatch(_Y_CENTER)

        self._frac_counter = 0
        self._state = _STATE_IDLE


    def foreground(self):
        '''Activate the application'''
        self._draw()
        wasp.system.request_event(wasp.EventMask.TOUCH | wasp.EventMask.SWIPE_UPDOWN | wasp.EventMask.BUTTON)
        wasp.system.request_tick(97)


    def sleep(self):
        '''Notify the application the device is about to sleep'''
        return False


    def tick(self, ticks):

        '''Notify the application that its periodic tick is due'''
        self._update()


    def touch(self, event):
        '''Notify the application of a touchscreen touch event'''

        pass


    def swipe(self, event):
        '''Notify the application of a touchscreen swipe event'''

        if event[0] == wasp.EventType.UP : 
            pass 

        if event[0] == wasp.EventType.DOWN : 
            pass 

        else : 
            pass 

    def press(self, button, state):

        '''Notify the application of a button-press event'''

        # state == True if button pressed
        if not state :        
            self.button_up = wasp.watch.rtc.get_uptime_ms()
            press_time_ms = self.button_up - self.button_down
            # print('UP {}'.format(wasp.watch.rtc.get_uptime_ms()))

            # long press    
            if press_time_ms > 1000 :
                self._reset()

            # short press 
            elif press_time_ms > 10 :

                if self._timer.started:
                    self._timer.stop()

                else:
                    self._timer.start()
                    self._state = _STATE_HIGH
                    self._vibrate_start()

        else : 
            self.button_down = wasp.watch.rtc.get_uptime_ms()
            # print('DOWN {}'.format(wasp.watch.rtc.get_uptime_ms()))


    def _update(self):

        '''Update the dynamic parts of the application display'''
        wasp.system.bar.update()
        self._timer.update()

        if self._state == _STATE_HIGH and self._timer.count > _FRAC_TIME_MS/10 : 

            self._high_frac_end()


        if self._state == _STATE_LOW and self._timer.count > _PERIOD_TIME_MS/10 :

            self._low_frac_end()


    def _high_frac_end(self) :

        self._state = _STATE_LOW
        self._vibrate_start()

    def _low_frac_end(self) : 

        self._period_end()
        self._state = _STATE_HIGH
        self._vibrate_start()

    def _period_end(self) :

        self._timer.reset()

        self._frac_counter += 1
        print('PERIOD END - {}'.format(self._frac_counter))
        self._draw_frac_counter()

        self._timer.start()


    def _vibrate_start(self) : 

        # vibrator duty cycle off time value (short duty = high vibration)

        # One vibration for HIGH period start
        wasp.watch.vibrator.pulse(duty=25, ms=100)

        # One vibration more for LOW period start
        if self._state == _STATE_LOW :
            time.sleep_ms(500)
            wasp.watch.vibrator.pulse(duty=25, ms=100)


    def _reset(self) :

        self._timer.reset()
        self._frac_counter = 0
        self._draw_frac_counter()


    def _draw(self):

        '''Draw the display from scratch'''
        draw = wasp.watch.drawable
        draw.fill()

        wasp.system.bar.draw()
        self._timer.draw()
        self._draw_frac_counter()   

    def _draw_frac_counter(self):

        draw = wasp.watch.drawable

        draw.set_font(fonts.sans36)
        draw.set_color(wasp.system.theme('ui'))

        draw.string('{}'.format(self._frac_counter), 0, _Y_CENTER, 120)