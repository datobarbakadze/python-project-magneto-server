from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from controller import scripts_db
from selenium.webdriver.common.by import By
from threading import Thread
import time
import re
class Controls:
    def __init__(self):
        self.routines = {
            "url": {
                "action": lambda p: self.url_opener(url=p),
                "parameter": True
            },
            "skip_ads": {
                "action": lambda: self.ads_skipper(),
                "parameter": False,
            },
            "escape_age": {
                "action": lambda: self.age_escaper(),
                "parameter": False,
            },
            "exec": {
                "action": lambda p: self.driver.execute_script(p),
                "parameter": True
            },
            "volume": {
                "action": lambda p: self.change_volume(p),
                "parameter": True
            },
            "fullscreen": {
                "action": lambda: self.toggle_fullscreen(),
                "parameter": True
            },
            "time": {
                "action": lambda p: self.time_stter(p),
                "parameter": True
            },
            "play": {
                "action": lambda: self.play_toggle(),
                "parameter": False
            },
            "big_play": {
                "action": lambda: self.big_play_btn(),
                "parameter": False
            },
            "speed": {
                "action": lambda p: self.change_speed(p),
                "parameter": True
            },
            "sub": {
                "action": lambda p: self.change_subtitle_language(p),
                "parameter": True
            },
            "hide_settings": {
                "action": lambda: self.hide_settings(),
                "parameter":False
            },
            "fast_forward":{
                "action": lambda: self.fast_forward(),
                "parameter": False
            },
            "rewind": {
                "action": lambda: self.rewind(),
                "parameter": False
            },
            "captions": {
                "action": lambda: self.captions_toggle(),
                "parameter": False
            },
            "exp":{
              "action": lambda: self.experiment(),
              "parameter": False
            },

        }
        self.languages = dict()
        self.quality = dict()
        self.speed = dict()
        self.subtitles = dict()
        self.initialed = False
        self.age_skipped = False
        self.state_status = False
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("excludeSwitches", ['enable-automation'])
        self.options.add_argument("--start-maximized")
        self.request_in_progress =0
        
    def run(self, action, param=None):
        self.request_in_progress += 1
        if not self.initialed:
            self.initialed = True
            self.driver = webdriver.Chrome(options=self.options, executable_path="../chromedriver.exe")
            self.wait = WebDriverWait(self.driver, 100)

        if param == None:
            self.routines[action]["action"]()
        else:
            self.routines[action]["action"](param)
        self.request_in_progress -= 1
        return


    def url_opener(self,url):
        if self.driver:
            self.driver.get(url)
        return

    def age_escaper(self):
        self.driver.execute_script(scripts_db.scripts["escape_age"])
        self.url_opener(self.driver.current_url)
        return

    def ads_skipper(self):
        try:
            ads_script = scripts_db.scripts["skip_ads"]
            print(ads_script)
            self.driver.execute_script(ads_script)
        except:
            pass
        return

    def change_volume(self, vol_level):
        print("bolume changing")
        try:
            volume_script = scripts_db.scripts["volume"](vol_level)
            print(volume_script)
            self.driver.execute_script(volume_script)
        except:
            pass
        return

    def toggle_fullscreen(self):
        try:
            fullscreen_btn = self.driver.find_element_by_xpath('//html')
            ActionChains(self.driver).move_to_element(fullscreen_btn).send_keys("f").perform()
        except Exception as e:
            print(e)
            pass
        return

    def time_stter(self,timve_val):
        try:
            time_script = scripts_db.scripts["time"](timve_val)
            print(time_script)
            self.driver.execute_script(time_script)
        except:
            pass
        return
    def play_toggle(self):
        try:
            play_toggle_btn = self.driver.find_element_by_class_name("vjs-play-control")
            ActionChains(self.driver).move_to_element(play_toggle_btn).click().perform()
            # stream.sendall('json{"volume":1,"time":1}'.encode('utf-8'))
        except Exception as e:
            print(e)
        return
    def big_play_btn(self):
        try:
            big_play_button_script = scripts_db.scripts["big_play"]
            self.driver.execute_script(big_play_button_script)
            # stream.sendall('json{"volume":1,"time":1}'.encode('utf-8'))
        except:
            pass
        return

    def experiment(self):
        try:
            s = """{type":"moviePlayer/PLAYER_WATCHING","payload":{"movieId":4420,"time":1602049185352,"duration":8178.092,"watched":1000.464928,"playingEpisode":0,"playingSeason":0,"playingLanguage":"GEO","playingQuality":"HIGH","synced":false}}"""
            print(""" return window.localStorage.setItem('iMoviesCrossTabSync/broadcastAction','"""+s+"""') """)
            b = self.driver.execute_script(" return window.localStorage.setItem('iMoviesCrossTabSync/broadcastAction','"+s+"')")


        except Exception as e:
            print(e)
        return


    def movie_settings(self):
        settings_holder = self.wait.until(lambda d: d.find_element_by_class_name("vjs-movie-settings-menu-holder"))
        menus = settings_holder.find_elements_by_css_selector("ul.vjs-menu-content")
        for ul_index, ul in enumerate(menus):
            title = ul.find_element_by_xpath("li[@class='vjs-menu-title']").get_attribute("innerHTML").strip()
            for index, li in enumerate(ul.find_elements_by_css_selector("li.vjs-menu-item")):
                # Thread(target=self.reset, args=[ul_index,index]).start()
                value = li.find_element_by_class_name("vjs-menu-item-text").get_attribute(
                    'innerHTML').strip().lower()
                if title == "სიჩქარე":
                    self.speed[value] = [ul_index,index]
                elif title == "გახმოვანება":
                    self.languages[value] = [ul_index,index]
                elif title == "ხარისხი":
                    self.quality[value] = [ul_index,index]
                elif title == "სუბტიტრები":
                    self.subtitles[value] = [ul_index,index]
        print(self.quality)

        print(str(self.languages))

        print(str(self.speed))

        print(str(self.subtitles))
        return

    def reset(self,m,i):
        reset_script = scripts_db.scripts["reset_lang"](m, i)
        self.driver.execute_script(reset_script)
        return



    def change_speed(self,speed_val):
        try:
            if speed_val == "normal":
                speed_val="1"
            else:
                speed_val = re.sub("[^0-9\.]", "", speed_val)
            speed_script = scripts_db.scripts["speed"](speed_val)
            self.driver.execute_script(speed_script)
        except Exception as e:
            print(e)
            pass
        return

    def change_subtitle_language(self,key):
        try:
            self.movie_settings()
            element = self.subtitles[key]
            settings_script = scripts_db.scripts["settings"](element[0], element[1])
            print(settings_script)
            self.driver.execute_script(settings_script)
        except:
            pass
        return

    def hide_settings(self):
        try:
            settings_click_script = scripts_db.scripts["settings_click"]
            self.driver.execute_script(settings_click_script)
        except Exception as e:
            print(e)
            pass
        return

    def fast_forward(self):
        try:
            fast_forward_script = scripts_db.scripts["fast_forward"]
            self.driver.execute_script(fast_forward_script)
        except Exception as e:
            print(e)
            pass
        return

    def rewind(self):
        try:
            rewind_script = scripts_db.scripts["rewind"]
            self.driver.execute_script(rewind_script)
        except Exception as e:
            print(e)
            pass
        return

    def captions_toggle(self):
        try:
            captions_script = scripts_db.scripts["captions"]
            print(captions_script)
            self.driver.execute_script(captions_script)
        except Exception as e:
            print(e)
            pass
        return

    def state_stream(self, conn):
        self.state_status = True
        print("state check began")
        while self.state_status:
            if self.request_in_progress == 0:
                try:
                    time_state = self.driver.execute_script(scripts_db.state_control("video.currentTime"))
                    volume_state = self.driver.execute_script(scripts_db.state_control("video.volume"))
                    muted_state = self.driver.execute_script(scripts_db.state_control("video.muted"))
                    fullscreen_state = self.driver.execute_script(scripts_db.state_control("document.fullscreen"))
                    play_state = self.driver.execute_script(scripts_db.state_control("video.paused"))
                    print(play_state)
                    conn.sendall(bytes("json{\"volume\":" + str(volume_state) + ",\"time\":" + str(time_state) + ",\"muted\":" + str(muted_state).lower() + ",\"fullscreen\":"+str(fullscreen_state).lower()+",\"paused\":"+str(play_state).lower()+"}","utf-8"))
                except ConnectionAbortedError as e:
                    print("I am an exception"+str(e))
                    self.state_status = False
                    break

                except Exception as e:
                    print(e)
                    pass
            time.sleep(0.5)
        return

    def test(self):
        print("test success")


# if __name__ == "__main__":
#     obj = Controls()
#     obj.movie_settings()