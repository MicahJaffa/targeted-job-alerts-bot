import os
import requests
import time
from score import score
from dotenv import load_dotenv

load_dotenv()

QUERIES = [
    # Multimedia
    "sports multimedia",
    "athletic department video production",
    "sports content creator",
    
    # Graphic Design
    "sports graphic design",
    "athletic department creative services",
    "sports visual branding",
    
    # Account Management
    "sports account coordinator",
    "sports agency account executive",
    "NIL account manager",
    
    # Social Media
    "sports social media coordinator",
    "sports digital media assistant",
    "athletic department social media",
    
    # Client Acquisition & Sponsorships
    "sports sponsorship activation",
    "sports partnership coordinator",
    "NIL partnerships",
    
    # AI & Analytics
    "sports data analyst",
    "sports marketing analytics",
    "athletic department data analyst"
]

TARGET_EMPLOYERS = [
    "Teamworks", "Athlete", "NIL",
    "NFL", "NBA", "MLB", "NHL", "MLS", "PGA", "NASCAR", "UFC",
    "ESPN", "Fox Sports", "NBC Sports", "CBS Sports", "Turner Sports",
    "Bleacher Report", "The Athletic", "Sports Illustrated",
    "Nike", "Adidas", "Under Armour", "New Balance", "Puma",
    "Gatorade", "Powerade", "Wilson", "Callaway",
    "Red Bull", "Fanatics", "Ticketmaster", "Live Nation",
    "Sportradar", "Stats Perform",
    "WME Sports", "CAA Sports", "Wasserman", "Endeavor",
    "IMG", "Octagon",
    "University of Florida", "Florida Gators",
    "Opendorse" 
]
SENIOR_KEYWORDS = [
    "senior", "director", "manager", "lead", "principal", 
    "head", "chief", "vp ", "sr ", "sr.", "executive", "specialist", "account executive", " iii", " ii", " iv"
]
JUNK_KEYWORDS = [
    "warehouse", "retail", "store", "cashier", "shift", 
    "packaging", "merchandise", "loss prevention", "stock",
    "delivery", "seasonal", "freight", "freelance", "part-time freelance", "championship", "national championship",
    "foosball", "unpaid", "freelance"
]
DIVISION_BUZZWORDS = [
    # Multimedia
    "video", "multimedia", "production", "videographer", "editor", "broadcast", 
    
    # Graphic Design
    "graphic", "design", "visual", "creative", "branding", "illustrator",
    
    # Account Management
    "account", "client", "coordinator", "executive", "liaison",
    
    # Social Media
    "social media", "content", "community", "tiktok", "instagram", "digital media",
    
    # Client Acquisition & Sponsorships
    "sponsorship", "partnership", "activation", "acquisition", "nil", "sales",
    
    # AI & Analytics
    "analytics", "data", "ai", "artificial intelligence", "analyst", "insights"
]
"""DIVISION_QUERIES = {
    "Multimedia": [
        "sports multimedia",
        "athletic department video production",
        "sports content creator",
        "sports video producer",
        "sports videographer",
        "broadcast production assistant sports",
        "sports video editor",
        "multimedia athletics",
        "sports broadcast",
        "sports livestream operator",
        "athletics video coordinator",
        "sports camera operator",
        "sports media production",
        "college athletics videographer",
        "sports highlight editor",
        "sports production",
        "college media production",
        "sports broadcasting",
        "digital media sports",
        "athletics media",
        "sports film",
        "video production athletics",
        "sports media coordinator",
    ],
    "Graphic Design": [
        "sports graphic design",
        "athletic department creative services",
        "sports visual branding",
        "athletic department designer",
        "sports branding designer",
        "sports creative services",
        "sports motion graphics",
        "sports art director",
        "athletics visual content",
        "sports digital designer",
        "college athletics graphic designer",
        "sports print design",
        "athletics brand identity",
        "sports creative",
        "athletics design",
        "sports visual media",
        "college sports design",
        "sports marketing design",
        "digital design athletics",
        "sports brand design",
    ],
    "Account Management": [
        "sports account coordinator",
        "sports agency account executive",
        "NIL account manager",
        "sports client coordinator",
        "NIL coordinator",
        "athlete relations coordinator",
        "college athletics account coordinator",
        "sports client services",
        "NIL talent manager",
        "sports agency coordinator",
        "athlete management",
        "sports business development",
        "college sports account executive",
        "NIL athlete coordinator",
        "sports relationship manager",
        "athlete services",
        "sports operations coordinator",
        "NIL management",
        "sports talent coordinator",
        "college athletics coordinator",
        "sports agency",
        "athlete brand management",
    ],
    "Social Media": [
        "sports social media coordinator",
        "sports digital media assistant",
        "athletic department social media",
        "sports content coordinator",
        "college athletics social media",
        "sports instagram tiktok coordinator",
        "sports digital content creator",
        "sports social media manager",
        "athletics online content",
        "sports community manager",
        "sports twitter coordinator",
        "college sports content",
        "sports influencer coordinator",
        "sports fan engagement",
        "sports content strategy",
        "athletics content",
        "sports digital marketing",
        "college sports digital",
        "sports online media",
        "sports content marketing",
        "athletics digital media",
        "sports media manager",
    ],
    "Client Acquisition & Sponsorships": [
        "sports sponsorship activation",
        "sports partnership coordinator",
        "NIL partnerships",
        "sports sponsorship coordinator",
        "sports corporate partnerships",
        "sports partnership sales",
        "NIL brand partnerships",
        "sports revenue partnerships",
        "sports brand activation",
        "college athletics sponsorship",
        "sports partnership development",
        "sports sales coordinator",
        "NIL deal coordinator",
        "sports partnership activation",
        "sports business partnerships",
        "athletics sponsorship",
        "sports corporate sales",
        "sports marketing partnerships",
        "sports revenue generation",
        "college sports sponsorship",
        "sports brand deals",
        "sports partnership marketing",
    ],
    "AI & Analytics": [
        "sports data analyst",
        "sports marketing analytics",
        "athletic department data analyst",
        "sports analytics",
        "sports business intelligence",
        "sports performance analyst",
        "sports technology analyst",
        "college athletics analytics",
        "sports machine learning",
        "sports data science",
        "athlete performance data",
        "sports AI",
        "sports fan analytics",
        "sports predictive analytics",
        "college sports data",
        "sports technology",
        "athletics data",
        "sports research analyst",
        "sports quantitative analyst",
        "sports operations analytics",
        "sports intelligence",
        "sports insights analyst",
    ],
}"""
DIVISION_QUERIES = {
    "Multimedia": [
        "sports (videographer OR video production OR broadcast)",
        "athletic department (multimedia OR content creator)",
        "sports (highlight editor OR media coordinator)",
    ],
    "Graphic Design": [
        "sports (graphic designer OR visual branding)",
        "athletic department (creative services OR motion graphics)",
    ],
    "Account Management": [
        "sports (account coordinator OR agency account executive)",
        "NIL (coordinator OR account manager OR talent manager)",
        "athlete relations coordinator",
    ],
    "Social Media": [
        "sports (social media coordinator OR digital media assistant)",
        "athletic department social media",
        "sports digital content creator",
    ],
    "Client Acquisition & Sponsorships": [
        "sports (sponsorship activation OR partnership coordinator)",
        "NIL (partnerships OR brand deals)",
        "sports corporate partnerships",
    ],
    "AI & Analytics": [
        "sports (data analyst OR business intelligence)",
        "sports (analytics OR performance analyst)",
        "athletic department data analyst",
    ],
}
ROLE_BLACKLIST = [
    "reporter", "anchor", "journalist", "news", "correspondent", "Trainer"
]
TRUSTED_DOMAINS = [
    "linkedin.com", "teamworkonline.com", "workdayjobs.com",
    "greenhouse.io", "lever.co", "indeed.com", "nfl.com",
    "nba.com", "mlb.com", "espncareers.com", "nike.com"
]
limits = [3, 2, 2, 3, 2, 1]
def get_previously_posted_jobs():
    if not os.path.exists("posted_jobs.txt"):
        return set()
        
    with open("posted_jobs.txt", "r") as file:
        return set(line.strip() for line in file.readlines())

