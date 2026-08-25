# ToDo_Manager.py
# CloudExify Python Internship — Month 2 — Project 4 (Final Project)
# Hafiz Hassam Ali Abdul Rehman | Registration No: CX-INT-2026-PY-0378
#
# Bonus features implemented:
#   1. Show overdue tasks (past due date) with visual warning
#   2. Edit task title, priority, due date, or category
#   3. Search tasks by keyword in title
#   4. Show tasks due today
#   5. Task categories (Work / Study / Personal)

import json
import os
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# ─────────────────────────────────────────────────────────────
# COLOR THEME
# Same small, consistent palette used in Projects 1 and 2.
# ─────────────────────────────────────────────────────────────
Header = Fore.CYAN + Style.BRIGHT
Success = Fore.GREEN + Style.BRIGHT
Error = Fore.RED + Style.BRIGHT
Warning = Fore.YELLOW + Style.BRIGHT
Info = Fore.BLUE + Style.BRIGHT
Result = Fore.WHITE + Style.BRIGHT
Question = Fore.CYAN + Style.BRIGHT
Option = Fore.WHITE
Title_Color = Fore.MAGENTA + Style.BRIGHT
Overdue_Color = Fore.RED + Style.BRIGHT
Due_Today_Color = Fore.YELLOW + Style.BRIGHT
Border_Color = Fore.WHITE + Style.DIM

Data_File_Path = "Tasks_Data.json"  # matches the sample data file shipped with this project
Priority_Order = {"High": 1, "Medium": 2, "Low": 3}
Categories_List = ["Work", "Study", "Personal"]
Next_Task_Id = 1


# ----------------------------------------------------------------------
# Display Helpers
# ----------------------------------------------------------------------

def Print_Border(Character="=", Length=60):
    print(Border_Color + Character * Length)


def Print_Title(Title_Text):
    Print_Border()
    print(Title_Color + f"   {Title_Text}")
    Print_Border()


def Print_Section(Section_Text):
    print(Header + f"\n{Section_Text}")


# ----------------------------------------------------------------------
# Date Helpers
# ----------------------------------------------------------------------

