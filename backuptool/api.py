from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
import backup

app = FastAPI()

class CreateBackupRequest(BaseModel):
    dir: str
    prev_backup: str

class CreateInitialBackupRequest(BaseModel):
    dir: str

@app.post("/create")
async def create_backup(request: CreateBackupRequest):
    """
    API endpoint to create a new incremental backup by comparing the current state of the directory
    with a previous backup.
    
    Args:
        request (CreateBackupRequest): JSON object with directory and previous backup file path.
    """
    dir = request.dir
    prev_backup = request.prev_backup

    if not os.path.isdir(dir):
        raise HTTPException(status_code=400, detail=f"Directory {dir} does not exist")
    
    if not os.path.isfile(prev_backup):
        raise HTTPException(status_code=400, detail=f"Backup file {prev_backup} does not exist")
    
    try:
        old = backup.Backup.load_from_file(prev_backup) 
        created = backup.Backup(dir, old=old.tree).dump()
        return {"message": "Backup created successfully", "filename": created}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating backup: {str(e)}")

@app.post("/create-initial")
async def create_initial_backup(request: CreateInitialBackupRequest):
    """
    API endpoint to create an initial backup of a directory.
    
    Args:
        request (CreateInitialBackupRequest): JSON object with directory path.
    """
    dir = request.dir
    
    # Validate directory existence
    if not os.path.isdir(dir):
        raise HTTPException(status_code=400, detail=f"Directory {dir} does not exist")
    
    try:
        created = backup.Backup(dir).dump()  # Create and save the initial backup
        return {"message": "Initial backup created successfully", "filename": created}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating initial backup: {str(e)}")



@app.post("/restore")
async def restore_backup(files: List[str]):
    """
     Endpoint for restoring from backup files.
     Takes a list of backup files and restores the state.
     """
    try:
        restore = backup.Restorer(files)
        restore.restore("out")
        return {"message": "Backup restored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error restoring backup: {str(e)}")
