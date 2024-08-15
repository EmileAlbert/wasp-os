# This file is auto generated from the wasp.toml. Manual changes will be overwritten. 

software_list = (
    ('apps.user.alarm', 'Alarm'),
    ('apps.user.timer', 'Timer'),
    ('apps.user.calculator', 'Calculator'),
    ('apps.user.disa_b_l_e', 'DisaBLE'),
    ('apps.user.faces', 'Faces'),
)

faces_list = (
    ('apps.user.clock','Clock'),
    ('apps.user.week_clock','WeekClock'),
    ('apps.user.chrono','Chrono'),
)

autoload_list = (
    ('apps.user.week_clock.WeekClockApp', True, False, True),
    ('apps.user.stopwatch.StopwatchApp', True, False, False),
    ('apps.user.heart.HeartApp', True, False, False),
    ('apps.user.alarm.AlarmApp', False, False, False),
    ('apps.user.timer.TimerApp', False, False, False),
    ('apps.user.faces.FacesApp', False, False, True),
)

