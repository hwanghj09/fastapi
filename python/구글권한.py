users = [
    {
        "name" : "황현준",
        "password" : "1234",
        "chage_text_authority" : True,
        "view_text_authority" : True
    },
    {
        "name" : "황주하",
        "password" : "1234",
        "chage_text_authority" : False,
        "view_text_authority_text_authority" : True
    },
    {
        "name" : "임태윤",
        "chage_text_authority" : False,
        "view_text_authority" : False
    }
]

text = "마ㅣㄴㅇ러ㅣㅁ나ㅓ리ㅏㄴ어리ㅏㅁㄴ어라넘이ㅏㄹㄴㅇ"
IsLogin = {"name": None, "status": False} 


def authority(_name,_authority):
    for user in users:
        if(user["name"] == _name):
            if user[_authority]:
                return True
            else:
                return False

def login():
    global IsLogin
    username = input("사용자 이름을 입력하세요 : ")
    password = input("비밀번호를 입력하세요 : ")

    for user in users:
        if user["name"] == username and user["password"] == password:
            IsLogin["name"] = username
            IsLogin["status"] = True
            print("로그인 성공")
            main()

    print("로그인 실패. 다시 시도하세요.")
    login()
            
def register():
    username = input("사용자 이름을 입력하세요 : ")
    password = input("비밀번호를 입력하세요 : ")
    check_password = input("다시 비밀번호를 입력하세요 : ")

    if password == check_password:
        for user in users:
            if user["name"] == username:
                print("이미 존재하는 사용자 이름입니다. 다른 이름을 입력하세요.")
                register()
                return  # 이미 존재하는 경우 함수 종료

        new_user = {
            "name": username,
            "password": password,
            "change_text_authority": False,
            "view_text_authority": False
        }
        users.append(new_user)
        print("회원가입 성공")
        main()
    else:
        print("비밀번호가 일치하지 않습니다. 다시 시도해주세요.")
        register()

def showtext():
    global text
    if authority(IsLogin["name"], "view_text_authority"):
        print(text)
        main()
        return

    print("텍스트를 보기 위한 권한이 없습니다.")
    main()

def edittext():
    global text
    if authority(IsLogin["name"], "chage_text_authority"):
        print("현재 텍스트:", text)
        new_text = input("변경할 텍스트 입력: ")
        text = new_text
        print("변경된 텍스트:", text)
        main()

def goto(number):
    if number==1:
        login()
    elif number==2:
        register()
    elif number==5:
        print(users)
        main()
    elif IsLogin["status"]:
        if number == 3:
            showtext()
        elif number == 4:
            edittext()
        else:
            print("Error")
    else:
        print("Error")

def main():
    print("----------------------------")
    print("1. 로그인")
    print("2. 회원가입")
    print("3. 텍스트 보기")
    print("4. 텍스트 변경")
    print("5. 유저 보기")
    print("----------------------------")
    usenumber = int(input("번호를 입력하세요 : "))
    goto(usenumber)

main()