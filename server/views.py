from rest_framework.response import Response
from rest_framework import status
from .forms import GoalForm, SubGoalForm
from .models import Goal, SubGoal
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.authtoken.models import Token
from join.authentication import BearerTokenAuthentication
from django.shortcuts import get_object_or_404

# 전체 목표, 세부 목표 불러오기 + 성공 백분률
@authentication_classes([BearerTokenAuthentication])
@api_view(["GET"])
def home(request):
    if request.method == "GET":
        user = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]).user
        goals = Goal.objects.filter(user = user)
        goals_data = []
        for goal in goals:
            subgoals = SubGoal.objects.filter(goal=goal)
            completed_subgoals = subgoals.filter(is_completed=True).count()
            completion_rate = completed_subgoals/5 * 100 # 백분율 반환
            subgoals_data = [{'id': subgoal.id, 'title': subgoal.title, 'is_completed': subgoal.is_completed} for subgoal in subgoals]
            goal_data = {'id': goal.id, 'title': goal.title, 
                        'subgoals': subgoals_data, 'completed_subgoals':completed_subgoals, 
                        'completion_rate' : completion_rate}
            goals_data.append(goal_data)
        return Response(goals_data)

# 새로운 목표 생성목표
@authentication_classes([BearerTokenAuthentication])
@api_view(['POST'])
def create_goal(request):
    if request.method == "POST":
        form = GoalForm(request.data)
        user = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]).user
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = user
            goal.save()
            goal_id = goal.id
            return Response({'detail': 'Goal created successfully', 'goal_id': goal_id}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([BearerTokenAuthentication])
@api_view(['POST'])
def create_goal_all(request):
    print(request.data)
    if request.method == "POST":
        user = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]).user
        for key, value in request.data.items():
            if key.startswith('title'):
                goal = Goal.objects.create(user=user, title=value)
                goal.save()

        return Response({'detail': 'Goals created successfully'}, status=status.HTTP_201_CREATED)
    return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# 목표 수정
@authentication_classes([BearerTokenAuthentication])
@api_view(['PUT'])
def update_goal(request, goal_id):
    try:
        user = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]).user
        goal = Goal.objects.get(id=goal_id, user=user)
    except Goal.DoesNotExist:
        return Response({'detail': "Goal not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "PUT":
        form = GoalForm(request.data, instance=goal)
        if form.is_valid():
            form.save()
            return Response({'detail': 'Goal updated successfully'})
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

# 목표 삭제
@authentication_classes([BearerTokenAuthentication])
@api_view(['DELETE'])
def delete_goal(request, goal_id):
    try:
        user = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]).user
        goal = Goal.objects.get(id=goal_id, user=user)
        goal.delete()
        return Response({'detail': 'Goal deleted successfully'})
    except Goal.DoesNotExist:
        return Response({'detail': "Goal not found"}, status=status.HTTP_404_NOT_FOUND)


# 세부 목표
# 새로운 세부 목표 생성
@authentication_classes([BearerTokenAuthentication])
@api_view(['POST'])
def create_subgoal(request, goal_id):
    if request.method == "POST":
        user = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]).user
        goal = get_object_or_404(Goal, id=goal_id, user=user)

        form = SubGoalForm(request.data)
        if form.is_valid():
            subgoal = form.save(commit=False)
            subgoal.goal = goal
            subgoal.title = request.data['title']
            subgoal.save()
            subgoal_id = subgoal.id
            return Response({'detail':"Subgoal created successfully", 'subgoal_id': subgoal_id}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

# 세부 목표 수정
@authentication_classes([BearerTokenAuthentication])
@api_view(['PUT'])
def update_subgoal(request, subgoal_id):
    if request.method == "PUT":
        subgoal = get_object_or_404(SubGoal, id=subgoal_id)

        title = request.data.get('title', None)
        if title is not None:
            subgoal.title = title
            

        is_completed = request.data.get('is_completed', None)
        if is_completed is not None:
            subgoal.is_completed = is_completed
        
        form = SubGoalForm(request.data, instance=subgoal)

        if form.is_valid():
            form.save()
            return Response({'detail': 'Subgoal updated successfully'})
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 세부 목표 삭제
@authentication_classes([BearerTokenAuthentication])
@api_view(['DELETE'])
def delete_subgoal(request, subgoal_id):
    try:
        subgoal = SubGoal.objects.get(id=subgoal_id)
        subgoal.delete()
        return Response({'detail': 'Subgoal deleted successfully'})
    except SubGoal.DoesNotExist:
        return Response({'detail': "Subgoal not found"}, status=status.HTTP_404_NOT_FOUND)