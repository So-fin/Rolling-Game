from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
import random
from .models import *
from .serializers import GameSerializer
from rest_framework.response import Response

# Create your views here.

symbols = ['cherry', 'lemon', 'orange', 'watermelon']
rewards = {
    'cherry': 10,
    'lemon': 20,
    'orange': 30,
    'watermelon': 40
}


class startGameView(APIView):
    def post(self, request):
        gamesession = GameSession.objects.create(user=User.objects.create(), is_active=True)
        serializer = GameSerializer(gamesession)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class rollView(APIView):
    def post(self, request, gamesession_id):
        
        def roll_result():
            return [random.choice(symbols) for i in range(3)]
        
        def is_winner(roll_result):
           return roll_result[0] == roll_result[1] == roll_result[2] 
        
        def get_result(gamesession):
            gamesession.credits -= 1
            roll_results = roll_result()
            
            if is_winner(roll_results):
                if gamesession.credits > 40 and gamesession.credits < 60:
                    if random.random() < 0.30:
                        roll_results = roll_results()
                        if is_winner(roll_results):
                            gamesession.credits += rewards[roll_results[0]]
                            gamesession.save()
                            return gamesession.credits
                if gamesession.credits > 60:
                    if random.random() < 0.60:
                        roll_results = roll_results()
                        if is_winner(roll_results):
                            gamesession.credits += rewards[roll_results[0]]
                            gamesession.save()
                            return gamesession.credits
                gamesession.credits += rewards[roll_results[0]]
            gamesession.save()
            return gamesession.credits, roll_results
        
        try:
            gamesession = GameSession.objects.get(id=gamesession_id)
        except GameSession.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if gamesession.credits < 1:
            return Response('You do not have credits to play the game')
        
        res = get_result(gamesession)
        return Response({'Roll result': res[1], 'Credits': res[0]})
    

class cashOutView(APIView):
    def post(self, request, gamesession_id):
        try:
            gamesession = GameSession.objects.get(id=gamesession_id, is_active=True)
        except GameSession.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user = gamesession.user
        user.account_credits += gamesession.credits
        user.save()
        
        gamesession.credits = 0
        gamesession.is_active = False
        gamesession.save()
        
        return Response('Cash out successful', status=status.HTTP_200_OK)