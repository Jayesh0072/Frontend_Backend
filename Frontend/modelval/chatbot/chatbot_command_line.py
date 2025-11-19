from chatbot import ChatBot 


def _validate_files(files):
    extensions = [f.split(".")[-1] for f in files]
    csvs = [e for e in extensions if e == "csv"]

    has_csv = len(csvs) > 0
    if has_csv and len(csvs) != len(extensions):
        raise Exception("You must either upload all csvs or no csvs")
    return has_csv


use_csvbot = False
while True:
    try:
        input_files = input("Please specify the name the files you would like to chat with (comma separated): ")
        files = input_files.split(",")
        if not files:
            print("\nYou must specify at least one file.\n")
        else: 
            chatbot = ChatBot(filenames=files)
            break
    except FileNotFoundError:
        print("\nUnable to find the given file.\n")


while True:
    input_query = input("Please ask the pdf a question (enter stop to end your conversation): ")
    if input_query.lower() == "stop":
        break
    print("\n")
    
    print(chatbot.ask(input_query))
    print("\n\n")
