from typing import List, Optional, Type
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.urls import reverse
from django.views import generic
from django.db.models import Model

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name: str = "polls/index.html"
    context_object_name: Optional[str] = "latest_question_list"

    def get_queryset(self) -> List[Question]:
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model: Type[Model] = Question
    template_name: str = "polls/detail.html"


class ResultsView(generic.DetailView):
    model: Type[Model] = Question
    template_name: str = "polls/results.html"


def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    question: Question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice: Choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {"question": question, "error_message": "You didn't select a choice."},
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))
