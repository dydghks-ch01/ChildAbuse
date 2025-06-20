from django.db import models

# Create your models here.
#add1_로그인구현법
class Member(models.Model):
    userid = models.CharField(max_length=50, unique=True)  # 사용자 ID (문자열, 고유)
    pw = models.CharField(max_length=128)  # 비밀번호 (문자열)

    def __str__(self):
        return self.userid
#add2
class Survey(models.Model):
    name = models.CharField(max_length=100)  # 이름
    user_id = models.CharField(max_length=100)  # 아이디
    위험도 = models.CharField(max_length=50)  # 위험도 (낮음, 보통, 높음)
    
    def __str__(self):
        return f"{self.name} ({self.user_id}) - {self.위험도}"

class Manage(models.Model):
    name = models.CharField(max_length=100)  # 이름
    user_id = models.CharField(max_length=100)  # 아이디
    항목1 = models.CharField(max_length=255)  # 항목 1
    항목2 = models.CharField(max_length=255)  # 항목 2
    항목3 = models.CharField(max_length=255)  # 항목 3
    # 필요에 따라 더 많은 항목들을 추가할 수 있습니다.

    def __str__(self):
        return f"{self.name} ({self.user_id})"