<pre>
<code>
  python manage.py runserver
</code>
</pre>

url http://127.0.0.1:8000/sentiment/sentiment_analysis/ 이동

<h1> Test Process </h1>

<h3> sentiment_analysis.py 테스트내용 변수 저장 </h3>
<pre>
<code>
  comment =  "귀여워❤️ 언니 올해는 5월이나 종강할때 꼭 시간내봐요 ㅎㅎ선배 넘 넘 귀엽다!!..."
  content = "#하루필름"
  hashtag = "하루필름"
</code>
</pre>

<h3> views.py 노래제목 가수 변수 저장 </h3>
<pre>
<code>
  title = list(sentiment_result['title'])
  artist = list(sentiment_result['artist'])
</code>
</pre>

<h3> sentiment_analysis.html 결과출력 </h3>
<img src="https://user-images.githubusercontent.com/67617475/167301233-d443fd34-5932-4c3d-a9e1-532e38b0cba0.png">