def Get_Today_Date():
    """Returns today's date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")


def Is_Date_Valid(Date_Text):
    """Checks if a date string is in YYYY-MM-DD format (or the no-date placeholder)."""
    if Date_Text == "No due date":
        return True
    try:
        datetime.strptime(Date_Text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def Is_Date_Overdue(Date_Text):
    """Checks if a due date has passed, comparing dates only (not time-of-day)."""
    if Date_Text == "No due date":
        return False
    try:
        Due_Date = datetime.strptime(Date_Text, "%Y-%m-%d").date()
        Today = datetime.now().date()
        return Due_Date < Today
    except ValueError:
        return False


def Is_Due_Today(Date_Text):
    """Checks if a due date is today."""
    if Date_Text == "No due date":
        return False
    try:
        Due_Date = datetime.strptime(Date_Text, "%Y-%m-%d").date()
        Today = datetime.now().date()
        return Due_Date == Today
    except ValueError:
        return False


# ----------------------------------------------------------------------
# File Operations
# ----------------------------------------------------------------------

def Load_Tasks():
    """Loads tasks from the JSON file, or creates sample tasks on first run."""
    global Next_Task_Id

    if not os.path.exists(Data_File_Path):
        return Create_Sample_Tasks()

    try:
        with open(Data_File_Path, "r") as File_Handle:
            All_Tasks = json.load(File_Handle)

        if All_Tasks:
            Next_Task_Id = max(Task_Item["Id"] for Task_Item in All_Tasks) + 1

        print(Success + f"Loaded {len(All_Tasks)} tasks from file.")
        return All_Tasks
    except json.JSONDecodeError:
        print(Error + "Error reading JSON file. Starting with an empty list.")
        return []
    except OSError as Error_Message:
        print(Error + f"Error loading tasks: {Error_Message}")
        return []


def Save_Tasks(All_Tasks):
    """Saves the full task list to the JSON file."""
    try:
        with open(Data_File_Path, "w") as File_Handle:
            json.dump(All_Tasks, File_Handle, indent=4)
        return True
    except OSError as Error_Message:
        print(Error + f"Error saving tasks: {Error_Message}")
        return False


def Create_Sample_Tasks():
    """Creates sample tasks for first-time users."""
    global Next_Task_Id

    Sample_Tasks = [
        {
            "Id": 1,
            "Title": "Complete Python Internship Projects",
            "Priority": "High",
            "Due_Date": "2026-07-30",
            "Status": "Pending",
            "Category": "Work",
            "Created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
        {
            "Id": 2,
            "Title": "Review All Project Submissions",
            "Priority": "High",
            "Due_Date": "2026-07-25",
            "Status": "Pending",
            "Category": "Work",
            "Created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
        {
            "Id": 3,
            "Title": "Prepare Final Documentation",
            "Priority": "Medium",
            "Due_Date": "2026-07-28",
            "Status": "Pending",
            "Category": "Work",
            "Created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
        {
            "Id": 4,
            "Title": "Study Advanced Python Concepts",
            "Priority": "High",
            "Due_Date": "2026-07-20",
            "Status": "Pending",
            "Category": "Study",
            "Created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
        {
            "Id": 5,
            "Title": "Complete Portfolio Website",
            "Priority": "High",
            "Due_Date": "2026-08-10",
            "Status": "Pending",
            "Category": "Personal",
            "Created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
        {
            "Id": 6,
            "Title": "Practice Coding Problems",
            "Priority": "Medium",
            "Due_Date": "2026-07-22",
            "Status": "Pending",
            "Category": "Study",
            "Created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
        {
            "Id": 7,
            "Title": "Update LinkedIn Profile",
            "Priority": "Low",
            "Due_Date": "2026-07-18",
            "Status": "Pending",
            "Category": "Personal",
            "Created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
        {
            "Id": 8,
            "Title": "Prepare for Final Interview",
            "Priority": "High",
            "Due_Date": "2026-07-15",
            "Status": "Done",
            "Category": "Work",
            "Created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
        {
            "Id": 9,
            "Title": "Clean Up Workspace",
            "Priority": "Low",
            "Due_Date": "2026-07-12",
            "Status": "Done",
            "Category": "Personal",
            "Created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
        {
            "Id": 10,
            "Title": "Organize Project Files",
            "Priority": "Medium",
            "Due_Date": "2026-07-16",
            "Status": "Done",
            "Category": "Work",
            "Created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
    ]

    Next_Task_Id = 11
    Save_Tasks(Sample_Tasks)
    print(Success + "Sample tasks created successfully.")
    return Sample_Tasks


# ----------------------------------------------------------------------
# Core Feature Functions
# ----------------------------------------------------------------------

def Add_Task(All_Tasks):
    """Adds a new task with title, priority, due date, and category."""
    global Next_Task_Id

    Print_Section("ADD NEW TASK")

    Title_Text = input(Question + "Task title: " + Style.RESET_ALL).strip()
    while not Title_Text:
        print(Error + "Title cannot be empty.")
        Title_Text = input(Question + "Task title: " + Style.RESET_ALL).strip()

    print(Info + "\nPriority Levels:")
    print(Option + "  1. High")
    print(Option + "  2. Medium")
    print(Option + "  3. Low")

    Priority_Value = ""
    while True:
        Priority_Choice = input(Question + "Select priority (1-3): " + Style.RESET_ALL).strip()
        if Priority_Choice == "1":
            Priority_Value = "High"
            break
        elif Priority_Choice == "2":
            Priority_Value = "Medium"
            break
        elif Priority_Choice == "3":
            Priority_Value = "Low"
            break
        else:
            print(Error + "Please enter 1, 2, or 3.")

    Due_Date_Value = ""
    while True:
        Due_Date_Value = input(
            Question + "Due date (YYYY-MM-DD) or press Enter to skip: " + Style.RESET_ALL
        ).strip()
        if not Due_Date_Value:
            Due_Date_Value = "No due date"
            break
        if Is_Date_Valid(Due_Date_Value):
            break
        print(Error + "Invalid date format. Use YYYY-MM-DD.")

    print(Info + "\nCategories:")
    for Index, Category_Name in enumerate(Categories_List, start=1):
        print(Option + f"  {Index}. {Category_Name}")

    Category_Value = ""
    while True:
        Raw_Choice = input(Question + "Select category (1-3): " + Style.RESET_ALL).strip()
        if not Raw_Choice.isdigit():
            print(Error + "Please enter a number.")
            continue
        Choice_Number = int(Raw_Choice)
        if 1 <= Choice_Number <= len(Categories_List):
            Category_Value = Categories_List[Choice_Number - 1]
            break
        print(Error + f"Please enter 1-{len(Categories_List)}.")

    New_Task = {
        "Id": Next_Task_Id,
        "Title": Title_Text,
        "Priority": Priority_Value,
        "Due_Date": Due_Date_Value,
        "Status": "Pending",
        "Category": Category_Value,
        "Created": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    All_Tasks.append(New_Task)
    Next_Task_Id += 1

    if Save_Tasks(All_Tasks):
        print(Success + f"\nTask added successfully! ID: {New_Task['Id']}")
        print(Info + f"  Title    : {New_Task['Title']}")
        print(Info + f"  Priority : {New_Task['Priority']}")
        print(Info + f"  Due      : {New_Task['Due_Date']}")
        print(Info + f"  Category : {New_Task['Category']}")


def View_Tasks(All_Tasks, Filter_Status=None, Filter_Priority=None, Filter_Category=None):
    """Displays tasks, optionally filtered by status, priority, or category."""
    if not All_Tasks:
        print(Warning + "\nNo tasks found.")
        return

    Display_List = All_Tasks
    if Filter_Status:
        Display_List = [Task_Item for Task_Item in All_Tasks if Task_Item["Status"] == Filter_Status]
    if Filter_Priority:
        Display_List = [Task_Item for Task_Item in Display_List if Task_Item["Priority"] == Filter_Priority]
    if Filter_Category:
        Display_List = [Task_Item for Task_Item in Display_List if Task_Item["Category"] == Filter_Category]

    if not Display_List:
        print(Warning + "\nNo tasks match your criteria.")
        return

    Display_List = sorted(Display_List, key=lambda Task_Item: Priority_Order.get(Task_Item["Priority"], 4))

    Print_Border()
    print(Title_Color + "                          TASK LIST")
    Print_Border()

    print(Header + f"{'ID':<5}{'Title':<32}{'Priority':<10}{'Status':<10}{'Category':<10}{'Due Date':<15}")
    print(Border_Color + "-" * 87)

    for Task_Item in Display_List:
        Status_Color = Success if Task_Item["Status"] == "Done" else Warning

        Overdue_Marker = ""
        if Task_Item["Status"] == "Pending" and Is_Date_Overdue(Task_Item["Due_Date"]):
            Overdue_Marker = Overdue_Color + "[OVERDUE] "
        elif Task_Item["Status"] == "Pending" and Is_Due_Today(Task_Item["Due_Date"]):
            Overdue_Marker = Due_Today_Color + "[TODAY] "

        if Task_Item["Priority"] == "High":
            Priority_Color = Overdue_Color
        elif Task_Item["Priority"] == "Medium":
            Priority_Color = Warning
        else:
            Priority_Color = Info

        Display_Title = Task_Item["Title"]
        if len(Display_Title) > 30:
            Display_Title = Display_Title[:27] + "..."

        print(
            f"{Overdue_Marker}{Task_Item['Id']:<5}{Display_Title:<32}"
            f"{Priority_Color}{Task_Item['Priority']:<10}"
            f"{Status_Color}{Task_Item['Status']:<10}"
            f"{Info}{Task_Item['Category']:<10}"
            f"{Option}{Task_Item['Due_Date']:<15}" + Style.RESET_ALL
        )

    Print_Border("-")

    Total_Pending = sum(1 for Task_Item in Display_List if Task_Item["Status"] == "Pending")
    Total_Done = sum(1 for Task_Item in Display_List if Task_Item["Status"] == "Done")
    Overdue_Count = sum(
        1 for Task_Item in Display_List
        if Task_Item["Status"] == "Pending" and Is_Date_Overdue(Task_Item["Due_Date"])
    )

    print(Info + f"  Total   : {len(Display_List)} tasks")
    print(Warning + f"  Pending : {Total_Pending}")
    print(Success + f"  Done    : {Total_Done}")
    if Overdue_Count > 0:
        print(Overdue_Color + f"  Overdue : {Overdue_Count}")
    Print_Border()


def Mark_Done(All_Tasks):
    """Marks a pending task as done."""
    if not All_Tasks:
        print(Warning + "\nNo tasks to mark as done.")
        return

    Pending_Tasks = [Task_Item for Task_Item in All_Tasks if Task_Item["Status"] == "Pending"]
    if not Pending_Tasks:
        print(Success + "\nAll tasks are already done.")
        return

    Print_Section("MARK TASK AS DONE")
    View_Tasks(All_Tasks, Filter_Status="Pending")

    Raw_Id = input(Question + "\nEnter task ID to mark as done: " + Style.RESET_ALL).strip()
    if not Raw_Id.isdigit():
        print(Error + "Please enter a valid number.")
        return
    Target_Id = int(Raw_Id)

    for Task_Item in All_Tasks:
        if Task_Item["Id"] == Target_Id:
            if Task_Item["Status"] == "Done":
                print(Warning + f"Task '{Task_Item['Title']}' is already done.")
                return
            Task_Item["Status"] = "Done"
            if Save_Tasks(All_Tasks):
                print(Success + f"\nTask '{Task_Item['Title']}' marked as done.")
            return

    print(Error + f"No task found with ID {Target_Id}.")


def Delete_Task(All_Tasks):
    """Deletes a task by ID, with confirmation."""
    if not All_Tasks:
        print(Warning + "\nNo tasks to delete.")
        return

    Print_Section("DELETE TASK")
    View_Tasks(All_Tasks)

    Raw_Id = input(Question + "\nEnter task ID to delete: " + Style.RESET_ALL).strip()
    if not Raw_Id.isdigit():
        print(Error + "Please enter a valid number.")
        return
    Target_Id = int(Raw_Id)

    for Index, Task_Item in enumerate(All_Tasks):
        if Task_Item["Id"] == Target_Id:
            Confirmation_Input = input(
                Warning + f"Delete '{Task_Item['Title']}'? (yes/no): " + Style.RESET_ALL
            ).strip().lower()
            if Confirmation_Input in ("yes", "y"):
                All_Tasks.pop(Index)
                if Save_Tasks(All_Tasks):
                    print(Success + "Task deleted successfully.")
            else:
                print(Info + "Deletion cancelled.")
            return

    print(Error + f"No task found with ID {Target_Id}.")


def Show_Overdue_Tasks(All_Tasks):
    """Bonus: shows tasks that are pending and past their due date."""
    if not All_Tasks:
        print(Warning + "\nNo tasks found.")
        return

    Overdue_Tasks = [
        Task_Item for Task_Item in All_Tasks
        if Task_Item["Status"] == "Pending" and Is_Date_Overdue(Task_Item["Due_Date"])
    ]

    if not Overdue_Tasks:
        print(Success + "\nNo overdue tasks. Keep up the good work!")
        return

    Print_Section("OVERDUE TASKS")
    View_Tasks(Overdue_Tasks)


def Show_Tasks_Due_Today(All_Tasks):
    """Bonus: shows tasks due today."""
    if not All_Tasks:
        print(Warning + "\nNo tasks found.")
        return

    Due_Today_Tasks = [
        Task_Item for Task_Item in All_Tasks
        if Task_Item["Status"] == "Pending" and Is_Due_Today(Task_Item["Due_Date"])
    ]

    if not Due_Today_Tasks:
        print(Info + "\nNo tasks due today.")
        return

    Print_Section("TASKS DUE TODAY")
    View_Tasks(Due_Today_Tasks)


def Search_Tasks(All_Tasks):
    """Bonus: searches tasks by keyword in the title."""
    if not All_Tasks:
        print(Warning + "\nNo tasks to search.")
        return

    Search_Keyword = input(Question + "Enter search keyword: " + Style.RESET_ALL).strip().lower()
    if not Search_Keyword:
        print(Error + "Please enter a keyword.")
        return

    Search_Results = [Task_Item for Task_Item in All_Tasks if Search_Keyword in Task_Item["Title"].lower()]

    if not Search_Results:
        print(Warning + f"\nNo tasks found containing '{Search_Keyword}'.")
        return

    Print_Section(f"SEARCH RESULTS: '{Search_Keyword}'")
    View_Tasks(Search_Results)


def Edit_Task(All_Tasks):
    """Bonus: edits a task's title, priority, due date, or category."""
    if not All_Tasks:
        print(Warning + "\nNo tasks to edit.")
        return

    Print_Section("EDIT TASK")
    View_Tasks(All_Tasks)

    Raw_Id = input(Question + "\nEnter task ID to edit: " + Style.RESET_ALL).strip()
    if not Raw_Id.isdigit():
        print(Error + "Please enter a valid number.")
        return
    Target_Id = int(Raw_Id)

    for Task_Item in All_Tasks:
        if Task_Item["Id"] == Target_Id:
            print(Info + f"\nCurrent Task: {Task_Item['Title']}")
            print(Info + f"  Priority : {Task_Item['Priority']}")
            print(Info + f"  Due Date : {Task_Item['Due_Date']}")
            print(Info + f"  Category : {Task_Item['Category']}")

            New_Title = input(Question + "\nNew title (Enter to keep): " + Style.RESET_ALL).strip()
            if New_Title:
                Task_Item["Title"] = New_Title

            print(Info + "\nPriority Levels:")
            print(Option + "  1. High")
            print(Option + "  2. Medium")
            print(Option + "  3. Low")
            print(Option + "  4. Keep current")

            Priority_Choice = input(Question + "Select priority (1-4): " + Style.RESET_ALL).strip()
            if Priority_Choice == "1":
                Task_Item["Priority"] = "High"
            elif Priority_Choice == "2":
                Task_Item["Priority"] = "Medium"
            elif Priority_Choice == "3":
                Task_Item["Priority"] = "Low"

            New_Due_Date = input(
                Question + "New due date (YYYY-MM-DD) or Enter to skip: " + Style.RESET_ALL
            ).strip()
            if New_Due_Date:
                if Is_Date_Valid(New_Due_Date):
                    Task_Item["Due_Date"] = New_Due_Date
                else:
                    print(Error + "Invalid date format. Keeping current date.")

            print(Info + "\nCategories:")
            for Index, Category_Name in enumerate(Categories_List, start=1):
                print(Option + f"  {Index}. {Category_Name}")
            print(Option + f"  {len(Categories_List) + 1}. Keep current")

            Raw_Category_Choice = input(Question + "Select category: " + Style.RESET_ALL).strip()
            if Raw_Category_Choice.isdigit():
                Category_Choice = int(Raw_Category_Choice)
                if 1 <= Category_Choice <= len(Categories_List):
                    Task_Item["Category"] = Categories_List[Category_Choice - 1]

            if Save_Tasks(All_Tasks):
                print(Success + "\nTask updated successfully.")
            return

    print(Error + f"No task found with ID {Target_Id}.")


