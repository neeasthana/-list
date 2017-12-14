import simplenote
import json

# GLOBALS
list_separator = "\n\n\n\n"
passwords_file_name = "passwords.json"
dictionary_file_name = "my_dict.json"



# GLOBAL FUNCTIONS
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



# Password Handling
with open(passwords_file_name, 'r') as passwords_file:
    passwords = json.load(passwords_file)
username = passwords["simplenote_username"]
password = passwords["simplenote_password"]



class SimplenoteInterface:
    """
    Simplenote interface for @list app
    """

    def __init__(self, reload = True):
        """
        Constructor - initializes simplenote and reloads lists
        """
        self.simplenote_api = simplenote.Simplenote(username, password)
        if reload:
            self.reload_lists()



    def reload_lists(self):
        """
        reloads the dictionary file with lists and tags
        """
        result = self.simplenote_api.get_note_list()
        with open(dictionary_file_name, 'w') as f:
            my_dict = {}
            for entry in result[0]:
                if entry["deleted"] == 0:
                    note_id = entry["key"]
                    message_body = self.simplenote_api.get_note(note_id)[0]["content"]
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



    ############ ADD TO LIST #############
    def get_lists_from_tag(self, tag):
        """
        takes a tag name as input and sends back list names of lists included within that tag
        """
        tag = _format_list_name(tag)
        with open(dictionary_file_name, 'r') as data_file:
            data = json.load(data_file)
            if tag in data:
                return data[tag]
            else:
                raise Exception("Tag is not in database. Consider refreshing the database or supplying another list name")
                return None



    def get_index_from_list_name(self, tag_entry, tag_name, list_name = None):
        """
        takes a tag name and list name as input and sends back the index of the list name within that tag
        """
        if list_name is not None:
            list_name= list_name.upper()
        
        list_names = tag_entry["list_names"]
        
        if list_name is None:
            if tag_name in list_names:
                list_name = tag_name
            else:
                return 0
        if list_name in list_names:
            return list_names.index(list_name)
        else:
            raise Exception("List Name is not in database. Consider refreshing the database or supplying another list name")
            return None



    def add_to_list(self, list_text, list_index, list_entry):
        """
        takes a lext text, list name, and new entry as input and adds the new entry to the list
        """
        lists_split = list_text.split(list_separator)
        target_list = lists_split[list_index]
        target_list = target_list + "\n- " + list_entry
        lists_split[list_index] = target_list
        lists_merge = list_separator.join(lists_split)
        return lists_merge



    def update_list(self, tag_id, updated_list_text):
        """
        sends back dictionary of update item
        """
        result = {"key":tag_id, "content":updated_list_text}
        print(self.simplenote_api.update_note(result))




    def get_list(list_id):
        """
        wrapper for get list by id functionality
        """
        list_object = self.simplenote_api.get_note(list_id)
        return list_object[0]["content"]



if __name__ == '__main__':
    s = SimplenoteInterface(False)
    p = s.get_lists_from_tag("books")
    print(p)
    print(s.get_index_from_list_name(p, "books"))
    print(" ".join(s.get_lists_from_tag("books")["list_names"]).lower())
