
scripts = {
    "skip_ads": """
        var ad_button = document.getElementsByClassName('vjs-skip-button-wrapper')[0];
        ad_button.click();
     """,
    "alert": "alert('hello world');\n",
    "escape_age": "document.cookie='age-confirmed=1986-01-05'\n",
    "volume": lambda vol: control_volume(vol),
    "time": lambda t: set_time(t),
    "big_play": """
        var big_play = document.getElementsByClassName('vjs-big-play-button')[0];
        big_play.click();
    """,
    "settings": lambda menu, item: settings_script(menu, item),
    "speed": lambda speed: """
        var speed_video = document.getElementsByClassName('vjs-tech')[0]; 
        speed_video.playbackRate = """+speed+""";
    """,
    "settings_click": """
        var l = document.getElementsByClassName('vjs-movie-settings-icon')[0];
        l.click();
    """,
    "reset_lang": lambda m,i: reset_langs_script(m,i),
    "fast_forward": """
        var forward_video = document.getElementsByClassName('vjs-tech')[0]; 
        forward_video.currentTime+=5;
    """,
    "rewind": """
        var rewind_video = document.getElementsByClassName('vjs-tech')[0]; 
        rewind_video.currentTime-=5;
    """,
    "captions": """
        var captions = document.getElementsByClassName('vjs-captions-toggle')[0];
        captions.click();
    """,






    "current_volume": """
    word
        var video = document.getElementsByClassName('vjs-tech')[0]; 
            return video.currentTime;
    """,

    "mute_check":"""
        
    """
}

def state_control(word):
    return """
            var video = document.getElementsByClassName('vjs-tech')[0]; 
                return """+word+""";
        """


def set_time(time_val):
    time_setter_script =  """
        var t_video = document.getElementsByClassName('vjs-tech')[0]; 
        t_video.currentTime = {0};
    """
    return time_setter_script.format(str(time_val))


def control_volume(volume_level):
    print("level 2 is begining")
    unmute_script=""
    if(float(volume_level)!=0):
        unmute_script = "if (muted=='muted'){" \
                        "var mute_control = document.getElementsByClassName('vjs-mute-control')[0];" \
                        " mute_control.click();" \
                        "}"

    script_string = """ 
            var video = document.getElementsByClassName('vjs-tech')[0]; 
            var muted = video.getAttribute("muted")
            {0}
            video.volume = {1};
    """
    return script_string.format(unmute_script,str(volume_level))

def reset_langs_script(m,i):
    script = """
        var m = document.getElementsByClassName('vjs-menu')[{0}];
        var i = m.getElementsByClassName('vjs-menu-item')[{1}];
        i.classList.remove("vjs-selected");
        i.setAttribute('aria-checked',false);
    """
    return script.format(str(m), str(i))

def settings_script(menu, item):
    script = """
        var menu = document.getElementsByClassName('vjs-menu')[{0}];
        var item = menu.getElementsByClassName('vjs-menu-item')[{1}];
        console.log(item);
        return item.click();
        
    """
    return script.format(str(menu),str(item))