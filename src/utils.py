import shutil
from pathlib import Path
from config import districts, districts_group_1, districts_group_2, districts_group_3, districts_group_4,districts_group_5


#delete file or folder
def delete(delete_path:Path):
    if delete_path.exists():
        shutil.rmtree(delete_path)


#create folders for jsonl and pdf
def createFolders(jsonl_folder:Path, pdf_folder:Path):
    jsonl_folder.mkdir(parents=True, exist_ok=True)
    pdf_folder.mkdir(parents=True, exist_ok=True)


def moveFiles(src:Path):
    dir_paths = []
    jsonl_folder = src/"jsonl"
    pdf_folder = src/"pdf"
    jsonl_folder.mkdir(parents=True, exist_ok=True)
    pdf_folder.mkdir(parents=True, exist_ok=True)

    for folder_path in sorted(src.iterdir()):
        if folder_path.name.isdigit():
            dir_paths.append(folder_path)
    
    if not dir_paths:
        print(f"{src} has been sorted")
        return
    
    #separately jsonl and pdf accordingly
    for dir in dir_paths:
        for file in dir.rglob("*"):
            year = dir.name
            file_extension = file.suffix.lower()
            #move .jsonl to jsonl folder
            if file_extension == ".jsonl": 
                shutil.move(str(file), str(jsonl_folder/file.name))
            #move pdf to pdf folder
            else: 
                shutil.move(str(file), str(pdf_folder/f"{year}_{file.name}"))

    #delete empty folders
    for dir in dir_paths:
        if dir.is_dir():
            try:
                dir.rmdir()
            except OSError:
                print(f"{dir} is not empty")
                continue

    print(f"PDF and JSONL files have been separated in {src}")
    

def main():
    #createFolders(Path("/workspace/alfred/justia_extraction/output/North Dakota/jsonl"), Path("/workspace/alfred/justia_extraction/output/North Dakota/pdf"))
    #delete(Path("/workspace/alfred/justia_extraction/output/Kansas"))
    #moveFiles(Path("/workspace/alfred/justia_extraction/output/North Dakota"))
    counter = 0
    for district in districts:
        #perform the sorting for those completed
        print(f"Sorting {district} PDFs and JSONLs")
        moveFiles(Path(f"/workspace/alfred/justia_extraction/output/{district}")) #enable this to sort the pdf and jsonl accordingly
        counter+=1
        #break
    print(f"Number of districts completed: {counter}")
    

main()