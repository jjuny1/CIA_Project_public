import time
import os
import subprocess
import sys
import threading
import shutil
from PIL import Image
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({
    "warning": "bold yellow",
    "error": "bold red",
    "info": "bold cyan"
})


def clear_terminal():
    # 운영체제에 맞는 터미널 클리어 명령어 실행
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # MacOS, Linux
        os.system('clear')


def run_python_files(directory, file_list):
    os.chdir(directory)  # 지정된 디렉토리로 이동
    print(f"현재 디렉토리: {os.getcwd()}")

    for file in file_list:
        print(f"\n=== {file} 실행 중 ===")
        try:
            result = subprocess.run(['python', file], check=True)  # 파일 실행
            if result.returncode != 0:
                print(f"{file} 실행 중 오류 발생. 프로그램을 종료합니다.")
                sys.exit(result.returncode)  # 실행 중 오류 발생 시 프로그램 종료
        except subprocess.CalledProcessError as e:
            print(f"Error running {file}: {e}")
            sys.exit(e.returncode)  # 오류 발생 시 프로그램 종료
        print(f"=== {file} 완료 ===\n")



def img_to_ascii():
    # ASCII 문자의 맵핑 (밝기 순서 반대로)
    ASCII_CHARS = [" ", ".", ",", ":", ";", "+", "*", "?", "%", "S", "#", "@"]

    # 이미지를 리사이즈하고 변환하는 함수
    def resize_image(image, new_width=100):
        width, height = image.size
        aspect_ratio = height / width
        new_height = int(aspect_ratio * new_width * 0.55)  # 이미지 비율 맞추기
        return image.resize((new_width, new_height))

    def grayify(image):
        return image.convert("L")  # 이미지를 회색조로 변환

    def pixels_to_ascii(image):
        pixels = image.getdata()
        ascii_str = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])  # 각 픽셀을 ASCII 문자로 변환
        return ascii_str

    def image_to_ascii(image_path, new_width=128):
        image = Image.open(image_path)

        image = resize_image(image, new_width)
        image = grayify(image)

        ascii_str = pixels_to_ascii(image)
        img_width = image.width
        ascii_img = "\n".join([ascii_str[i:i + img_width] for i in range(0, len(ascii_str), img_width)])

        return ascii_img

    # 가운데 정렬 함수
    def center_ascii_art(ascii_art):
        # 터미널 너비 가져오기
        terminal_width = shutil.get_terminal_size().columns
        centered_art = []

        for line in ascii_art.splitlines():
            # 각 줄을 가운데로 맞추기
            line_length = len(line)
            padding = (terminal_width - line_length) // 2
            centered_line = ' ' * padding + line
            centered_art.append(centered_line)

        return "\n".join(centered_art)

    # ASCII 아트로 변환
    ascii_art = image_to_ascii("kshieldj.png", new_width=64)

    # 가운데 정렬
    centered_ascii_art = center_ascii_art(ascii_art)

    # 일반적인 print로 출력 (rich.print 대신 사용)
    print(centered_ascii_art)

def text_to_ascii():
    from pyfiglet import Figlet
    f = Figlet(font='roman', width=150)

    def DrawText(text, center=True):
        if center:
            print(*[x.center(shutil.get_terminal_size().columns) for x in f.renderText(text).split("\n")], sep="\n")
        else:
            print(f.renderText(text))

    DrawText('CIA_PROJECT', center=True)

# 터미널에서 텍스트를 가운데 정렬하는 함수
def center_text(text, is_korean=False):
    terminal_width = shutil.get_terminal_size().columns
    if is_korean:
        # 한글은 2배로 길이를 계산 (공백도 포함)
        text_length = sum(2 if ord(char) > 128 else 1 for char in text)  # 한글은 2, 영어는 1로 계산
    else:
        # 영어는 기본 길이 계산 (공백 포함)
        text_length = len(text)
    # 텍스트의 길이를 기준으로 공백 추가하여 가운데 정렬
    spaces = (terminal_width - text_length) // 2
    return ' ' * spaces + text

