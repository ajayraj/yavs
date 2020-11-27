# yavs

### Yet Another Video Site

#### Requirements to Deploy
###### Frontend: HTML, CSS (Bootstrap)
###### Backend: Django (Python), PostgreSQL, NGINX, Gunicorn, Django-RQ (Docker, Redis)
###### NLP: Python - SpeechRecognition, Spacy,Word Vector models, WordCloud
###### ETC: FFmpeg

##### Notes:
Tested both BERT and Word Vector models for predicting category of an uploaded video. I found that Spacy's Word Vector en_core_md model with stopwords removed and lemmatization worked best for my use case. BERT was trained with and without stopwords and lemmatization and performed worse in each case, particularly having a hilarious consistent error with confusing videos marked children's entertainment with significantly more adult comedy. Ideally, it would have been preferable to run BERT without stopwords and lemmatization as the model is able to bi-directionally make better use of all the context provided. Given the imperfect nature of speech transcription and that unclear audio/speech and incorrect transcriptions must expected at times, my hypothesis is that any mistakes could have been magnified in the BERT model due to excess emphasis being placed on incorrect contexts. The Word Vector model was faster, much more memory efficient, and more consistently accurate for this classification task.
