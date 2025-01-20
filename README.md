<div align="center">
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
<h3>Copyright 2024, The Karakters Kompany</h3>
<a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"><img src="https://GDjkhp.github.io/img/PDF_32.png" width=32></a><a href="https://github.com/GDjkhp/ama-facial-recognition"><img src="https://GDjkhp.github.io/img/git.png" width=32></a>
<details><summary><b>Developers' Notes</b></summary>
<h3>fuck i need money so bad i need to publish this messed up paper tas need pa ma-bookbind kasi requirements potek nayan i hate college so much im dedicating this project sa lahat ng mga nasa kolehiyo pa kasi grabe dinanas ko (>_<)</h3>
<img src="https://GDjkhp.github.io/img/preview_ai.jpg" height=320>
<br>
if you enjoyed the time you wasted then it's not a waste of time <3
<br>
<a href="https://paypal.me/GDjkhp">donate kayo if you find this repo helpful, minimum lang sweldo ko sa trabaho :3</a>
<br>
halos lahat ng python script ay AI generated ni OpenAI at Claude, kaya kung may tanong kayo, wag sakin, tanong nyo sa kanila XD
</details>
</div>

## para saan to?
para mas mapadali mag monitor ng mga tao sa paligid kasi may trust issues si eman (spy ng china)

### mga use case:
* pwedeng gawing biometrics at cctv surveillance
* nakakatamad magsulat sa logbook, merong pa bang contact-tracing?
* para mawalan ng trabaho si manong guard >:D

## pano to gamitin?
### madali lang to guys need mo lang neto:
* computer na may internet connection (preferably windows pero pwede rin linux or mac)
* python na hindi kalumaan (need mo rin vs code para mas maganda mag edit)
* camera (mas malinaw mas maganda)

### kung ready na lahat, sundan mo to:
1. install all required libraries: requirements.txt or pwede rin mano-mano good luck (hint: pip install)
2. download mo lahat ng mga script: [download as zip](https://github.com/GDjkhp/ama-facial-recognition/archive/refs/heads/master.zip)
3. enroll mo mukha mo: set-up mo si server ([server_capture.py](https://gdjkhp.github.io/ama-facial-recognition/server_capture.py)) then picture picture ([mp_client.py](https://gdjkhp.github.io/ama-facial-recognition/mp_client.py))
4. train mo si AI: extract mo lahat ng mga mukha ([readdb.py](https://gdjkhp.github.io/ama-facial-recognition/readdb.py)) then train ([mp_train.py](https://gdjkhp.github.io/ama-facial-recognition/mp_train.py))
5. finally try mo na sya congrats: ([mp_deploy.py](https://gdjkhp.github.io/ama-facial-recognition/mp_deploy.py))

## recipe
* `imgbeddings` vector embeddings tokenizer for images to assign names for each faces, powered by openai's clip model (credit goes to this [video](https://www.youtube.com/watch?v=Y0dLgtF4IHM))
* `mediapipe` 3D face detection by google (credit goes to eman)
* `opencv-contrib-python` cameras, yeah just for the cameras
* `pyqt5` gui nothing too fancy
* `numpy` numbers and array things
* `pillow` image processing
* `flask`, `requests` server/client network stuff (optional)

## format ng mga files at structure ng source code
* `/*.py` lahat ng logic nandito
* `/requirements.txt` lahat ng required python libraries nandito
* `/json/*.json` base64 image data ng mga mukha + other information na nakalap ni server
* `/received_images/{name}/*.png or *.jpg` lahat ng mga mukha na ni train ni AI
* `/face_embeddings.json` AI weight pagkatapos i-train
* `/face_detection_logs.csv` dito nagtatala ng date and time at camera forda person
* `/LICENSE` DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
* `/README.md` itong binabasa mo

<marquee><h3>hindi rito kasama node.js server at client code, gamitin nyo nalang server_capture.py at mp_client.py pero kung need nyo to, chat nyo nalang si eman (O_o)</h3></marquee>