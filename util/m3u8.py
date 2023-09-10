# 4.08.2023

# Import
import os, re, glob, time, tqdm, requests, subprocess, sys, shutil
from functools import partial
from requests.models import Response
from multiprocessing.dummy import Pool
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

def get_fake_headers():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=10)
    user_agent = user_agent_rotator.get_random_user_agent()
    return {"User-Agent" : user_agent}

def get_custom_header():
    return  {
        'accept': '*/*',
        'accept-language': 'it-IT,it;q=0.9',
        'dnt': '1',
        'origin': 'https://www.xvideos.com',
        'User-Agent': get_fake_headers()['User-Agent']
    }

def download_ts_file(ts_url: str, store_dir: str, attemp=3):
    ts_name = ts_url.split('/')[-1].split("?")[0]
    ts_dir = store_dir + "/" + ts_name
    if(not os.path.isfile(ts_dir)):
        for i in range(attemp):
            try:
                ts_res = requests.get(ts_url, headers=get_custom_header())
                if(ts_res.status_code != 200):
                    print("GET TS => ", ts_name, " STATUS => ", ts_res.status_code , "RETRY == ", i)
                if(ts_res.status_code == 200):
                    break
                if(ts_res.status_code == 472):
                    print("TOO MUCH REQ")
                    sys.exit(0)
            except Exception:
                pass
            time.sleep(0.5)
        if isinstance(ts_res, Response) and ts_res.status_code == 200:
            with open(ts_dir, 'wb+') as f:
                f.write(ts_res.content)
        else:
            print(f"Failed to download streaming file: {ts_name}.")

def download(m3u8_link, merged_mp4):
    m3u8_http_base = m3u8_link.rstrip(m3u8_link.split("/")[-1])
    m3u8_content = requests.get(m3u8_link, headers=get_custom_header()).text
    m3u8 = m3u8_content.split('\n')
    ts_url_list = []
    ts_names = []
    for i_str in range(len(m3u8)):
        line_str = m3u8[i_str]
        if line_str.startswith("#EXTINF"):
            ts_url = m3u8[i_str+1]
            ts_names.append(ts_url.split('/')[-1])
            if not ts_url.startswith("http"):
                ts_url = m3u8_http_base + ts_url
            ts_url_list.append(ts_url)
    if(len(ts_url_list) != 0):
        os.makedirs("temp_ts", exist_ok=True)
        pool = Pool(20)
        gen = pool.imap(partial(download_ts_file, store_dir="temp_ts"), ts_url_list)
        for _ in tqdm.tqdm(gen, total=len(ts_url_list)):
            pass
        pool.close()
        pool.join()
        time.sleep(.5)
        downloaded_ts = sorted(glob.glob("temp_ts\*.ts"), key=lambda x:float(re.findall("(\d+)",x)[0]))
        files_str = "concat:"
        for ts_filename in downloaded_ts:
            files_str += ts_filename+'|'
        files_str.rstrip('|')
        subprocess.run(['ffmpeg', '-i', files_str, '-c', 'copy', '-bsf:a', 'aac_adtstoasc', merged_mp4], stderr=subprocess.DEVNULL)
        print("mp4 file merging completed.")
        shutil.rmtree("temp_ts")
    else:
        print("No file to download")