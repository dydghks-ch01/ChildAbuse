#add1_일일위험구현법
import pickle
import pandas as pd
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from accounts.models import Member
from students.models import Child

# 홈 화면 뷰
def home(request):
    return render(request, 'home.html')

# 위험 예측 화면 뷰
def danger(request):
    return render(request, 'danger.html')

# 모델 로드 함수
def load_model():
    model_path = os.path.join(settings.BASE_DIR, 'danger', 'model', 'child_abuse_model.pkl')
    print(f"모델 경로: {model_path}")
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    return model

# 예측 함수
def predict_abuse_risk(input_data, model):
    input_df = pd.DataFrame([input_data])
    prob = model.predict_proba(input_df)[0][1] * 100
    label = model.predict(input_df)[0]
    abuse_type = "학대 위험" if label == 1 else "안전"
    return round(prob, 2), abuse_type

# 헬퍼 함수들: 문자열을 수치로 변환
def state_to_score(state):
    score_map = {'낮음': 0, '보통': 1, '높음': 2}
    return score_map.get(state, 0)  # 기본값: '낮음' (0)

def sex_to_numeric(sex):
    sex_map = {'남': 0, '여': 1}
    return sex_map.get(sex, 0)  # 기본값: '남' (0)

def family_type_to_numeric(family_type):
    map_ = {
        '핵가족': 0,
        '확대가족': 1,
        '노인가족': 2,
        '한부모가족-부': 3,
        '한부모가족-모': 4,
        '계부모가족': 5,
        '혼합가족': 6,
        '위탁가족': 7,
        '다문화가족': 8
    }
    return map_.get(family_type, 5)  # 기본값: '계부모가족' (5), 데이터 예시에 따라 설정

def region_to_numeric(region):
    map_ = {
        '도봉구': 0,
        '노원구': 1,
        '성북구': 2,
        '강남구': 3,
        '강북구': 4
    }
    return map_.get(region, 1)  # 기본값: '노원구' (1), 데이터 예시에 따라 설정

def depression_to_numeric(depression):
    map_ = {
        '매우 좋지 않음': 0,
        '좋지 않음': 1,
        '보통': 2,
        '좋음': 3,
        '매우 좋음': 4
    }
    return map_.get(depression, 0)  # 기본값: '매우 좋지 않음' (0)

def relation_to_numeric(relation):
    map_ = {
        '매우 좋지 않음': 0,
        '좋지 않음': 1,
        '보통': 2,
        '좋음': 3,
        '매우 좋음': 4
    }
    return map_.get(relation, 1)  # 기본값: '좋지 않음' (1), 데이터 예시에 따라 설정

# 예측 뷰
def predict_abuse(request):
    if request.method == "POST":
        name = request.POST.get('name')
        user_id = request.POST.get('user_id')

        if not name or not user_id:
            return JsonResponse({"error": "이름과 아이디를 입력하세요."}, status=400)

        try:
            # Member와 Child 모델 사용
            try:
                teacher = Member.objects.get(userid=user_id)
                child = Child.objects.get(name=name, teacher_id=teacher)
            except Member.DoesNotExist:
                return JsonResponse({"error": f"교사 ID {user_id}에 해당하는 교사가 없습니다."}, status=404)
            except Child.DoesNotExist:
                return JsonResponse({"error": f"{name} (교사: {user_id})에 해당하는 아동이 없습니다."}, status=404)

            # Child 데이터 디버깅 출력
            print(f"Child 데이터: id={child.id}, name={child.name}, sex={child.sex}, age={child.age}, "
                  f"weight={child.weight}, height={child.height}, family_type={child.family_type}, "
                  f"father_age={child.father_age}, mother_age={child.mother_age}, region={child.region}, "
                  f"depression={child.depression}, parent_relation={child.parent_relation}, "
                  f"friend_relation={child.friend_relation}, state={child.state}, teacher_id={child.teacher_id.userid}")

            # 모델 입력 데이터 구성 (모든 필드를 수치형으로 변환)
            input_data = {
                '연령': child.age,
                '몸무게': child.weight,
                '키': child.height,
                '성별': sex_to_numeric(child.sex),
                '가족 유형': family_type_to_numeric(child.family_type),
                '아버지 나이': child.father_age,
                '어머니 나이': child.mother_age,
                '거주 지역': region_to_numeric(child.region),
                '우울감 정도': depression_to_numeric(child.depression),
                '부모와의 관계': relation_to_numeric(child.parent_relation),
                '교우 관계': relation_to_numeric(child.friend_relation),
                '일일보고': state_to_score(child.state)
            }
            print(f"input_data: {input_data}")

            # 모델 로드 및 예측 실행
            model = load_model()
            risk_prob, abuse_type = predict_abuse_risk(input_data, model)

            return JsonResponse({
                'risk_prob': risk_prob,
                'abuse_type': abuse_type
            }, status=200)
        
        except Exception as e:
            print(f"예측 중 오류 발생: {str(e)}")
            return JsonResponse({
                'error': f'서버 오류: {str(e)}',
                'risk_prob': 0,
                'abuse_type': '알 수 없음'
            }, status=500)
    
    return render(request, 'danger.html')