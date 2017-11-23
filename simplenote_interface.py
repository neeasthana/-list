import simplenote
import json

# GLOBALS
list_separator = "\n\n\n\n"
passwords_file_name = "passwords.json"
dictionary_file_name = "my_dict.json"



# Password Handling
with open(passwords_file_name, 'r') as passwords_file:
    passwords = json.load(passwords_file)
username = passwords["simplenote_username"]
password = passwords["simplenote_password"]



class SimplenoteInterface:
    """
    Simplenote interface for @list app
    """

    def __init__(self):
        """
        Constructor - initializes simplenote and reloads lists
        """
        self.simplenote = simplenote.Simplenote(username, password)
        self.reload_lists()



    def reload_lists(self):
        """
        reloads the dictionary file with lists and tags
        """
        result = simplenote.get_note_list()
        with open(dictionary_file_name, 'w') as f:
            my_dict = {}
            for entry in result[0]:
                if entry["deleted"] == 0:
                    note_id = entry["key"]
                    message_body = simplenote.get_note(note_id)[0]["content"]
                    list_names = _profile_lists(message_body)

                    tags = entry["tags"]
                    if(entry and tags):
                        for tag in tags:
                            result_dict = {}
                            result_dict["list_id"] = note_id
                            result_dict["list_names"] = list_names
                            my_dict[tag.upper()] = result_dict
            print(my_dict)
            json.dump(my_dict, f)


    def _format_list_name(list_name):
        """
        Takes a list name as input and processes it so that the app can understand it
        """
        list_name = list_name.strip()
        list_name = list_name.strip(":")
        list_name = list_name.replace(" ", "") #remove all whitespace
        list_name = list_name.replace("#", "") #replace all list beginnings
        list_name = list_name.upper()
        return list_name
        #TODO: add support for "/" or multi-named lists




    def _profile_lists(message_body):
        """
        Takes a single big list and splits it into sublists (returned)
        """
        lists_split = message_body.split(list_separator)
        list_names = []
        for split in lists_split:
            list_name = split.split("\n")[0]
            list_name = _format_list_name(list_name)
            list_names.append(list_name)
        return list_names



if __name__ == '__main__':
    s = SimplenoteInterface()
    print(s.simplenote)