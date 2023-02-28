def login():
    with open('user.txt','r') as f:
    # Create comma delimited, str list with "\n" removed.
        cred_list = (f.read().replace("\n",",").replace(" ","")).split(",")
        user_arr = []
        passw_arr = []
    
        # Generate username and password array. Pw's have odd index.
        for i in range(len(cred_list)):
            if i % 2 != 0:
                passw_arr.append(cred_list[i])
            else:
                user_arr.append(cred_list[i])
        # User Prompt.
        usern, passw = (input("\nPlease enter a valid username\n\n: ").lower(),
                       input("\nPlease enter a valid password\n\n: "))

        # Check username array for against input prompt.
        while usern not in user_arr:
                usern = input("\nPlease enter a valid username\n\n: ").lower()

        # Check pw is present in passw_arr and corresponds with username via index.
        while (passw not in passw_arr or
                   passw_arr.index(passw) != user_arr.index(usern)):
            passw = input("\nPlease enter a valid password\n\n: ")
    menu(usern) # Passes username to menu fn
  
def menu(username):
    
    # Admin menu.
    while True:
        if username.lower() == "admin":
            menu = input(
"""
Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my tasks
gr - generate reports
vs - View statistics
e - Exit

: """
                   ).lower()
        # Menu for non-admin.
        else:
            menu = input(
"""
Select one of the following Options below:
a - Adding a task
va - View all tasks
vm - View my tasks
e - Exit

: """
                   ).lower()

        if menu == 'r':
            reg_user()
           
        elif menu == 'a':
            add_task()

        elif menu == 'va':
            view_all()
            
        elif menu == 'vm':
            view_mine(username) # Passes user name to view_mine fn

        elif menu == 'gr':
            gen_reports()

        elif menu == 'vs':
            view_stats()

        elif menu == 'e':
            print('\nGoodbye!!!\n\n')
            exit()

        else:
            print("\nYou have made a wrong choice, Please Try again")

def reg_user():
    # Code block entering new credentials and verifying pw.
    with open('user.txt', 'r') as f:
        nu_user  = input("\nPlease enter a new username\n\n: ").lower()
        check = f.read()

        while nu_user in check:
            nu_user = input(
f"""
{nu_user} is already exists.
Please enter a new username.

: """
                      ).lower()
        nu_pass = input("\nPlease a enter a new password\n\n: ")
        confirm_pass = input("\nPlease confirm new password\n\n: ")

        while nu_pass != confirm_pass:
            confirm_pass = (input(
"""
The confirmation does not match,
please re-confirm new password.

: """
                                ))
        with open('user.txt', 'a') as f:
            f.write(f"\n{nu_user}, {nu_pass}")
        print("\nUser has been registered.\n\n")

def add_task():
    import datetime
    # Code block only allows tasks to be created for existing users.
    
    assignee = input("\nPlease input username of task assignee.\n\n: ").lower()
    with open('user.txt', 'r') as f:
        assignee_check = f.read()

        while (assignee not in assignee_check or
                   len(assignee) < 3):
            assignee = input(
f"""
{assignee} is not an existing user.
Please enter an existing username.

: """
                            ).lower()
    # Other requested user prompts and variables.
    tsk_title = input("\nPlease input the task title.\n\n: ")
    tsk_desc = input("\nPlease input the task description.\n\n: ")
    # Date generated and formatted automatically from datetime module.
    asgn_date = ((datetime.date.today()).strftime("%d %b %Y"))
    input_date = input(
"""
Please enter a new due date.
format: DDMMYYYY

: """
                 )
    while (len(input_date) > 8 or
                len(input_date) < 8 or
                    input_date.isdigit() == False):
            
        input_date = input(
"""
This date format is not valid.
format: DDMMYYYY

Please enter a new due date.

: """
                     )
    from datetime import datetime    
    date = datetime.strptime(input_date,'%d%m%Y')
    due_date = datetime.strftime(date,"%d %b %Y")   
    comp = input("\nis the task complete? Yes/No.\n\n: ")
    with open('tasks.txt', 'a') as g:
        g.write(f"\n{assignee}, {tsk_title}, {tsk_desc}, {asgn_date}, {due_date}, {comp}")
    print(f"\n Task had been added for {assignee}.")
