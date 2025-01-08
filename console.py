#!/usr/bin/python3
"""Command interpreter for Holberton AirBnB project
"""
import cmd
import models
from models import storage
import shlex
import ast


class HBNBCommand(cmd.Cmd):
    """Command interpreter class"""

    prompt = '(hbnb) '
    valid_classes = {'BaseModel', 'User', 'State', 'City',
                    'Amenity', 'Place', 'Review'}

    def emptyline(self):
        """Do nothing when empty line is entered"""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def do_create(self, arg):
        """Creates a new instance of a class with given parameters
        Args:
            arg (str): Class name and parameters for instance creation
        """
        if not arg:
            print("** class name missing **")
            return
        
        args = arg.split()
        class_name = args[0]
        
        if class_name not in models.classes:
            print("** class doesn't exist **")
            return
        
        # Extract parameters from arguments
        params = {}
        for param in args[1:]:
            try:
                key, value = param.split('=', 1)
                # Handle string with quotes
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]  # Remove quotes
                    value = value.replace('_', ' ')  # Replace _ with space
                    value = value.replace('\\"', '"')  # Handle escaped quotes
                    params[key] = value
                # Handle float
                elif '.' in value:
                    try:
                        params[key] = float(value)
                    except ValueError:
                        continue
                # Handle integer
                else:
                    try:
                        params[key] = int(value)
                    except ValueError:
                        continue
            except ValueError:
                continue
        
        # Create instance with parameters
        instance = models.classes[class_name](**params)
        instance.save()
        print(instance.id)

    def do_show(self, arg):
        """Prints string representation of an instance"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in models.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in models.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """Prints string representation of all instances"""
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            for value in storage.all().values():
                obj_list.append(str(value))
        elif args[0] in models.classes:
            for key in storage.all():
                if key.split('.')[0] == args[0]:
                    obj_list.append(str(storage.all()[key]))
        else:
            print("** class doesn't exist **")
            return
        print(obj_list)

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in models.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if len(args) == 3:
            print("** value missing **")
            return
        setattr(storage.all()[key], args[2], ast.literal_eval(args[3]))
        storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
