from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from os import listdir
from os import path
import subprocess
import json

qtile_path = path.join(path.expanduser("~"), ".config", "qtile")


# THEME

theme = "material-darker" # only if available in ~/.config/qtile/themes

theme_path = path.join(qtile_path, "themes", theme)

# map color name to hex values
with open(path.join(theme_path, "colors.json")) as f:
    colors = json.load(f)
colorgb = colors['orange']
img = {}

# map image name to its path
img_path = path.join(theme_path, "img")
for i in listdir(img_path):
    img[i.split(".")[0]] = path.join(img_path, i)


# AUTOSTART

@hook.subscribe.startup_once
def autostart():
    script = path.join(qtile_path, "autostart.sh")
    subprocess.call([script])


# KEYS

mod = "mod1"

#          Special  KeyCap  Actions
keys = [Key(key[0], key[1], *key[2:]) for key in [
    # ------------ Window Configs ------------

    #Screenshots
    ([], "Print", lazy.spawn("escrotum -C")),
    ([mod], "Print", lazy.spawn("escrotum ~/Pictures/Screenshots/screenshot_%d_%m_%Y_%H_%M_%S.png")),
    ([mod, "shift"], "s", lazy.spawn("escrotum -s ")),

    # Switch between windows in current stack pane
    ([mod], "j", lazy.layout.down()),
    ([mod], "k", lazy.layout.up()),
    ([mod], "h", lazy.layout.left()),
    ([mod], "l", lazy.layout.right()),

    # Change window sizes
    ([mod, "control"], "h", lazy.layout.grow_left()),
    ([mod, "control"], "l", lazy.layout.grow_right()),
    ([mod, "control"], "j", lazy.layout.grow_down()),
    ([mod, "control"], "k", lazy.layout.grow_up()),
    ([mod], "n", lazy.layout.normalize()),

    # Move windows up or down in current stack
    ([mod, "shift"], "j", lazy.layout.shuffle_down()),
    ([mod, "shift"], "k", lazy.layout.shuffle_up()),
    ([mod, "shift"], "h", lazy.layout.shuffle_left()),
    ([mod, "shift"], "l", lazy.layout.shuffle_right()),
    ([mod], "space", lazy.layout.next()),

    # Toggle between different layouts as defined below
    ([mod], "Tab", lazy.next_layout()),

    # Qtile
    ([mod, "control"], "r", lazy.restart()),
    ([mod, "control"], "q", lazy.shutdown()),


    # Swap panes of split stack
    ([mod, "shift"], "space", lazy.layout.rotate()),
    ([mod, "shift"], "Return", lazy.layout.toggle_split()),

    # ------------ Apps Configs ------------

    ([mod], "w", lazy.window.kill()),
    ([mod], "q", lazy.spawn("rofi -show drun")),
    ([mod], "o", lazy.spawn("ms-office-online")),
    ([mod], "t", lazy.spawn("teams")),
    ([mod], "e", lazy.spawn("goneovim")),
    ([mod], "i", lazy.spawn("kitty")),
    ([mod], "r", lazy.spawncmd("picom --experimental-backends &")),

    # ------------ Hardware Configs ------------

    # Volume
    ([], "XF86AudioLowerVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ -5%"
    )),
    ([], "XF86AudioRaiseVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ +5%"
    )),
    ([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute @DEFAULT_SINK@ toggle"
    )),
    #Brightness
    ([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    ([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
]]


# GROUPS

groups = [Group(i) for i in [("TERM"), "DEV", "NET", "CHAT", "MEDIA"]]

for i, group in enumerate(groups):
    # Each workspace is identified by a number starting at 1
    actual_key = str(i + 1)
    keys.extend([
        # Switch to workspace N (actual_key)
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        # Send window to workspace N (actual_key)
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])
@hook.subscribe.startup_once
def color():
    if group.name==str("TERM") :
        colorgb = colors['green']
        return colorgb
    if group.name==str("MEDIA") :
        colorgb = colors['red']
        return colorgb
    if group.name==str("FS") :
        colorgb = colors['yellow']
        return colorgb


# LAYOUTS

layout_conf = {
    'border_focus': colors['fg3'][0],
    'border_width': 2,
    'border_normal': colors['bg1'][0],
    'margin': 3
}

layouts = [
        layout.Max(),
    layout.MonadTall(**layout_conf),
    #layout.MonadWide(**layout_conf),
    #layout.Matrix(columns=2, **layout_conf),
    layout.Bsp(**layout_conf),
    layout.Stack(
        **layout_conf,
        num_stacks=2,
        fair = True, 
        ),
    # layout.Columns(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]


# WIDGETS

# Reusable configs for displaying different widgets on different screens

def base(fg='bg0', bg='bg'):
    return {
        'foreground': colors[fg],
        'background': colors[bg]
    }


separator = {
    **base(),
    'linewidth': 0,
    'padding': 3,
}

group_box = {
    'foreground': colors['fg3'],
    'background': colors['fg3'],
    'font': 'Ubuntu Bold',
    'fontsize': 10,
    'margin_y': 3,
    'margin_x': 2,
    'padding_y': 4,
    'padding_x': 5,
    'borderwidth': 1,
    'block_highlight_text_color': colors['bg1'],
    'active': colors['bg0'],
    'inactive': colors['bg2'],
    'rounded': True,
    'highlight_method': 'block',
    'this_current_screen_border':colorgb ,
    'this_screen_border': colors['bg'],
    'other_current_screen_border': colors['orange'],
    'other_screen_border': colors['bg']
}

window_name = {
    **base(fg='fg'),
    'font': 'Ubuntu Bold',
    'fontsize': 11,
    'padding': 5
}

systray = {
    'background': colors['bg'],
    'padding': 5
}

text_box = {
    'font': 'Ubuntu',
    'fontsize': 13,
    'padding': 3
}

current_layout_icon = {
    'scale': 0.50,
    'background': colors['red'],
}

current_layout = {
    'padding': 5
}

clock = {
    'format': '%H:%M '
}

volume_icon = {
     'emoji':True,
     'fontsize': 15,
     'padding': 3
} 
pomodoro = {
    'background': colors['fg3'],
    'color_active': colors['bg'],
    'color_inactive': colors['bg'],
    'color_break' : colors['bg'],
    'padding': 5,
    'fontsize': 13,
    'font': 'Ubuntu',
    'prefix_inactive':'Work',
    'prefix_break':'',
    'prefix_pause':'',
    'prefix_active':'',
}

def workspaces():
    return [
        widget.Sep(**separator),
        widget.GroupBox(**group_box),
        widget.Image(
            filename=img['gb-dark']
        ),
        widget.Image(
            filename=img['testgb']
        ),
        widget.Sep(**separator),
        widget.WindowName(**window_name,format='{class}@mrmango1')
    ]


def powerline_base():
    return [
        widget.CurrentLayoutIcon(
            **current_layout_icon,
        ),
        widget.Image(
            filename=img['middle-red']
        ),
        widget.CurrentLayout(
            **base(bg='fg3'),
            **current_layout
        ),
        widget.Image(
            filename=img['s-green']
        ),
        widget.Image(
            filename=img['bg-green']
        ),
        widget.TextBox(
            **base(bg='green'),
            **text_box,
            text=''
        ),
        widget.Image(
            filename=img['middle-green']
        ),
        widget.Pomodoro(
            **pomodoro
        ),
        widget.Image(
            filename=img['s-yellow']
        ),
        widget.Image(
            filename=img['bg-yellow']
        ),
        widget.TextBox(
            **base(bg='yellow'),
            fontsize=21,
            padding=7,
            text='',
        ),
        widget.Image(
            filename=img['fg-yellow']
        ),
        widget.Clock(
            **base(bg='fg3'),
            **clock,
        ),
        widget.Image(
            filename=img['test1']
        ),
        widget.Image(
            filename=img['bg-blue']
        ),
        widget.Volume(
            **base(bg='blue'),
            **volume_icon
        ),
        widget.Image(
            filename=img['fg-blue']
        ),
        widget.Volume(
            **base(bg='fg3'),
            padding=5,
        )
    ]


laptop_widgets = [
    *workspaces(),

    widget.Sep(
        **separator
    ),
    widget.Systray(
        **systray
    ),
    widget.Sep(
        **separator
    ),
    widget.Image(
        filename=img['bg-red']
    ),
    widget.Image(
        filename=img['fg-red']
    ),
    *powerline_base(),
    widget.Sep(
        **separator
    ),
 ]


monitor_widgets = [
    *workspaces(),
    widget.Image(
        filename=img['bg-to-secondary']
    ),
    *powerline_base()
]

widget_defaults = {
    'font': 'Ubuntu Mono',
    'fontsize': 13,
    'padding': 2
}
extension_defaults = widget_defaults.copy()


# SCREENS

screens = [
    Screen(top=bar.Bar(laptop_widgets, 24, opacity=0.85))
]

# check connected monitors
monitors_status = subprocess.run(
    "xrandr | grep 'connected' | cut -d ' ' -f 2",
    shell=True,
    stdout=subprocess.PIPE
).stdout.decode("UTF-8").split("\n")[:-1]

if monitors_status.count("connected") == 2:
    screens.append(
        Screen(top=bar.Bar(monitor_widgets, 24, opacity=0.95))
    )


# MOUSE

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]


# OTHER STUFF

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
        float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='confirm'),  # gitk
    Match(wm_class='dialog'),  # gitk
    Match(wm_class='download'),  # gitk
    Match(wm_class='error'),  # ssh-askpass
    Match(title='file_progress'),  # gitk
    Match(title='notification'),  # GPG key password entry
    Match(wm_class='splash'),  # ssh-askpass
    Match(wm_class='toolbar'),  # ssh-askpass
    ],
    border_focus=colors["fg3"][0],
    border_width=0
)
auto_fullscreen = True
focus_on_window_activation = "smart"

wmname = "LG3D"
