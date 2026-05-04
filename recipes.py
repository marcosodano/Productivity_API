####### LIBRARIES #######
import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse




####### GLOBAL VARIABLES #######
router = APIRouter()





####### FUNCTIONS #######
# Create upload directory for recipes
UPLOAD_DIR = ".recipes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Allowed file extensions
allowed_extensions = {".jpg", ".jpeg", ".pdf", ".txt", ".doc", ".docx", ".xls"}
####### FUNCTIONS #######
# Build a file path
def create_file_path(filename):
    file_path = os.path.join(UPLOAD_DIR, filename)
    return file_path


# Return a safe filename string
def create_safe_filename(filename):
    filename_wo_ext, extension = os.path.splitext(filename.lower())
    check_file_ext(extension)
    clean_filename = "".join(char for char in filename_wo_ext if char.isalnum() or char == " " or char == "_")
    safe_filename = clean_filename.strip().replace(" ", "_") + extension
    return (safe_filename, extension)


# Verify file extension
def check_file_ext(extension):
    if extension not in allowed_extensions:
        raise HTTPException(
            status_code = 400,
            detail = f"Extension {extension} not allowed. Allowed file types: {', '.join(allowed_extensions)}"
        )





####### API METHODS #######
@router.get("/home/")
def home():
    return {"Message": "Welcome to your recipe manager!"}


@router.post("/upload-recipe/")
async def upload_recipe(
    recipe_name: str = Form(...),
    file: UploadFile = File(...),
):

    # 1. Create a safe filename
    safe_filename, extension = create_safe_filename(file.filename)

    # 2. Save the file
    file_path = create_file_path(safe_filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 3. Return the info
    return {
        "Dish" : recipe_name,
        "Saves as" : safe_filename,
        "Status:" : "Recipe saved successfully!"
    }


@router.get("/list-recipes/")
def list_recipes():
    # os.listdir() opens a folder and grabe the names of all the file inside
    saved_files = os.listdir(UPLOAD_DIR)

    return {
        "Message:" : "Here is what's in your vault!",
        "Total recipes:": len(saved_files),
        "Recipes:": saved_files
        }


@router.get("/get-recipe/{filename}")
def get_recipe_file(filename: str):
    # 1. Build the exact path to the file that has to be retrieved
    file_path = create_file_path(filename)

    # 2. Check if the file patch exists
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code = 400,
            detail = f"Error: Ooops! The file {filename} does not exist."
        )
    
    # 3. If it exists, send the actual file to the browser
    return FileResponse(file_path)


@router.delete("/delete-recipe/{filename}")
def delete_recipe(filename: str):
    # 1. Build the exact path to the file that has to be deleted
    file_path = create_file_path(filename)

    # 2. Check if the file patch exists
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code = 400,
            detail = f"Error: Ooops! The file {filename} does not exist."
        )
    
    # 3. Remove the file
    os.remove(file_path)

    # 4. Return message
    return {"message" : f"Successfully deleted {filename} from the vault."}


@router.put("/update-recipe/{filename}")
def update_recipe(
    filename : str,
    file: UploadFile = File(...)
):
    # 1. Build the exact path to the file that has to be updated
    file_path = create_file_path(filename)

    # 2. Check if the file patch exists
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code = 400,
            detail = f"Error: Ooops! The file {filename} does not exist."
        )
    
    # 3. Create a safe filename for the updated file
    safe_filename, extension = create_safe_filename(file.filename)
    
    # 4. Overwrite the old file with the new one
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"Message:" : f"Successfully updated '{filename}' with your new file!"}