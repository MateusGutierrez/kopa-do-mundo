from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from rest_framework.response import Response
from .models import Team
from django.forms import model_to_dict
from utils import data_processing
from exceptions import ImpossibleTitlesError, InvalidYearCupError, NegativeTitlesError

# Create your views here.


class TeamsView(APIView):
    def get(self, req: Request) -> Response:
        teams = Team.objects.all()
        teams_list = []
        for team in teams:
            nationalTeams = model_to_dict(team)
            teams_list.append(nationalTeams)
        return Response(teams_list, status.HTTP_200_OK)

    def post(self, req: Request) -> Response:
        try:
            data_processing(req.data)
        except (
            ImpossibleTitlesError,
            NegativeTitlesError,
            InvalidYearCupError,
        ) as err:
            return Response(
                {"error": str(err.message)}, status=status.HTTP_400_BAD_REQUEST
            )
        team = Team.objects.create(**req.data)

        converted_team = model_to_dict(team)
        return Response(converted_team, status.HTTP_201_CREATED)


class TeamDetailView(APIView):
    def get(self, req: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"}, status=status.HTTP_404_NOT_FOUND
            )
        converted_team = model_to_dict(team)
        return Response(converted_team, status=status.HTTP_200_OK)

    def delete(self, req: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"}, status=status.HTTP_404_NOT_FOUND
            )
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, req: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"}, status=status.HTTP_404_NOT_FOUND
            )
        for k, v in req.data.items():
            setattr(team, k, v)

        team.save()
        converted_team = model_to_dict(team)
        return Response(converted_team, status=status.HTTP_200_OK)
