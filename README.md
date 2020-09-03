# pythonProject
Sample Python scripts for utility operation(s).

## Include but not limited to:

  - Downloader; which Downloads using Multi-Threads, threads segments range from 1 up-to 64.
    It has Download abilities ranging from:
    - Multiple thread download (just like IDM).
    - Scheduling downloads {facture reserved for the next millstone].
  - Lottery API: scraps the South African National lottery site:
    - Developed using Flask.
    - Game Resource Info; offered by this API include but not limited to these Games:
        - Lotto
            - API url reference '/lotto'
        - Lotto Plus 1
            - API url reference '/lotto_plus_1'
        - Lotto Plus 2
            - API url reference '/lotto_plus_2'
        - Daily Lotto
            - API url reference '/daily_lotto'
        - Powerball
            - API url reference '/powerball'
        - Powerball Plus
            - API url reference '/powerball_plus'
    - API Provides the following; and referenced using the API url seen above suffix:
      - Latest draw results.
        - API url reference suffix '/draw'
      - Previous draw results.  
        - API url reference suffix '/history'
      - How to play the games.
        - API url reference suffix '/info'
 
  - Experimental Script(s):
    - client.py , server.py , webcam.py and main.py; are for live streaming of:
        -server side webcam live feed, to requesting client(s).
        -main entry-point is main.py
    - turtleDraw.py: for learning the turtle package.
    
 ##
 Disclaimer, I created this repo; just for fun, and to showcase Python usage.
 I'd like you to contribute to this repo. lets add more useful scripts.