def view_all():
    
    with open('tasks.txt', 'r') as g:
        # Requested readouts. Also generates task number.
        line_num = 0
        for line in g:
            line_num += 1
            task = line.split(",")
            print(
f"""
_________________________________________________________________________________________
    
Task no.:                {line_num}
Task:                    {task[1].strip()}
Assigned to:             {task[0].strip()}
Date assigned:           {task[3].strip()}
Expected Completion:     {task[4].strip()}
Task description:
    {task[2].strip()}.
_________________________________________________________________________________________
"""
            )

def view_mine(user):
    # Creates list of tasks and counts tasks of current user.
    with open('tasks.txt', 'r') as g:
        user_tasks = 0
        tasks = []
        for line in g:
            task = line.split(",")
            tasks.append(task)
            if user in task:
                user_tasks += 1

    # While True menu provides requested options for actions. used "3" instead of "-1" for return to prev.            
    while True:
        view_type = input(
"""
Please select from the following options:

1. View all user tasks
2. View specific user task
3. Return to main menu

: """
                    )
        # Exception if no tasks for user.       
        if view_type == "1":
            if user_tasks == 0:
                print("\nYou have no pending tasks.\n\n")
                break

            with open('tasks.txt', 'r') as g:
                # Generates task list and prints user tasks. also updates list on successive selections   
                task_no = 0
                for task in tasks:
                    if user in task:
                        task_no += 1
                        print(
f"""
_________________________________________________________________________________________

Task no.:                {task_no}
Task:                    {task[1].strip()}
Assigned to:             {task[0].strip()}
Date assigned:           {task[3].strip()}
Expected Completion:     {task[4].strip()}
Task description:
    {task[2].strip()}.
_________________________________________________________________________________________
"""
                        )
        
        # Displays selected user task.
        elif view_type == "2":
            
            if user_tasks == 0:
                print("\nYou have no pending tasks.\n\n")
                break
            
            with open('tasks.txt', 'r') as g:
                view_task = int(input(f"\nPlease enter the task number of {user_tasks} tasks you wish to view\n\n: "))
                task_no = 0
                
                for task in tasks:
                    if user in task:
                        task_no += 1
                        if task_no == view_task:
                            print(
f"""
_________________________________________________________________________________________

Task no.:                {task_no}
Task:                    {task[1].strip()}
Assigned to:             {task[0].strip()}
Date assigned:           {task[3].strip()}
Task complete:           {task[4].strip()}
Task description:
    {task[2].strip()}.
_________________________________________________________________________________________
"""
                            )
                            
                            # Requested editing options   
                            while True:
                                modify = input(
"""
Would you like to :
            
1. Edit this task?
2. Mark this task complete?
3. Return to the previous menu.?
            
Please type the appropriate number.
            
: """
                                        )

                                # Exception if task marked complete       
                                if modify == "1":
                                    
                                    if task[5].lower().strip() == "yes":
                                        print(
"""
This task has been marked complete.
You may not modify it.
"""
                                        )
                                        return # Forces return to main menu and allows tasks to be refreshed
                                            
                                    elif task_no == view_task:
                                        
                                        # Requested sub options    
                                        while True:
                                            edit_task = input(
"""
Would you like to edit:
        
1. date?
2. assignee?
3. Return to the previous menu.
        
Please type the appropriate number.
        
: """
                                                        )
                                            
                                            # Date change    
                                            if edit_task == "1":
                                                task_date = input(
"""
Please enter a new due date.
format: DDMMYYYY

: """
                                                            )
                                                
                                                while (len(task_date) > 8 or
                                                            len(task_date) < 8 or
                                                                task_date.isdigit() == False): 
                                                    task_date = input(
"""
This date format is not valid.
format: DDMMYYYY

Please enter a new due date.

: """
                                                                )
                                                    
                                                from datetime import datetime    
                                                date = datetime.strptime(task_date,'%d%m%Y')
                                                task[4] = datetime.strftime(date,"%d %b %Y")
                                                
                                                with open('tasks.txt', 'w+') as g:
                                                    
                                                    for task in tasks:
                                                        g.write(f"{','.join(task)}")
                                                    print("\n\nThe due date has been changed!\n")
                                                    return

                                            # Assignee change    
                                            elif edit_task == "2":
                                                new_asgn = input(
"""
Please enter a new assignee.

: """
                                                            ).lower()
                                                # Exception for non existing user           
                                                with open('user.txt', 'r') as f:
                                                    assignee_check = f.read()
                                                    
                                                    while new_asgn not in assignee_check:
                                                        new_asgn = input(
f"""
{new_asgn} is not an existing user.
Please enter an existing username.

: """
                                                                    ).lower()
                                                    task[0] = new_asgn
                                                    
                                                    with open('tasks.txt', 'w+') as g:
                                                        
                                                        for task in tasks:
                                                            g.write(f"{','.join(task)}")
                                                            
                                                    print(f"\n\nThe assignee has been changed to {new_asgn}!\n\n")
                                                    return       
                                                
                                            # Return to previous menu
                                            elif edit_task == "3":
                                                break

                                            else:
                                                print("\nYou have not made a valid selection.\n\n")
                                
                                # Mark Task complete
                                if modify == "2":
                                    task[5] = "Yes\n"
                                    
                                    with open('tasks.txt', 'w+') as g:
                                        
                                        for task in tasks:
                                            g.write(f"{','.join(task)}")
                                            
                                    print("\n\nThis task has been marked complete.\n\n\n")
                                    return

                                if modify == "3":
                                    break
                                        
                                else:
                                    print("\nYou have not made a valid selection.\n\n")                       
                                
        elif view_type == "3":
            break

        else:
            print("\nYou have not selected a valid option.\n\n")

