<script src="https://GDjkhp.github.io/scripts/aiface.js"></script>
<div style="position: relative;" markdown="1">
<link rel="stylesheet" href="https://GDjkhp.github.io/styles/style_cursor.css">
<link rel="icon" href="https://GDjkhp.github.io/img/kagura-hd.png">

<div align="center">
<h1>fuck i need money so bad i need to publish this disgusting paper tas need pa ma-bookbind kasi requirements potek nayan i hate college so much im dedicating this project sa lahat ng mga nasa kolehiyo pa kasi grabe dinanas ko >_<</h1>
<img src="https://GDjkhp.github.io/img/preview_ai.jpg" height=320>
<br>
if you enjoyed the time you wasted then it's not a waste of time <3
<br>
<a href="https://paypal.me/GDjkhp">donate</a> kayo if you find this repo helpful minimum lang sweldo ko sa trabaho :3
<br>
halos lahat ng python script ay AI generated ni OpenAI at Claude, kaya kung may tanong kayo, wag sakin, tanong nyo sa kanila XD
<br>
<h1>AMA Facial Recognition: Digital Records-logs Management System</h1>
A Thesis Presented to the Faculty of AMA Computer College Lucena Campus, Lucena City
<br>
In Partial Fulfilment of the Requirements for the Degree Bachelor of Science in Computer Science
<br>
<br>
John Emmanuel S. Marco
<br>
John Kennedy H. Peña
<br>
<img src="https://GDjkhp.github.io/img/previewai.png" width=720>
<h1>Copyright 2024, The Karakters Kompany</h1>
lisensya? anong pinagsasasabi mo? ofc meron. need mo <a href="http://www.wtfpl.net">hunter license</a> OwO
<br>
<a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"><img src="https://GDjkhp.github.io/img/PDF_32.png" width=32></a><a href="https://github.com/GDjkhp/ama-facial-recognition"><img src="https://GDjkhp.github.io/img/git.png" width=32></a>
</div>
<h1>para saan to?</h1>
para mas mapadali mag monitor ng mga tao sa paligid kasi may trust issues si eman (spy ng china)

<h3>mga use case:</h3>

* pwedeng gawing biometrics at cctv surveillance
* nakakatamad magsulat sa logbook, merong pa bang contact-tracing?
* para mawalan ng trabaho si manong guard >:)

<h1>pano to gamitin?</h1>
<h3>madali lang to guys need mo lang neto:</h3>

* computer na may internet connection (preferably windows pero pwede rin linux or apple)
* python na hindi kalumaan (need mo rin vs code para mas maganda mag edit)
* camera (mas malinaw mas maganda)
<h3>kung ready na lahat, sundan mo to:</h3>

1. install all reqiured libraries: requirements.txt or pwede rin mano-mano good luck (hint: pip install)
2. download mo lahat ng mga script: [download as zip](https://github.com/GDjkhp/ama-facial-recognition/archive/refs/heads/master.zip)
3. enroll mo mukha mo: set-up mo si server (server_capture.py) then picture picture (mp_client.py)
4. train mo si AI: extract mo lahat ng mga mukha (readdb.py) then train (mp_train.py)
5. finally try mo na sya congrats: (mp_deploy.py)
<h1>format ng mga files at structure ng source code</h1>

* `/*.py` lahat ng logic nandito
* `/requirements.txt` lahat ng required python libraries nandito
* `/json/*.json` mga data ng mga mukha + other information na nakalap ni server
* `/received_images/{name}/*.png or *.jpg` lahat ng mga mukha na ni train ni AI
* `/face_embeddings.json` AI weight pagkatapos i-train
* `/face_detection_logs.csv` dito nagtatala ng date and time at camera forda person
* `/LICENSE` DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
* `/README.md` itong binabasa mo

<marquee><h3>hindi rito kasama node.js server at client code, gamitin nyo nalang server_capture.py at mp_client.py :) pero kung need nyo to, chat nyo nalang si eman O_o</h3></marquee>
</div>