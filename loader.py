from flask import *
from db.interactions import *
from microservices.mail import EmailService

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4%234524Q8z\n\xec]/'
users = UsersDatabase()
skills = SkillsDatabase()
mailer_service = EmailService("smtp.mail.ru", 587, "damirrimskiy@mail.ru", "ksWuSnMTvRjRe6KFr97v")
feed = FeedManager()