def gen_reports():
    import datetime
    # Setup counters and list to generate stats.
    tasks = []
    tot_tasks = 0
    comp_tasks = 0
    incomp_tasks = 0
    in_over = 0
    
    with open('tasks.txt', 'r') as g:

        # Reads most current version of tasks.txt.
        for line in g:
            tot_tasks += 1              
            task = line.split(",")
            tasks.append(task)
            
        for task in tasks:
            # Converts due date to datetime format for comparison with todays date.
            due_date = datetime.datetime.strptime(task[4].strip(), "%d %b %Y").date()
            today = datetime.date.today()

            # Counter Increment conditions.
            if task[5].lower().strip() == "yes":
                comp_tasks += 1
            
            elif task[5].lower().strip() == "no":
                incomp_tasks += 1
        
            while (today > due_date and
                  task[5].lower().strip() == "no"):
                in_over += 1
                break

               
        incomp_per = ((incomp_tasks
                      / tot_tasks)
                      * 100)
        in_over_per = ((in_over
                        / tot_tasks)
                       *100)
        with open('task_overview.txt', 'w+') as h:
            h.write(
# Requested txt output.
# Technically, generated tasks is 2 less than total as tasks.txt had 2 pre - existing.
f"""
********************
Task Overview Report
********************
________________________________________________________________________

Total no. of tasks ................................................ {tot_tasks}
Total no. of task_manager.py generated tasks: ..................... {tot_tasks-2}
Total no. of completed tasks: ..................................... {comp_tasks}
Total no. of incomplete tasks: .................................... {incomp_tasks}
Total no. of incomplete, overdue tasks: ........................... {in_over}
Percentage of incomplete tasks: ................................... {round(incomp_per, 2)}%
percentage of overdue tasks: ...................................... {round(in_over_per, 2)}%
________________________________________________________________________

"""
            )
            
    with open('user.txt', 'r') as i:

        # Counter and list setup
        tot_user = 0
        users= []

        # increment counter and populate. list
        for line in i:
            tot_user += 1
            user_cred = line.split(",")
            users.append(user_cred[0])

        # Setup empty dictionaries.  
        user_tasks = dict((el,0) for el in users)
        usr_tsk_com = dict((el,0) for el in users)
        usr_tsk_inc = dict((el,0) for el in users)
        usr_tsk_ovr = dict((el,0) for el in users)
        user_comp_per = dict((el,0) for el in users)
        user_incomp_per = dict((el,0) for el in users)
        user_in_ovr_per = dict((el,0) for el in users)
        user_tot_per = dict((el,0) for el in users)
        
        
        for sys_user in users:
            
            for task in tasks:
                due_date = datetime.datetime.strptime(task[4].strip(), "%d %b %Y").date()
                today = datetime.date.today()

                # Below condition creates keys for all users set at zero for user tasks.
                # Output still populates for all users even if a user has zero activity.
                # The following do not work as If/Elif statements.
                if sys_user in task:
                    user_tasks[sys_user] = user_tasks.get(sys_user, 0) + 1

                # Creates user keys for complete tasks.
                if (task[5].lower().strip() == "yes"
                          and sys_user in task):
                    usr_tsk_com[sys_user] = usr_tsk_com.get(sys_user, 0) + 1
                    
                # if/else groups avoid division by zero error for % calc and write result to dict.
                if user_tasks[sys_user] == 0:
                    user_comp_per[sys_user] = "N/A"
                else:
                    user_comp_per[sys_user] = (round(((usr_tsk_com[sys_user]
                                              / user_tasks[sys_user])
                                              * 100), 2))
                    
                # Creates user keys for incomplete tasks.    
                if (task[5].lower().strip() == "no" and
                      sys_user in task):
                    usr_tsk_inc[sys_user] = usr_tsk_inc.get(sys_user, 0) + 1
                    
                if user_tasks[sys_user] == 0:
                    user_incomp_per[sys_user] = "N/A"
                else:    
                    user_incomp_per[sys_user] = (round(((usr_tsk_inc[sys_user]
                                                 / user_tasks[sys_user])
                                                 * 100), 2))
                    
                # Creates keys for incomplete and overdue tasks.
                if (today > due_date and
                          sys_user in task and
                              task[5].lower().strip() == "no"):
                    usr_tsk_ovr[sys_user] = usr_tsk_ovr.get(sys_user, 0) + 1
                    
                if user_tasks[sys_user] == 0:
                    user_in_ovr_per[sys_user] = "N/A"
                else:    
                    user_in_ovr_per[sys_user] = (round(((usr_tsk_ovr[sys_user]
                                                / user_tasks[sys_user])
                                                * 100), 2))

                user_tot_per[sys_user] = (round(((user_tasks[sys_user]
                                        / tot_tasks)
                                        * 100), 2))

    # Requested Output file        
    with open('user_overview.txt', 'w') as j:
        j.write(
"""
*********************
User Overview Reports
*********************
"""     )
        
        for sys_user in users:
            j.write(
f"""
User overview for {sys_user}:
_________________________________________________________________________

Total Users ....................................................... {tot_user}
Total no. of tasks ................................................ {tot_tasks}
Total no. of task_manager.py generated tasks: ..................... {tot_tasks - 2}
Total no. of user's tasks: ........................................ {user_tasks[sys_user]}
Percentage of total tasks assigned: ............................... {user_tot_per[sys_user]}%
Percentage of assigned tasks complete: ............................ {user_comp_per[sys_user]}%
Percentage of assigned tasks T.B.C: ............................... {user_incomp_per[sys_user]}%
Percentage of assigned tasks overdue and incomplete: .............. {user_in_ovr_per[sys_user]}%
_________________________________________________________________________

"""
            )
    print("\n\n'Task Overview' and 'User Overview' reports have been generated.\n")
   