def Show_Statistics(All_Tasks):
    """Displays overall and category-wise task statistics."""
    if not All_Tasks:
        print(Warning + "\nNo tasks to show statistics for.")
        return

    Total_Tasks = len(All_Tasks)
    Done_Count = sum(1 for Task_Item in All_Tasks if Task_Item["Status"] == "Done")
    Pending_Count = Total_Tasks - Done_Count
    High_Pending_Count = sum(
        1 for Task_Item in All_Tasks if Task_Item["Priority"] == "High" and Task_Item["Status"] == "Pending"
    )
    Overdue_Count = sum(
        1 for Task_Item in All_Tasks
        if Task_Item["Status"] == "Pending" and Is_Date_Overdue(Task_Item["Due_Date"])
    )

    Category_Stats = {}
    for Category_Name in Categories_List:
        Category_Stats[Category_Name] = sum(1 for Task_Item in All_Tasks if Task_Item["Category"] == Category_Name)

    Print_Border()
    print(Title_Color + "                        TASK STATISTICS")
    Print_Border()

    print(Result + f"  Total Tasks           : {Total_Tasks}")
    print(Success + f"  Completed Tasks       : {Done_Count}")
    print(Warning + f"  Pending Tasks         : {Pending_Count}")
    print(Overdue_Color + f"  High Priority Pending : {High_Pending_Count}")
    if Overdue_Count > 0:
        print(Overdue_Color + f"  Overdue Tasks         : {Overdue_Count}")

    if Total_Tasks > 0:
        Completion_Rate = (Done_Count / Total_Tasks) * 100
        print(Info + f"  Completion Rate       : {Completion_Rate:.1f}%")

    Print_Border("-")
    print(Title_Color + "               CATEGORY BREAKDOWN")
    Print_Border("-")

    for Category_Name, Count in Category_Stats.items():
        Percentage = (Count / Total_Tasks) * 100 if Total_Tasks > 0 else 0
        Bar_Length = int(Percentage / 2)
        Bar_Display = "#" * Bar_Length + "-" * (50 - Bar_Length)
        print(Info + f"  {Category_Name:<10} {Bar_Display} {Count} ({Percentage:.1f}%)")

    Print_Border()


