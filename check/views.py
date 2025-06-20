#add1_일일위험구현법
from django.shortcuts import render, redirect
from django.contrib import messages
from students.models import Child
from accounts.models import Member
import logging  # logging 모듈 임포트

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')

def detail(request):
    return render(request, 'check_detail.html')

def check(request):
    if request.method == 'POST':
        name = request.POST.get('uname')
        teacher_id = request.POST.get('uid')
        if name and teacher_id:
            print(f"Check: name={name}, teacher_id={teacher_id}, total_score=0")
            logger.info(f"Check: name={name}, teacher_id={teacher_id}, total_score=0")
            context = {'name': name, 'teacher_id': teacher_id, 'total_score': 0}
            return render(request, 'check_survey1.html', context)
        else:
            messages.error(request, '이름과 아이디를 입력해주세요.')
    return render(request, 'check.html')

def survey1(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        teacher_id = request.POST.get('teacher_id')
        total_score = int(request.POST.get('total_score', 0))
        print(f"Survey1 입력: name={name}, teacher_id={teacher_id}, total_score={total_score}")
        logger.info(f"Survey1 입력: name={name}, teacher_id={teacher_id}, total_score={total_score}")
        
        score_map = {'매우 아니다': 1, '아니다': 2, '보통': 3, '맞다': 4, '매우 맞다': 5}
        q1 = request.POST.get('Q1')
        q2 = request.POST.get('Q2')
        q3 = request.POST.get('Q3')
        q4 = request.POST.get('Q4')
        q5 = request.POST.get('Q5')
        
        if all([q1, q2, q3, q4, q5]):
            total_score += sum(score_map.get(q, 0) for q in [q1, q2, q3, q4, q5])
            print(f"Survey1 출력: name={name}, teacher_id={teacher_id}, total_score={total_score}")
            logger.info(f"Survey1 출력: name={name}, teacher_id={teacher_id}, total_score={total_score}")
            context = {'name': name, 'teacher_id': teacher_id, 'total_score': total_score}
            return render(request, 'check_survey2.html', context)
        else:
            messages.error(request, '모든 문항에 응답해야 다음 페이지로 이동할 수 있습니다.')
            return render(request, 'check_survey1.html', {'name': name, 'teacher_id': teacher_id, 'total_score': total_score})
    return redirect('check')

def survey2(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        teacher_id = request.POST.get('teacher_id')
        total_score = int(request.POST.get('total_score', 0))
        print(f"Survey2 입력: name={name}, teacher_id={teacher_id}, total_score={total_score}")
        logger.info(f"Survey2 입력: name={name}, teacher_id={teacher_id}, total_score={total_score}")
        
        score_map = {'매우 아니다': 1, '아니다': 2, '보통': 3, '맞다': 4, '매우 맞다': 5}
        q6 = request.POST.get('Q6')
        q7 = request.POST.get('Q7')
        q8 = request.POST.get('Q8')
        q9 = request.POST.get('Q9')
        q10 = request.POST.get('Q10')
        
        if all([q6, q7, q8, q9, q10]):
            total_score += sum(score_map.get(q, 0) for q in [q6, q7, q8, q9, q10])
            print(f"Survey2 출력: name={name}, teacher_id={teacher_id}, total_score={total_score}")
            logger.info(f"Survey2 출력: name={name}, teacher_id={teacher_id}, total_score={total_score}")
            context = {'name': name, 'teacher_id': teacher_id, 'total_score': total_score}
            return render(request, 'check_survey3.html', context)
        else:
            messages.error(request, '모든 문항에 응답해야 다음 페이지로 이동할 수 있습니다.')
            return render(request, 'check_survey2.html', {'name': name, 'teacher_id': teacher_id, 'total_score': total_score})
    return redirect('check')

def survey3(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        teacher_id = request.POST.get('teacher_id')
        total_score = int(request.POST.get('total_score', 0))
        print(f"Survey3 입력: name={name}, teacher_id={teacher_id}, total_score={total_score}")
        logger.info(f"Survey3 입력: name={name}, teacher_id={teacher_id}, total_score={total_score}")
        
        score_map = {'매우 아니다': 1, '아니다': 2, '보통': 3, '맞다': 4, '매우 맞다': 5}
        q11 = request.POST.get('Q11')
        q12 = request.POST.get('Q12')
        q13 = request.POST.get('Q13')
        q14 = request.POST.get('Q14')
        q15 = request.POST.get('Q15')
        
        if all([q11, q12, q13, q14, q15]):
            total_score += sum(score_map.get(q, 0) for q in [q11, q12, q13, q14, q15])
            print(f"Survey3 계산 후: name={name}, teacher_id={teacher_id}, total_score={total_score}")
            logger.info(f"Survey3 계산 후: name={name}, teacher_id={teacher_id}, total_score={total_score}")
            
            if total_score <= 25:
                result = '낮음'
            elif total_score <= 50:
                result = '보통'
            else:
                result = '높음'

            if name and teacher_id:
                try:
                    teacher = Member.objects.get(userid=teacher_id)
                    child = Child.objects.get(name=name, teacher_id=teacher)
                    child.state = result
                    child.save()
                    messages.success(request, f'{name}의 상태가 "{result}"로 업데이트되었습니다.')
                    print(f"DB 업데이트 성공: {name}, {result}")
                    logger.info(f"DB 업데이트 성공: {name}, {result}")
                except Member.DoesNotExist:
                    messages.error(request, f'교사 ID {teacher_id}에 해당하는 교사가 없습니다.')
                    print(f"교사 조회 실패: teacher_id={teacher_id}")
                    logger.error(f"교사 조회 실패: teacher_id={teacher_id}")
                except Child.DoesNotExist:
                    messages.error(request, f'{name} (교사: {teacher_id})에 해당하는 아동이 없습니다.')
                    existing_children = Child.objects.all()
                    if existing_children:
                        messages.info(request, f'현재 DB에 존재하는 아동: {list(existing_children)}')
                    else:
                        messages.info(request, 'DB에 아동 데이터가 없습니다.')
                    print(f"아동 조회 실패: name={name}, teacher_id={teacher_id}")
                    logger.error(f"아동 조회 실패: name={name}, teacher_id={teacher_id}")
                except Exception as e:
                    messages.error(request, f'업데이트 중 오류 발생: {str(e)}')
                    print(f"오류 발생: {str(e)}")
                    logger.error(f"오류 발생: {str(e)}")
            else:
                messages.error(request, '이름 또는 교사 ID가 누락되었습니다.')
                print("이름 또는 교사 ID 누락")
                logger.error("이름 또는 교사 ID 누락")

            return render(request, 'check_result.html', {'result': result, 'total_score': total_score, 'name': name, 'teacher_id': teacher_id})
        else:
            messages.error(request, '모든 문항에 응답해야 다음 페이지로 이동할 수 있습니다.')
            return render(request, 'check_survey3.html', {'name': name, 'teacher_id': teacher_id, 'total_score': total_score})
    return redirect('check')

def result(request):
    messages.info(request, '설문을 완료하려면 설문 페이지를 진행해주세요.')
    return redirect('check')
#add2