def view_stats():
    # Gen reports if not already done so
    gen_reports()
    with open('user.txt', 'r') as f:
        
        # Code block for requested statistics.
        with open('tasks.txt', 'r') as g:
            
            cnt_user =0
            cnt_task =0
            
            for line in f:
                cnt_user += 1
                
            for line in g:
                cnt_task += 1
            print(
f"""
*****************
System statistics
*****************
___________________________________

Number of users: ............... {cnt_user}
Number of tasks: ................{cnt_task}
___________________________________
"""
            )
    # Code block for stats read from earlier ouput txt file.
    with open('task_overview.txt', 'r') as x:
        
        with open('user_overview.txt', 'r') as y:
            task_overv = x.read()
            user_overv = y.read()
            print(task_overv)
            print(user_overv)
        
login()
def login():
    with open('user.txt','r') as f:
    # Create comma delimited, str list with "\n" removed.
        cred_list = (f.read().replace("\n",",").replace(" ","")).split(",")
        user_arr = []
        passw_arr = []
    
        # Generate username and password array. Pw's have odd index.
        for i in range(len(cred_list)):
            if i % 2 != 0:
                passw_arr.append(cred_list[i])
            else:
                user_arr.append(cred_list[i])
        # User Prompt.
        usern, passw = (input("\nPlease enter a valid username\n\n: ").lower(),
                       input("\nPlease enter a valid password\n\n: "))

        # Check username array for against input prompt.
        while usern not in user_arr:
                usern = input("\nPlease enter a valid username\n\n: ").lower()

        # Check pw is present in passw_arr and corresponds with username via index.
        while (passw not in passw_arr or
                   passw_arr.index(passw) != user_arr.index(usern)):
            passw = input("\nPlease enter a valid password\n\n: ")
    menu(usern) # Passes username to menu fn
  