# ----------------------------------------------------------------------
# Menu / Program Entry Point
# ----------------------------------------------------------------------

def Show_Menu():
    Print_Border()
    print(Title_Color + "                  TO-DO LIST MANAGER")
    Print_Border()
    print(Option + "   1.  Add Task")
    print(Option + "   2.  View All Tasks")
    print(Option + "   3.  View Pending Tasks")
    print(Option + "   4.  View High Priority Tasks")
    print(Option + "   5.  Mark Task as Done")
    print(Option + "   6.  Delete Task")
    print(Option + "   7.  Edit Task")
    print(Option + "   8.  Search Tasks")
    print(Option + "   9.  Show Overdue Tasks")
    print(Option + "  10.  Show Tasks Due Today")
    print(Option + "  11.  Show Statistics")
    print(Option + "  12.  Save & Exit")
    Print_Border()


def Main():
    """Main program entry point."""
    Print_Title("WELCOME TO TO-DO LIST MANAGER")
    print(Info + "  Organize your tasks efficiently.")
    print(Warning + "  Tasks auto-save to a JSON file.")
    Print_Border()
    print()

    All_Tasks = Load_Tasks()

    while True:
        Show_Menu()
        User_Choice = input(Question + "Choose an option (1-12): " + Style.RESET_ALL).strip()

        if User_Choice == "1":
            Add_Task(All_Tasks)
        elif User_Choice == "2":
            View_Tasks(All_Tasks)
        elif User_Choice == "3":
            View_Tasks(All_Tasks, Filter_Status="Pending")
        elif User_Choice == "4":
            View_Tasks(All_Tasks, Filter_Priority="High")
        elif User_Choice == "5":
            Mark_Done(All_Tasks)
        elif User_Choice == "6":
            Delete_Task(All_Tasks)
        elif User_Choice == "7":
            Edit_Task(All_Tasks)
        elif User_Choice == "8":
            Search_Tasks(All_Tasks)
        elif User_Choice == "9":
            Show_Overdue_Tasks(All_Tasks)
        elif User_Choice == "10":
            Show_Tasks_Due_Today(All_Tasks)
        elif User_Choice == "11":
            Show_Statistics(All_Tasks)
        elif User_Choice == "12":
            if Save_Tasks(All_Tasks):
                print(Success + "\nTasks saved successfully.")
            print(Title_Color + "\nGoodbye! Keep being productive.")
            break
        else:
            print(Error + "Invalid choice. Please enter 1-12.")

        input(Option + "\nPress Enter to continue..." + Style.RESET_ALL)


if __name__ == "__main__":
    Main()
