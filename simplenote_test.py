import simplenote

username = "neeasthana@gmail.com"
password = "Waterbottle94"

simplenote = simplenote.Simplenote(username, password)

print("got here")

result = simplenote.get_note_list()

print(result)

print(simplenote.get_note("a31b6fa882c94c61ba53c52e0230798c")[0]["content"])