def menu(username):
    
    # Admin menu.
    while True:
        if username.lower() == "admin":
            menu = input(
"""
Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my tasks
gr - generate reports
vs - View statistics
e - Exit

: """
                   ).lower()
        # Menu for non-admin.
        else:
            menu = input(
"""
Select one of the following Options below:
a - Adding a task
va - View all tasks
vm - View my tasks
e - Exit

: """
                   ).lower()

        if menu == 'r':
            reg_user()
           
        elif menu == 'a':
            add_task()

        elif menu == 'va':
            view_all()
            
        elif menu == 'vm':
            view_mine(username) # Passes user name to view_mine fn

        elif menu == 'gr':
            gen_reports()

        elif menu == 'vs':
            view_stats()

        elif menu == 'e':
            print('\nGoodbye!!!\n\n')
            exit()

        else:
            print("\nYou have made a wrong choice, Please Try again")

def reg_user():
    # Code block entering new credentials and verifying pw.
    with open('user.txt', 'r') as f:
        nu_user  = input("\nPlease enter a new username\n\n: ").lower()
        check = f.read()

        while nu_user in check:
            nu_user = input(
f"""
{nu_user} is already exists.
Please enter a new username.

: """
                      ).lower()
        nu_pass = input("\nPlease a enter a new password\n\n: ")
        confirm_pass = input("\nPlease confirm new password\n\n: ")

        while nu_pass != confirm_pass:
            confirm_pass = (input(
"""
The confirmation does not match,
please re-confirm new password.

: """
                                ))
        with open('user.txt', 'a') as f:
            f.write(f"\n{nu_user}, {nu_pass}")
        print("\nUser has been registered.\n\n")

def add_task():
    import datetime
    # Code block only allows tasks to be created for existing users.
    
    assignee = input("\nPlease input username of task assignee.\n\n: ").lower()
    with open('user.txt', 'r') as f:
        assignee_check = f.read()

        while (assignee not in assignee_check or
                   len(assignee) < 3):
            assignee = input(
f"""
{assignee} is not an existing user.
Please enter an existing username.

: """
                            ).lower()
    # Other requested user prompts and variables.
    tsk_title = input("\nPlease input the task title.\n\n: ")
    tsk_desc = input("\nPlease input the task description.\n\n: ")
    # Date generated and formatted automatically from datetime module.
    asgn_date = ((datetime.date.today()).strftime("%d %b %Y"))
    input_date = input(
"""
Please enter a new due date.
format: DDMMYYYY

: """
                 )
    while (len(input_date) > 8 or
                len(input_date) < 8 or
                    input_date.isdigit() == False):
            
        input_date = input(
"""
This date format is not valid.
format: DDMMYYYY

Please enter a new due date.

: """
                     )
    from datetime import datetime    
    date = datetime.strptime(input_date,'%d%m%Y')
    due_date = datetime.strftime(date,"%d %b %Y")   
    comp = input("\nis the task complete? Yes/No.\n\n: ")
    with open('tasks.txt', 'a') as g:
        g.write(f"\n{assignee}, {tsk_title}, {tsk_desc}, {asgn_date}, {due_date}, {comp}")
    print(f"\n Task had been added for {assignee}.")
