from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient("mongodb+srv://xyz:*****@cluster0.o08khqt.mongodb.net/")
db = client["ytmanager"]
video_collection = db["youtube_videos"]


def add_video(name, time):
    video_collection.insert_one({"name": name, "time": time})


def delete_video(id):
    video_collection.delete_one({"_id": ObjectId(id)})


def update_video(id, new_name, new_time):
    video_collection.update_one({"_id": ObjectId(id)}, {"$set": {"name": new_name, "time": new_time}})


def show_list():
    for video in video_collection.find():
        print(f"ID: {video["_id"]} -->  name: {video["name"]}, time: {video["time"]}")


def main():
    while True:
        print("ENTER THE CHOICE FROM THE MENU")
        print("1. Add the video to database")
        print("2. Remove video from database")
        print("3. Update a video")
        print("4. List all videos")
        print("5. Exit")
        choice = int(input("Enter your choice: "))
        match(choice):

            case 1:
                name = input("Enter the video name:")
                time = input("Enter the duration of video:")
                add_video(name, time)
            
            case 2:
                video_id = input("Enter video id to be deleted:")
                delete_video(video_id)
            
            case 3:
                video_id = input("Enter the video id to be updated:")
                new_name = input("Enter the new video name:")
                new_time = input("Enter the new duration of video:")
                add_video(new_name, new_time)
            
            case 4:
                show_list()
            
            case 5:
                print("Exiting.....")
                break
            
            case _:
                print(f"{choice} is invalid choice.")


if __name__ == "__main__":
    main()
