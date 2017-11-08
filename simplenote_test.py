import simplenote

username = "neeasthana@gmail.com"
password = "Waterbottle94"

"""
simplenote = simplenote.Simplenote(username, password)

result = simplenote.get_note_list()

print(result)

print(simplenote.get_note("a31b6fa882c94c61ba53c52e0230798c")[0]["content"])
"""

def test(message_body):
    message_split = message_body.split(" ")
    if message_split[0][0] is "@":
        list_name = message_split[0][1:]
        message_body = " ".join(message_split[1:])
        print(list_name, message_body)
    else:
        print("Error. Message does not start with a list name")

if __name__ == '__main__':
    #test("@list something else is here")
    simplenote = simplenote.Simplenote(username, password)

    result = simplenote.get_note_list()

    for entry in result[0]:
        print(entry['deleted'], entry["key"])
        if entry["deleted"] == 0:
            print(simplenote.get_note(entry["key"]))
        print()
    #print(simplenote.get_note("a31b6fa882c94c61ba53c52e0230798c")[0]["content"])
