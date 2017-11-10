import simplenote
import json

username = "neeasthana@gmail.com"
password = "Waterbottle94"


simplenote = simplenote.Simplenote(username, password)
"""
result = simplenote.get_note_list()

print(result)

print(simplenote.get_note("a31b6fa882c94c61ba53c52e0230798c")[0]["content"])
"""




def profile_lists(message_body):
    lists_split = message_body.split("\n\n\n\n")
    for split in lists_split:
        print(split.split("\n")[0])
    return None

    

def add_keys_and_list_names():
    result = simplenote.get_note_list()
    with open('my_dict.json') as f:
        my_dict = json.load(f)
        for entry in result[0]:
            if entry["deleted"] == 0:
                note_id = entry["key"]
                print(note_id)
                message_body = simplenote.get_note(note_id)[0]["content"]
                list_names = profile_lists(message_body)
                my_dict[note_id] = list_names
                print()
        print(my_dict)



def test(message_body):
    message_split = message_body.split(" ")
    if message_split[0][0] is "@":
        message_body = " ".join(message_split[1:])
        
        lists_split = message_body.split("\n\n\n")



    else:
        print("Error. Message does not start with a list name")

if __name__ == '__main__':
    #test("@list something else is here")

    add_keys_and_list_names()
    #print(simplenote.get_note("a31b6fa882c94c61ba53c52e0230798c")[0]["content"])
