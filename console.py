#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            re_l = [i.strip(",") for i in lexer]
            re_l.append(brackets.group())
            return re_l
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        re_l = [i.strip(",") for i in lexer]
        re_l.append(curly_braces.group())
        return re_l


class HBNBCommand(cmd.Cmd):
    """Defines the AirBnB command interpreter.
    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Revalueiew"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            arg_s = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg_s[1])
            if match is not None:
                command = [arg_s[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(arg_s[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        arg_s = parse(arg)
        if len(arg_s) == 0:
            print("** class name missing **")
        elif arg_s[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg_s[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        arg_s = parse(arg)
        obj_dict = storage.all()
        if len(arg_s) == 0:
            print("** class name missing **")
        elif arg_s[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_s) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_s[0], arg_s[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(arg_s[0], arg_s[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        arg_s = parse(arg)
        obj_dict = storage.all()
        if len(arg_s) == 0:
            print("** class name missing **")
        elif arg_s[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_s) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_s[0], arg_s[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(arg_s[0], arg_s[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        arg_s = parse(arg)
        if len(arg_s) > 0 and arg_s[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj_l = []
            for obj in storage.all().values():
                if len(arg_s) > 0 and arg_s[0] == obj.__class__.__name__:
                    obj_l.append(obj.__str__())
                elif len(arg_s) == 0:
                    obj_l.append(obj.__str__())
            print(obj_l)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        arg_s = parse(arg)
        count = 0
        for obj in storage.all().values():
            if arg_s[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        arg_s = parse(arg)
        obj_dict = storage.all()

        if len(arg_s) == 0:
            print("** class name missing **")
            return False
        if arg_s[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arg_s) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg_s[0], arg_s[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(arg_s) == 2:
            print("** attribute name missing **")
            return False
        if len(arg_s) == 3:
            try:
                type(eval(arg_s[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arg_s) == 4:
            obj = obj_dict["{}.{}".format(arg_s[0], arg_s[1])]
            if arg_s[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[arg_s[2]])
                obj.__dict__[arg_s[2]] = valtype(arg_s[3])
            else:
                obj.__dict__[arg_s[2]] = arg_s[3]
        elif type(eval(arg_s[2])) == dict:
            obj = obj_dict["{}.{}".format(arg_s[0], arg_s[1])]
            for key, value in eval(arg_s[2]).items():
                if (key in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[key]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = valtype(value)
                else:
                    obj.__dict__[key] = value
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