def view_all():
    
    with open('tasks.txt', 'r') as g:
        # Requested readouts. Also generates task number.
        line_num = 0
        for line in g:
            line_num += 1
            task = line.split(",")
            print(
f"""
_________________________________________________________________________________________
    
Task no.:                {line_num}
Task:                    {task[1].strip()}
Assigned to:             {task[0].strip()}
Date assigned:           {task[3].strip()}
Expected Completion:     {task[4].strip()}
Task description:
    {task[2].strip()}.
_________________________________________________________________________________________
"""
            )

def view_mine(user):
    # Creates list of tasks and counts tasks of current user.
    with open('tasks.txt', 'r') as g:
        user_tasks = 0
        tasks = []
        for line in g:
            task = line.split(",")
            tasks.append(task)
            if user in task:
                user_tasks += 1

    # While True menu provides requested options for actions. used "3" instead of "-1" for return to prev.            
    while True:
        view_type = input(
"""
Please select from the following options:

1. View all user tasks
2. View specific user task
3. Return to main menu

: """
                    )
        # Exception if no tasks for user.       
        if view_type == "1":
            if user_tasks == 0:
                print("\nYou have no pending tasks.\n\n")
                break

            with open('tasks.txt', 'r') as g:
                # Generates task list and prints user tasks. also updates list on successive selections   
                task_no = 0
                for task in tasks:
                    if user in task:
                        task_no += 1
                        print(
f"""
_________________________________________________________________________________________

Task no.:                {task_no}
Task:                    {task[1].strip()}
Assigned to:             {task[0].strip()}
Date assigned:           {task[3].strip()}
Expected Completion:     {task[4].strip()}
Task description:
    {task[2].strip()}.
_________________________________________________________________________________________
"""
                        )
        
        # Displays selected user task.
        elif view_type == "2":
            
            if user_tasks == 0:
                print("\nYou have no pending tasks.\n\n")
                break
            
            with open('tasks.txt', 'r') as g:
                view_task = int(input(f"\nPlease enter the task number of {user_tasks} tasks you wish to view\n\n: "))
                task_no = 0
                
                for task in tasks:
                    if user in task:
                        task_no += 1
                        if task_no == view_task:
                            print(
f"""
_________________________________________________________________________________________

Task no.:                {task_no}
Task:                    {task[1].strip()}
Assigned to:             {task[0].strip()}
Date assigned:           {task[3].strip()}
Task complete:           {task[4].strip()}
Task description:
    {task[2].strip()}.
_________________________________________________________________________________________
"""
                            )
                            
                            # Requested editing options   
                            while True:
                                modify = input(
"""
Would you like to :
            
1. Edit this task?
2. Mark this task complete?
3. Return to the previous menu.?
            
Please type the appropriate number.
            
: """
                                        )

                                # Exception if task marked complete       
                                if modify == "1":
                                    
                                    if task[5].lower().strip() == "yes":
                                        print(
"""
This task has been marked complete.
You may not modify it.
"""
                                        )
                                        return # Forces return to main menu and allows tasks to be refreshed
                                            
                                    elif task_no == view_task:
                                        
                                        # Requested sub options    
                                        while True:
                                            edit_task = input(
"""
Would you like to edit:
        
1. date?
2. assignee?
3. Return to the previous menu.
        
Please type the appropriate number.
        
: """
                                                        )
                                            
                                            # Date change    
                                            if edit_task == "1":
                                                task_date = input(
"""
Please enter a new due date.
format: DDMMYYYY

: """
                                                            )
                                                
                                                while (len(task_date) > 8 or
                                                            len(task_date) < 8 or
                                                                task_date.isdigit() == False): 
                                                    task_date = input(
"""
This date format is not valid.
format: DDMMYYYY

Please enter a new due date.

: """
                                                                )
                                                    
                                                from datetime import datetime    
                                                date = datetime.strptime(task_date,'%d%m%Y')
                                                task[4] = datetime.strftime(date,"%d %b %Y")
                                                
                                                with open('tasks.txt', 'w+') as g:
                                                    
                                                    for task in tasks:
                                                        g.write(f"{','.join(task)}")
                                                    print("\n\nThe due date has been changed!\n")
                                                    return

                                            # Assignee change    
                                            elif edit_task == "2":
                                                new_asgn = input(
"""
Please enter a new assignee.

: """
                                                            ).lower()
                                                # Exception for non existing user           
                                                with open('user.txt', 'r') as f:
                                                    assignee_check = f.read()
                                                    
                                                    while new_asgn not in assignee_check:
                                                        new_asgn = input(
f"""
{new_asgn} is not an existing user.
Please enter an existing username.

: """
                                                                    ).lower()
                                                    task[0] = new_asgn
                                                    
                                                    with open('tasks.txt', 'w+') as g:
                                                        
                                                        for task in tasks:
                                                            g.write(f"{','.join(task)}")
                                                            
                                                    print(f"\n\nThe assignee has been changed to {new_asgn}!\n\n")
                                                    return       
                                                
                                            # Return to previous menu
                                            elif edit_task == "3":
                                                break

                                            else:
                                                print("\nYou have not made a valid selection.\n\n")
                                
                                # Mark Task complete
                                if modify == "2":
                                    task[5] = "Yes\n"
                                    
                                    with open('tasks.txt', 'w+') as g:
                                        
                                        for task in tasks:
                                            g.write(f"{','.join(task)}")
                                            
                                    print("\n\nThis task has been marked complete.\n\n\n")
                                    return

                                if modify == "3":
                                    break
                                        
                                else:
                                    print("\nYou have not made a valid selection.\n\n")                       
                                
        elif view_type == "3":
            break

        else:
            print("\nYou have not selected a valid option.\n\n")

