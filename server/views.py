from rest_framework.response import Response
from rest_framework import status
from .forms import GoalForm, SubGoalForm
from .models import Goal, SubGoal
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required

# 전체 목표, 세부 목표 불러오기 + 성공 백분률
@login_required
@api_view(["GET"])
def home(request):
    if request.method == "GET":
        goals = Goal.objects.filter(user = request.user)
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
# 목표
@login_required
@api_view(['POST', 'PUT', 'DELETE'])
def goal(request, goal_id=None):
    # 새로운 목표 생성
    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            goal_id = goal.id
            return Response({'detail': 'Goal created successfully', 'goal_id': goal_id}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    # 목표 수정
    if request.method == "PUT":
        try:
            goal = Goal.objects.get(pk = goal_id, user=request.user)
        except Goal.DoesNotExist:
            return Response({'detail': "Goal not found"}, status=status.HTTP_404_NOT_FOUND)
        form = GoalForm(request.data, instance=goal)
        if form.is_valid():
            form.save()
            return Response({'detail': 'Goal updated successfully'})
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 목표 삭제
    if request.method == "DELETE":
        try:
            goal = Goal.objects.get(pk=goal_id, user=request.user)
            goal.delete()
            return Response({'detail': 'Goal deleted successfully'})
        except Goal.DoesNotExist:
            return Response({'detail': "Goal not found"}, status=status.HTTP_404_NOT_FOUND)
        

# 세부 목표
@login_required
@api_view(['POST', 'PUT', 'DELETE'])
def subgoal(request, goal_id=None, subgoal_id = None):
    # 새로운 세부 목표 생성
    if request.method == "POST":
        try:
            goal = Goal.objects.get(pk=goal_id, user=request.user)
        except Goal.DoesNotExist:
            return Response({'detail': "Goal not found"}, status=status.HTTP_404_NOT_FOUND)
        form = SubGoalForm(request.data)
        if form.is_valid():
            subgoal = form.save(commit=False)
            subgoal.goal = goal
            subgoal.save()
            subgoal_id = subgoal.id
            return Response({'detail':"Subgoal created succeessfully", 'subgoal_id': subgoal_id}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    # 세부 목표 수정
    if request.method == "PUT":
        try:
            subgoal = SubGoal.objects.get(pk=subgoal_id, user=request.user)
        except SubGoal.DoesNotExist:
            return Response({'detail': "Subgoal not found"}, status=status.HTTP_404_NOT_FOUND)
        
        form = SubGoalForm(request.data, instance=subgoal)
        if form.is_valid():
            form.save()
            return Response({'detail': 'Subgoal updated successfully'})
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    # 세부 목표 삭제
    if request.method == "DELETE":
        try:
            subgoal = SubGoal.objects.get(pk=subgoal_id, user=request.user)
        except SubGoal.DoesNotExist:
            return Response({'detail': "Subgoal not found"}, status=status.HTTP_404_NOT_FOUND)
        subgoal.delete()
        return Response({'detail': 'Subgoal deleted successfully'})