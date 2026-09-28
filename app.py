import os
import schedule
import time
from dotenv import load_dotenv
from slack_bot import post_jobs
from job_search import get_jobs

load_dotenv()

def run():
    print("Fetching jobs...")
    jobs = get_jobs()
    post_jobs(jobs)
    print(f"Posted {len(jobs)} jobs!")
    #ee
#schedule.every().day.at("09:00").do(run)
#schedule.every().day.at("17:00").do(run)
#schedule.every().tuesday.at("17:00").do(run)
#schedule.every().thursday.at("17:00").do(run)
if __name__ == "__main__":
    print("Bot is running!")
    run()
    #while True:
      #  schedule.run_pending()
      #  time.sleep(60)
