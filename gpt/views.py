from django.shortcuts import render
import openai
from openai import OpenAI
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse, HttpResponseForbidden, HttpRequest, HttpResponseServerError
import json
from user.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import markdown
import time
from decouple import config, UndefinedValueError
import collections

try:
    client = OpenAI(
        api_key=config('OPENAI_APIKEY'),
        base_url='https://api.ai-yyds.com/v1'
    )
except UndefinedValueError:
    client = None

def mdconv(text: str):
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.codehilite',
            'markdown.extensions.meta',
            'markdown.extensions.extra',
            'pymdownx.arithmatex'
        ],
        extension_configs={
            'pymdownx.arithmatex': {
                'generic': True
            }
        }
    )
    res = md.convert(text)
    return res

history = {}

@login_required(login_url='user:login')
def gpt(request: HttpRequest):
    user = request.user
    context = {
        "user": user,
        'messages': [{
            'role': x['role'],
            'content': x['content'] if x['role'] =='user' else mdconv(x['content'])
        } for x in history.get(user.id, [])]
    }
    if request.method == 'GET':
        return render(request, 'gpt/gpt.html', context)
    elif request.method == 'POST':
        if client == None:
            return HttpResponseServerError('OpenAI API Key not found')
        
        input = request.POST

        if input['model'] == 'gpt-4' and 'gpt4_permitted' not in [ x.name for x in user.groups.all() ]:
            return HttpResponseForbidden('您无权访问GPT4')
        
        msg = {
            "role": "user",
            "content": input['prompt']
        }
        if history.get(user.id):
            history[user.id].append(msg)
        else:
            history[user.id] = collections.deque([msg], maxlen=80)

        try:
            completion = client.chat.completions.create(
                model=input['model'],
                messages=list(history[user.id])
            )
        except Exception as e:
            return HttpResponseServerError(str(e))
        
        reply = completion.choices[0].message.content

        history[user.id].append({
            'role': 'assistant',
            'content': reply
        })

        return JsonResponse({
            'model': input['model'],
            'content': mdconv(reply)
        })
