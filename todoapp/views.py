#클래스형 View를 만들기 위해서 import
from django.views import View
#csrf 설정을 위한 import
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#데이터 모델을 가져오기 위한 import
from .models import Todo
#날짜와 시간을 사용하기 위한 import
from datetime import datetime

#JSON으로 응답을 하기 위한 import
from django.http import JsonResponse

#클라이언트의 정보를 JSON 문자열로 만들기 위한 import
import json


#Todo 클래스의 인스턴스를 디셔너리로 변환해주는 함수
#JsonResponse로 JSON 데이터를 출력하고자 하면 빠르게 JSON문자열로 만들때 dict만 가능
#dict는 JSON문자열과 표현 방법이 같기 때문
#python application 개발자가 될거라면 함수를 만들때 매개변수의 자료형을 기재하고 
#return type을 기재하는 형태로 만들어주는 것이 좋다.
def todoToDictionary(todo:Todo) -> dict:
    result = {
        '''"키이름" : 데이터'''
        "id" : todo.id,
        "userid" : todo.userid,
        "title" : todo.title,
        "done" : todo.done,
        "regdate" : todo.regdate,
        "moddate" : todo.moddate
    }
    return result




#csrf 설정으로 클라이언트 애플리케이션을 별도로 구현하는 경우 필수
@method_decorator(csrf_exempt, name = 'dispatch')
class Todoview(View):
    def post(self, request):
        #클라이언트의 데이터를 json 형식으로 가져오기
        request = json.loads(request.body)

        #userid 와 title 매개변수 값을 읽어서 저장
        #클라이언트에서 입력해주는 데이터만 읽어오면 됨
        
        userid = request["userid"]
        title = request["title"]
        #모델 인스턴스를 생성
        todo = Todo()
        todo.userid = userid
        todo.title = title

        todo.save()

        #userid와 일치하는 데이터만 추출
        todos = Todo.objects.filter(userid = userid)
        #todos = todoToDictionary(todos)
        return JsonResponse({"list":list(todos.values())})

    def get(self, request):
        #userid 라는 파라미터를 읽기
        userid = request.GET["userid"]
        todos = Todo.objects.filter(userid = userid)
        return JsonResponse({"list":list(todos.values())})

    def put(self, request):
        #클라이언트의 데이터를 json 형식으로 가져오기
        request = json.loads(request.body)

        #userid 와 id, done 매개변수 값을 읽어서 저장
        #클라이언트에서 입력해주는 데이터만 읽어오면 됨
        
        userid = request["userid"]
        id = request["id"]

        done = request["done"]

        #수정할 데이터를 찾아옴
        todo = Todo.objects.get(id=id)
        #수정할 내용을 대입
        todo.done = done
        todo.userid = userid
        #save는 기본키의 값이 있으면 수정이고 없으면 삽입
        todo.save()


        todo.save()

        #userid와 일치하는 데이터만 추출
        todos = Todo.objects.filter(userid = userid)
        #todos = todoToDictionary(todos)
        return JsonResponse({"list":list(todos.values())})

    def delete(self, request):
        #클라이언트의 데이터를 json 형식으로 가져오기
        request = json.loads(request.body)

        #userid 와 id, done 매개변수 값을 읽어서 저장
        #클라이언트에서 입력해주는 데이터만 읽어오면 됨
        
        userid = request["userid"]
        id = request["id"]

        #수정할 데이터를 찾아옴
        todo = Todo.objects.get(id=id)
        #수정할 내용을 대입
        if todo.userid == userid:
            todo.delete()
        #save는 기본키의 값이 있으면 수정이고 없으면 삽입

        #userid와 일치하는 데이터만 추출
        todos = Todo.objects.filter(userid = userid)
        #todos = todoToDictionary(todos)
        return JsonResponse({"list":list(todos.values())})