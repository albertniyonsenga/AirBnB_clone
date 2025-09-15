# AirBnB Clone - The Console

## Description
This is the first step towards building the **AirBnB clone** web application.  
In this step, we create a **command interpreter** in Python that allows us to manage AirBnB objects.  

The command interpreter works like a shell but is limited to specific use-cases for the project.  
It will be extended in future steps to support database storage, RESTful APIs, and a front-end interface.

---

## Command Interpreter
The command interpreter provides a way to:

- Create new objects (e.g., `User`, `Place`, `City`, etc.)
- Retrieve objects from storage (file storage for now, later database)
- Perform operations on objects (count, compute stats, etc.)
- Update object attributes
- Delete objects

Objects are serialized and stored in a JSON file.  
The flow of data is as follows:


---

## How to Start It
Clone this repository:
```bash
git clone https://github.com/Ntagungira-cmd/alu-AirBnB_clone.git
cd alu-AirBnB_clone
```
make the console executable:
```bash
chmod +x console.py
```

run the console in interactive mode:
```bash
./console.py
```
or in non-interactive mode:
```bash
echo "help" | ./console.py
```