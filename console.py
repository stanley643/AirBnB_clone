#!/usr/bin/python3
"""The AirBnB console"""
import cmd
from datetime import datetime
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the program (Ctrl-D)"""
        print("")
        return True

    def emptyline(self):
        """Do nothing on an empty line"""
        pass

    def do_count(self, arg):
        """Prints the number of instances of a class."""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        try:
            # Updated: Check for all classes explicitly
            if class_name not in ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]:
                print("** class doesn't exist **")
                return

            count = len(eval(class_name).all())
            print(count)
        except NameError:
            print("** class doesn't exist **")
        except SyntaxError:
            print("** invalid syntax **")

    def do_create(self, arg):
        """Creates a new instance of a class, saves it, and prints the id."""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        try:

            if class_name not in ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]:
                print("** class doesn't exist **")
                return

            new_instance = eval(class_name)()
            new_instance.save()
            print(new_instance.id)
        except NameError:
            print("** class doesn't exist **")
        except SyntaxError:
            print("** invalid syntax **")

    def do_show(self, arg):
        """Prints the string representation of an instance based on its ID."""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name_with_show = args[0]
        try:

            class_name = class_name_with_show.split('.')[0]
            if class_name not in ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]:
                print("** class doesn't exist **")
                return

            if class_name_with_show.count('.') != 1:
                print("** invalid syntax **")
                return

            instance_id = class_name_with_show.split('.')[1]
            
            instance = storage.get(f"{class_name}.{instance_id}")
            if instance is not None:
                print(instance)
            else:
                print("** no instance found **")

        except NameError:
            print("** class doesn't exist **")
        except SyntaxError:
            print("** invalid syntax **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id."""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name_with_destroy = args[0]
        try:

            class_name = class_name_with_destroy.split('.')[0]
            if class_name not in ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]:
                print("** class doesn't exist **")
                return

            if class_name_with_destroy.count('.') != 1:
                print("** invalid syntax **")
                return

            instance_id = class_name_with_destroy.split('.')[1]

            try:
                del storage.all()[f"{class_name}.{instance_id}"]
                storage.save()
            except KeyError:
                print("** no instance found **")

        except NameError:
            print("** class doesn't exist **")
        except SyntaxError:
            print("** invalid syntax **")

    def do_all(self, arg):
        """Prints all string representations of all instances."""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        try:

            if class_name not in ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]:
                print("** class doesn't exist **")
                return

            instances = eval(class_name).all()
            print([str(instance) for instance in instances])
        except NameError:
            print("** class doesn't exist **")
        except SyntaxError:
            print("** invalid syntax **")

    def do_update(self, arg):
        """Updates an instance based on the class name and id."""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name_with_update = args[0]
        try:

            class_name = class_name_with_update.split('.')[0]
            if class_name not in ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]:
                print("** class doesn't exist **")
                return

            if class_name_with_update.count('.') != 1:
                print("** invalid syntax **")
                return

            instance_id = class_name_with_update.split('.')[1]

            try:
                instance = storage.all()[f"{class_name}.{instance_id}"]
            except KeyError:
                print("** no instance found **")
                return

            if len(args) < 3:
                print("** attribute name missing **")
                return

            if len(args) < 4:
                print("** value missing **")
                return

            if args[3][0] != '{' or args[-1][-1] != '}':
                print("** invalid syntax **")
                return

            attribute_dict_str = ' '.join(args[3:])
            try:
                attribute_dict = eval(attribute_dict_str)
            except SyntaxError:
                print("** invalid syntax **")
                return

            if not isinstance(attribute_dict, dict):
                print("** invalid syntax **")
                return

            for key, value in attribute_dict.items():
                setattr(instance, key, value)

            instance.save()

        except NameError:
            print("** class doesn't exist **")
        except SyntaxError:
            print("** invalid syntax **")

if __name__ == '__main__':
    HBNBCommand().cmdloop()
