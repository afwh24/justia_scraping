from pathlib import Path

#Basic config
base_url = "https://law.justia.com"
districts = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut","Delaware", "District of Columbia","Florida","Georgia", "Hawaii", "Idaho", "Illinois", "Indiana","Iowa","Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

#manually split districts into groups for parallelism 
#manually remove district in group that has been fully processed (to make checkpoint faster)
districts_group_1 = []
districts_group_2 = ["Florida"]
districts_group_3 = ["Georgia"]

districts_group_4 = []
districts_group_5 = []

output_root_dir = Path("/workspace/alfred/justia_extraction/output")
log_file ="/workspace/alfred/justia_extraction/errors.txt"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

