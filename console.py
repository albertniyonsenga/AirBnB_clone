#!/usr/bin/python3
"""
Console module
Entry point of the command interpreter
"""

import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter for AirBnB clone"""

    prompt = "(hbnb) "
    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the program with EOF (Ctrl+D)"""
        print()
        return True

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def do_create(self, arg):
        """Create a new instance of a class"""
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        class_name = args[0]

        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return

        kwargs = {}

        for param in args[1:]:
            if "=" in param:
                key, value = param.split("=", 1)
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1].replace('_', ' ')
                kwargs[key] = value

        try:
            obj = self.__classes[class_name](**kwargs)
            obj.save()
            print(obj.id)
        except Exception as e:
            print(f"** error: {e} **")

    def do_show(self, arg):
        """Show an instance by class name and id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        obj = storage.all().get(key)
        if obj:
            print(obj)
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Delete an instance based on class name and id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        all_objs = storage.all()
        if key in all_objs:
            del all_objs[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Print all string representations of instances"""
        args = arg.split()
        all_objs = storage.all()

        if len(args) == 0:
            # Print all instances
            print([str(obj) for obj in all_objs.values()])
        else:
            class_name = args[0]
            if class_name not in self.__classes:
                print("** class doesn't exist **")
                return
            # Print instances of specific class
            filtered = [str(obj) for key, obj in all_objs.items()
                        if key.startswith(class_name + ".")]
            print(filtered)

    def do_update(self, arg):
        """Update an instance based on class name and id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = f"{args[0]}.{args[1]}"
        all_objs = storage.all()
        if key not in all_objs:
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        obj = all_objs[key]
        attr_name = args[2]
        attr_value = args[3]

        # Don't update id, created_at, updated_at
        if attr_name in ["id", "created_at", "updated_at"]:
            return

        # Remove quotes if present
        if attr_value.startswith('"') and attr_value.endswith('"'):
            attr_value = attr_value[1:-1]

        # Try to cast to appropriate type
        if hasattr(obj, attr_name):
            current_value = getattr(obj, attr_name)
            if isinstance(current_value, int):
                try:
                    attr_value = int(attr_value)
                except ValueError:
                    pass
            elif isinstance(current_value, float):
                try:
                    attr_value = float(attr_value)
                except ValueError:
                    pass

        setattr(obj, attr_name, attr_value)
        obj.save()

    def do_help(self, arg):
        """Help command"""
        return super().do_help(arg)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
