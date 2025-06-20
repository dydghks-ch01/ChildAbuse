from django.db import models

# Create your models here.
#add1_일일위험구현법
class Child(models.Model):
    id = models.AutoField(primary_key=True)  # 자동 증가 ID (새로운 primary key)
    teacher_id = models.ForeignKey('accounts.member', on_delete=models.CASCADE, to_field='userid')  # 교사 ID (외래키)
    name = models.CharField(max_length=100)  # 아이 이름
    sex = models.CharField(max_length=10)  # 성별
    age = models.IntegerField()  # 나이
    weight = models.FloatField()  # 몸무게
    height = models.FloatField()  # 키
    family_type = models.CharField(max_length=50)  # 가족 유형
    father_age = models.IntegerField()  # 아버지 나이
    mother_age = models.IntegerField()  # 어머니 나이
    region = models.CharField(max_length=50)  # 거주 지역
    depression = models.CharField(max_length=20)  # 우울감 정도
    parent_relation = models.CharField(max_length=20)  # 부모와의 관계
    friend_relation = models.CharField(max_length=20)  # 교우 관계
    state = models.CharField(max_length=50, default='낮음')

    def __str__(self):
        return self.name
#add2