# 이탤릭체 적용 후 가운데 정렬된 텍스트 출력 함수
def print_italic_centered(text, is_korean=False):
    # 터미널에서 이탤릭체가 지원되는지 확인해야 함 (이탤릭체 지원 여부는 환경에 따라 달라짐)
    # ANSI 이스케이프 시퀀스를 사용하여 이탤릭체 적용
    italic_text = f"\x1B[3m{text}\x1B[23m"
    # 가운데 정렬 후 출력
    centered_text = center_text(italic_text, is_korean)
    print(centered_text)

def make_choice():
    while True:
        user_input = input(">> ✔ 하고자 하는 작업을 고르십시오. (1 또는 2): ").strip()  # 사용자 입력 받기

        if user_input == "1":
            # 새로운 게시물 탐색
            directory = "./Data_Crawling_bot"
            python_files = ["google_crawlbot.py", "csv_clean.py", "ExtractID.py", "csv_to_sqldb.py"]  # 실행 순서에 맞게 파일 리스트 작성
            run_python_files(directory, python_files)
            
            second_choice = input(">> ✔ 검색 데이터가 모두 정리되었습니다. 이어서 Telegram 계정 분석도 하시겠습니까? (y/n) : ").strip()
            if second_choice.lower() == "y":
                second_directory = "../Telegram_Search_bot"
                python_files = ["configure.py", "create_DB.py", "channel.py", "message.py", "telegram_to_html.py"]
                run_python_files(second_directory, python_files)
            break  # 올바른 입력이므로 루프 종료

        elif user_input == "2":
            # 기존 Telegram 계정 분석
            print("분석 전에, /Telegram_Search_bot/message.json을 올바르게 작성하였는지 반드시 확인해주십시오.")
            time.sleep(3)
            directory = "./Telegram_Search_bot"
            python_files = ["configure.py", "create_DB.py", "channel.py", "message.py", "telegram_to_html.py"]
            run_python_files(directory, python_files)

            break  # 올바른 입력이므로 루프 종료

        else:
            print("잘못된 입력입니다. 다시 입력해주십시오.")

# 스피너 애니메이션 함수
def spinner():
    for char in "|/-\\":
        sys.stdout.write(char)  # 캐릭터 출력
        sys.stdout.flush()  # 즉시 출력
        time.sleep(0.1)  # 애니메이션 속도
        sys.stdout.write('\b')  # 이전 캐릭터 지우기

# 스피너를 백그라운드에서 실행
def spinner_thread():
    while not stop_spinner:  # 스피너를 멈추는 조건
        spinner()

# 프로세스가 돌아가는 효과를 주기 위한 스피너 실행 예시
def install_requirements():
    print("Initializing ...")
    global stop_spinner
    stop_spinner = False
    spinner_thread_instance = threading.Thread(target=spinner_thread)  # 스피너 백그라운드 스레드 시작
    spinner_thread_instance.start()
    
    try:
        # subprocess로 pip install -q -r requirements.txt 실행
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
        print("Requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")  # 실제 작업이 진행되는 동안(예: pip 설치 시) 대체
    finally:
        stop_spinner = True  # 작업이 완료되면 스피너 멈춤
        spinner_thread_instance.join()  # 스레드 종료 대기

if __name__ == "__main__":
    install_requirements()
    time.sleep(2)
    clear_terminal()
    img_to_ascii()  # 케쉴주 이미지 띄우기
    text_to_ascii()  # CIA_PROJECT 글자 띄우기
    time.sleep(1)
    print_italic_centered("Organized crime constitutes nothing less than a guerilla war against society.")
    print_italic_centered("    조직화된 범죄는 반사회적인 게릴라 전쟁과 다를 바 없다.", is_korean=True)
    print_italic_centered("- Lyndon B. Johnson -")
    time.sleep(2)

    print("\n\n")
    print("CIA_PROJECT Shell \nCopyright (C) TEAM_CIA & ws1004. All rights reserved.")
    time.sleep(1)

    print("\n")
    console = Console(theme=custom_theme)
    print("단독으로 실행하기 원하는 프로세스가 있다면, readme를 참고하여 powershell 명령으로 실행하십시오.\n")
    console.print(":mag: 1) 새로운 게시물 탐색 | :mobile_phone: 2) 기존 Telegram 계정 분석")
    make_choice()
