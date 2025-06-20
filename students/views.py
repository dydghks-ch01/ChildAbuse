#add1_일일위험구현법
from django.shortcuts import render, redirect, get_object_or_404
from .models import Child
from django.contrib import messages
import logging
from accounts.models import Member

logger = logging.getLogger(__name__)
def manage(request):
    # 모든 아동 데이터를 가져옴
    children = Child.objects.all()
    return render(request, 'manage.html', {'children': children})

def manage_form(request):
    if request.method == 'POST':
        # 세션에서 teacher_id 가져오기
        teacher_id = request.session.get('userid')
        if not teacher_id:
            messages.error(request, '로그인된 교사 ID가 유효하지 않습니다.')
            return redirect('login')  # 로그인 페이지로 리다이렉션

        # 폼 데이터 가져오기
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        family_type = request.POST.get('family_type')
        father_age = request.POST.get('father_age')
        mother_age = request.POST.get('mother_age')
        region = request.POST.get('region')
        depression = request.POST.get('depression')
        parent_relation = request.POST.get('parent_relation')
        friend_relation = request.POST.get('friend_relation')
        state = "낮음"  # 기본값

        logger.info(f"아동 입력: name={name}, teacher_id={teacher_id}")

        # 모든 필수 입력값 확인
        required_fields = [name, sex, age, weight, height, family_type, father_age, mother_age, 
                           region, depression, parent_relation, friend_relation, state]
        if all(required_fields):
            try:
                Child.objects.create(
                    teacher_id_id=teacher_id,  # 로그인된 teacher_id 사용
                    name=name,
                    sex=sex,
                    age=int(age),
                    weight=float(weight),
                    height=float(height),
                    family_type=family_type,
                    father_age=int(father_age),
                    mother_age=int(mother_age),
                    region=region,
                    depression=depression,
                    parent_relation=parent_relation,
                    friend_relation=friend_relation,
                    state=state
                )
                messages.success(request, '아동 정보가 성공적으로 저장되었습니다.')
                return redirect('manage')
            except Exception as e:
                logger.error(f"데이터 저장 중 오류 발생: {str(e)}")
                messages.error(request, f'데이터 저장 중 오류 발생: {str(e)}')
        else:
            messages.error(request, '모든 항목을 입력하세요.')
    return render(request, 'manage_form.html')

def manage_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        teacher_id = request.POST.get('teacher_id')  # 교사 ID로 변경
        if name and teacher_id:
            # 교사 ID가 실제로 존재하는지 확인
            if not Member.objects.filter(userid=teacher_id).exists():
                messages.error(request, f'존재하지 않는 교사 ID입니다: {teacher_id}')
                return render(request, 'manage_register.html')
            request.session['name'] = name
            request.session['teacher_id'] = teacher_id
            return redirect('manage_register')
        else:
            messages.error(request, '이름과 교사 ID를 입력하세요.')
    return render(request, 'manage_register.html')

def manage_detail(request, child_id):
    # child_id로 아동 데이터 조회
    child = get_object_or_404(Child, id=child_id)
    return render(request, 'manage_detail.html', {'child': child})
#add2

def home(request):
    return render(request, 'home.html')

def manage_form_view(request):
    return render(request, 'manage_form/manage.html')

def manage_view(request):
    return render(request, 'manage.html')  # manage.html 템플릿을 반환
def main(request):
    return render(request, 'main.html')

# def report(request):
#     return render(request, 'report.html')

# def login(request):
#     return render(request, 'home.html')