def save_posted_job(job_id):
    with open("posted_jobs.txt", "a") as file:
        file.write(f"{job_id}\n")
def is_trusted_source(job: dict) -> bool:
    url = job.get("job_apply_link", "") or job.get("job_google_link", "")
    return any(domain in url for domain in TRUSTED_DOMAINS)
def assign_division(job):
    title = job.get("job_title", "").lower()
    description = job.get("job_description", "").lower()
    full_text = f"{title} {description}"
    
    matched_divisions = []
    
    for division_name, buzzwords in DIVISIONS.items():
        if any(buzzword in full_text for buzzword in buzzwords):
            matched_divisions.append(division_name)
            
    if matched_divisions:
        job["agency_division"] = ", ".join(matched_divisions)
        return True
        
    return False
def has_buzzword(job):
    title = job.get("job_title", "").lower()
    description = job.get("job_description", "").lower()

    full_text = f"{title} {description}"
    
    return any(buzzword in full_text for buzzword in DIVISION_BUZZWORDS)
def is_entry_level(job):
    title = job.get("job_title", "").lower()
    if not title:
        return False
    if any(keyword in title for keyword in SENIOR_KEYWORDS):
        return False
    if any(keyword in title for keyword in JUNK_KEYWORDS):
        return False
    #if any(keyword in title for keyword in ROLE_BLACKLIST):
       # return False
    return True
