from core.navigator import Browser

BASE_URL = "https://www.eurowin.bet"
API_BASE_URL = "https://eurowin.e-way.tech:3000"


class Api(Browser):

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        self.auth()

    def auth(self):
        if not self.username or not self.password:
            print("Usuário e senha não foram informados!!!")
            exit(0)
        payload = {
            "email": self.username,
            "password": self.password,
        }
        self.headers["host"] = API_BASE_URL.replace("https://", "")
        self.headers["origin"] = f"{BASE_URL}"
        self.headers["referer"] = f"{BASE_URL}/"
        response = self.send_request(
            "POST",
            f"{API_BASE_URL}/api/auth/getuser",
            data=payload,
            headers=self.headers
        )
        print(response)
        return response
