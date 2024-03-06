from fastapi import APIRouter, status, File, UploadFile, HTTPException, Depends


from utils import cloudinary
from config.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from utils.predict import predict_image
from utils.oauth2 import get_current_user
from sqlmodel import select
from utils import extractFrames
import os

import uuid

from models.File import Files
from models.User import User
from schemas.File import FilesOut
from schemas.Result import Result

from typing import List

IMAGEDIR = "images/"
VIDEODIR = "videos/"
FRAME_OUTPUT_DIR = "output_frames/"


router = APIRouter(prefix="/file", tags=["Uploads"])


# @router.get('/', response_model= list[schemas.GetFiles])
# def all(db: Session = Depends(database.get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return fileuploder_methods.get_all(db)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Result)
async def create(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    user_id=Depends(get_current_user),
):
    filename = file.filename
    size = int(file.size // 1024)
    file_extension = filename.split(".")[-1]
    print(file_extension)

    if not file_extension:
        raise HTTPException(status_code=400, detail="Invalid file type")
    # file.filename = f"{file_id}.{file_extension}"
    contents = await file.read()

    try:
        if file_extension in ["jpg", "jpeg", "png", ""]:
            with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
                f.write(contents)

            response = await cloudinary.upload_file(f"{IMAGEDIR}{file.filename}")
            url = response.get("url").replace('http', 'https')

            result, confidence = await predict_image(contents)

            file = Files(
                file_id=str(uuid.uuid4()),
                filename=filename,
                url=url,
                user_id=user_id,
                size=size,
                result=result,
            )

            session.add(file)
            await session.commit()

            return Result(result=result, confidence=confidence,type="image")


        elif file_extension == "mp4":
                # Process video
            # Save the video file
            with open(f"{VIDEODIR}{file.filename}", "wb") as f:
                f.write(contents)

            # Extract frames from the video
            extractFrames.remove_similar_frames_with_faces(f"{VIDEODIR}{file.filename}", FRAME_OUTPUT_DIR)

            # Process each frame and predict
            predicted_results = []
            for frame_filename in os.listdir(FRAME_OUTPUT_DIR):
                frame_path = os.path.join(FRAME_OUTPUT_DIR, frame_filename)

                # Predict using the predict_image function
                frame_contents = open(frame_path, "rb").read()
                result,confidence = await predict_image(frame_contents)
                # frame_output = await predict_image(frame_contents)
                # predicted_class = frame_output["result","confidence"]
                predicted_results.append(result)
                # print(predicted_results)

            predicted_class = predicted_results
             # Count the number of "real" and "fake" predictions
            num_real = sum(1 for pred in predicted_results if pred == "real")
            num_fake = sum(1 for pred in predicted_results if pred == "fake")

            # Determine the majority class
            if num_real > num_fake:
                majority_class = "real"
            else:
                majority_class = "fake"

            # Remove the frames after showing result
            for frame_filename in os.listdir(FRAME_OUTPUT_DIR):
                frame_path = os.path.join(FRAME_OUTPUT_DIR, frame_filename)
                os.remove(frame_path)

            return Result(result=majority_class, confidence=0,type="video")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # elif file_extension in "mp4":
    #     with open(f"{VIDEODIR}{file.filename}", "wb") as f:
    #         f.write(contents)

    # return {"file_id": filename}
    
    

            # video_path = f"{VIDEODIR}{file.filename}"
            # with open(video_path, "wb") as f:
            #     f.write(contents)

            # # Upload video to Cloudinary
            # cloudinary_response = cloudinary.upload_file(video_path)
            # video_url = cloudinary_response.get("url")

            # # Save file record to database
            # file_record = Files(
            #     file_id=str(uuid.uuid4()),
            #     filename=filename,
            #     url=video_url,
            #     user_id=user_id,
            #     size=size,
            #     result=[],  # No result for videos yet, you may modify this if needed
            # )
            # session.add(file_record)
            # await session.commit()

            # return {"message": "Video uploaded successfully", "url": video_url}
            
            # return predicted_class


@router.get("/history", response_model=List[FilesOut])
async def get_history(
    user_id=Depends(get_current_user), session: AsyncSession = Depends(get_session)
):
    try:
        res = await session.execute(select(Files).where(Files.user_id == user_id))

        if res:
            photos = res.scalars().all()
        print(f"{photos=}")

        return photos
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
