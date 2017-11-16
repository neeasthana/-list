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

def format_list_name(list_name):
    list_name = list_name.strip()
    list_name = list_name.strip(":")
    list_name = list_name.replace(" ", "") #remove all whitespace
    list_name = list_name.replace("#", "") #replace all list beginnings
    list_name = list_name.upper()
    return list_name
    #TODO: add support for "/" or multi-named lists




def profile_lists(message_body):
    lists_split = message_body.split("\n\n\n\n")
    list_names = []
    for split in lists_split:
        list_name = split.split("\n")[0]
        list_name = format_list_name(list_name)
        list_names.append(list_name)
    return list_names



def add_keys_and_list_names():
    result = simplenote.get_note_list()
    with open('my_dict.json', 'w') as f:
        my_dict = {}
        for entry in result[0]:
            if entry["deleted"] == 0:
                note_id = entry["key"]
                message_body = simplenote.get_note(note_id)[0]["content"]
                list_names = profile_lists(message_body)

                tags = entry["tags"]
                if(entry and tags):
                    for tag in tags:
                        result_dict = {}
                        result_dict["list_id"] = note_id
                        result_dict["list_names"] = list_names
                        my_dict[tag.upper()] = result_dict
        print(my_dict)
        json.dump(my_dict, f)



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