def gen_reports():
    import datetime
    # Setup counters and list to generate stats.
    tasks = []
    tot_tasks = 0
    comp_tasks = 0
    incomp_tasks = 0
    in_over = 0
    
    with open('tasks.txt', 'r') as g:

        # Reads most current version of tasks.txt.
        for line in g:
            tot_tasks += 1              
            task = line.split(",")
            tasks.append(task)
            
        for task in tasks:
            # Converts due date to datetime format for comparison with todays date.
            due_date = datetime.datetime.strptime(task[4].strip(), "%d %b %Y").date()
            today = datetime.date.today()

            # Counter Increment conditions.
            if task[5].lower().strip() == "yes":
                comp_tasks += 1
            
            elif task[5].lower().strip() == "no":
                incomp_tasks += 1
        
            while (today > due_date and
                  task[5].lower().strip() == "no"):
                in_over += 1
                break

               
        incomp_per = ((incomp_tasks
                      / tot_tasks)
                      * 100)
        in_over_per = ((in_over
                        / tot_tasks)
                       *100)
        with open('task_overview.txt', 'w+') as h:
            h.write(
# Requested txt output.
# Technically, generated tasks is 2 less than total as tasks.txt had 2 pre - existing.
f"""
********************
Task Overview Report
********************
________________________________________________________________________

Total no. of tasks ................................................ {tot_tasks}
Total no. of task_manager.py generated tasks: ..................... {tot_tasks-2}
Total no. of completed tasks: ..................................... {comp_tasks}
Total no. of incomplete tasks: .................................... {incomp_tasks}
Total no. of incomplete, overdue tasks: ........................... {in_over}
Percentage of incomplete tasks: ................................... {round(incomp_per, 2)}%
percentage of overdue tasks: ...................................... {round(in_over_per, 2)}%
________________________________________________________________________

"""
            )
            
    with open('user.txt', 'r') as i:

        # Counter and list setup
        tot_user = 0
        users= []

        # increment counter and populate. list
        for line in i:
            tot_user += 1
            user_cred = line.split(",")
            users.append(user_cred[0])

        # Setup empty dictionaries.  
        user_tasks = dict((el,0) for el in users)
        usr_tsk_com = dict((el,0) for el in users)
        usr_tsk_inc = dict((el,0) for el in users)
        usr_tsk_ovr = dict((el,0) for el in users)
        user_comp_per = dict((el,0) for el in users)
        user_incomp_per = dict((el,0) for el in users)
        user_in_ovr_per = dict((el,0) for el in users)
        user_tot_per = dict((el,0) for el in users)
        
        
        for sys_user in users:
            
            for task in tasks:
                due_date = datetime.datetime.strptime(task[4].strip(), "%d %b %Y").date()
                today = datetime.date.today()

                # Below condition creates keys for all users set at zero for user tasks.
                # Output still populates for all users even if a user has zero activity.
                # The following do not work as If/Elif statements.
                if sys_user in task:
                    user_tasks[sys_user] = user_tasks.get(sys_user, 0) + 1

                # Creates user keys for complete tasks.
                if (task[5].lower().strip() == "yes"
                          and sys_user in task):
                    usr_tsk_com[sys_user] = usr_tsk_com.get(sys_user, 0) + 1
                    
                # if/else groups avoid division by zero error for % calc and write result to dict.
                if user_tasks[sys_user] == 0:
                    user_comp_per[sys_user] = "N/A"
                else:
                    user_comp_per[sys_user] = (round(((usr_tsk_com[sys_user]
                                              / user_tasks[sys_user])
                                              * 100), 2))
                    
                # Creates user keys for incomplete tasks.    
                if (task[5].lower().strip() == "no" and
                      sys_user in task):
                    usr_tsk_inc[sys_user] = usr_tsk_inc.get(sys_user, 0) + 1
                    
                if user_tasks[sys_user] == 0:
                    user_incomp_per[sys_user] = "N/A"
                else:    
                    user_incomp_per[sys_user] = (round(((usr_tsk_inc[sys_user]
                                                 / user_tasks[sys_user])
                                                 * 100), 2))
                    
                # Creates keys for incomplete and overdue tasks.
                if (today > due_date and
                          sys_user in task and
                              task[5].lower().strip() == "no"):
                    usr_tsk_ovr[sys_user] = usr_tsk_ovr.get(sys_user, 0) + 1
                    
                if user_tasks[sys_user] == 0:
                    user_in_ovr_per[sys_user] = "N/A"
                else:    
                    user_in_ovr_per[sys_user] = (round(((usr_tsk_ovr[sys_user]
                                                / user_tasks[sys_user])
                                                * 100), 2))

                user_tot_per[sys_user] = (round(((user_tasks[sys_user]
                                        / tot_tasks)
                                        * 100), 2))

    # Requested Output file        
    with open('user_overview.txt', 'w') as j:
        j.write(
"""
*********************
User Overview Reports
*********************
"""     )
        
        for sys_user in users:
            j.write(
f"""
User overview for {sys_user}:
_________________________________________________________________________

Total Users ....................................................... {tot_user}
Total no. of tasks ................................................ {tot_tasks}
Total no. of task_manager.py generated tasks: ..................... {tot_tasks - 2}
Total no. of user's tasks: ........................................ {user_tasks[sys_user]}
Percentage of total tasks assigned: ............................... {user_tot_per[sys_user]}%
Percentage of assigned tasks complete: ............................ {user_comp_per[sys_user]}%
Percentage of assigned tasks T.B.C: ............................... {user_incomp_per[sys_user]}%
Percentage of assigned tasks overdue and incomplete: .............. {user_in_ovr_per[sys_user]}%
_________________________________________________________________________

"""
            )
    print("\n\n'Task Overview' and 'User Overview' reports have been generated.\n")
   
def view_stats():
    # Gen reports if not already done so
    gen_reports()
    with open('user.txt', 'r') as f:
        
        # Code block for requested statistics.
        with open('tasks.txt', 'r') as g:
            
            cnt_user =0
            cnt_task =0
            
            for line in f:
                cnt_user += 1
                
            for line in g:
                cnt_task += 1
            print(
f"""
*****************
System statistics
*****************
___________________________________

Number of users: ............... {cnt_user}
Number of tasks: ................{cnt_task}
___________________________________
"""
            )
    # Code block for stats read from earlier ouput txt file.
    with open('task_overview.txt', 'r') as x:
        
        with open('user_overview.txt', 'r') as y:
            task_overv = x.read()
            user_overv = y.read()
            print(task_overv)
            print(user_overv)
        
login()
