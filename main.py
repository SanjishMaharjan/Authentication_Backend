from fastapi import FastAPI
import uvicorn

from routers import authentication
from config.db import init_db


from routers import user as user_router
from routers import fileuploader


IMAGEDIR = "images/"
VIDEODIR = "videos/"
PORT = 8000
# DATABASE_URL = "sqlite:///./test.db"


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(
    user_router.router,
)
app.include_router(
    authentication.router,
)
app.include_router(
    fileuploader.router,
)

# origins = ["http://localhost", "http://localhost:3000", "exp://192.168.1.111:8081", "http://192.168.1.77"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.post("/upload")
# async def create_upload_file(file: UploadFile = File(...)):
#     # print(file.filename)
#     # filename = file.filename
#     # file_extension = filename.split(".")[-1]
#     # print(file_extension)

#     # if not file_extension:
#     #     raise HTTPException(status_code=400, detail="Invalid file type")
#     # # file.filename = f"{file_id}.{file_extension}"
#     # contents = await file.read()
#     # if file_extension in [ "jpg", "jpeg",'png',""]:
#     #     with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
#     #         f.write(contents)
#     #     response = cloudinary.uploader.upload(f"{IMAGEDIR}{file.filename}")
#     #     print(response.get("url"))
#     #     print()

#     # elif file_extension in "mp4":
#     #     with open(f"{VIDEODIR}{file.filename}", "wb") as f:
#     #         f.write(contents)
#     # return {"file_id": filename}

#     contents = await file.read()
#     images = Image.open(io.BytesIO(contents))

#     img = images.resize((256, 256))

#     img_array = image.img_to_array(img)
#     img_array = img_array.reshape(1, 256, 256, 3)

#     predicted_class = (
#         np.where(np.round(model.predict(img_array)) > 0.5, "real", "fake").item(),
#         model.predict(img_array).item(),
#     )

#     return {"predicted_class": predicted_class}

#     # async with database.transaction():
#     #     # Save file information to the database
#     #     await database.execute(
#     #         file_table.insert().values(file_id=file_id, filename=file.filename)
#     #     )

#     # Save the file


# # @app.get("/show/{file_id}")
# # async def read_file(file_id: str):
# #     # Retrieve the filename based on the file_id
# #     query = file_table.select().where(file_table.c.file_id == file_id)
# #     file_info = await database.fetch_one(query)

# #     if not file_info:
# #         raise HTTPException(status_code=404, detail="File not found")

# #     filename = file_info["filename"]

# #     if filename.endswith(".jpg"):
# #         path = f"{IMAGEDIR}{filename}"
# #     elif filename.endswith(".mp4"):
# #         path = f"{VIDEODIR}{filename}"
# #     else:
# #         raise HTTPException(status_code=500, detail="Unexpected file type")

# #     return FileResponse(path)

if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=PORT, reload=True)
    server = uvicorn.Server(config)
    server.run()