def is_target_employer(job):
    employer = job.get("employer_name", "")
    if not employer:
        return False
    return any(target.lower() in employer.lower() for target in TARGET_EMPLOYERS)

def get_jobs() -> list:

    url = "https://jsearch.p.rapidapi.com/search-v2"
    headers = {
        "x-rapidapi-key": os.environ.get("RAPIDAPI_KEY"),
        "x-rapidapi-host": "jsearch.p.rapidapi.com",
    }

    all_jobs = []
    seen_ids = get_previously_posted_jobs()
    timeout = 120

    print(f"Running {len(DIVISION_QUERIES)} queries...")
    div_on = 0
    with requests.Session() as session:
        for division, queries in DIVISION_QUERIES.items():
            for search_term in queries:
                querystring = {
                    "query": search_term,
                    "num_pages": "2",
                    "country": "us",
                    "date_posted": "month",
                    "employment_types": "INTERN",
                 }

            try:
                print(f"[{div_on+1}/{len(DIVISION_QUERIES)}] Searching: '{division}'...")
                response = session.get(url, headers=headers, params=querystring, timeout=timeout)
                response.raise_for_status()

                data = response.json().get("data", {})
                jobs = data if isinstance(data, list) else data.get("jobs", [])
                job_amount = 0
                div_on += 1
                temp_jobs = []
                

                
                for job in jobs:
                    job_id = job.get("job_id")
                    if job_id and job_id in seen_ids:
                        continue
                    if not is_entry_level(job):
                        continue
                    if not has_buzzword(job):
                        continue
                    if not is_trusted_source(job):
                        continue
                    if job_id in seen_ids:
                        print(f"Skipping job {job_id}")
                        continue
                    job["job_score"] = score(job, div_on)
                    job["agency_division"] = division
                    temp_jobs.append(job)
                    print(f"{job.get('job_title')} @ {job.get('employer_name')} job score: {job.get('job_score')} → {job.get('agency_division')}")
                top_jobs = []
                for job in temp_jobs:
                    if len(top_jobs) < limits[div_on - 1]:
                        top_jobs.append(job)
                    else:
                        min_score_job = min(top_jobs, key=lambda x: x.get("job_score", 0))
                        if job.get("job_score", 0) > min_score_job.get("job_score", 0):
                            top_jobs.remove(min_score_job)
                            top_jobs.append(job)
                all_jobs.extend(top_jobs)
                for job in top_jobs:
                    print(f" saved job: {job.get('job_title')} @ {job.get('employer_name')} job score: {job.get('job_score')} → {job.get('agency_division')}")
                    save_posted_job(job.get("job_id"))
            except requests.exceptions.HTTPError as e:
                status = response.status_code
                error_body = response.text.lower()

                # RapidAPI returns 429 (quota exceeded) or 403 (unauthorized/exhausted plan)
                if status == 429 or (status == 403 and "quota" in error_body) or "exceeded" in error_body:
                    print("RapidAPI monthly credit quota exhausted.")
                    credit_alert_job = {
                        "job_title": "out of credits",
                        "employer_name": "RapidAPI Alert",
                        "job_city": "N/A",
                        "job_country": "N/A",
                        "job_employment_type": "N/A",
                        "agency_division": "System",
                        "job_apply_link": "https://rapidapi.com"
                    }
                    if not all_jobs:
                        all_jobs.append(credit_alert_job)
                    else:
                        all_jobs[0] = credit_alert_job
                    return all_jobs

                print(f"HTTP Error: {e}")
            except requests.exceptions.Timeout:
                print(f"Query timed out. Skipping.")
            except Exception as e:
                print(f"API Error: {e}")

            time.sleep(2)

    print(f"\nTotal unique matching jobs: {len(all_jobs)}")
    return all_jobs