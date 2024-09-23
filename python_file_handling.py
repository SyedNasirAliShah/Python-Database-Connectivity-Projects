import json
def load_data():
    try:
        with open("videos.txt", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def store_data(videos):
    with open("videos.txt", "w") as file:
        json.dump(videos, file)

def add_video(videos):
    name = input("Enter the name of video:")
    duration = input("Enter the total time(length): ")
    videos.append({"name": name, "duration": duration})
    store_data(videos)

def remove_video(videos):
    show_list(videos)
    index = int(input("Enter the video number to update: "))
    if 1 <= index <= len(videos):
        del videos[index - 1]
        store_data(videos)
    else:
        print("Invalid number...")
    
def update_video(videos):
    show_list(videos)
    index = int(input("Enter the video number to update: "))
    if 1 <= index <= len(videos):
        name = input("Enter new video name:")
        duration = input("Enter new video duration(length):")
        videos[index - 1] = {"name": name, "duration": duration}
        store_data(videos)
    else:
        print("Invalid number...")

def show_list(videos):
    for index, video in enumerate(videos, start=1):
        if index == 1:
            print(f"   VIDEO  ->  DURATION")
            print(f"   -----      --------")
        print(f"{index}. {video['name']} -> {video['duration']}")

def main():
    videos = load_data()
    while True:
        print("ENTER THE CHOICE FROM THE MENU")
        print("1. Add the video to file")
        print("2. Remove video from file")
        print("3. Update a video")
        print("4. List all videos")
        print("5. Exit")
        choice = int(input("Enter your choice: "))
        match(choice):
            case 1:
                add_video(videos)
            case 2:
                remove_video(videos)
            case 3:
                update_video(videos)
            case 4:
                show_list(videos)
            case 5:
                print("Exiting.....")
                break
            case _:
                print(f"{choice} is invalid choice.")

if __name__ == "__main__":
    main()