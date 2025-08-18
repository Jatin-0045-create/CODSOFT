def todo():
    tasks = []
    completed = [] 
    print("----- This is Your To-Do List -----") 
    
    total_task = int(input("Enter how many tasks you want to add to the list: "))
    
    for i in range(total_task):
        task_name = input(f"Enter task {i+1}: ")
        tasks.append(task_name)
    
    print(f"Your today's to-do list is: {tasks}")
    
    while True:        
        print("\n----- MENU -----")
        print("1: Add a Task")
        print("2: Update a Task")
        print("3: Delete a Task")
        print("4: Mark as Done")
        print("5: Exit")        
        
        choice = int (input("Enter your choice: "))
        
        if choice == 1:
            new_task = input("Enter the task you want to add: ")
            tasks.append(new_task)
            print(f"Task: '{new_task}' has been successfully added to the To-Do list...")
            print(f"To-do list: {tasks}")
        
        elif choice == 2:
            up_task = input("Enter the task name you want to update: ")
            if up_task in tasks:
                updated_task  = input("Enter new task: ")
                index = tasks.index(up_task)
                tasks[index] = updated_task
                print (f"Task: '{updated_task}' has been successfully updated to the To-Do list...")
                print(f"To-do list: {tasks}")        

        elif choice == 3:   
            del_task = input("Which task do you want to delete from the to-do list: ")
            if del_task in tasks:
                index = tasks.index(del_task)
                del tasks[index]
                print (f"Task: '{del_task}' has been deleted from the To-Do list...")          
                print(f"To-do list: {tasks}")

        elif choice == 4:
            done_task = input ("Enter the task you have completed: ")
            if done_task in tasks:
                tasks.remove(done_task)
                completed.append(done_task)
                print(f"'{done_task}' completed!")
                print(f"Pending task: {tasks}")
                print(f"Completed task: {completed}")

        elif choice == 5: 
            print("Exiting the To-do list...")
            break
        
        else: 
            print("Invalid Choice")
            
todo() 