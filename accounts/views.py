from django.shortcuts import render, redirect
from django.http import JsonResponse


# Create your views here.
#add1
from django.db import connection
from .models import Member
from django.contrib import messages

def goLogin(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')
# def login(request):
#     return render(request, 'login.html')

from django.shortcuts import render, redirect
from .models import Member

def signup(request):
    return render(request, 'signup.html')

def registerMember(request):
    if request.method == 'POST':
        user_id = request.POST.get('userid')
        password = request.POST.get('pw')
        password_confirm = request.POST.get('pw_confirm')

        # 비밀번호 확인
        if password != password_confirm:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return render(request, 'signup.html')

        # 중복 ID 체크
        if Member.objects.filter(userid=user_id).exists():
            messages.error(request, '이미 존재하는 아이디입니다.')
            return render(request, 'signup.html')

        # Django ORM으로 저장
        try:
            member = Member(userid=user_id, pw=password)
            member.save()
            return redirect('login')
        except Exception as e:
            return render(request, 'signup.html', {'error': str(e)})
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        user_id = request.POST.get('userid')
        password = request.POST.get('pw')

        try:
            member = Member.objects.get(userid=user_id, pw=password)
            # 로그인 성공 시 세션에 사용자 정보 저장
            request.session['userid'] = member.userid
            return redirect('main')  # 홈 화면으로 리다이렉트
        except Member.DoesNotExist:
            return render(request, 'login.html', {'error': '아이디 또는 비밀번호가 잘못되었습니다.'})

    return render(request, 'login.html')

def logout(request):
    # 세션 삭제
    request.session.flush()  # 모든 세션 데이터 삭제
    # 또는 특정 키만 삭제: del request.session['user_id']
    return redirect('home')  # 로그아웃 후 홈 화면으로 리다이렉트

def goLoginHtml(request):
    return render(request, 'login.html')

#add2
def save_survey(request):
    if request.method == "POST":
        name = request.POST.get('name')
        user_id = request.POST.get('user_id')
        위험도 = request.POST.get('위험도')  # 예: "낮음", "보통", "높음"
        
        # Survey 모델에 저장
        survey = Survey(name=name, user_id=user_id, 위험도=위험도)
        survey.save()
        
        return redirect('check_detail')  # 예시: check_detail 페이지로 이동
    
def save_manage(request):
    if request.method == "POST":
        name = request.POST.get('name')
        user_id = request.POST.get('user_id')
        항목1 = request.POST.get('항목1')
        항목2 = request.POST.get('항목2')
        항목3 = request.POST.get('항목3')
        
        # Manage 모델에 저장
        manage = Manage(name=name, user_id=user_id, 항목1=항목1, 항목2=항목2, 항목3=항목3)
        manage.save()
        
        return redirect('manage_form')  # 예시: manage_form 페이지로 이동
    

def predict_abuse(request):
    if request.method == 'POST':
        # 폼 데이터에서 값 추출
        name = request.POST.get('name')
        user_id = request.POST.get('user_id')
        
        # 예측 로직 처리 (임시 예시 데이터)
        risk_prob = 85  # 예측 확률 예시
        abuse_type = "신체 학대"  # 예측된 학대 유형 예시

        # 예측 결과를 JSON으로 반환
        return JsonResponse({
            'risk_prob': risk_prob,
            'abuse_type': abuse_type
        })
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
