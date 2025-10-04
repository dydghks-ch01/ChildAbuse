# 머신러닝, Django, 웹 을 활용한 어린이집의 가정 내 학대 분석 예측 및 신고 팀 프로젝트

## 📝 프로젝트 소개

ChildAbuse 는 Django을 활용하여 어린이집의 가정 내 아동학대 의심 아동 조기 발견 및 신고 자동화 솔루션 웹 페이지를 제작한 프로젝트 입니다.

## ✅ 핵심 기능

- 아동학대 위험도 예측 설문: 아동학대 위험도를 예측하기 위한 일일 설문 페이지를 제작했습니다.
  - 위험도 예측 질문 정의
 
    ```
    const questions = {
      "Q1": "최근 아이가 평소보다 위축되거나 불안한 모습을 보이나요?",
      "Q2": "아이가 갑자기 공격적인 행동을 보이나요?",
      "Q3": "아이가 특정 신체 부위를 자주 숨기려 하거나 멍, 상처가 자주 발견되나요?",
      "Q4": "아이가 수면 장애(악몽, 불면증 등)를 겪고 있다고 보이나요?",
      "Q5": "아이가 특정 상황(예: 큰 소리, 특정 단어)에 과민 반응을 보이나요?",
      "Q6": "부모가 등·하원 시 아이에게 과도한 신체적 접촉을 하나요?",
      "Q7": "부모가 아이에게 위협적인 언행을 하나요?",
      "Q8": "아이가 부모와의 관계에 대해 말할 때 지속적으로 부정적인 표현을 하나요?",
      "Q9": "아이가 가정에서의 생활에 대해 이야기할 때 비정상적으로 회피하는 경향을 보이나요?",
      "Q10": "부모가 등·하원 시 눈에 띄게 화가 나 있거나 감정 기복이 심한 모습을 보이나요?",
      "Q11": "아이가 수업 중에도 지속적으로 집중하지 못하거나 산만한 모습을 보이나요?",
      "Q12": "아이가 또래 친구들과의 관계에서 지속적으로 위축되거나 왕따를 당하는 모습이 보이나요?",
      "Q13": "아이가 지속적으로 슬퍼하거나 무기력한 상태를 보이나요?",
      "Q14": "최근 아이가 식사량이 갑자기 줄었거나 과식하는 경향을 보이나요?",
      "Q15": "아이가 또래보다 말이 늦거나, 언어 표현이 제한적인 모습을 보이나요?"
    };
    ```

  - 각 페이지별 일일 위험도 점수 취합


    ```python
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
    ```

  - 취합 점수로 위험도 예측 및 결과 페이지로 전송
  
    ```python
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

            return render(request, 'check_result.html', {'result': result, 'total_score': total_score, 'name': name, 'teacher_id': teacher_id})
        else:
            messages.error(request, '모든 문항에 응답해야 다음 페이지로 이동할 수 있습니다.')
            return render(request, 'check_survey3.html', {'name': name, 'teacher_id': teacher_id, 'total_score': total_score})
    return redirect('check')

    def result(request):
        messages.info(request, '설문을 완료하려면 설문 페이지를 진행해주세요.')
        return redirect('check')
    ```

- 위험도 예측: 위험도 예측 머신러닝 모델을 만들어 pkl 파일로 저장하고 주어진 데이터들을 토대로 모델을 실행합니다.

  - 예측 모델 제작 및 저장
  
    ```python
    import pickle
    import pandas as pd
    from sklearn.model_selection import train_test_split, GridSearchCV
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from imblearn.over_sampling import SMOTE
    from sklearn.metrics import classification_report, roc_auc_score
    
    # 데이터 로드
    df = pd.read_csv("modified_child_abuse_data.csv", encoding="utf-8-sig")
    
    # '학대_여부' 칼럼 추가 (1: 학대 있음, 0: 학대 없음)
    df['학대_여부'] = (df['학대 유형'] != '없음').astype(int)
    
    # 순서가 있는 범주형 변수에 대한 매핑 정의
    ordinal_mappings = {
        '우울감 정도': {'매우 좋지 않음': 0, '좋지 않음': 1, '보통': 2, '좋음': 3, '매우 좋음': 4},
        '부모와의 관계': {'매우 좋지 않음': 0, '좋지 않음': 1, '보통': 2, '좋음': 3, '매우 좋음': 4},
        '교우 관계': {'매우 좋지 않음': 0, '좋지 않음': 1, '보통': 2, '좋음': 3, '매우 좋음': 4},
        '일일보고': {'낮음': 0, '보통': 1, '높음': 2}
    }
    
    # 매핑 적용
    for col, mapping in ordinal_mappings.items():
        df[col] = df[col].map(mapping)
    
    # 순서 없는 범주형 변수에 LabelEncoder 적용
    categorical_features = ['성별', '가족 유형', '거주 지역', '학대 유형', '언어폭행 핵심 단어']
    label_encoders = {}
    
    for feature in categorical_features:
        le = LabelEncoder()
        df[feature] = le.fit_transform(df[feature])
        label_encoders[feature] = le
    
    # feature 및 target 정의
    features = ['성별', '연령', '몸무게', '키', '가족 유형', '아버지 나이', '어머니 나이', 
                '거주 지역', '우울감 정도', '부모와의 관계', '교우 관계', '일일보고', 
                '학대 유형', '언어폭행 핵심 단어']
    X = df[features]
    y = df['학대_여부']
    
    # 데이터 분할
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 데이터 불균형 처리 (SMOTE)
    smote = SMOTE(random_state=42)
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
    
    # 전처리 파이프라인
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), ['연령', '몸무게', '키', '아버지 나이', '어머니 나이']),
            ('cat', 'passthrough', ['성별', '가족 유형', '거주 지역', '우울감 정도', '부모와의 관계', 
                                    '교우 관계', '일일보고', '학대 유형', '언어폭행 핵심 단어'])
        ])
    
    # 모델 파이프라인
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(random_state=42))
    ])
    
    # 하이퍼파라미터 튜닝
    param_grid = {
        'classifier__n_estimators': [100, 200],
        'classifier__max_depth': [10, 20, None],
        'classifier__min_samples_split': [2, 5],
        'classifier__class_weight': ['balanced', None]
    }
    
    grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='f1', n_jobs=-1)
    grid_search.fit(X_train_balanced, y_train_balanced)
    
    # 최적 모델
    best_model = grid_search.best_estimator_
    print(f"최적 파라미터: {grid_search.best_params_}")
    
    # 테스트 데이터로 평가
    y_pred = best_model.predict(X_test)
    y_pred_proba = best_model.predict_proba(X_test)[:, 1]
    
    # 성능 평가
    print("\n분류 성능 보고서:")
    print(classification_report(y_test, y_pred))
    print(f"ROC-AUC 점수: {roc_auc_score(y_test, y_pred_proba):.4f}")
    
    # 모델 저장
    with open('child_abuse_model.pkl', 'wb') as model_file:
        pickle.dump(best_model, model_file)
    
    print("모델이 child_abuse_model.pkl로 저장되었습니다.")
    ```

  - 예측 모델 데이터 정리, 불러오기 및 실행
  
    ```python
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
    ```
